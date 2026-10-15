"""Preview figure for the Hugging Face dataset card (the Hub viewer cannot render the parquet image bytes):
two images per split of each benchmark, drawn with a fixed seed, plus two example rows for the card table.
Usage: python scripts/hf_card_samples.py [--out outputs/hf_dataset]  -> <out>/samples/overview.jpg"""
import argparse, io, os, sys
import numpy as np, pyarrow.parquet as pq
from PIL import Image
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "figures_src")); import paper_style  # noqa: F401  (fonts, palette)
ap = argparse.ArgumentParser(); ap.add_argument("--out", default=os.path.join(ROOT, "outputs", "hf_dataset")); a = ap.parse_args()

ROWS = {  # benchmark -> (row title, [(set, class_name or None, column label)])
    "ophthalmology": ("Ophthalmology\nFLAIR", [("id", "normal", "ID: normal"), ("id", "diabetic retinopathy", "ID: diabetic retinopathy"),
                       ("semantic", None, "semantic: glaucoma, AMD"), ("covariate", None, "covariate: ultra-widefield"), ("far", None, "far: natural images")]),
    "radiology": ("Radiology\nUniMed-CLIP", [("id", "normal", "ID: normal"), ("id", "pneumonia", "ID: pneumonia"),
                   ("semantic", None, "semantic: other findings"), ("covariate", None, "covariate: paediatric CXR"), ("far", None, "far: natural images")]),
    "pathology": ("Pathology\nQuiltNet", [("id", "benign", "ID: benign"), ("id", "malignant", "ID: malignant"),
                   ("semantic", None, "semantic: other tissues"), ("covariate", None, "covariate: other hospital"), ("far", None, "far: natural images")]),
}
SET_COL = {"id": paper_style.C_NORMAL, "semantic": paper_style.C_SEM, "covariate": paper_style.C_UWF, "far": paper_style.C_FAR}

def thumb(b, px=256):
    im = Image.open(io.BytesIO(b)).convert("RGB"); w, h = im.size; s = min(w, h)
    return im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s)).resize((px, px), Image.LANCZOS)

fig = plt.figure(figsize=(10.0, 3.95), dpi=160)
gs = fig.add_gridspec(3, 11, width_ratios=[1.05] + [1] * 10, wspace=0.06, hspace=0.42, left=0.005, right=0.995, top=0.93, bottom=0.01)
examples = {}
for r, (bench, (title, cols)) in enumerate(ROWS.items()):
    t = pq.read_table(os.path.join(a.out, f"{bench}.parquet"), columns=["set", "label", "class_name", "source", "path", "image"]).to_pandas()
    if bench == "ophthalmology": examples = t
    ax = fig.add_subplot(gs[r, 0]); ax.axis("off"); ax.text(0.0, 0.5, title, fontsize=8.5, fontweight="bold", va="center", ha="left", linespacing=1.4)
    for c, (s, cls, label) in enumerate(cols):
        g = t[(t.set == s) & ((t.class_name == cls) if cls else True)]
        strat = g.groupby("class_name").sample(1, random_state=0)  # semantic / covariate: different classes where there are several
        pick = strat.sample(2, random_state=0) if (s in ("semantic", "covariate") and len(strat) >= 2) else g.sample(2, random_state=0)
        for k, (_, row) in enumerate(pick.iterrows()):
            ax = fig.add_subplot(gs[r, 1 + 2 * c + k]); ax.imshow(thumb(row.image)); ax.set_xticks([]); ax.set_yticks([])
            for sp in ax.spines.values(): sp.set_edgecolor(SET_COL[s]); sp.set_linewidth(1.6)
            if k == 0: ax.text(1.03, 1.06, label, transform=ax.transAxes, ha="center", va="bottom", fontsize=6.6, color=paper_style.INK)
os.makedirs(os.path.join(a.out, "samples"), exist_ok=True)
p = os.path.join(a.out, "samples", "overview.jpg"); fig.savefig(p, dpi=160, pil_kwargs={"quality": 88}); print(p, os.path.getsize(p) // 1024, "KB")
# two example rows (ID and covariate) for the card table
for s in ("id", "covariate"):
    row = examples[examples.set == s].iloc[0]; w, h = Image.open(io.BytesIO(row.image)).size
    print(f"| `{row.set}` | {row.label} | {row.class_name} | {row.source} | `{row.path}` | PNG, {w} x {h} px |")
