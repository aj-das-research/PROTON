"""Export the real data for the TikZ method figure: 2-D projection of FLAIR embeddings (ultra-widefield stream, seed 0),
end-of-stream DR-queue members of PROTON and PROTON+ (with PROTON+ anchor weights), both DR prototypes, one real
ultra-widefield image (t=413) and the queue composition used for the bank glyph. Writes data.tex + thumbnails."""
import os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "/mnt/hdd2/Abhijit/projects/PROTON")
from proton.data import load_benchmark
from proton.features import load_features
from proton.evaluate import prepare, run_proton_stream
from proton.streams import make_stream
from proton.online import proton_plus_config
D = os.path.dirname(os.path.abspath(__file__))
b = load_benchmark("ophthalmology"); P = prepare(b, load_features("ophthalmology", b.vlm))
pool, n_id = P.pool("covariate"); order, is_ood = make_stream(n_id, len(pool) - n_id, seed=0); idx = pool[order]
r0 = run_proton_stream(P, pool, order); r1 = run_proton_stream(P, pool, order, config=proton_plus_config())
det0, det1 = r0["detector"], r1["detector"]; E, lab, sets = P.embeds, P.labels, P.sets
T = 413; i_s = idx[T]; conf, sp0, sp1 = r1["conf"][T], r0["s_proto"][T], r1["s_proto"][T]
idm, cov = sets == "id", sets == "covariate"
c = E[idm].mean(0); d1 = E[cov].mean(0) - c; d1 /= np.linalg.norm(d1)
d2 = E[idm & (lab == 1)].mean(0) - E[idm & (lab == 0)].mean(0); d2 -= (d2 @ d1) * d1; d2 /= np.linalg.norm(d2)
proj = lambda X: np.c_[(np.atleast_2d(X) - c) @ d1, (np.atleast_2d(X) - c) @ d2]
Zdr, Zcv = proj(E[idm & (lab == 1)]), proj(E[cov])
xlo, xhi = np.percentile(Zdr[:, 0], 1), np.percentile(Zcv[:, 0], 99.5)
ylo, yhi = min(np.percentile(Zcv[:, 1], 0.5), np.percentile(Zdr[:, 1], 3)), np.percentile(Zdr[:, 1], 99.5)
PW, PH, M = 4.30, 1.70, 0.13                                  # panel size (cm) and inner margin
def to_panel(Z):
    Z = np.atleast_2d(Z); x = M + (Z[:, 0] - xlo) / (xhi - xlo) * (PW - 2 * M); y = M + (Z[:, 1] - ylo) / (yhi - ylo) * (PH - 2 * M)
    return np.c_[x, y]
def inside(Q): return (Q[:, 0] > 0.04) & (Q[:, 0] < PW - 0.04) & (Q[:, 1] > 0.04) & (Q[:, 1] < PH - 0.04)
key = {E[i].round(5).tobytes(): i for i in pool}
def members(det):
    Mx = np.stack(det.banks[1]); ids = [key.get(np.asarray(m, np.float32).round(5).tobytes()) for m in Mx]
    return Mx, np.array([sets[i] == "covariate" if i is not None else False for i in ids])
M0, sh0 = members(det0); M1, sh1 = members(det1)
w1 = np.exp((M1 @ det1.mu_dom - 1) / det1.cfg.bandwidth); share = w1[sh1].sum() / w1.sum()
med = np.median(w1[~sh1]); wn = np.where(w1 < 0.15 * med, -1.0, np.clip(w1 / w1[~sh1].max(), 0, 1))
rng = np.random.default_rng(0)
out = []
def coords(Q): return ",".join(f"{x:.3f}/{y:.3f}" for x, y in Q)
for name, m in [("bgNormal", idm & (lab == 0)), ("bgDR", idm & (lab == 1)), ("bgUWF", cov)]:
    Q = to_panel(proj(E[m])); Q = Q[inside(Q)]; out.append(f"\\def\\{name}{{{coords(Q)}}}")
for tag, Mx, sh, ww in [("A", M0, sh0, np.ones(len(M0))), ("B", M1, sh1, wn)]:
    Q = to_panel(proj(Mx)); keep = inside(Q)
    out.append(f"\\def\\memID{tag}{{{','.join(f'{x:.3f}/{y:.3f}/{max(w, 0):.2f}' for (x, y), s, w, k in zip(Q, sh, ww, keep) if k and not s)}}}")
    out.append(f"\\def\\memUWF{tag}{{{','.join(f'{x:.3f}/{y:.3f}/{w:.2f}' for (x, y), s, w, k in zip(Q, sh, ww, keep) if k and s)}}}")
pA = to_panel(proj(det0.prototypes[1]))[0]; pB = to_panel(proj(det1.prototypes[1]))[0]; xs = to_panel(proj(E[i_s]))[0]
out += [f"\\def\\pAx{{{pA[0]:.3f}}}", f"\\def\\pAy{{{pA[1]:.3f}}}", f"\\def\\pBx{{{pB[0]:.3f}}}", f"\\def\\pBy{{{pB[1]:.3f}}}", f"\\def\\sX{{{xs[0]:.3f}}}", f"\\def\\sY{{{xs[1]:.3f}}}",
        f"\\def\\spA{{{sp0:.2f}}}", f"\\def\\spB{{{sp1:.2f}}}", f"\\def\\conf{{{conf:.2f}}}",
        f"\\def\\shiftedPct{{{round(100 * sh0.mean())}}}", f"\\def\\weightPct{{{round(100 * share)}}}", f"\\def\\PW{{{PW}}}", f"\\def\\PH{{{PH}}}"]
# queue glyph: 10 chips, one per decile of the queue (oldest -> newest); the number of red chips equals the queue's
# shifted share rounded to tenths, placed at the deciles with the most shifted members
def comp(det, cls, n=10):
    Mx = list(det.banks[cls]); ids = [key.get(np.asarray(m, np.float32).round(5).tobytes()) for m in Mx]
    q = np.array([i is not None and sets[i] == "covariate" for i in ids]); bins = np.array_split(q, n)
    k = int(round(n * q.mean())); red = set(np.argsort([-b.sum() for b in bins], kind="stable")[:k]) if k else set()
    return ",".join("u" if j in red else ("n" if cls == 0 else "d") for j in range(n))
out += [f"\\def\\queueN{{{comp(det0, 0)}}}", f"\\def\\queueD{{{comp(det0, 1)}}}"]
open(os.path.join(D, "data.tex"), "w").write("\n".join(out) + "\n")
# thumbnails
os.makedirs(os.path.join(D, "img"), exist_ok=True)
picks = {"n1": np.where(idm & (lab == 0))[0][3], "d1": np.where(idm & (lab == 1))[0][5], "u1": i_s, "d2": np.where(idm & (lab == 1))[0][9]}
for k, i in picks.items():
    Image.open(b.paths()[i]).convert("RGB").resize((256, 256), Image.LANCZOS).save(os.path.join(D, "img", f"{k}.jpg"), quality=92)
print(f"conf {conf:.3f} spA {sp0:.3f} spB {sp1:.3f} shifted {sh0.mean():.0%} weight {share:.1%} queueD {comp(det0, 1)}")
