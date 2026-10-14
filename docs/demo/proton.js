/* PROTON / PROTON+ in plain JavaScript (mirrors proton/online.py). No dependencies. */
export class Welford {
  constructor() { this.n = 0; this.mean = 0; this.m2 = 0; }
  update(x) { this.n += 1; const d = x - this.mean; this.mean += d / this.n; this.m2 += d * (x - this.mean); return this.variance; }
  get variance() { return this.n > 1 ? this.m2 / (this.n - 1) : 0; }
}
const sigmoid = (x) => 1 / (1 + Math.exp(-x));
const dot = (a, b) => { let s = 0; for (let i = 0; i < a.length; i++) s += a[i] * b[i]; return s; };
const norm = (a) => Math.sqrt(dot(a, a)) + 1e-12;
const normalize = (a) => { const n = norm(a); return a.map((v) => v / n); };
export const softmax = (z) => { const m = Math.max(...z); const e = z.map((v) => Math.exp(v - m)); const s = e.reduce((a, b) => a + b, 0); return e.map((v) => v / s); };

export const DEFAULTS = { gamma: 0.7, M: 100, kMin: 5, alphaMin: 0.3, alphaMax: 0.7, sigma2_0: 0.02, slope: 100,
  // PROTON+ switches
  protoMode: "mean", bandwidth: 0.1, msIters: 3, admission: "confidence", kappa: 2.0, normalize: "none" };
export const PLUS = { protoMode: "domain", bandwidth: 0.1, msIters: 3, admission: "consistency", kappa: 2.0, normalize: "zscore" };

export class PROTON {
  constructor(C, cfg = {}) { this.C = C; this.cfg = Object.assign({}, DEFAULTS, cfg); this.reset(); }
  reset() {
    this.banks = Array.from({ length: this.C }, () => []);
    this.prototypes = Array(this.C).fill(null);
    this.welford = new Welford(); this.baseStats = new Welford(); this.protoStats = new Welford(); this.admStats = new Welford();
    this.muDom = null; this.t = 0; this.tCalib = null; this.history = [];
  }
  get calibrated() { return this.banks.every((b) => b.length >= this.cfg.kMin); }
  bankSizes() { return this.banks.map((b) => b.length); }
  _enqueue(c, e) {
    const bank = this.banks[c]; if (bank.length === this.cfg.M) bank.shift(); bank.push(e);
    const d = e.length; const mean = new Array(d).fill(0);
    for (const v of bank) for (let i = 0; i < d; i++) mean[i] += v[i];
    this.prototypes[c] = normalize(mean);
    if (this.cfg.protoMode === "domain") this._domainAnchored();
  }
  _domainAnchored() {
    const all = this.banks.flat(); if (!all.length) return; const d = all[0].length; const h = this.cfg.bandwidth;
    let mu = new Array(d).fill(0); for (const v of all) for (let i = 0; i < d; i++) mu[i] += v[i]; mu = normalize(mu);
    for (let it = 0; it < this.cfg.msIters; it++) {
      const acc = new Array(d).fill(0);
      for (const v of all) { const w = Math.exp((dot(v, mu) - 1) / h); for (let i = 0; i < d; i++) acc[i] += w * v[i]; }
      mu = normalize(acc);
    }
    this.muDom = mu;
    this.banks.forEach((bank, c) => {
      if (!bank.length) return; const acc = new Array(d).fill(0);
      for (const v of bank) { const w = Math.exp((dot(v, mu) - 1) / h); for (let i = 0; i < d; i++) acc[i] += w * v[i]; }
      this.prototypes[c] = normalize(acc);
    });
  }
  protoScore(e) { let best = -1; for (const p of this.prototypes) if (p) best = Math.max(best, dot(e, p)); return 1 - best; }
  alpha(v) { const c = this.cfg; return c.alphaMax - sigmoid(c.slope * (v - c.sigma2_0)) * (c.alphaMax - c.alphaMin); }
  step(e, p, sBase) {
    const cfg = this.cfg; this.t += 1; const v = this.welford.update(sBase); const calibrated = this.calibrated;
    let sProto = NaN, a = 1, s = sBase, zb = NaN, zp = NaN;
    if (calibrated) {
      sProto = this.protoScore(e); a = this.alpha(v);
      if (cfg.normalize === "zscore") {
        this.baseStats.update(sBase); this.protoStats.update(sProto);
        zb = (sBase - this.baseStats.mean) / (Math.sqrt(this.baseStats.variance) + 1e-6);
        zp = (sProto - this.protoStats.mean) / (Math.sqrt(this.protoStats.variance) + 1e-6);
        s = a * zb + (1 - a) * zp;
      } else s = a * sBase + (1 - a) * sProto;
    } else if (cfg.normalize === "zscore") {
      this.baseStats.update(sBase); s = (sBase - this.baseStats.mean) / (Math.sqrt(this.baseStats.variance) + 1e-6);
    }
    if (calibrated && this.tCalib === null) this.tCalib = this.t;
    const conf = Math.max(...p); const cHat = p.indexOf(conf);
    let updated = conf >= cfg.gamma; let rejected = false;
    if (updated && cfg.admission === "consistency" && this.prototypes[cHat] && calibrated) {
      const dHat = 1 - dot(e, this.prototypes[cHat]);
      if (this.admStats.n >= cfg.kMin) { const thr = this.admStats.mean + cfg.kappa * Math.sqrt(this.admStats.variance); updated = dHat <= thr; rejected = !updated; }
      if (updated) this.admStats.update(dHat);
    }
    if (updated) this._enqueue(cHat, e);
    const rec = { score: s, sBase, sProto, alpha: a, variance: v, calibrated, updated, rejected, pred: cHat, conf, zb, zp, t: this.t };
    this.history.push(rec); return rec;
  }
}

/* ---- image preprocessing identical to FLAIR: /255, long side -> 512, zero-pad right/bottom, CHW, no normalisation */
export function preprocessToTensor(img, size = 512) {
  const canvas = document.createElement("canvas"); canvas.width = size; canvas.height = size;
  const ctx = canvas.getContext("2d"); ctx.fillStyle = "black"; ctx.fillRect(0, 0, size, size);
  const scale = Math.max(img.naturalWidth || img.width, img.naturalHeight || img.height) / size;
  const w = Math.floor((img.naturalWidth || img.width) / scale), h = Math.floor((img.naturalHeight || img.height) / scale);
  ctx.imageSmoothingQuality = "high"; ctx.drawImage(img, 0, 0, w, h);
  const data = ctx.getImageData(0, 0, size, size).data; const out = new Float32Array(3 * size * size);
  for (let i = 0; i < size * size; i++) { out[i] = data[4 * i] / 255; out[size * size + i] = data[4 * i + 1] / 255; out[2 * size * size + i] = data[4 * i + 2] / 255; }
  return { data: out, dims: [1, 3, size, size], canvas };
}
