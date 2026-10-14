"""Exercise TeX initialization at the CLI, compiling when pdfLaTeX is present."""

import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest


SKILL = Path(os.environ.get("PAPER_SKILL_DIR", Path(__file__).resolve().parents[1]))
INIT = SKILL / "scripts" / "init_paper.py"


class TexInitializerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "paper"

    def initialize(self, *arguments, target=None):
        return subprocess.run(
            [sys.executable, str(INIT), str(target or self.root), *arguments],
            capture_output=True, text=True,
        )

    def create(self, *arguments):
        result = self.initialize(*arguments)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def read_json(self, filename):
        return json.loads((self.root / filename).read_text(encoding="utf-8"))

    def compile_project(self):
        profile = self.read_json("overleaf-project.json")
        command = shlex.split(profile["compile_command"])
        result = subprocess.run(command, cwd=self.root, capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((self.root / "main.pdf").read_bytes().startswith(b"%PDF-"))
        log = (self.root / "main.log").read_text(encoding="utf-8", errors="replace")
        self.assertNotIn("Undefined control sequence", log)
        self.assertNotIn("LaTeX Error", log)
        self.assertNotIn("There were undefined references", log)

    def test_default_has_complete_tex_graph_and_ordered_appendix(self):
        self.create("--title", "A supplied working title")
        main = (self.root / "main.tex").read_text(encoding="utf-8")
        self.assertIn(r"\title{A supplied working title}", main)
        inputs = re.findall(r"^\\input\{([^}]+)\}", main, re.MULTILINE)
        expected = [
            "sections/abstract", "sections/introduction", "sections/related-work",
            "sections/problem-setting", "sections/method", "sections/experiments",
            "sections/results", "sections/discussion", "sections/conclusion",
            "appendix/background", "appendix/method-details", "appendix/experiment-details",
            "appendix/prompts", "appendix/extended-results", "appendix/qualitative-results",
            "appendix/discussion", "appendix/faq",
        ]
        self.assertEqual(inputs, expected)
        for name in expected:
            self.assertTrue((self.root / (name + ".tex")).is_file(), name)
        self.assertEqual(
            {str(path.relative_to(self.root)) for path in self.root.rglob("*.tex")},
            {"main.tex", *(name + ".tex" for name in expected)},
        )
        for name in ("artifacts", "figures", "prompts"):
            self.assertTrue((self.root / name).is_dir())
        self.assertTrue((self.root / "project-brief.md").is_file())
        self.assertFalse((self.root / "paper.md").exists())

    def test_scaffold_contains_no_invented_evidence_or_venue_rules(self):
        self.create()
        self.assertEqual(self.read_json("evidence-ledger.json"), {
            "schema_version": 1, "claims": [], "evidence": [], "citations": [],
        })
        self.assertEqual((self.root / "references.bib").read_bytes(), b"")
        venue = self.read_json("venue-profile.json")
        expected_venue = json.loads((SKILL / "assets" / "venue-profile.example.json").read_text(encoding="utf-8"))
        self.assertEqual(venue, expected_venue)
        main = (self.root / "main.tex").read_text(encoding="utf-8")
        active = "\n".join(line for line in main.splitlines() if not line.lstrip().startswith("%"))
        self.assertIn("Working draft: generic scaffold, not a venue template.", active)
        self.assertIn(r"\documentclass{article}", active)
        for command in (r"\cite", r"\bibliography", r"\addbibresource", r"\onecolumn", r"\twocolumn", r"\geometry", r"\setlength"):
            self.assertNotIn(command, active)
        # Blank sections must not quietly contain fabricated prose or result tables.
        for directory in ("sections", "appendix"):
            for path in (self.root / directory).glob("*.tex"):
                if path.name == "abstract.tex":
                    continue
                active_lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("%")]
                self.assertEqual(len(active_lines), 1, path.name)
                self.assertRegex(active_lines[0], r"^\\section\{[^}]+\}$")

    def test_profile_records_local_defaults_without_claiming_remote_connection(self):
        self.create()
        profile = self.read_json("overleaf-project.json")
        self.assertEqual(profile["main_document"], "main.tex")
        self.assertEqual(profile["compiler"], "pdflatex")
        self.assertEqual(profile["bibliography_files"], ["references.bib"])
        self.assertIsNone(profile["bibliography_backend"])
        self.assertEqual(profile["connection"]["mode"], "unconnected")
        self.assertIsNone(profile["project_id"])
        self.assertIsNone(profile["project_url"])
        self.assertEqual(profile["venue_verification"], "unknown")
        self.assertEqual(profile["build"]["candidate_status"], "not_run")
        self.assertFalse(profile["synchronization"]["readback_verified"])
        self.assertEqual(set(profile["files"]["tex"]), {str(path.relative_to(self.root)) for path in self.root.rglob("*.tex")})

    @unittest.skipUnless(shutil.which("pdflatex"), "pdfLaTeX is not installed")
    def test_default_compiles_with_recorded_command_and_empty_bibliography(self):
        self.create()
        self.compile_project()
        self.assertFalse((self.root / "main.bbl").exists())

    @unittest.skipUnless(shutil.which("pdflatex"), "pdfLaTeX is not installed")
    def test_literal_title_metacharacters_compile_without_tex_injection(self):
        title = r"A & B_1: 50% of $x$ #2 {study} ~ ^ \input{missing-file}"
        self.create("--title", title)
        main = (self.root / "main.tex").read_text(encoding="utf-8")
        expected_title = r"\title{A \& B\_1: 50\% of \$x\$ \#2 \{study\} \textasciitilde{} \textasciicircum{} \textbackslash{}input\{missing-file\}}"
        self.assertIn(expected_title, main)
        self.compile_project()

    def test_explicit_markdown_preserves_legacy_project_layout(self):
        title = "Plain # title with 50% & a_underscore"
        self.create("--format", "markdown", "--title", title)
        self.assertTrue((self.root / "paper.md").read_text(encoding="utf-8").startswith("# " + title + "\n"))
        for directory in ("artifacts", "figures", "supplement"):
            self.assertTrue((self.root / directory).is_dir())
        self.assertFalse((self.root / "main.tex").exists())
        self.assertFalse((self.root / "overleaf-project.json").exists())
        self.assertEqual(self.read_json("evidence-ledger.json")["claims"], [])

    def test_existing_project_is_unchanged_in_either_mode(self):
        self.create()
        manuscript = self.root / "main.tex"
        manuscript.write_text("Author work must remain intact.\n", encoding="utf-8")
        before = {str(path.relative_to(self.root)): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        for output_format in ("tex", "markdown"):
            with self.subTest(output_format=output_format):
                result = self.initialize("--format", output_format)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Nothing was overwritten", result.stderr)
                after = {str(path.relative_to(self.root)): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
                self.assertEqual(before, after)

    def test_even_an_empty_existing_directory_is_rejected(self):
        self.root.mkdir()
        result = self.initialize()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_existing_file_and_dangling_symlink_are_not_replaced(self):
        self.root.write_text("existing file", encoding="utf-8")
        self.assertNotEqual(self.initialize().returncode, 0)
        self.assertEqual(self.root.read_text(encoding="utf-8"), "existing file")
        link = Path(self.temp.name) / "dangling"
        link.symlink_to("missing")
        self.assertNotEqual(self.initialize(target=link).returncode, 0)
        self.assertTrue(link.is_symlink())
        self.assertFalse((link.parent / "missing").exists())

    def test_invalid_input_does_not_create_project(self):
        for arguments in (("--format", "pdf"), ("--title", " "), ("--title", "Two\nlines")):
            with self.subTest(arguments=arguments):
                result = self.initialize(*arguments)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stderr)
                self.assertFalse(self.root.exists())


if __name__ == "__main__":
    unittest.main()
