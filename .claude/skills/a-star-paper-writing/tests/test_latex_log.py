"""Integration checks against real compiler logs; no scientific results."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_latex_log.py"


class LatexLogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def inspect(self, path):
        result = subprocess.run([sys.executable, str(SCRIPT), str(path), "--json"], capture_output=True, text=True)
        self.assertNotIn("Traceback", result.stderr)
        return result.returncode, json.loads(result.stdout)

    def compile(self, body, file_line=False):
        if not shutil.which("pdflatex"):
            self.skipTest("pdflatex unavailable; real compiler-log test not run")
        (self.root / "main.tex").write_text("\\documentclass{article}\n\\begin{document}\n" + body + "\n\\end{document}\n")
        cmd = ["pdflatex", "-interaction=nonstopmode", "-no-shell-escape"]
        if file_line:
            cmd.append("-file-line-error")
        self.last_compile = subprocess.run(cmd + ["main.tex"], cwd=self.root, capture_output=True, timeout=30)
        return self.root / "main.log"

    def test_real_clean_log_reports_only_limited_inspection(self):
        code, report = self.inspect(self.compile("A plain document."))
        self.assertEqual(code, 0, report)
        self.assertTrue(report["pdf_output_reported"])
        self.assertFalse(report["source_revision_verified"])
        self.assertFalse(report["pdf_verified"])
        self.assertFalse(report["sync_verified"])

    def test_pdf_emitted_despite_missing_citation_and_reference_is_flagged(self):
        code, report = self.inspect(self.compile("See \\ref{absent} and \\cite{missing}."))
        self.assertEqual(code, 1)
        self.assertTrue(report["pdf_output_reported"])
        codes = {r["code"] for r in report["issues"]}
        self.assertIn("undefined_reference", codes)
        self.assertIn("undefined_citation", codes)

    def test_recovered_tex_error_is_not_success_even_with_pdf(self):
        code, report = self.inspect(self.compile("Text \\NoSuchCommand text."))
        self.assertEqual(code, 1)
        self.assertEqual(report["status"], "errors_detected")

    def test_file_line_error_format_is_recognized(self):
        code, report = self.inspect(self.compile("Text \\NoSuchCommand text.", file_line=True))
        self.assertEqual(code, 1)
        self.assertEqual(report["status"], "errors_detected")

    def test_recovered_file_line_errors_outside_message_allowlist(self):
        for body in ("Text & text.", "Text # text."):
            with self.subTest(body=body):
                code, report = self.inspect(self.compile(body, file_line=True))
                self.assertNotEqual(self.last_compile.returncode, 0)
                self.assertTrue(report["pdf_output_reported"])
                self.assertEqual(code, 1, report)
                self.assertEqual(report["status"], "errors_detected")
                self.assertIn("file_line_error", {r["code"] for r in report["issues"]})

    def test_real_package_warning_is_not_classified_as_error(self):
        code, report = self.inspect(self.compile(
            "\\PackageWarning{audit-fixture}{A package advisory}Text.", file_line=True
        ))
        self.assertEqual(self.last_compile.returncode, 0)
        self.assertNotEqual(report["status"], "errors_detected", report)
        self.assertNotIn("file_line_error", {r["code"] for r in report["issues"]})

    def test_multiple_successful_invocations_have_final_output_evidence(self):
        self.compile("A first complete run.")
        self.assertEqual(self.last_compile.returncode, 0)
        transcript = self.root / "build.log"
        transcript.write_bytes(self.last_compile.stdout)
        self.compile("A second complete run.")
        self.assertEqual(self.last_compile.returncode, 0)
        with transcript.open("ab") as sink:
            sink.write(self.last_compile.stdout)
        code, report = self.inspect(transcript)
        self.assertEqual(code, 0, report)
        self.assertEqual(report["engine_invocation_count"], 2)
        self.assertTrue(report["pdf_output_reported"])
        self.assertGreater(report["latest_invocation_start_line"], 1)

    def test_earlier_pdf_does_not_hide_interrupted_final_invocation(self):
        self.compile("A complete first run.")
        self.assertEqual(self.last_compile.returncode, 0)
        transcript = self.root / "build.log"
        transcript.write_bytes(self.last_compile.stdout)
        (self.root / "main.tex").write_text(
            "\\documentclass{article}\n\\begin{document}\n"
            "\\loop\\iftrue\\repeat\n\\end{document}\n"
        )
        with transcript.open("ab") as sink:
            proc = subprocess.Popen(
                ["pdflatex", "-interaction=nonstopmode", "-no-shell-escape", "main.tex"],
                cwd=self.root, stdout=sink, stderr=subprocess.STDOUT,
            )
            try:
                proc.wait(timeout=1)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)
            finally:
                if proc.poll() is None:
                    proc.kill()
                    proc.wait(timeout=5)
        self.assertNotEqual(proc.returncode, 0)
        code, report = self.inspect(transcript)
        self.assertEqual(report["engine_invocation_count"], 2, report)
        self.assertEqual(code, 1, report)
        self.assertFalse(report["pdf_output_reported"])
        self.assertIn("no_pdf_output_reported", {r["code"] for r in report["issues"]})

    def test_empty_or_unrelated_text_never_reports_clean_build(self):
        path = self.root / "unrelated.log"
        path.write_text("An arbitrary status message.\n")
        code, report = self.inspect(path)
        self.assertEqual(code, 1)
        self.assertFalse(report["tex_engine_banner_seen"])
        self.assertFalse(report["pdf_output_reported"])

    def test_unreadable_path_is_structured_error(self):
        code, report = self.inspect(self.root / "missing.log")
        self.assertEqual(code, 2)
        self.assertEqual(report["status"], "invalid_input")


if __name__ == "__main__":
    unittest.main()
