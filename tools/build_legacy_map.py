#!/usr/bin/env python3
"""Keeps links to the previous README's section anchors working, invisibly.

    python3 tools/build_legacy_map.py

The previous README used long bilingual heading anchors (for example
`#-paths-to-money--пути-к-деньгам`). Other pages and repositories may still link to them, so
each of those anchors is kept as an empty `<a name="…">` placed directly above the README
section that now covers the same topic. Nothing is rendered; the README itself does not refer
to its earlier layout. The anchor lines are generated (marker `<!-- legacy-anchors -->`); do
not edit them by hand.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inventory import inventory  # noqa: E402

ARCHIVE = "archive/README_2026-11-17_pre-marketing-update.md"
MARK = "<!-- legacy-anchors -->"
# (first line, last line) of the archived README -> heading of the README.md section that covers it
RANGES = [
    (1, 45, "## At a glance"), (46, 74, "## About"), (75, 92, "## Research and patents"),
    (93, 116, "## Ecosystem map"), (117, 185, "## Component status"), (186, 205, "## Research and patents"),
    (206, 225, "## Team"), (226, 247, "## Accreditations and timeline"), (248, 308, "## Legal entities"),
    (309, 495, "## Paths to money"), (496, 539, "## Track record"), (540, 600, "## Outreach"),
    (601, 639, "## Funding"), (640, 789, "## Media and channels"), (790, 869, "## Target markets"),
    (870, 912, "## Roadmap"), (913, 931, "## Partnerships"), (932, 942, "## Disclaimer"),
    (943, 956, "## Funding"), (957, 964, "## Contact"),
]
# (first line, last line, docs page stem): where each part of the archived README lives in docs/
PAGES = [
    (1, 45, None), (46, 74, "ECOSYSTEM"), (75, 92, "RESEARCH_AND_IP"), (93, 185, "ECOSYSTEM"),
    (186, 205, "RESEARCH_AND_IP"), (206, 225, "TEAM"), (226, 247, "RESEARCH_AND_IP"),
    (248, 308, "LEGAL_ENTITIES"), (309, 373, "PATHS_TO_MONEY_RESEARCH"),
    (374, 495, "PATHS_TO_MONEY_PRODUCTS"), (496, 539, "TRACK_RECORD"), (540, 600, "OUTREACH"),
    (601, 639, "FUNDING"), (640, 789, "MEDIA_AND_CHANNELS"), (790, 869, "TARGET_MARKETS"),
    (870, 912, "ROADMAP"), (913, 942, "PARTNERSHIPS_AND_TERMS"), (943, 956, "FUNDING"),
    (957, 964, "PARTNERSHIPS_AND_TERMS"),
]


def main():
    heads = inventory(open(ARCHIVE, encoding="utf-8").read())["headings"]
    by_section = {}
    for h in heads:
        for a, b, sec in RANGES:
            if a <= h["line"] <= b:
                by_section.setdefault(sec, []).append(h["anchor"])
    lines = [ln for ln in open("README.md", encoding="utf-8").read().split("\n") if not ln.startswith(MARK)]
    out, placed = [], set()
    for ln in lines:
        if ln in by_section and ln not in placed:
            placed.add(ln)
            out.append(MARK + "".join('<a name="%s"></a>' % a for a in by_section[ln]))
        out.append(ln)
    missing = set(by_section) - placed
    if missing:
        raise SystemExit("README.md has no section for: %s" % sorted(missing))
    open("README.md", "w", encoding="utf-8").write("\n".join(out))
    print("README.md: %d legacy anchors kept above %d sections" % (sum(len(v) for v in by_section.values()), len(placed)))


if __name__ == "__main__":
    main()
