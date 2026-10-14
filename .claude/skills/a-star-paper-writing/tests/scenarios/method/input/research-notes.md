# Author notes

Working name: BudgetRoute. A router chooses one or three samples before a final
answer based on a learned uncertainty score. Trained on development split only.
We have a standard fixed-three-sample baseline and our adaptive router. Same
base model and test examples. Method can reduce calls, but timing was not measured.

Test accuracy (%), three runs:
- baseline: 70.2, 70.8, 71.4
- proposed: 70.4, 71.0, 71.6

Mean model calls per question: baseline 3.0, proposed 2.0 (aggregation already
computed by author; per-example log not supplied).

Shifted-domain accuracy (%), one run: baseline 55.0, proposed 49.0.
No confidence intervals or statistical tests run. No human evaluation.

Example IDs: ex001 both correct; ex002 proposed correct/baseline wrong;
ex003 proposed wrong/baseline correct. Exact input/output text not supplied.

Venue profile (provided by author for this exercise): main content 8 pages,
references unlimited, two-column appendix, AI drafting allowed with disclosure.
Official source not provided. Related-work bibliography is not supplied.
