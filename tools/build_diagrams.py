#!/usr/bin/env python3
"""Builds the bilingual SVG diagrams in docs/assets/diagrams/ (never hand-edit the output).

    python3 tools/build_diagrams.py

Each tools/diagrams_*.py module redraws a group of the legacy PNG diagrams from assets/diagrams/
(kept as the record of the originals) as separate English and Russian SVG files in the shared
style of tools/svgkit.py. Labels are transcribed from the PNG; no content is added.
"""
import glob
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def main():
    for path in sorted(glob.glob(os.path.join(HERE, "diagrams_*.py"))):
        importlib.import_module(os.path.basename(path)[:-3]).build()


if __name__ == "__main__":
    main()
