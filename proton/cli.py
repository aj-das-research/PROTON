"""Command-line interface.

    proton prepare-data  [--root R] [--seed 0] [--domains ophthalmology radiology pathology]
    proton extract       --benchmark ophthalmology [--model flair] [--device cuda]
    proton run           --benchmark ophthalmology [--n-perm 5] [--no-grid]
    proton score         --features outputs/features/ophthalmology__flair.npz [--prompts vanilla] [--gamma 0.7 ...]
    proton figures       --benchmark ophthalmology
"""
from __future__ import annotations

import argparse
import json
import sys


def main(argv=None):
    ap = argparse.ArgumentParser(prog="proton", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("prepare-data", help="build benchmark manifests from raw downloads")
    p.add_argument("--root", default=None)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--domains", nargs="*", default=None)

    p = sub.add_parser("extract", help="extract and cache VLM features for a benchmark")
    p.add_argument("--benchmark", required=True)
    p.add_argument("--model", default=None)
    p.add_argument("--device", default=None)
    p.add_argument("--batch-size", type=int, default=32)
    p.add_argument("--no-local", action="store_true", help="skip patch features (GL-MCM)")
    p.add_argument("--force", action="store_true")

    p = sub.add_parser("run", help="reproduce all tables for a benchmark")
    p.add_argument("--benchmark", required=True)
    p.add_argument("--n-perm", type=int, default=5)
    p.add_argument("--prompts", default=None)
    p.add_argument("--device", default=None)
    p.add_argument("--no-grid", action="store_true")

    p = sub.add_parser("figures", help="render the paper figures for a benchmark (needs cached features)")
    p.add_argument("--benchmark", required=True)

    p = sub.add_parser("score", help="run PROTON once over the default stream and print metrics per shift")
    p.add_argument("--benchmark", required=True)
    p.add_argument("--prompts", default=None)
    p.add_argument("--base", default="mcm")
    p.add_argument("--gamma", type=float, default=0.7)
    p.add_argument("--M", type=int, default=100)
    p.add_argument("--seed", type=int, default=0)

    a = ap.parse_args(argv)
    if a.cmd == "prepare-data":
        from .data import manifests
        argv2 = []
        if a.root: argv2 += ["--root", a.root]
        argv2 += ["--seed", str(a.seed)]
        if a.domains: argv2 += ["--domains", *a.domains]
        sys.argv = ["manifests"] + argv2
        manifests.main()
    elif a.cmd == "extract":
        from .features import extract_features
        f = extract_features(a.benchmark, a.model, local=not a.no_local, batch_size=a.batch_size, device=a.device,
                             force=a.force)
        print({k: getattr(v, "shape", v) for k, v in f.items() if k != "text_counts"})
    elif a.cmd == "run":
        from .experiments.tables import run_benchmark
        out = run_benchmark(a.benchmark, n_perm=a.n_perm, prompt_set=a.prompts, device=a.device, grid=not a.no_grid)
        print(json.dumps({k: v.get("proton", v) if isinstance(v, dict) and "proton" in v else "ok" for k, v in out.items()},
                         indent=1, default=float)[:2000])
    elif a.cmd == "figures":
        from .experiments.figures import make_all
        make_all(a.benchmark)
    elif a.cmd == "score":
        from .data import load_benchmark
        from .evaluate import evaluate_proton, evaluate_static, prepare
        from .features import load_features
        bench = load_benchmark(a.benchmark)
        P = prepare(bench, load_features(a.benchmark, bench.vlm), prompt_set=a.prompts)
        st = evaluate_static(P, names=[a.base])[a.base]
        pr = evaluate_proton(P, n_perm=1, seed0=a.seed, base=a.base, gamma=a.gamma, M=a.M)
        for sh in pr:
            print(f"{sh:10s} {a.base}: AUROC {st[sh]['auroc']:.1f}  PROTON: AUROC {pr[sh]['auroc']:.1f} "
                  f"AUPR {pr[sh]['aupr']:.1f} FPR95 {pr[sh]['fpr95']:.1f}")


if __name__ == "__main__":
    main()
