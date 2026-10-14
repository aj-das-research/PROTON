import os
import numpy as np
from PIL import Image

from proton.data.custom import manifest_from_folders, register_benchmark
from proton.data import load_specs


def _folder(tmp, name, n):
    d = tmp / name; d.mkdir()
    for i in range(n):
        Image.fromarray(np.random.default_rng(i).integers(0, 255, (16, 16, 3), dtype=np.uint8)).save(d / f"{i}.png")
    return str(d)


def test_manifest_from_folders(tmp_path):
    ids = {"normal": _folder(tmp_path, "n", 6), "disease": _folder(tmp_path, "d", 6)}
    oods = {"semantic": _folder(tmp_path, "s", 4), "far": _folder(tmp_path, "f", 3)}
    df = manifest_from_folders("toy", ids, oods, n_id=4, n_ood=None, bank=2, seed=0, root=str(tmp_path))
    counts = df.groupby("set").size().to_dict()
    assert counts == {"id": 8, "id_bank": 4, "semantic": 4, "far": 3}
    assert set(df[df.set == "id"].label) == {0, 1} and (df[df.set != "id"].label.isin([-1, 0, 1])).all()
    spec = register_benchmark("toy", "flair", list(ids), "a photo of {}", "data/benchmarks/toy/manifest.csv",
                              spec_file=str(tmp_path / "local.yaml"))
    assert spec["prompts"]["default"] == [["a photo of normal"], ["a photo of disease"]]
    assert "ophthalmology" in load_specs()
