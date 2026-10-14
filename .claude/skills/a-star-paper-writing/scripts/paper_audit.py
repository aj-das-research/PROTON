#!/usr/bin/env python3
"""Check a paper project's evidence ledger and recorded venue rules (Python 3.9+).

Usage: paper_audit.py PROJECT_DIR [--mode draft|ready] [--json]
Inputs: PROJECT_DIR/evidence-ledger.json and PROJECT_DIR/venue-profile.json.
See assets/*.example.json for schema version 1. Artifact paths are relative to
PROJECT_DIR; absolute paths, traversal, and symlinks escaping it are rejected.
Exit 0: mechanical checks pass; 1: unresolved checks; 2: invalid input/schema.
Draft mode reports unresolved items as pending; ready mode calls them blockers.

This is a ledger consistency checker, not a LaTeX parser or a truth detector.
It cannot certify source authenticity, manuscript coverage, scientific validity,
PDF formatting, official-rule accuracy, or conference acceptance.
"""

import argparse
import datetime as dt
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import urlparse


STATUSES = {"verified", "pending", "unsupported"}
CLAIM_KINDS = {"empirical", "theoretical", "methodological", "background", "limitation"}
EVIDENCE_KINDS = {"experiment", "proof", "analysis", "literature", "artifact"}
SCOPE_KEYS = ("dataset", "split", "metric", "unit", "baseline", "budget")
POLICIES = {"included_in_main_limit", "separate_limited", "unlimited", "not_allowed"}
LIMITATIONS = [
    "Artifact existence and optional hashes do not prove that evidence is true or provenance is authentic.",
    "Only registered claims and citations are checked; manuscript completeness and citation entailment need human review.",
    "Venue rules are user-recorded metadata; this tool does not fetch official rules or inspect PDF pages and formatting.",
    "A recorded AI-assistance policy does not establish that actual assistance or disclosure complies with it.",
    "Passing these checks does not certify submission readiness, scientific quality, or acceptance.",
]


def strict_json(path):
    """Reject nonstandard constants, duplicate keys, and nonfinite overflow."""
    def reject_constant(value):
        raise ValueError("nonfinite JSON number: " + value)

    def unique_keys(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ValueError("duplicate JSON key: " + key)
            obj[key] = value
        return obj

    def finite(value):
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError("nonfinite JSON number")
        if isinstance(value, dict):
            for item in value.values():
                finite(item)
        elif isinstance(value, list):
            for item in value:
                finite(item)

    with path.open(encoding="utf-8") as handle:
        value = json.load(handle, parse_constant=reject_constant, object_pairs_hook=unique_keys)
    finite(value)
    return value


class Audit:
    def __init__(self, root, mode):
        self.root = root
        self.mode = mode
        self.issues = []
        self.counts = {"claims": 0, "evidence": 0, "citations": 0}

    def issue(self, code, path, message, invalid=False):
        severity = "error" if invalid else ("pending" if self.mode == "draft" else "blocker")
        self.issues.append({"severity": severity, "code": code, "path": path, "message": message})

    def obj(self, value, path, required):
        if not isinstance(value, dict):
            self.issue("schema", path, "Expected an object.", True)
            return {}
        for key in required:
            if key not in value:
                self.issue("schema", path + "." + key, "Required field is missing.", True)
        return value

    def array(self, value, path):
        if not isinstance(value, list):
            self.issue("schema", path, "Expected an array.", True)
            return []
        return value

    def text(self, value, path, required=True):
        if value is not None and not isinstance(value, str):
            self.issue("schema", path, "Expected a string or null.", True)
            return False
        if value is None or not value.strip():
            if required:
                self.issue("unresolved", path, "A documented value is required.")
            return False
        return True

    def enum(self, value, path, choices):
        if not isinstance(value, str) or value not in choices:
            self.issue("schema", path, "Expected one of: " + ", ".join(sorted(choices)) + ".", True)
            return False
        return True

    def date(self, value, path):
        if not self.text(value, path):
            return
        try:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                raise ValueError()
            parsed = dt.date.fromisoformat(value)
            if parsed > dt.datetime.now(dt.timezone.utc).date():
                self.issue("future_date", path, "Verification/provenance date is in the future.")
        except ValueError:
            self.issue("schema", path, "Expected a valid ISO date (YYYY-MM-DD).", True)

    def url(self, value, path):
        if not self.text(value, path):
            return
        try:
            parsed = urlparse(value)
            # urlparse is a splitter: hostname alone does not validate a port,
            # and parsing can discard some raw control characters silently.
            parsed.port
            valid = (parsed.scheme in {"http", "https"} and parsed.hostname
                     and not any(c.isspace() or ord(c) < 32 or 127 <= ord(c) <= 159 for c in value))
        except ValueError:
            valid = False
        if not valid:
            self.issue("schema", path, "Expected an absolute HTTP(S) source URL.", True)

    def status(self, value, path):
        if self.enum(value, path, STATUSES) and value != "verified":
            self.issue("unverified", path, "Record is " + value + "; resolve or remove the associated claim before submission.")

    def path(self, value, label):
        if not self.text(value, label):
            return None
        candidate = PurePosixPath(value)
        if candidate.is_absolute() or ".." in candidate.parts or "\\" in value or re.match(r"^[A-Za-z]:", value):
            self.issue("unsafe_path", label, "Use a relative path inside the project without '..' or backslashes.", True)
            return None
        try:
            resolved = (self.root / value).resolve()
            resolved.relative_to(self.root)
        except (ValueError, OSError, RuntimeError):
            self.issue("unsafe_path", label, "Path resolves outside the project or cannot be resolved safely.", True)
            return None
        if not resolved.is_file():
            self.issue("missing_artifact", label, "Artifact does not exist as a regular file: " + value)
            return None
        try:
            if resolved.stat().st_size == 0:
                self.issue("empty_artifact", label, "An empty artifact cannot substantiate a claim: " + value)
        except OSError as error:
            self.issue("unreadable_artifact", label, str(error))
            return None
        return resolved

    def records(self, ledger, key, required):
        result = {}
        entries = self.array(ledger.get(key), key)
        self.counts[key] = len(entries)
        if not entries:
            self.issue("empty_" + key, key, "No " + key + " are registered; this ledger cannot pass readiness checks.")
        for index, entry in enumerate(entries):
            path = key + "[" + str(index) + "]"
            obj = self.obj(entry, path, required)
            record_id = obj.get("id")
            if not isinstance(record_id, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_.:-]*", record_id):
                self.issue("schema", path + ".id", "Expected a nonempty ID starting with a letter; use letters, digits, _, ., :, or -.", True)
            elif record_id in result:
                self.issue("duplicate_id", path + ".id", "Duplicate ID: " + record_id, True)
            else:
                result[record_id] = (obj, path)
        return result

    def links(self, record, key, path, targets):
        ids = self.array(record.get(key), path + "." + key)
        seen = set()
        for index, target_id in enumerate(ids):
            label = path + "." + key + "[" + str(index) + "]"
            if not isinstance(target_id, str):
                self.issue("schema", label, "Expected an ID string.", True)
            elif target_id in seen:
                self.issue("duplicate_link", label, "Duplicate linked ID: " + target_id, True)
            elif target_id not in targets:
                self.issue("dangling_id", label, "No record exists for linked ID: " + target_id, True)
            elif targets[target_id][0].get("status") != "verified":
                self.issue("unverified_support", label, "Supporting record is not verified: " + target_id)
            if isinstance(target_id, str):
                seen.add(target_id)
        return ids

    def ledger(self, value):
        ledger = self.obj(value, "ledger", ("schema_version", "claims", "evidence", "citations"))
        if type(ledger.get("schema_version")) is not int or ledger.get("schema_version") != 1:
            self.issue("schema", "ledger.schema_version", "Expected integer schema version 1.", True)
        claims = self.records(ledger, "claims", ("id", "text", "kind", "status", "evidence_ids", "citation_ids"))
        evidence = self.records(ledger, "evidence", ("id", "kind", "status", "artifact", "locator", "scope", "provenance"))
        citations = self.records(ledger, "citations", ("id", "status", "title", "authors", "year", "source_url", "verified_on"))

        for entry, path in citations.values():
            self.status(entry.get("status"), path + ".status")
            self.text(entry.get("title"), path + ".title")
            authors = self.array(entry.get("authors"), path + ".authors")
            if not authors:
                self.issue("unresolved", path + ".authors", "Verified author metadata is required.")
            for index, author in enumerate(authors):
                self.text(author, path + ".authors[" + str(index) + "]")
            year = entry.get("year")
            if year is None:
                self.issue("unresolved", path + ".year", "Verified publication year is required.")
            elif type(year) is not int or not 1000 <= year <= 9999:
                self.issue("schema", path + ".year", "Expected a four-digit integer year.", True)
            self.url(entry.get("source_url"), path + ".source_url")
            self.date(entry.get("verified_on"), path + ".verified_on")

        for entry, path in evidence.values():
            self.status(entry.get("status"), path + ".status")
            self.enum(entry.get("kind"), path + ".kind", EVIDENCE_KINDS)
            artifact = self.path(entry.get("artifact"), path + ".artifact")
            self.text(entry.get("locator"), path + ".locator")
            scope = self.obj(entry.get("scope"), path + ".scope", SCOPE_KEYS)
            empirical = isinstance(entry.get("kind"), str) and entry.get("kind") in {"experiment", "analysis"}
            for key in SCOPE_KEYS:
                self.text(scope.get(key), path + ".scope." + key, required=empirical)
            provenance = self.obj(entry.get("provenance"), path + ".provenance", ("producer", "created_on", "description"))
            self.text(provenance.get("producer"), path + ".provenance.producer")
            self.date(provenance.get("created_on"), path + ".provenance.created_on")
            self.text(provenance.get("description"), path + ".provenance.description")
            if "values" in entry:
                values = self.obj(entry["values"], path + ".values", ())
                for name, number in values.items():
                    if type(number) not in {int, float}:
                        self.issue("schema", path + ".values." + name, "Expected a finite numeric value (not a string, boolean, or null).", True)
            if "sha256" in provenance:
                digest = provenance["sha256"]
                if not isinstance(digest, str) or not re.fullmatch(r"[a-fA-F0-9]{64}", digest):
                    self.issue("schema", path + ".provenance.sha256", "Expected a SHA-256 hexadecimal digest.", True)
                elif artifact:
                    try:
                        actual = hashlib.sha256()
                        with artifact.open("rb") as handle:
                            for block in iter(lambda: handle.read(1024 * 1024), b""):
                                actual.update(block)
                        if actual.hexdigest() != digest.lower():
                            self.issue("hash_mismatch", path + ".provenance.sha256", "Artifact differs from the recorded digest.")
                    except OSError as error:
                        self.issue("unreadable_artifact", path + ".artifact", str(error))

        for entry, path in claims.values():
            self.text(entry.get("text"), path + ".text")
            self.enum(entry.get("kind"), path + ".kind", CLAIM_KINDS)
            self.status(entry.get("status"), path + ".status")
            evidence_ids = self.links(entry, "evidence_ids", path, evidence)
            citation_ids = self.links(entry, "citation_ids", path, citations)
            kind = entry.get("kind")
            if isinstance(kind, str) and kind in {"empirical", "theoretical", "methodological"} and not evidence_ids:
                self.issue("missing_support", path + ".evidence_ids", "This claim requires at least one project evidence artifact.")
            elif entry.get("kind") == "background" and not citation_ids:
                self.issue("missing_support", path + ".citation_ids", "A background claim requires a verified citation.")
            elif not evidence_ids and not citation_ids:
                self.issue("missing_support", path, "Claim has no registered evidence or citation.")
            if entry.get("kind") == "empirical":
                supported = any(isinstance(item, str) and item in evidence and evidence[item][0].get("kind") in ("experiment", "analysis") for item in evidence_ids)
                if evidence_ids and not supported:
                    self.issue("evidence_kind", path + ".evidence_ids", "An empirical claim needs experiment or analysis evidence with its evaluation scope.")
            if entry.get("kind") == "theoretical":
                supported = any(isinstance(item, str) and item in evidence and evidence[item][0].get("kind") == "proof" for item in evidence_ids)
                if evidence_ids and not supported:
                    self.issue("evidence_kind", path + ".evidence_ids", "A theoretical guarantee needs at least one proof artifact; experimental evidence cannot establish it.")

    def venue(self, value):
        venue = self.obj(value, "venue", ("schema_version", "venue", "year", "track", "stage", "verified_url", "retrieved_on", "rules"))
        if type(venue.get("schema_version")) is not int or venue.get("schema_version") != 1:
            self.issue("schema", "venue.schema_version", "Expected integer schema version 1.", True)
        for key in ("venue", "track", "stage"):
            self.text(venue.get(key), "venue." + key)
        year = venue.get("year")
        if year is None:
            self.issue("unresolved", "venue.year", "Conference year must be recorded.")
        elif type(year) is not int or not 1000 <= year <= 9999:
            self.issue("schema", "venue.year", "Expected a four-digit integer year.", True)
        self.url(venue.get("verified_url"), "venue.verified_url")
        self.date(venue.get("retrieved_on"), "venue.retrieved_on")
        rules = self.obj(venue.get("rules"), "venue.rules", ("main_text", "references", "appendix", "ai_assistance"))
        for key in ("main_text", "references", "appendix"):
            path = "venue.rules." + key
            required = ("status", "page_limit", "notes") + (() if key == "main_text" else ("policy",))
            if key == "appendix":
                required += ("columns",)
            rule = self.obj(rules.get(key), path, required)
            status = rule.get("status")
            if self.enum(status, path + ".status", {"unknown", "verified"}) and status == "unknown":
                self.issue("unknown_rule", path, "Verify the official rule for this venue, year, track, and stage.")
            self.text(rule.get("notes"), path + ".notes", required=False)
            limit = rule.get("page_limit")
            if limit is not None and (type(limit) is not int or limit < 1):
                self.issue("schema", path + ".page_limit", "Expected a positive integer page limit or null.", True)
            if key == "main_text":
                if limit is None:
                    self.issue("unknown_rule", path + ".page_limit", "Record the explicit main-text page limit; do not assume 11 pages.")
                continue
            policy = rule.get("policy")
            if policy is None or policy == "unknown":
                self.issue("unknown_rule", path + ".policy", "Reference/appendix policy has not been verified.")
            elif self.enum(policy, path + ".policy", POLICIES):
                if policy == "separate_limited" and limit is None:
                    self.issue("unknown_rule", path + ".page_limit", "A separately limited section needs its explicit page limit.")
                elif policy != "separate_limited" and limit is not None:
                    self.issue("contradictory_rule", path + ".page_limit", "Only 'separate_limited' uses a separate page limit; otherwise use null.")
            if key == "appendix":
                columns = rule.get("columns")
                if columns is None or columns == "unknown":
                    self.issue("unknown_rule", path + ".columns", "Record the permitted appendix format; do not assume one column.")
                else:
                    self.enum(columns, path + ".columns", {"one_column", "two_column", "venue_template", "not_applicable"})
                    if policy == "not_allowed" and columns != "not_applicable":
                        self.issue("contradictory_rule", path + ".columns", "An appendix that is not allowed must use not_applicable.")
                    if isinstance(policy, str) and policy in POLICIES - {"not_allowed"} and columns == "not_applicable":
                        self.issue("contradictory_rule", path + ".columns", "An allowed appendix needs a verified format.")

        path = "venue.rules.ai_assistance"
        ai = self.obj(rules.get("ai_assistance"), path, ("status", "mode", "disclosure", "source_url", "retrieved_on", "notes"))
        if self.enum(ai.get("status"), path + ".status", {"unknown", "verified"}) and ai.get("status") == "unknown":
            self.issue("unknown_rule", path + ".status", "Verify the official AI-assistance policy before drafting.")
        if self.enum(ai.get("mode"), path + ".mode", {"unknown", "drafting_allowed", "editing_author_text_only", "prohibited"}) and ai.get("mode") == "unknown":
            self.issue("unknown_rule", path + ".mode", "Record the permitted assistance mode; do not infer drafting permission.")
        self.text(ai.get("disclosure"), path + ".disclosure")
        self.url(ai.get("source_url"), path + ".source_url")
        self.date(ai.get("retrieved_on"), path + ".retrieved_on")
        self.text(ai.get("notes"), path + ".notes", required=False)

    def report(self):
        invalid = any(issue["severity"] == "error" for issue in self.issues)
        status = "invalid" if invalid else ("pending" if self.mode == "draft" else "blocked") if self.issues else "checks_passed"
        return {"mode": self.mode, "status": status, "project": str(self.root), "counts": self.counts,
                "submission_readiness_certified": False, "issues": self.issues, "limitations": LIMITATIONS}, 2 if invalid else 1 if self.issues else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project_dir", type=Path)
    parser.add_argument("--mode", choices=("draft", "ready"), default="draft")
    parser.add_argument("--json", action="store_true", help="Emit a machine-readable JSON report instead of plain text.")
    args = parser.parse_args(argv)
    root_error = None
    try:
        root = args.project_dir.expanduser().resolve()
    except (OSError, ValueError, RuntimeError) as error:
        root = args.project_dir
        root_error = str(error)
    audit = Audit(root, args.mode)
    if root_error is not None:
        audit.issue("project", str(root), "Cannot resolve project directory: " + root_error, True)
    elif not root.is_dir():
        audit.issue("project", str(root), "Project directory does not exist.", True)
    else:
        for filename, check in (("evidence-ledger.json", audit.ledger), ("venue-profile.json", audit.venue)):
            try:
                # Ledger and profile symlinks must obey the same project boundary.
                path = (root / filename).resolve()
                path.relative_to(root)
                check(strict_json(path))
            except (OSError, ValueError, RecursionError, RuntimeError) as error:
                audit.issue("input", filename, str(error), True)
    report, exit_code = audit.report()
    if args.json:
        print(json.dumps(report, indent=2, allow_nan=False))
    else:
        print("Ledger audit: " + report["status"] + " (" + args.mode + ")")
        print("Project: " + str(root))
        print("Records: " + ", ".join(str(count) + " " + key for key, count in audit.counts.items()))
        for issue in audit.issues:
            print(issue["severity"].upper() + " [" + issue["code"] + "] " + issue["path"] + ": " + issue["message"])
        for limitation in LIMITATIONS:
            print("Limit: " + limitation)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
