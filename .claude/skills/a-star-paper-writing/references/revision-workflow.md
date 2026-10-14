# Revision workflow in the author's Overleaf projects

Follow this whenever you rewrite, cut or restructure a draft the author shares.
It is usually an Overleaf project cloned with git. The rules come from the
author's corrections to agents and from the lab's September 2026 workflow.

## 1. Before touching the text

- **Pull first.** Run `git fetch` and `git pull --rebase` on the Overleaf clone,
  and record the commit. The author and their co-authors edit in parallel, and
  agents have edited stale copies.
- **Build the file Overleaf compiles.** Confirm the root, for example
  `iclr2027_conference.tex`. Keep one main file and no orphaned copies.
- **Propose, then edit.** "first you'd tell me what you do want to change".
  For titles, abstracts, figures and anything structural, show the options or
  the diff in chat first. Small edits that the user asked for, one paragraph
  at a time, can go straight in.
- **Edit only what was asked.** Do not re-edit the author's captions, abstract
  or contributions unless asked. Do not change results, methods or setup
  during a writing pass. Near a deadline, do not start experiments or
  restructure unless asked.
- **Work one section at a time.** The author decides when to move on. Sketch
  and critique the argument before writing. Say what to add as well as what to
  cut, and push back when a requested change weakens the paper. Be a co-author,
  not a transcriptionist.

## 2. Marking changes for co-authors (labreview v3.13)

Load the lab package. The ICLR and NeurIPS option set is
`\usepackage[draft,singlecolumn,marginwidth=1.6cm,marginsep=1.95cm]{labreview}`.
Take the current `labreview.sty` from `spotai-research`, or from the
`a-star-paper-review` skill's `assets/`.

- **Rewritten text is yellow.** Use `\ReviewMarker{sentence}` for a sentence,
  and wrap whole paragraphs in `\begin{ReviewMarkerBlock} ... \end{ReviewMarkerBlock}`.
  Remove the yellow only when the author accepts the section.
- **Explain each change** with a short margin note tagged for the agent, never
  with a person's name: `\Review[Kshitij (AI-assisted)]{anchor}{what changed and why}`.
  The lab also uses `ai-assistant` and `AI-assisted reviewer`, so match the
  paper's existing tag. End every note with a short grey id (`\RevID{ab12}`).
- **New numbers are orange.** A number first computed during the rewrite gets
  `\NewFinding{...}` (colour FFB86B) and a note naming its source file, so that
  co-authors can verify it. Claim it with "We find that".
- **Protect parameterless macros** with `\ReviewProtect{\method}`, or soul fails
  with "Reconstruction failed".
- **Preserve the existing notes** from Nils, co-authors and reviewers. For
  requests to "go over the comments one by one", use the `a-star-paper-review`
  skill's comment-resolution workflow and keep an id ledger.

## 3. Evidence during a rewrite

- **Recompute, don't copy.** When a metric or definition changes, recompute
  every affected table and figure from the stored predictions. Reproduce the
  published cells first, then check them independently.
- **Stay honest.** If a claim fails under the new numbers, say so in a note and
  in your reply. Never keep it quietly.
- **Stay consistent.** After any change to numbers or settings, check the
  abstract, introduction, tables, captions, appendix and conclusion for the
  old value. The `a-star-paper-review` skill's `number_audit.py` automates the
  first pass.

## 4. Build and check the layout after every edit

Build the final-mode PDF (labreview `final`) and check:

- the main-text page count, which must fit the limit (the conclusion ends on
  the last allowed page); report it;
- Figure 1 is still on page 1;
- no text wraps around the wrong float, and no float stands alone on a page;
- no paragraph ends on one or two words, which you can check with
  `pdftotext -layout` or PyMuPDF.

Then build draft mode and look at the rendered pages with the notes. Run
`python scripts/style_lint.py <changed .tex files>`.

## 5. Cutting to the page limit

1. Measure the overflow in the final-mode PDF, in lines.
2. Go sentence by sentence and put a margin note on each sentence that can be
   cut, shortened, merged or moved to the appendix. Give each note its saving:
   "CUT, −2 lines", "SHORTEN, −1 line", "MERGE with next", "MOVE to App. C".
3. Mark a RECOMMENDED set that meets the limit, with stale or duplicated claims
   first, and an OPTIONAL set.
4. Keep notes to about 20 words, grouped per paragraph. More than about 8 notes
   per page overlap in the margin.
5. Protect the abstract and the introduction. Cut there only what is wrong or
   duplicated.
6. Land exactly on the limit with a full last page. If a cut leaves space, fill
   it with the most valuable appendix material, such as a figure the
   introduction motivates.

Space savers the author likes:

- three or four plots in one row;
- `wrapfigure` or `wraptable` for smaller floats, with no wrapped text shorter
  than the float;
- shorter captions;
- merging a page that holds only one figure.

## 6. Push

- Push only after a clean build. Limited per-paragraph edits during a joint
  editing session carry standing approval. Large or structural pushes need
  explicit approval.
- Fetch and rebase first, and commit only the files you edited.
- Push under the author's identity: `user.name=Mishrakshitij`,
  `user.email=45433504+Mishrakshitij@users.noreply.github.com`. Add no AI
  co-author trailer; this is the author's standing rule.
- Confirm the push by reading back the remote, and tell the author that it
  landed. When the project has a meta-repository, update its submodule pointer
  as well.
