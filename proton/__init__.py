"""PROTON: PROtotype-based Test-time ONline OOD detection for vision-language models.

Public API (stable):
    proton.metrics.ood_metrics            AUROC / AUPR / FPR@95 (OOD = positive class)
    proton.scores.static                   MCM, Max-Logit, Energy, Entropy, GL-MCM, TAG-MCM, hierarchical MCM
    proton.online.PROTON                   the online detector (Algorithm 1 of the paper) and ablation variants
    proton.online.score_stream             convenience: run any base score through PROTON over a stream
    proton.streams.make_stream             reproducible test streams (ID fraction, permutations, label noise)
    proton.features.extract_features       cached image/text embedding extraction for registered VLMs
    proton.models.load_model               registry of frozen VLM wrappers (flair, unimedclip, quiltnet, open_clip:*)
    proton.data.load_benchmark             registry of benchmarks (ophthalmology, radiology, pathology, custom)
"""
from .metrics import ood_metrics, auroc, aupr, fpr_at_tpr
from .online import PROTON, score_stream
from .streams import make_stream

__version__ = "0.1.0"
__all__ = ["ood_metrics", "auroc", "aupr", "fpr_at_tpr", "PROTON", "score_stream", "make_stream", "__version__"]
