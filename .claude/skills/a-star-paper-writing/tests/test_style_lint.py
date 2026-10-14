"""Tests for scripts/style_lint.py (house-style lint)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import style_lint  # noqa: E402

SAMPLE = r"""
\begin{abstract}
In this pilot study we reach 61.2\% and 70.1\% and 72.4\% and .81 accuracy.
\end{abstract}
To address these limitations, we propose X --- a method that notably improves results; it is striking.
Across three seed runs, Qwen3.5-9B reaches .645 (Appendix~\ref{app:a}) and runs 3x faster.
Figure~\ref{fig:a} shows that X significantly beats Y. See results/table1.json for the run askr_v3_final.
% This commented sentence uses a semicolon; and --- an em dash, but must be ignored.
We use \texttt{Qwen3.5-9B}; the value $\alpha=.5$ appears in math.
\Review[Nils]{some words}{a note with a semicolon; and hype like groundbreaking}
"""


def rules(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for f in style_lint.lint_text("sample.tex", text, set(style_lint.RULES)):
        counts[f["rule"]] = counts.get(f["rule"], 0) + 1
    return counts


class StyleLintTests(unittest.TestCase):
    def test_flags_house_style_violations(self) -> None:
        c = rules(SAMPLE)
        for rule in ("S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S14"):
            self.assertIn(rule, c, rule)

    def test_ignores_comments_texttt_and_review_notes(self) -> None:
        c = rules(SAMPLE)
        self.assertEqual(c["S01"], 1)  # the commented em dash is ignored
        self.assertEqual(c["S08"], 1)  # the \texttt model name is fine
        self.assertEqual(c.get("S03", 0), 2)  # 'notably', 'striking'; not 'groundbreaking' inside the review note

    def test_clean_prose_passes(self) -> None:
        clean = "We propose \\texttt{Qwen}-based X. It reaches $65.1 \\pm 1.4$, an 11.7\\% relative gain over SFT, as Table~\\ref{t} shows.\n"
        self.assertEqual(rules(clean), {})


if __name__ == "__main__":
    unittest.main()
