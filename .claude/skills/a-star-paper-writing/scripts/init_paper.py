#!/usr/bin/env python3
"""Initialize a paper project without inventing evidence (Python 3.9+).

Usage: init_paper.py NEW_PROJECT_DIR [--title TITLE] [--format tex|markdown]
The target directory must not exist. This command never merges or overwrites.
The default is a compilable generic TeX working draft, not a venue template.
Use --format markdown for the legacy paper.md scaffold. Both formats create
a project brief, an empty evidence ledger, and an unknown venue profile.
The empty project deliberately does not pass paper_audit.py readiness checks.
"""

import argparse
import json
from pathlib import Path
import sys


PAPER = """# {title}

<!-- DRAFT: No claims or results have been verified. Use claim IDs in drafting
notes to connect factual statements to evidence-ledger.json. Remove these
comments only after evidence review. Adapt headings and page budget to the
verified venue and the paper type. -->

## Abstract

<!-- Problem; why it matters; specific limitation; proposal; verified findings. -->

## 1 Introduction

<!-- Problem, motivation, limitation, idea, mechanism, evaluation, contributions. -->

## 2 Related Work

<!-- Organize by the research question and methodological progression.
Add Background here or as a separate section only when needed. -->

## 3 Method

<!-- Define setting, assumptions, inputs, outputs, notation, and procedure.
For a benchmark paper, adapt this section to benchmark design and protocol. -->

## 4 Experiments

<!-- Datasets/splits, implementation, baselines, metrics, budget, and uncertainty. -->

## 5 Results and Analysis

<!-- Evidence-backed results, ablations, failure cases, and qualitative examples. -->

## 6 Discussion and Limitations

<!-- Scope, tradeoffs, limitations, and what the evidence does not establish. -->

## 7 Conclusion

<!-- One concise paragraph when appropriate; do not introduce new findings. -->

## References

<!-- Add only verified references, with matching entries in the evidence ledger. -->

## Appendix

<!-- Include only if the current venue permits it. Order: optional background;
method details; experiment/reproduction details; exact prompts; extended
results and analyses; detailed qualitative cases; reader FAQs (up to 12–15).
Keep information essential to judging the central contribution in the main text. -->
"""


TEX_MAIN = r"""% WORKING DRAFT: generic scaffold, not a venue template.
% Run the initial pdfLaTeX pass from this directory using the compile_command
% recorded in overleaf-project.json. Rerun as needed to resolve cross-references
% when real content is added; enable a bibliography backend only when needed.
% Replace the document class and preamble with the verified official template
% before submission. Record its source and version in overleaf-project.json.
% Do not change margins, fonts, or column layout to evade venue page limits.
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

\title{@@TITLE@@}
\author{}
\date{}

\begin{document}
\maketitle
\begin{center}
\textbf{Working draft: generic scaffold, not a venue template.}
\end{center}

% No claims, results, or references have been verified. Record real evidence
% before drafting factual claims; keep claim IDs in drafting comments.
\begin{abstract}
\input{sections/abstract}
\end{abstract}

\input{sections/introduction}
\input{sections/related-work}
\input{sections/problem-setting}
\input{sections/method}
\input{sections/experiments}
\input{sections/results}
\input{sections/discussion}
\input{sections/conclusion}

% references.bib is intentionally empty. Verify real citation metadata first.
% After adding real entries and citing them in the manuscript, enable the
% bibliography using the official template's bibliography commands and style.
% For this generic draft only, these commands can be used once citations exist:
% \bibliographystyle{plain}
% \bibliography{references}
% Do not run BibTeX on this citation-free scaffold.

% Verify whether the venue permits an appendix, its placement, and its limits.
% Keep material essential to judging the central contribution in the main text.
% The verified venue template controls the appendix's column layout.
\appendix
\input{appendix/background}
\input{appendix/method-details}
\input{appendix/experiment-details}
\input{appendix/prompts}
\input{appendix/extended-results}
\input{appendix/qualitative-results}
\input{appendix/discussion}
\input{appendix/faq}

\end{document}
"""

TEX_SECTIONS = (
    ("introduction", "Introduction", "Problem, motivation, specific limitation, idea, mechanism, evaluation, and contributions."),
    ("related-work", "Related Work", "Organize verified references by research question and methodological progression."),
    ("problem-setting", "Problem Setting", "Define the setting, assumptions, inputs, outputs, notation, and scope."),
    ("method", "Method", "Describe the procedure or benchmark design. Connect theoretical claims to supplied proofs."),
    ("experiments", "Experiments", "Specify data, splits, implementation, baselines, metrics, compute budget, and uncertainty."),
    ("results", "Results and Analysis", "Add only evidence-backed findings, ablations, failure cases, and qualitative examples."),
    ("discussion", "Discussion and Limitations", "Explain scope, tradeoffs, limitations, and what the evidence does not establish."),
    ("conclusion", "Conclusion", "Summarize supported contributions concisely. Do not introduce new findings."),
)

TEX_APPENDIX = (
    ("background", "Additional Background", "Include optional background only when it helps the reader and the venue permits it."),
    ("method-details", "Method Details", "Provide derivations, proofs, algorithms, and implementation details backed by actual work."),
    ("experiment-details", "Experiment and Reproduction Details", "Record environments, dependencies, seeds, configurations, and exact reproduction commands."),
    ("prompts", "Exact Prompts", "Record exact prompts from prompts/, model versions, decoding settings, and revision history."),
    ("extended-results", "Extended Results and Analyses", "Include supplementary tables and analyses only after checking their source artifacts."),
    ("qualitative-results", "Qualitative Cases", "Show actual examples and failure cases with the sampling and selection rules."),
    ("discussion", "Extended Discussion", "Expand supported interpretation and limitations without introducing unsupported claims."),
    ("faq", "Reader FAQs", "Answer substantive reader questions with supported facts; usually no more than 12--15 questions."),
)


def escape_latex(text):
    """Treat the supplied title as text, including literal TeX metacharacters."""
    replacements = {
        "\\": r"\textbackslash{}", "{": r"\{", "}": r"\}",
        "$": r"\$", "&": r"\&", "#": r"\#", "%": r"\%",
        "_": r"\_", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(character, character) for character in text)


def tex_files(title):
    files = {
        "main.tex": TEX_MAIN.replace("@@TITLE@@", escape_latex(title)),
        "references.bib": "",
        "sections/abstract.tex": (
            "% Problem; why it matters; specific limitation; proposal; verified findings.\n"
            "\\noindent\\textit{Draft abstract pending evidence review.}\n"
        ),
    }
    for directory, sections in (("sections", TEX_SECTIONS), ("appendix", TEX_APPENDIX)):
        for name, heading, guidance in sections:
            files[directory + "/" + name + ".tex"] = "\\section{" + heading + "}\n\n% " + guidance + "\n"
    return files


def initial_venue():
    return {
        "schema_version": 1,
        "venue": None, "year": None, "track": None, "stage": None,
        "verified_url": None, "retrieved_on": None,
        "rules": {
            "main_text": {"status": "unknown", "page_limit": None, "notes": None},
            "references": {"status": "unknown", "policy": "unknown", "page_limit": None, "notes": None},
            "appendix": {"status": "unknown", "policy": "unknown", "page_limit": None, "columns": "unknown", "notes": None},
            "ai_assistance": {"status": "unknown", "mode": "unknown", "disclosure": None, "source_url": None, "retrieved_on": None, "notes": None},
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project_dir", type=Path)
    parser.add_argument("--title", default="Untitled research paper")
    parser.add_argument("--format", choices=("tex", "markdown"), default="tex", help="manuscript format (default: tex)")
    args = parser.parse_args(argv)
    target = args.project_dir.expanduser()
    if target.exists() or target.is_symlink():
        parser.error("target already exists; choose a new directory. Nothing was overwritten.")
    if not args.title.strip() or "\n" in args.title or "\r" in args.title:
        parser.error("title must be one nonempty line")
    assets = Path(__file__).resolve().parents[1] / "assets"
    try:
        brief = (assets / "project-brief.md").read_text(encoding="utf-8")
        overleaf_profile = None
        if args.format == "tex":
            overleaf_profile = json.loads((assets / "overleaf-project.example.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print("Cannot read project template: " + str(error), file=sys.stderr)
        return 2
    files = {
        "project-brief.md": brief,
        "evidence-ledger.json": json.dumps({"schema_version": 1, "claims": [], "evidence": [], "citations": []}, indent=2) + "\n",
        "venue-profile.json": json.dumps(initial_venue(), indent=2) + "\n",
    }
    if args.format == "tex":
        files.update(tex_files(args.title.strip()))
        overleaf_profile.update({
            "local_root": str(target.resolve()),
            "main_document": "main.tex",
            "compiler": "pdflatex",
            "bibliography_files": ["references.bib"],
            "compile_command": "pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error main.tex",
            "compile_working_directory": ".",
        })
        overleaf_profile["files"]["tex"] = sorted(name for name in files if name.endswith(".tex"))
        overleaf_profile["unresolved"].append("Select and enable the bibliography backend after adding verified citations and adopting the verified venue template.")
        files["overleaf-project.json"] = json.dumps(overleaf_profile, indent=2) + "\n"
        directories = ("artifacts", "figures", "prompts", "sections", "appendix")
    else:
        files["paper.md"] = PAPER.format(title=args.title.strip())
        directories = ("artifacts", "figures", "supplement")
    try:
        target.mkdir(parents=True, exist_ok=False)
        for directory in directories:
            (target / directory).mkdir()
        for name, content in files.items():
            with (target / name).open("x", encoding="utf-8") as handle:
                handle.write(content)
    except OSError as error:
        print("Initialization stopped: " + str(error) + ". Inspect " + str(target) + " for any partial output.", file=sys.stderr)
        return 2
    print("Created paper project: " + str(target.resolve()))
    if args.format == "tex":
        print("TeX working draft: main.tex (pdfLaTeX). This generic scaffold is not a venue template.")
    print("No evidence, citations, venue rules, or experimental results were invented.")
    print("Next: complete project-brief.md, verify venue-profile.json, and register real evidence before drafting claims.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
