# Blind comparison

Assessment uses only each task's request, supplied notes/CSV, and candidate passages. Fidelity and compliance take priority over style.

## Method: B preferred, narrowly

Both passages accurately specify the frozen models, top-20 candidate set, strict gap threshold, per-dataset development calibration, and changing test routing fraction. Their reported accuracies, routing fractions, and differences match the CSV. Both stay within the requested passage lengths, identify the exercise as synthetic, avoid novelty claims, and acknowledge the mixed comparison with query length. Neither has a material factual or compliance defect.

B gives the more informative comparison with random routing: its accuracy gains come “with latency increases of 1, 0, and 1 ms.” A reports the same accuracy gains without that cost difference. This matters because the task concerns the accuracy–latency tradeoff, and the random baseline is not uniformly matched in measured latency. B also reports the always-rerank latency reduction as 44.9–46.3%, accurately resolving the range that A rounds to approximately 45–46%; A's approximation is reasonable, not an error. B places the shared evaluation setup and latency definition in Method, letting Results focus on the observed comparisons.

A usefully states that the length baseline has identical test routing fractions as well as identical latency; B explicitly supplies only the latter comparison. That omission is minor. Overall, B's advantage is fuller comparative accounting, not stronger evidence or a materially different method description.

## Theory: B preferred, narrowly

Both passages preserve the exact-null-space result, the zero-dimensional case, the thresholded right-singular projector including the entire null space, and the exact-arithmetic bound. Both define the norms, correctly work the supplied illustration, and limit retention to predictions on the fixed rows of X. Both fit the requested scope and length. Neither has a material mathematical or compliance defect.

B develops each result where it is needed: it defines the null space explicitly, states exact retention, immediately proves it using XN = 0, and interprets the surviving update as components “invisible to the fixed old examples.” It then introduces the implemented projector and writes the intermediate equality between prediction-shift norm and the norm of XP_epsilon u. This connects the mathematical statement to the actual update with little backtracking and helps a reader with basic linear algebra follow the argument.

A's combined proposition is a clear formal presentation, and its separate proof is correct. However, the thresholded construction and its interpretation are spread across the proposition, proof, and implementation paragraphs. B's local statement–proof–interpretation sequence is slightly easier to follow. A's additional explicit nonlinear-network limitation does not change the comparison: B already confines both claims to the fixed linear setting. The preference concerns exposition, not missing mathematical safeguards.
