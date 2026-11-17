#!/usr/bin/env python3
"""Points the detail pages at the redrawn SVG diagrams.

    python3 tools/link_diagrams.py [PREFIX ...]

For every legacy diagram `assets/diagrams/STEM.png` that has both `docs/assets/diagrams/STEM.en.svg`
and `STEM.ru.svg`, English pages under docs/ are switched to the English SVG and Russian pages to the
Russian SVG. Diagrams without a redrawn pair keep the PNG. The PNG files stay in assets/diagrams/ as
the record of the originals. Run tools/build_readme_excerpts.py afterwards.
"""
import glob
import os
import re
import sys


def main():
    only = sys.argv[1:]  # optional: limit to diagram number prefixes, e.g. "04" "13"
    n = 0
    for page in sorted(glob.glob("docs/*.md")):
        lang = "ru" if page.endswith(".ru.md") else "en"
        text = open(page, encoding="utf-8").read()

        def repl(m):
            stem = m.group(1)
            if only and not any(stem.startswith(o) for o in only):
                return m.group(0)
            if all(os.path.exists("docs/assets/diagrams/%s.%s.svg" % (stem, l)) for l in ("en", "ru")):
                return "(assets/diagrams/%s.%s.svg)" % (stem, lang)
            return m.group(0)

        new = re.sub(r"\(\.\./assets/diagrams/([\w-]+)\.png\)", repl, text)
        if new != text:
            n += 1
            open(page, "w", encoding="utf-8").write(new)
    print("pages updated:", n)


if __name__ == "__main__":
    main()
