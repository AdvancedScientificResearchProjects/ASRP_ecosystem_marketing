"""Regression gate: the repackaged pages must keep every element of the archived README.

Run from the repository root:  python3 -m unittest discover -s tests -v
"""
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class NoLossTest(unittest.TestCase):
    def test_hard_checks_pass(self):
        r = subprocess.run([sys.executable, "tools/verify_no_loss.py"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout[-2000:])
        self.assertIn("RESULT: PASS", r.stdout)

    def test_visuals_build_and_fit(self):
        """The generator aborts when a label does not fit its container or a font is too small."""
        r = subprocess.run([sys.executable, "tools/build_visuals.py"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout[-2000:] + r.stderr[-2000:])

    def test_readme_excerpts_are_in_sync_with_docs(self):
        """README sections pulled from docs/ must equal a fresh build (no hand edits, no drift)."""
        before = {f: open(os.path.join(ROOT, f), encoding="utf-8").read() for f in ("README.md", "README.ru.md")}
        r = subprocess.run([sys.executable, "tools/build_readme_excerpts.py"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr[-2000:])
        for f, old in before.items():
            self.assertEqual(old, open(os.path.join(ROOT, f), encoding="utf-8").read(), f + " excerpts are stale")

    def test_every_page_has_a_twin_and_backlinks(self):
        docs = os.path.join(ROOT, "docs")
        for name in sorted(os.listdir(docs)):
            if not name.endswith(".md"):
                continue
            twin = name[:-6] + ".md" if name.endswith(".ru.md") else name[:-3] + ".ru.md"
            self.assertTrue(os.path.exists(os.path.join(docs, twin)), "missing language twin for " + name)
            head = open(os.path.join(docs, name), encoding="utf-8").read().split("\n")[:4]
            self.assertIn(twin, head[0], "no language switch on line 1 of " + name)
            self.assertIn("README", head[2], "no back-link to the index on line 3 of " + name)


if __name__ == "__main__":
    unittest.main()
