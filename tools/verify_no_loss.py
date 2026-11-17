#!/usr/bin/env python3
"""No-loss verification: old root README (archived) vs the new page structure.

Usage (from the repository root):
    python3 tools/verify_no_loss.py [--json reports/inventory/verification.json]
                                    [--md reports/inventory/verification.md]

What is compared
    OLD  = archive/README_2026-11-17_pre-marketing-update.md (byte-identical to tag
           pre-marketing-update-2026-11:README.md; the script checks that too)
    NEW  = README.md, README.ru.md, docs/*.md  (archive/ and reports/ are NOT counted,
           otherwise everything would trivially "survive")
    EN corpus = NEW files that are not *.ru.md, RU corpus = NEW *.ru.md files.

Checks (H = hard, fails the run; S = soft, listed for human review)
    H1 archive is byte-identical to the tagged README
    H2 every external/internal URL of OLD is present in NEW
    H3 every number token of OLD is present in NEW
    H4 every date, e-mail, @handle and code span of OLD is present in NEW
    H5 every image of OLD is still referenced in NEW and the file exists
    H6 every heading anchor of OLD exists as a legacy <a id> in README.md
    H7 no broken relative link / fragment in any tracked Markdown file
    H8 no file deleted relative to the tag
    S1 every proper name of OLD is present in NEW
    S2 sentence level: word-trigram coverage of every OLD text segment in the same-language
       corpus (threshold 0.8)
    S3 table rows per language >= table rows in OLD
    S4 URLs / numbers present in one language corpus but missing in the other

Standard library only.
"""
import argparse
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inventory import inventory, github_slug, MDLINK_RE  # noqa: E402

ARCHIVE = "archive/README_2026-11-17_pre-marketing-update.md"
TAG = "pre-marketing-update-2026-11"
THRESHOLD = 0.8
WAIVERS = "reports/inventory/waivers.json"
WORD_RE = re.compile(r"[^\W_]+", re.UNICODE)


def read(p):
    return open(p, encoding="utf-8").read()


def words(s):
    return [w.lower() for w in WORD_RE.findall(s)]


def trigrams(ws):
    return {tuple(ws[i:i + 3]) for i in range(len(ws) - 2)}


def token_present(tok, text):
    return re.search(r"(?<![\d])" + re.escape(tok) + r"(?![\d])", text) is not None


def new_files():
    fs = ["README.md", "README.ru.md"] + sorted(glob.glob("docs/*.md"))
    return [f for f in fs if os.path.exists(f)]


def tracked_markdown():
    out = subprocess.run(["git", "ls-files", "-co", "--exclude-standard", "*.md"],
                         capture_output=True, text=True).stdout.split("\n")
    return [f for f in out if f and not f.startswith("archive/")]


def anchors_of(path):
    text = read(path)
    seen = {}
    ids = set()
    in_code = False
    for line in text.split("\n"):
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^(#{1,6}) (.*)$", line)
        if m:
            ids.add(github_slug(m.group(2).strip(), seen))
        for a in re.findall(r"<a\s+(?:id|name)=\"([^\"]+)\"", line):
            ids.add(a)
    return ids


def check_links(files):
    broken = []
    cache = {}
    for f in files:
        text = read(f)
        in_code = False
        for n, line in enumerate(text.split("\n"), 1):
            if line.startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            targets = [m.group(3) for m in MDLINK_RE.finditer(line)]
            targets += re.findall(r"(?:src|href)=\"([^\"]+)\"", line)
            for t in targets:
                if re.match(r"^[a-z]+:", t):
                    continue
                path, _, frag = t.partition("#")
                target = f if not path else os.path.normpath(os.path.join(os.path.dirname(f), path))
                if not os.path.exists(target):
                    broken.append({"file": f, "line": n, "target": t, "why": "missing file"})
                    continue
                if frag and target.endswith(".md"):
                    if target not in cache:
                        cache[target] = anchors_of(target)
                    from urllib.parse import unquote
                    if unquote(frag) not in cache[target]:
                        broken.append({"file": f, "line": n, "target": t, "why": "missing anchor"})
    return broken


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    ap.add_argument("--md")
    a = ap.parse_args()

    res = {"hard": {}, "soft": {}, "stats": {}}
    old_text = read(ARCHIVE)
    old = inventory(old_text)

    tagged = subprocess.run(["git", "show", "%s:README.md" % TAG], capture_output=True).stdout
    res["hard"]["H1_archive_identical_to_tag"] = (
        [] if hashlib.sha256(tagged).hexdigest() == hashlib.sha256(old_text.encode("utf-8")).hexdigest()
        else ["archive differs from %s:README.md" % TAG])
    res["stats"]["archive_sha256"] = hashlib.sha256(old_text.encode("utf-8")).hexdigest()

    files = new_files()
    en_files = [f for f in files if not f.endswith(".ru.md")]
    ru_files = [f for f in files if f.endswith(".ru.md")]
    en = "\n".join(read(f) for f in en_files)
    ru = "\n".join(read(f) for f in ru_files)
    allt = en + "\n" + ru
    res["stats"]["new_files"] = {f: len(read(f)) for f in files}

    # H2 URLs
    res["hard"]["H2_urls_missing"] = [u for u in old["urls"] if u not in allt]
    res["soft"]["S4_urls_missing_in_en"] = [u for u in old["urls"] if u in allt and u not in en]
    res["soft"]["S4_urls_missing_in_ru"] = [u for u in old["urls"] if u in allt and u not in ru]
    # H3 numbers
    res["hard"]["H3_numbers_missing"] = [x for x in old["numbers"] if not token_present(x, allt)]
    res["soft"]["S4_numbers_missing_in_en"] = [
        x for x in old["numbers"] if token_present(x, allt) and not token_present(x, en)]
    res["soft"]["S4_numbers_missing_in_ru"] = [
        x for x in old["numbers"] if token_present(x, allt) and not token_present(x, ru)]
    # H4 identifiers
    miss = []
    for k in ("dates", "emails", "handles", "code_spans"):
        miss += ["%s: %s" % (k, x) for x in old[k] if x not in allt]
    res["hard"]["H4_identifiers_missing"] = miss
    # H5 images
    img_miss = []
    for im in old["images"]:
        base = os.path.basename(im["target"])
        if base not in allt:
            img_miss.append(im["target"] + " (not referenced)")
        if not os.path.exists(im["target"]):
            img_miss.append(im["target"] + " (file missing)")
    res["hard"]["H5_images_missing"] = img_miss
    # H6 legacy anchors
    readme_ids = anchors_of("README.md") if os.path.exists("README.md") else set()
    res["hard"]["H6_legacy_anchors_missing"] = [
        h["anchor"] for h in old["headings"] if h["anchor"] not in readme_ids]
    # H7 links
    res["hard"]["H7_broken_links"] = check_links(tracked_markdown())
    # H8 deleted files
    deleted = subprocess.run(["git", "diff", "--name-only", "--diff-filter=D", TAG],
                             capture_output=True, text=True).stdout.split()
    res["hard"]["H8_deleted_files"] = deleted

    # S1 names
    res["soft"]["S1_names_missing"] = [n for n in old["names"] if n not in allt]

    # S2 sentence-level coverage.
    # The old README interleaved both languages on one line, so a "segment" can still straddle
    # the seam (e.g. "**Client **/** Клиент:** governments"). Each segment is therefore cut into
    # runs of same-script words; Latin runs are looked up in the EN corpus, Cyrillic runs in the
    # RU corpus (proper nouns and identifiers stay Latin on RU pages, so a Latin run may also be
    # satisfied by the RU corpus and vice versa is not allowed). Coverage = share of the
    # segment's word n-grams (n = 3, or the run length if shorter) found in the corpus.
    def script(w):
        if re.search(r"[А-Яа-яЁё]", w):
            return "ru"
        if re.search(r"[A-Za-z]", w):
            return "en"
        return None

    def runs(ws):
        out, cur, cur_s = [], [], None
        for w in ws:
            s = script(w)
            if s is None or s == cur_s or cur_s is None:
                cur.append(w)
                cur_s = cur_s or s
            else:
                out.append((cur_s, cur))
                cur, cur_s = [w], s
        if cur:
            out.append((cur_s or "en", cur))
        return out

    def grams(ws, n):
        return [tuple(ws[i:i + n]) for i in range(len(ws) - n + 1)]

    corp = {}
    for key, txt in (("en", en), ("ru", ru)):
        ws = words(txt)
        corp[key] = {n: set(grams(ws, n)) for n in (1, 2, 3)}
    low = []
    counted = {"en": 0, "ru": 0, "mixed": 0}
    for s in old["segments"]:
        ws = words(s["text"])
        if not ws:
            continue
        counted[s["lang"] if s["lang"] in counted else "mixed"] += 1
        total = hit = 0
        for sc, run in runs(ws):
            n = min(3, len(run))
            for g in grams(run, n):
                total += 1
                if g in corp[sc][n] or (sc == "en" and g in corp["ru"][n]):
                    hit += 1
        cov = hit / total if total else 1.0
        if cov < THRESHOLD:
            low.append({"line": s["line"], "lang": s["lang"], "coverage": round(cov, 2),
                        "text": s["text"][:220]})
    res["soft"]["S2_low_coverage_segments"] = low
    res["stats"]["segments_checked"] = counted
    res["stats"]["segments_low"] = len(low)

    # S3 table rows
    def rows(text):
        return len(inventory(text)["table_rows"])
    res["stats"]["table_rows"] = {"old": len(old["table_rows"]), "new_en": rows(en), "new_ru": rows(ru)}
    res["soft"]["S3_table_rows_short"] = [
        k for k in ("new_en", "new_ru") if res["stats"]["table_rows"][k] < len(old["table_rows"])]

    res["stats"]["old_counts"] = old["counts"]

    # Waivers: every deliberate deviation is a recorded decision with a reason, never a silent
    # loosening of the check (ASRP quality standard, "no bypass without a recorded decision").
    res["waived"] = []
    if os.path.exists(WAIVERS):
        for w in json.load(open(WAIVERS, encoding="utf-8"))["waivers"]:
            for kind in ("hard", "soft"):
                items = res[kind].get(w["check"])
                if not items:
                    continue
                keep = [i for i in items if w["match"] not in json.dumps(i, ensure_ascii=False)]
                if len(keep) != len(items):
                    res["waived"].append({"check": w["check"], "match": w["match"], "reason": w["reason"],
                                          "items": len(items) - len(keep)})
                    res[kind][w["check"]] = keep
    hard_fail = {k: v for k, v in res["hard"].items() if v}
    res["result"] = "FAIL" if hard_fail else "PASS"

    if a.json:
        open(a.json, "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
    lines = ["# No-loss verification", "",
             "Generated by `tools/verify_no_loss.py`. Result of hard checks: **%s**." % res["result"], "",
             "| Check | Kind | Items in old README | Findings |", "|---|---|---:|---:|"]
    sizes = {"H1": 1, "H2": len(old["urls"]), "H3": len(old["numbers"]),
             "H4": sum(len(old[k]) for k in ("dates", "emails", "handles", "code_spans")),
             "H5": len(old["images"]), "H6": len(old["headings"]), "H7": "-", "H8": "-",
             "S1": len(old["names"]), "S2": sum(counted.values()), "S3": len(old["table_rows"]), "S4": "-"}
    for kind in ("hard", "soft"):
        for k, v in res[kind].items():
            lines.append("| `%s` | %s | %s | %d |" % (k, kind, sizes.get(k[:2], "-"), len(v)))
    lines += ["", "Table rows: old %(old)d, new EN %(new_en)d, new RU %(new_ru)d." % res["stats"]["table_rows"], ""]
    for kind in ("hard", "soft"):
        for k, v in res[kind].items():
            if v:
                lines += ["## %s" % k, ""]
                for item in v[:400]:
                    lines.append("- `%s`" % (json.dumps(item, ensure_ascii=False) if not isinstance(item, str) else item))
                lines.append("")
    if res["waived"]:
        lines += ["## Waived (recorded decisions)", ""]
        for w in res["waived"]:
            lines.append("- `%s` · `%s` · %d item(s): %s" % (w["check"], w["match"], w["items"], w["reason"]))
        lines.append("")
    if a.md:
        open(a.md, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("RESULT:", res["result"])
    for kind in ("hard", "soft"):
        for k, v in res[kind].items():
            print("  %-32s %d" % (k, len(v)))
    print("  table rows", res["stats"]["table_rows"], "| waived:", sum(w["items"] for w in res["waived"]))
    return 1 if hard_fail else 0


if __name__ == "__main__":
    sys.exit(main())
