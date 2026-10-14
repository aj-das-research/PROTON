"""The browser demo re-implements PROTON/PROTON+ in JavaScript; check it against the Python reference (needs node)."""
import json, os, shutil, subprocess
import numpy as np
import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS = os.path.join(ROOT, "docs", "demo", "assets", "ophthalmology.json")

JS = """
import { PROTON, PLUS, softmax } from "%s/docs/demo/proton.js";
import fs from "fs";
const spec = JSON.parse(fs.readFileSync("%s"));
const order = JSON.parse(process.argv[2]);
for (const [name, cfg] of [["proton", {}], ["plus", PLUS]]) {
  const det = new PROTON(2, cfg); const out = [];
  for (const i of order) {
    const e = spec.examples[i].embedding;
    const logits = spec.text_embeds.map((t) => spec.logit_scale * t.reduce((s, v, k) => s + v * e[k], 0));
    const p = softmax(logits); out.push(det.step(e, p, -Math.max(...p)).score);
  }
  console.log(name + " " + JSON.stringify(out));
}
"""


@pytest.mark.skipif(shutil.which("node") is None or not os.path.exists(ASSETS), reason="needs node and demo assets")
def test_js_matches_python(tmp_path):
    from proton.online import PROTON, proton_plus_config
    from proton.scores.static import softmax
    spec = json.load(open(ASSETS))
    order = (np.random.default_rng(0).permutation(len(spec["examples"])).tolist()) * 3
    T, s = np.array(spec["text_embeds"]), spec["logit_scale"]
    ref = {}
    for name, cfg in [("proton", None), ("plus", proton_plus_config())]:
        det, out = PROTON(2, cfg), []
        for i in order:
            e = np.array(spec["examples"][i]["embedding"]); p = softmax(s * T @ e)
            out.append(det.step(e, p, -p.max())["score"])
        ref[name] = np.array(out)
    script = tmp_path / "t.mjs"; script.write_text(JS % (ROOT, ASSETS))
    res = subprocess.run(["node", str(script), json.dumps(order)], capture_output=True, text=True, check=True)
    for line in res.stdout.strip().splitlines():
        name, arr = line.split(" ", 1)
        assert np.allclose(np.array(json.loads(arr)), ref[name], atol=1e-4), name
