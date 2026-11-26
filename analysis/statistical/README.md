# Statistical analysis

The script `statistical_analysis.py` reproduces the paired comparisons reported from the six systems on the 300-example primary evaluation set.

## Inputs

The script reads the six per-system CSVs under `results/primary_300/`. Each CSV contains:

- `sample_id`: SHA-256 of the compact JSON serialization of `[source_dataset, split, context, question]`;
- `source_dataset` and `split`;
- the per-example metrics listed in the paper (Exact Match, Token F1, ROUGE-1, ROUGE-L, METEOR, BERTScore precision/recall/F1, semantic similarity, and SacreBLEU).

The source context, question, and reference-answer text are not redistributed. The `sample_id` supports exact paired alignment across the six result files without republishing source benchmark text.

## Procedure

- Paired model comparisons are aligned by `sample_id`.
- 95% percentile bootstrap confidence intervals use 20,000 paired resamples.
- Wilcoxon signed-rank tests are two-sided.
- Holm correction is applied within each hypothesis family.
- Random seed: 42; the interaction analysis uses seed 142.
- Rank-biserial effect sizes and per-comparison win/tie rates are reported.
- The backbone-by-regime interaction uses the difference-in-differences contrast described in the script docstring and paper.

## Run

From the repository root:

```bash
python -m pip install -r analysis/statistical/requirements.txt
python analysis/statistical/statistical_analysis.py
```

Outputs are written to `results/statistical_analysis/`.

The interaction analysis sorts `sample_id` values before bootstrap resampling to make its output deterministic across Python processes. This removes variability caused by iterating over an unordered set; see `docs/STATISTICAL_REPRODUCIBILITY_CHECK.md`.
