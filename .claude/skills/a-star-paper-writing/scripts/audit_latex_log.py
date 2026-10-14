#!/usr/bin/env python3
"""Triage a downloaded or local LaTeX log without executing TeX (Python 3.9+).

Usage: audit_latex_log.py BUILD.log [--json]
Exit 0: no recognized issues in a complete-looking LaTeX/PDF log.
Exit 1: errors, unresolved references/citations, layout warnings, or incomplete log.
Exit 2: unreadable input. This does not compile, modify, or synchronize a project.
The caller must associate the log with the actual source revision and inspect
the corresponding PDF. A log alone does not prove freshness or build success.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


PATTERNS = [
    ("tex_error", "error", re.compile(r"^!|(?:LaTeX|Package [\w.-]+) Error:|Fatal error occurred|Emergency stop|I can't find file", re.I)),
    ("undefined_citation", "warning", re.compile(r"(?:Citation.*undefined|undefined citations|citation.*not found|couldn't open database file)", re.I)),
    ("undefined_reference", "warning", re.compile(r"(?:Reference.*undefined|undefined references)", re.I)),
    ("duplicate_label", "warning", re.compile(r"(?:Label.*multiply defined|multiply-defined labels)", re.I)),
    ("rerun_needed", "warning", re.compile(r"(?:Rerun to get cross-references right|Label\(s\) may have changed|Please \(re\)run (?:Biber|BibTeX)|Please rerun LaTeX|rerunfilecheck Warning)", re.I)),
    ("overfull_box", "warning", re.compile(r"Overfull \\[hv]box", re.I)),
    ("missing_character", "warning", re.compile(r"Missing character:", re.I)),
    ("font_substitution", "warning", re.compile(r"(?:Font shape.*undefined|Some font shapes were not available|Size substitutions with differences)", re.I)),
    ("bibliography_failure", "error", re.compile(r"(?:Biber|BibTeX).*ERROR|I found no \\bibdata command|I couldn't open style file", re.I)),
]

# File-line mode removes the usual leading "!" from many recovered TeX errors.
# Classify their source location, not a necessarily incomplete list of messages.
FILE_LINE_DIAGNOSTIC = re.compile(
    r"^(?P<path>(?:[A-Za-z]:)?[^\r\n]+?):(?P<line>\d+):\s*(?P<message>\S.*)$"
)
WARNING_PREFIX = re.compile(
    r"^(?:(?:LaTeX(?: Font)?|Package \S+|Class \S+|pdfTeX|XeTeX|LuaTeX|LuaHBTeX)\s+)?Warning\b|^Overfull \\[hv]box\b",
    re.I,
)
ADVISORY_PREFIX = re.compile(
    r"^(?:(?:LaTeX(?: Font)?|Package \S+|Class \S+)\s+)?Info\b|^Underfull \\[hv]box\b",
    re.I,
)
ENGINE_BANNER = re.compile(r"^This is (?:pdfTeX|XeTeX|LuaHBTeX|LuaTeX|e-TeX|TeX)\b", re.M)

LIMITS = [
    "Inspects only recognized messages in the supplied log; it is not a TeX parser or an exhaustive compiler-error classifier.",
    "Does not execute a compiler, check its exit code, inspect PDF bytes, or establish which source revision produced the log.",
    "A reported PDF output is not proof that the document is current, visually correct, or free of recovered TeX errors.",
    "Completion markers describe the final recognized engine invocation; recognized diagnostics from all invocations are retained.",
    "Warnings need context and visual review; benign underfull-box notices are counted separately, not treated as failures.",
    "Does not verify scientific claims, venue compliance, collaborator state, or Overleaf synchronization.",
]


def inspect_log(raw, path):
    text = raw.decode("utf-8", errors="replace")
    issues = []
    seen = set()

    def add_issue(code, severity, number, line):
        key = (code, line.strip())
        if key not in seen:
            issues.append({"code": code, "severity": severity, "log_line": number, "message": line.strip()[:500]})
            seen.add(key)

    for number, line in enumerate(text.splitlines(), 1):
        diagnostic = FILE_LINE_DIAGNOSTIC.match(line)
        if diagnostic:
            message = diagnostic["message"]
            if WARNING_PREFIX.search(message):
                add_issue("file_line_warning", "warning", number, line)
            elif not ADVISORY_PREFIX.search(message):
                add_issue("file_line_error", "error", number, line)
        for code, severity, pattern in PATTERNS:
            if pattern.search(line):
                add_issue(code, severity, number, line)
    invocations = list(ENGINE_BANNER.finditer(text))
    engine_seen = bool(invocations)
    latest_start = invocations[-1].start() if invocations else 0
    latest_text = text[latest_start:]
    latest_line = text.count("\n", 0, latest_start) + 1 if invocations else None
    latex_seen = "LaTeX2e" in latest_text or "LaTeX3" in latest_text
    output_seen = bool(re.search(r"Output written on\s+[^\r\n]*(?:\r?\n[^\r\n]*)?\.pdf\b", latest_text))
    if not engine_seen or not latex_seen:
        issues.append({"code": "unrecognized_or_partial_log", "severity": "warning", "log_line": latest_line, "message": "A full LaTeX engine banner was not found for the final invocation; obtain the complete build log."})
    if not output_seen:
        issues.append({"code": "no_pdf_output_reported", "severity": "warning", "log_line": latest_line, "message": "No PDF output marker was found for the final invocation; inspect build completion and the actual PDF."})
    if "\ufffd" in text:
        issues.append({"code": "decoding_replacements", "severity": "warning", "log_line": None, "message": "Some log bytes were not valid UTF-8; inspect the original log encoding."})
    error = any(issue["severity"] == "error" for issue in issues)
    return {
        "status": "errors_detected" if error else "issues_detected" if issues else "no_known_issues",
        "log": str(path), "log_sha256": hashlib.sha256(raw).hexdigest(),
        "tex_engine_banner_seen": engine_seen, "latex_format_seen": latex_seen,
        "engine_invocation_count": len(invocations), "latest_invocation_start_line": latest_line,
        "pdf_output_reported": output_seen,
        "underfull_box_advisories": len(re.findall(r"Underfull \\[hv]box", text)),
        "source_revision_verified": False, "pdf_verified": False, "sync_verified": False,
        "issues": issues, "limitations": LIMITS,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("log", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = inspect_log(args.log.read_bytes(), args.log)
    except (OSError, ValueError, RuntimeError) as error:
        report = {"status": "invalid_input", "log": str(args.log), "issues": [{"code": "unreadable_log", "severity": "error", "message": str(error)}], "limitations": LIMITS}
        code = 2
    else:
        code = 1 if report["issues"] else 0
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("LaTeX log: " + report["status"])
        for issue in report["issues"]:
            print(issue["severity"].upper() + " [" + issue["code"] + "] " + issue["message"])
        print("This log inspection does not verify source freshness, the PDF, or Overleaf sync.")
    return code


if __name__ == "__main__":
    sys.exit(main())
