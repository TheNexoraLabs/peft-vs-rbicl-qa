# Statistical reproducibility check

The paired analysis was re-run from the repository’s data-minimized per-example metric files. The script reads the public `sample_id` rather than requiring original context/question/reference text.

| Output | Rows | Result |
|---|---:|---|
| `primary_hypothesis_results.csv` | 70 | Numerical outputs match archived values (within floating-point precision). |
| `paper_statistical_table.csv` | 70 | Numerical outputs match archived values (within floating-point precision). |
| `interaction_results.csv` | 10 | Point estimates, paired counts, Wilcoxon p-values, Holm-adjusted p-values, and effect sizes match. Bootstrap CI bounds differ slightly because the updated script sorts sample IDs before resampling. |

The original interaction code converted a Python `set` directly to a list before bootstrap resampling. Set iteration order can vary between processes, changing the bootstrap index sequence. The released script sorts the shared sample IDs first, making the interaction confidence intervals deterministic. This is a reproducibility correction; it does not change the paired point estimates, sample counts, test statistics, adjusted p-values, or effect sizes.

The per-example result files contain `sample_id`, source dataset, split, and numerical metrics only. Generated predictions and source benchmark text are not included in those files.

The public `sample_id` values are SHA-256 hashes derived from the prepared source tuple `[source_dataset, split, context, question]`. The source text is not redistributed.
