#!/usr/bin/env python3
"""Lint LaTeX prose against the house style (references/house-style.md).

Flags what the author and their lab repeatedly correct:
  em dashes, semicolons, hype and LLM-marker words, formulaic openers,
  parenthetical cross-references, figure-first sentences, decimals without a
  leading zero, model names outside \\texttt{}, '10x' multipliers, 'significant'
  without a test, underselling and report-style phrasing, long paragraphs, and
  number-heavy abstracts.

  python style_lint.py FILE_OR_DIR [...] [--json] [--rules S01,S04] [--max 20]

LaTeX comments, verbatim blocks, math and labreview margin comments are
ignored, so the lint reads only the prose a reader sees. Exit code 0 means no
findings, 1 means findings, and 2 means bad input. This is a mechanical aid: it
cannot judge argument or truth. Python 3.9+, standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RULES = {
    "S01": ("em dash in prose", "recast with a comma, parentheses, or a second sentence"),
    "S02": ("semicolon in prose", "split into two sentences"),
    "S03": ("hype or LLM-marker word", "state the measured property instead"),
    "S04": ("formulaic opener or filler sentence", "start with the content"),
    "S05": ("parenthetical cross-reference", "write the pointer into the sentence: 'as Appendix B shows'"),
    "S06": ("sentence opens with 'Figure X shows'", "state the point first, then cite the figure inside the sentence"),
    "S07": ("decimal without a leading zero", "write 0.645, not .645"),
    "S08": ("model name outside \\texttt{}", "write \\texttt{Qwen3.5-9B}"),
    "S09": ("multiplier written as '10x'", "write $10\\times$"),
    "S10": ("'significant' without a statistical test", "give the test and p-value, or state the number"),
    "S11": ("underselling wording", "describe scope by what the work covers; no 'pilot', 'toy', 'earlier study'"),
    "S12": ("report-style phrasing", "state the protocol once in the setup; no run names, file paths, or experiment numbers"),
    "S13": ("paragraph longer than about 7 printed lines", "one point per paragraph; split it"),
    "S14": ("abstract carries many numbers", "at most one or two numbers, at the end, each with metric and baseline"),
}

HYPE = [
    "groundbreaking", "cutting-edge", "paradigm", "holistic", "delve", "delves", "showcase", "showcases",
    "unprecedented", "revolutionary", "seamless", "seamlessly", "remarkable", "remarkably", "striking",
    "strikingly", "crucially", "importantly", "notably", "tapestry", "intricate", "pivotal", "realm",
    "underscore", "underscores", "harness", "unlock", "unlocks", "empower", "empowers", "meticulous",
    "meticulously", "commendable",
]
FORMULAIC = [
    r"to address (these|this|the above) (limitations?|challenges?|issues?|gaps?)", r"to obtain this property",
    r"in this paper, we", r"concretely,", r"it is worth noting", r"it can be (observed|seen) that", r"in summary,",
    r"taken together,", r"this section (begins|presents|describes|introduces)", r"we now (ask|turn|describe|present)",
    r"plays a (crucial|key|vital|pivotal) role", r"in recent years", r"has (gained|attracted|received) (significant|considerable|increasing|growing) attention",
    r"(first|second|third)ly,",
]
UNDERSELL = [
    r"\bpilot (study|studies|experiments?)\b", r"\btoy (tasks?|examples?|settings?|problems?)\b",
    r"\bpreliminary (results?|evidence|study)\b", r"\bearlier (study|version|draft)\b", r"\bprevious (version|draft)\b",
    r"\bsmall[- ]scale\b", r"\bonly marginal(ly)?\b", r"\bwe were unable to\b", r"\bunfortunately,",
]
REPORT = [
    r"\bacross (three|3|five|5|two|2) (seed runs|seeds runs|runs)\b", r"\bexp\d+\b", r"\bexperiment \d{2,}\b",
    r"\b[\w\-]+/[\w\-/]+\.(json|csv|py|yaml|jsonl|txt)\b", r"\bjob (id )?\d{4,}\b", r"\brun [a-z0-9_\-]+_(v\d|final)\b",
]
MODEL_RE = re.compile(r"(?<![\w\\{/-])((?:Qwen|Llama|LLaMA|Gemma|Mistral|Mixtral|DeepSeek|Kimi|Phi|OLMo|Gemini|Claude|GPT|Falcon|GLM)[\w.\-]*\d[\w.\-]*)")
REVIEW_MACROS = re.compile(r"\\(Review(Caption|FigureBox|TableBox|EquationBox|AlgorithmLine|ReplaceComment|Replace|Delete|Add|Note|Mark)?|Nils|RevID)\b")


def blank_region(chars: list[str], a: int, b: int) -> None:
    for i in range(a, min(b, len(chars))):
        if chars[i] != "\n":
            chars[i] = " "


def prose_view(text: str) -> str:
    """Same-length text with comments, verbatim, math and review comments blanked."""
    chars = list(text)
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c == "\\":
            m = re.match(r"\\begin\{(verbatim|lstlisting|minted|comment|equation\*?|align\*?|gather\*?|multline\*?|displaymath)\}", text[i:])
            if m:
                end = text.find("\\end{" + m.group(1) + "}", i)
                end = n if end < 0 else end + len(m.group(1)) + 6
                blank_region(chars, i, end)
                i = end
                continue
            if text.startswith("\\[", i):
                end = text.find("\\]", i + 2)
                end = n if end < 0 else end + 2
                blank_region(chars, i, end)
                i = end
                continue
            i += 2
            continue
        if c == "%":
            end = text.find("\n", i)
            end = n if end < 0 else end
            blank_region(chars, i, end)
            i = end
            continue
        if c == "$":
            j = i + 1
            while j < n and not (text[j] == "$" and text[j - 1] != "\\"):
                j += 1
            blank_region(chars, i, j + 1)
            i = j + 1
            continue
        i += 1
    view = "".join(chars)
    # drop the comment argument of labreview macros so reviewer notes are not linted as prose
    for m in REVIEW_MACROS.finditer(view):
        k = m.end()
        while k < n and view[k] in " [":
            if view[k] == "[":
                close = view.find("]", k)
                k = close + 1 if close > 0 else k + 1
            else:
                k += 1
        groups = []
        for _ in range(4):
            if k < n and view[k] == "{":
                depth, j = 0, k
                while j < n:
                    if view[j] == "\\":
                        j += 2
                        continue
                    if view[j] == "{":
                        depth += 1
                    elif view[j] == "}":
                        depth -= 1
                        if depth == 0:
                            break
                    j += 1
                groups.append((k, j))
                k = j + 1
            else:
                break
        name = m.group(1)
        if name == "RevID":
            continue
        drop = groups[1:] if name in ("Review", "ReviewCaption", "Nils") else groups[2:] if "Box" in name or name == "ReviewMark" else groups[2:] if name == "ReviewReplaceComment" else []
        for a, b in drop:
            blank_region(chars, a, b + 1)
    return "".join(chars)


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def excerpt(text: str, pos: int, width: int = 90) -> str:
    return " ".join(text[max(0, pos - width // 2): pos + width // 2].split())


def lint_text(path: str, text: str, enabled: set[str]) -> list[dict]:
    view = prose_view(text)
    low = view.lower()
    out: list[dict] = []

    def add(rule: str, pos: int) -> None:
        if rule in enabled:
            out.append({"file": path, "line": line_of(text, pos), "rule": rule, "what": RULES[rule][0],
                        "fix": RULES[rule][1], "excerpt": excerpt(text, pos)})

    in_table = [False] * len(view)
    for m in re.finditer(r"\\begin\{tabular\*?\}.*?\\end\{tabular\*?\}", view, re.S):
        for t in range(m.start(), m.end()):
            in_table[t] = True
    for m in re.finditer(r"---|\u2014", view):
        if not in_table[m.start()]:
            add("S01", m.start())
    for m in re.finditer(r"(?<!\\);", view):
        if not in_table[m.start()]:
            add("S02", m.start())
    for w in HYPE:
        for m in re.finditer(r"\b" + re.escape(w) + r"\b", low):
            add("S03", m.start())
    for pat in FORMULAIC:
        for m in re.finditer(pat, low):
            add("S04", m.start())
    for m in re.finditer(r"\((?:see\s+)?(?:App\.|Appendix|Fig\.|Figure|Tab\.|Table|Sec\.|Section|\\S|\\[cC]ref|\\ref)", view):
        add("S05", m.start())
    for m in re.finditer(r"(?:^|[.!?]\s+)((?:Figure|Fig\.|Table)~?\\ref\{[^}]*\}|\\[Cc]ref\{[^}]*\})\s+(shows|illustrates|presents|reports|summarizes|depicts|demonstrates)", view, re.M):
        add("S06", m.start(1))
    nocomment = re.sub(r"(?<!\\)%[^\n]*", lambda m: " " * len(m.group(0)), text)
    for m in re.finditer(r"(?<![\w.\\}\]\d/])\.\d+\b", nocomment):
        add("S07", m.start())  # applies in prose, math and tables alike
    for m in MODEL_RE.finditer(view):
        before = view[max(0, m.start() - 9): m.start()]
        if "texttt{" in before or "\\tt " in before or "cite" in before or "label{" in before:
            continue
        add("S08", m.start())
    for m in re.finditer(r"(?<![\w$])\d+(?:\.\d+)?\s?x(?![\w])", view):
        add("S09", m.start())
    for m in re.finditer(r"\bsignificant(ly)?\b", low):
        sent = low[max(0, m.start() - 160): m.start() + 160]
        if not re.search(r"p\s*[<=]|p-value|t-test|wilcoxon|bootstrap|confidence interval|permutation", sent):
            add("S10", m.start())
    for pat in UNDERSELL:
        for m in re.finditer(pat, low):
            add("S11", m.start())
    for pat in REPORT:
        for m in re.finditer(pat, low):
            add("S12", m.start())
    pos = 0
    for block in re.split(r"\n[ \t]*\n", view):
        start = view.find(block, pos)
        pos = start + len(block)
        if re.search(r"\\begin\{(figure|table|itemize|enumerate|algorithm|abstract)", block):
            continue
        words = len(re.sub(r"\\[A-Za-z]+|[{}%]", " ", block).split())
        if words > 150:
            add("S13", start)
    ab = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.S)
    if ab:
        nums = re.findall(r"\d+(?:\.\d+)?\s*\\?%|\d+\.\d+", ab.group(1))
        if len(nums) > 2:
            add("S14", ab.start())
    return out


def gather(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            files.extend(sorted(x for x in p.rglob("*.tex") if ".git" not in x.parts))
        elif p.is_file():
            files.append(p)
        else:
            raise FileNotFoundError(raw)
    return files


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--rules", help="comma-separated subset, e.g. S01,S07")
    ap.add_argument("--max", type=int, default=25, help="max findings listed per rule")
    args = ap.parse_args(argv)
    try:
        files = gather(args.paths)
    except FileNotFoundError as exc:
        print(f"not found: {exc}", file=sys.stderr)
        return 2
    enabled = set(args.rules.split(",")) if args.rules else set(RULES)
    findings: list[dict] = []
    for f in files:
        findings.extend(lint_text(str(f), f.read_text(encoding="utf-8", errors="replace"), enabled))
    seen: dict[str, int] = {}
    listed = []
    for item in sorted(findings, key=lambda r: (r["rule"], r["file"], r["line"])):
        seen[item["rule"]] = seen.get(item["rule"], 0) + 1
        if seen[item["rule"]] <= args.max:
            listed.append(item)
    if args.json:
        print(json.dumps({"counts": seen, "findings": listed}, indent=2, ensure_ascii=False))
    else:
        for item in listed:
            print(f"{item['file']}:{item['line']}: {item['rule']} {item['what']}: {item['excerpt']}  -> {item['fix']}")
        if seen:
            print("counts: " + ", ".join(f"{k}={v}" for k, v in sorted(seen.items())), file=sys.stderr)
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
