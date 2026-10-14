"""Observable CLI tests. Run: python -m unittest discover -s tests -v.

PAPER_SKILL_DIR can point to a development installation of the skill.
All result values and metadata below are synthetic test fixtures, not research.
"""

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
CANDIDATES = [Path(os.environ["PAPER_SKILL_DIR"])] if "PAPER_SKILL_DIR" in os.environ else [REPO / "skills" / "a-star-paper-writing", REPO / "a-star-paper-writing", REPO]
SKILL = next((path for path in CANDIDATES if (path / "scripts" / "paper_audit.py").is_file()), CANDIDATES[0])
AUDIT = SKILL / "scripts" / "paper_audit.py"
INIT = SKILL / "scripts" / "init_paper.py"


class PaperToolsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "paper"
        result = subprocess.run([sys.executable, str(INIT), str(self.root), "--title", "Synthetic test"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.ledger = {
            "schema_version": 1,
            "claims": [{"id": "C1", "text": "Synthetic fixture has an observed score of 0.8 on its held-out set.", "kind": "empirical", "status": "verified", "evidence_ids": ["E1"], "citation_ids": ["R1"]}],
            "evidence": [{"id": "E1", "kind": "experiment", "status": "verified", "artifact": "artifacts/results.json", "locator": "JSON key score", "scope": {"dataset": "synthetic test fixture", "split": "held-out", "metric": "accuracy", "unit": "fraction", "baseline": "synthetic reference", "budget": "one fixture run"}, "values": {"score": 0.8}, "provenance": {"producer": "unit test", "created_on": "2026-01-01", "description": "Fixture created in a temporary directory; no scientific significance."}}],
            "citations": [{"id": "R1", "status": "verified", "title": "Synthetic citation used only for unit testing", "authors": ["Test Author"], "year": 2023, "source_url": "https://example.org/synthetic-source", "verified_on": "2026-01-01"}],
        }
        self.venue = {
            "schema_version": 1, "venue": "Synthetic Test Conference", "year": 2026, "track": "Synthetic track", "stage": "submission", "verified_url": "https://example.org/synthetic-rules", "retrieved_on": "2026-01-01",
            "rules": {
                "main_text": {"status": "verified", "page_limit": 9, "notes": "Synthetic fixture only."},
                "references": {"status": "verified", "policy": "unlimited", "page_limit": None, "notes": "Synthetic fixture only."},
                "appendix": {"status": "verified", "policy": "unlimited", "page_limit": None, "columns": "venue_template", "notes": "Synthetic fixture only."},
                "ai_assistance": {"status": "verified", "mode": "drafting_allowed", "disclosure": "Synthetic policy requires a tool-use statement.", "source_url": "https://example.org/synthetic-ai-policy", "retrieved_on": "2026-01-01", "notes": "Synthetic fixture only."},
            },
        }
        (self.root / "artifacts" / "results.json").write_text('{"score": 0.8}\n', encoding="utf-8")

    def save(self):
        (self.root / "evidence-ledger.json").write_text(json.dumps(self.ledger), encoding="utf-8")
        (self.root / "venue-profile.json").write_text(json.dumps(self.venue), encoding="utf-8")

    def run_audit(self, mode="ready", save=True):
        if save:
            self.save()
        result = subprocess.run([sys.executable, str(AUDIT), str(self.root), "--mode", mode, "--json"], capture_output=True, text=True)
        self.assertNotIn("Traceback", result.stderr)
        return result.returncode, json.loads(result.stdout)

    def assert_issue(self, report, code):
        self.assertIn(code, [issue["code"] for issue in report["issues"]], report)

    def test_project_root_symlink_loop_reports_json_error(self):
        loop = Path(self.temp.name) / "loop"
        loop.symlink_to(loop.name)
        result = subprocess.run([sys.executable, str(AUDIT), str(loop), "--json"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "invalid")
        self.assert_issue(report, "project")

    def test_legitimate_registered_evidence_passes_mechanical_checks_only(self):
        code, report = self.run_audit()
        self.assertEqual(code, 0)
        self.assertEqual(report["status"], "checks_passed")
        self.assertFalse(report["submission_readiness_certified"])
        self.assertTrue(report["limitations"])

    def test_initializer_contains_no_invented_records_or_venue_rules(self):
        ledger = json.loads((self.root / "evidence-ledger.json").read_text())
        self.assertEqual(ledger, {"schema_version": 1, "claims": [], "evidence": [], "citations": []})
        venue = json.loads((self.root / "venue-profile.json").read_text())
        self.assertIsNone(venue["rules"]["main_text"]["page_limit"])
        self.assertEqual(venue["rules"]["ai_assistance"]["mode"], "unknown")
        code, report = self.run_audit(mode="draft", save=False)
        self.assertEqual(code, 1)
        self.assertEqual(report["status"], "pending")
        self.assert_issue(report, "empty_claims")

    def test_initializer_never_overwrites_existing_work(self):
        manuscript = self.root / "paper.md"
        manuscript.write_text("Keep this work.", encoding="utf-8")
        result = subprocess.run([sys.executable, str(INIT), str(self.root)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(manuscript.read_text(), "Keep this work.")

    def test_unsupported_empirical_claim_blocks_ready_mode(self):
        self.ledger["claims"][0]["status"] = "unsupported"
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assertEqual(report["status"], "blocked")
        self.assert_issue(report, "unverified")

    def test_claim_without_evidence_does_not_pass(self):
        self.ledger["claims"][0]["evidence_ids"] = []
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assert_issue(report, "missing_support")

    def test_theoretical_guarantee_cannot_rely_only_on_experiments(self):
        self.ledger["claims"][0]["kind"] = "theoretical"
        self.ledger["claims"][0]["text"] = "Synthetic procedure has a convergence guarantee."
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assert_issue(report, "evidence_kind")

    def test_theoretical_claim_with_registered_proof_passes_mechanical_checks(self):
        self.ledger["claims"][0]["kind"] = "theoretical"
        self.ledger["claims"][0]["text"] = "Synthetic lemma has a supplied proof."
        evidence = self.ledger["evidence"][0]
        evidence["kind"] = "proof"
        evidence["artifact"] = "artifacts/proof.md"
        evidence["locator"] = "Synthetic lemma and proof"
        evidence["scope"] = {key: None for key in evidence["scope"]}
        (self.root / "artifacts" / "proof.md").write_text("Synthetic lemma: 1 = 1. Proof: reflexivity of equality.\n")
        code, report = self.run_audit()
        self.assertEqual(code, 0)
        self.assertFalse(report["submission_readiness_certified"])

    def test_missing_artifact_blocks_readiness(self):
        (self.root / "artifacts" / "results.json").unlink()
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assert_issue(report, "missing_artifact")

    def test_empty_artifact_blocks_readiness(self):
        (self.root / "artifacts" / "results.json").write_text("")
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assert_issue(report, "empty_artifact")

    def test_nan_and_overflow_are_invalid_json_numbers(self):
        self.save()
        path = self.root / "evidence-ledger.json"
        original = path.read_text()
        for value in ("NaN", "Infinity", "-Infinity", "1e9999"):
            with self.subTest(value=value):
                path.write_text(original.replace('"score": 0.8', '"score": ' + value))
                code, report = self.run_audit(save=False)
                self.assertEqual(code, 2)
                self.assert_issue(report, "input")

    def test_invalid_schema_rejected_without_traceback(self):
        for invalid in ([], {"schema_version": True}, {"schema_version": 1, "claims": "not an array", "evidence": [], "citations": []}):
            with self.subTest(invalid=invalid):
                self.ledger = invalid
                code, report = self.run_audit()
                self.assertEqual(code, 2)
                self.assert_issue(report, "schema")

    def test_malformed_nested_types_are_rejected_without_traceback(self):
        self.ledger["claims"][0]["kind"] = {"bad": "type"}
        self.ledger["evidence"][0]["kind"] = ["experiment"]
        self.ledger["evidence"][0]["scope"] = None
        self.venue["rules"]["appendix"]["policy"] = ["unlimited"]
        code, report = self.run_audit()
        self.assertEqual(code, 2)
        self.assert_issue(report, "schema")

    def test_traversal_and_absolute_paths_are_rejected(self):
        for path in ("../outside.json", "/etc/passwd", "C:\\outside.json"):
            with self.subTest(path=path):
                self.ledger["evidence"][0]["artifact"] = path
                code, report = self.run_audit()
                self.assertEqual(code, 2)
                self.assert_issue(report, "unsafe_path")

    def test_symlink_escaping_project_is_rejected(self):
        outside = Path(self.temp.name) / "outside.json"
        outside.write_text('{"score": 0.8}')
        (self.root / "artifacts" / "escape.json").symlink_to(outside)
        self.ledger["evidence"][0]["artifact"] = "artifacts/escape.json"
        code, report = self.run_audit()
        self.assertEqual(code, 2)
        self.assert_issue(report, "unsafe_path")

    def test_duplicate_and_dangling_ids_rejected(self):
        self.ledger["evidence"].append(copy.deepcopy(self.ledger["evidence"][0]))
        self.ledger["claims"][0]["citation_ids"] = ["missing"]
        code, report = self.run_audit()
        self.assertEqual(code, 2)
        self.assert_issue(report, "duplicate_id")
        self.assert_issue(report, "dangling_id")

    def test_verified_label_cannot_replace_citation_metadata(self):
        self.ledger["citations"][0]["source_url"] = None
        self.ledger["citations"][0]["title"] = None
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assert_issue(report, "unresolved")

    def test_unknown_venue_rules_block_ready_mode(self):
        self.venue["rules"]["main_text"] = {"status": "unknown", "page_limit": None, "notes": None}
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assert_issue(report, "unknown_rule")

    def test_unknown_ai_policy_cannot_produce_clean_report(self):
        self.venue["rules"]["ai_assistance"] = {"status": "unknown", "mode": "unknown", "disclosure": None, "source_url": None, "retrieved_on": None, "notes": None}
        for mode in ("draft", "ready"):
            with self.subTest(mode=mode):
                code, report = self.run_audit(mode=mode)
                self.assertEqual(code, 1)
                self.assert_issue(report, "unknown_rule")

    def test_ai_policy_needs_source_date_and_disclosure_rule(self):
        original = copy.deepcopy(self.venue["rules"]["ai_assistance"])
        for field in ("source_url", "retrieved_on", "disclosure"):
            with self.subTest(field=field):
                self.venue["rules"]["ai_assistance"] = copy.deepcopy(original)
                self.venue["rules"]["ai_assistance"][field] = None
                code, report = self.run_audit()
                self.assertEqual(code, 1)
                self.assert_issue(report, "unresolved")

    def test_ai_policy_invalid_source_and_date_are_rejected(self):
        self.venue["rules"]["ai_assistance"]["source_url"] = "not a URL"
        self.venue["rules"]["ai_assistance"]["retrieved_on"] = "2026-13-40"
        code, report = self.run_audit()
        self.assertEqual(code, 2)
        self.assert_issue(report, "schema")

    def test_source_urls_reject_invalid_ports_and_raw_control_characters(self):
        sources = (
            (self.ledger["citations"][0], "source_url"),
            (self.venue, "verified_url"),
            (self.venue["rules"]["ai_assistance"], "source_url"),
        )
        invalid_urls = (
            "https://example.org:invalid/synthetic-source",
            "https://example.org:65536/synthetic-source",
            "https://example.org/synthetic-source\x00",
            "\x01https://example.org/synthetic-source",
            "https://example.org/synthetic-source\x7f",
        )
        for record, field in sources:
            original = record[field]
            for value in invalid_urls:
                with self.subTest(field=field, value=value):
                    record[field] = value
                    code, report = self.run_audit()
                    self.assertEqual(code, 2)
                    self.assert_issue(report, "schema")
            record[field] = original

    def test_source_url_with_valid_explicit_port_passes(self):
        self.ledger["citations"][0]["source_url"] = "https://example.org:8443/synthetic-source"
        code, report = self.run_audit()
        self.assertEqual(code, 0)
        self.assertFalse(report["submission_readiness_certified"])

    def test_known_restrictive_ai_policy_does_not_certify_actual_compliance(self):
        for mode in ("editing_author_text_only", "prohibited"):
            with self.subTest(mode=mode):
                self.venue["rules"]["ai_assistance"]["mode"] = mode
                code, report = self.run_audit()
                self.assertEqual(code, 0)
                self.assertFalse(report["submission_readiness_certified"])

    def test_optional_hash_detects_changed_artifact(self):
        self.ledger["evidence"][0]["provenance"]["sha256"] = "0" * 64
        code, report = self.run_audit()
        self.assertEqual(code, 1)
        self.assert_issue(report, "hash_mismatch")

    def test_duplicate_json_keys_are_rejected(self):
        self.save()
        path = self.root / "evidence-ledger.json"
        path.write_text('{"schema_version": 1, "schema_version": 2, "claims": [], "evidence": [], "citations": []}')
        code, report = self.run_audit(save=False)
        self.assertEqual(code, 2)
        self.assert_issue(report, "input")


if __name__ == "__main__":
    unittest.main()
