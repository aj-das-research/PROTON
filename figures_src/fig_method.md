# fig2_method brief and representation contract

- Slot: two-column width (7.0 in) method figure; paper (arXiv article, \linewidth), README and project page.
- One sentence: given an unlabelled stream scored by a frozen VLM, anchoring the class prototypes of the online bank to
  the dominant imaging-domain mode and gating admission by prototype consistency keeps the prototype distance informative
  when confidently misclassified shifted inputs enter the bank.
- Example: three real thumbnails (FIVES fundus, DeepDRiD ultra-widefield, Imagenette); the inset scatter is an
  illustrative schematic, labelled as such, not measured data.
- Nodes/edges: frozen VLM (image tower -> e_t; text tower cached -> T; softmax p_t) | S_MCM = -max p | per-class FIFO
  bank D_c | (1) mean-shift anchor mu_dom over the union of queues, domain-weighted prototypes mu_c, S_proto |
  (2) consistency admission after scoring (max p >= gamma and d_t <= m_t + kappa s_t) -> enqueue, dashed feedback |
  (3) z-scored fusion with the variance-driven alpha_t; z(S_MCM) before calibration.
- Novelty localisation: orange badges 1-3 and orange borders; grey = unchanged PROTON machinery.
- Label budget: about 60 words plus equations.
- Source of truth: proton/online.py (PROTONConfig defaults; proton_plus_config).
