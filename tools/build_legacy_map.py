#!/usr/bin/env python3
"""Builds the "where the old README sections went" table in README.md and README.ru.md.

    python3 tools/build_legacy_map.py

The table is generated from the archived README's headings, so it cannot drift from it:
every old heading becomes (a) a legacy anchor `<a name="old-anchor">` in README.md, so links
from other repositories to `README.md#old-anchor` still land somewhere meaningful, and
(b) a pointer to the page (and, when the heading text matches, the exact heading) that now
holds the section. The block between the `legacy-map` markers is replaced; do not hand-edit it.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inventory import inventory, github_slug  # noqa: E402

ARCHIVE = "archive/README_2026-11-17_pre-marketing-update.md"
# (first line, last line, page stem) in the archived README
RANGES = [
    (1, 45, None), (46, 74, "ECOSYSTEM"), (75, 92, "RESEARCH_AND_IP"), (93, 185, "ECOSYSTEM"),
    (186, 205, "RESEARCH_AND_IP"), (206, 225, "TEAM"), (226, 247, "RESEARCH_AND_IP"),
    (248, 308, "LEGAL_ENTITIES"), (309, 373, "PATHS_TO_MONEY_RESEARCH"),
    (374, 495, "PATHS_TO_MONEY_PRODUCTS"), (496, 539, "TRACK_RECORD"), (540, 600, "OUTREACH"),
    (601, 639, "FUNDING"), (640, 789, "MEDIA_AND_CHANNELS"), (790, 869, "TARGET_MARKETS"),
    (870, 912, "ROADMAP"), (913, 942, "PARTNERSHIPS_AND_TERMS"), (943, 956, "FUNDING"),
    (957, 964, "PARTNERSHIPS_AND_TERMS"),
]
TITLES = {
    "en": {"ECOSYSTEM": "Ecosystem", "RESEARCH_AND_IP": "Research and IP", "TEAM": "Team",
           "LEGAL_ENTITIES": "Legal entities", "PATHS_TO_MONEY_RESEARCH": "Paths to money: research",
           "PATHS_TO_MONEY_PRODUCTS": "Paths to money: products", "TRACK_RECORD": "Track record",
           "OUTREACH": "Outreach", "FUNDING": "Funding and patrons", "MEDIA_AND_CHANNELS": "Media and channels",
           "TARGET_MARKETS": "Target markets", "ROADMAP": "Roadmap",
           "PARTNERSHIPS_AND_TERMS": "Partnerships and terms"},
    "ru": {"ECOSYSTEM": "Экосистема", "RESEARCH_AND_IP": "Исследования и ИС", "TEAM": "Команда",
           "LEGAL_ENTITIES": "Юридические лица", "PATHS_TO_MONEY_RESEARCH": "Пути к деньгам: исследования",
           "PATHS_TO_MONEY_PRODUCTS": "Пути к деньгам: продукты", "TRACK_RECORD": "Кейсы",
           "OUTREACH": "Аутрич", "FUNDING": "Финансирование и меценаты", "MEDIA_AND_CHANNELS": "Медиа и каналы",
           "TARGET_MARKETS": "Целевые рынки", "ROADMAP": "Дорожная карта",
           "PARTNERSHIPS_AND_TERMS": "Партнёрство и условия"},
}
HEAD = {"en": ("Old section", "Now lives in", "this README (title, badges, navigation)"),
        "ru": ("Раздел старого README", "Где теперь", "этот README (заголовок, бейджи, навигация)")}


def page_of(line):
    for a, b, p in RANGES:
        if a <= line <= b:
            return p
    return None


def norm(s):
    return re.sub(r"[^\w]+", " ", s, flags=re.UNICODE).strip().lower()


def halves(title):
    """English and Russian half of an old bilingual heading, emoji stripped."""
    parts = [p.strip() for p in title.split("**/**")]
    clean = [re.sub(r"^[^\w(«]+", "", p, flags=re.UNICODE).strip() for p in parts]
    en = clean[0]
    ru = clean[-1] if len(clean) > 1 else clean[0]
    return en, ru


def page_headings(path):
    out, seen = {}, {}
    for line in open(path, encoding="utf-8").read().split("\n"):
        m = re.match(r"^(#{2,6}) (.*)$", line)
        if m:
            out[norm(m.group(2))] = github_slug(m.group(2).strip(), seen)
    return out


def build(lang, heads):
    ext = ".md" if lang == "en" else ".ru.md"
    cache = {}
    rows = []
    cur = None
    for h in heads:
        if h["level"] <= 2:
            cur = {"h": h, "kids": []}
            rows.append(cur)
        elif cur is not None:
            cur["kids"].append(h)
    c1, c2, here = HEAD[lang]
    out = ["| %s | %s |" % (c1, c2), "|---|---|"]
    for r in rows:
        allh = [r["h"]] + r["kids"]
        anchors = "".join('<a name="%s"></a>' % x["anchor"] for x in allh) if lang == "en" else ""
        label = halves(r["h"]["text"])[0 if lang == "en" else 1]
        targets = []
        pages_seen = set()
        for x in allh:
            p = page_of(x["line"])
            if p is None:
                t = here
            else:
                path = "docs/%s%s" % (p, ext)
                if path not in cache:
                    cache[path] = page_headings(path)
                frag = cache[path].get(norm(halves(x["text"])[0 if lang == "en" else 1]))
                name = TITLES[lang][p]
                if frag is None and x is not r["h"] and p in pages_seen:
                    continue
                pages_seen.add(p)
                if x is r["h"] or frag is None:
                    t = "[%s](%s%s)" % (name, path, "#" + frag if frag and x is r["h"] else "")
                else:
                    t = "[%s](%s#%s)" % (halves(x["text"])[0 if lang == "en" else 1], path, frag)
            if t not in targets:
                targets.append(t)
        out.append("| %s%s | %s |" % (anchors, label, " · ".join(targets)))
    return "\n".join(out)


def main():
    heads = inventory(open(ARCHIVE, encoding="utf-8").read())["headings"]
    for lang, readme in (("en", "README.md"), ("ru", "README.ru.md")):
        text = open(readme, encoding="utf-8").read()
        a = text.index("<!-- legacy-map:start -->") + len("<!-- legacy-map:start -->")
        b = text.index("<!-- legacy-map:end -->")
        text = text[:a] + "\n" + build(lang, heads) + "\n" + text[b:]
        open(readme, "w", encoding="utf-8").write(text)
        print("updated", readme)


if __name__ == "__main__":
    main()
