# Results validation and curation report

## Automatic evaluation files

The public results include six systems evaluated on the primary 300-example test set and the overlap-filtered 280-example sensitivity set. The 280-example set is an exact subset of the 300-example set; the same 20 sample IDs are excluded from every system. All six systems share the same sample IDs and row order within each evaluation set. Each per-example public result file contains stable `sample_id`, `source_dataset`, `split`, and numerical metrics only. Generated answer text and source benchmark context, questions, and references are omitted.

The Q1/primary Token F1 means and Q2/overlap-filtered Token F1 means match the manuscript tables to four decimal places. The six-system primary and sensitivity values are recorded in this report's source CSVs and `summary_metrics_long.csv`.

## Statistical analysis

The paired statistical-analysis script was adapted to align samples by `sample_id`, so source benchmark text is not required. It runs from the compact public result files. The two 70-row primary output tables reproduce the supplied archived results within floating-point precision. The 10-row interaction output reproduces point estimates, paired counts, Wilcoxon p-values, Holm-adjusted p-values, and effect sizes. Its bootstrap confidence intervals are now deterministic because IDs are sorted before resampling; small interval-bound differences from the earlier implementation are documented in `STATISTICAL_REPRODUCIBILITY_CHECK.md`.

## Human evaluation

The aggregate human-evaluation set contains 1,200 model responses: 200 responses per system, drawn from 50 question instances per source dataset for each of six systems. The sample-alignment diagnostic confirms that the input signatures correspond across systems, although the model-specific sample-ID fields differ. Human acceptability is reported as `No error + F*`, with dataset-stratified 95% percentile bootstrap confidence intervals (20,000 resamples; seed 42). The agreement summary reports 722 exact agreements out of 1,200 (60.17%) and Cohen's kappa of approximately 0.397.

The adjudicated row-level annotation source and individual annotator files are not included. The aggregate outputs are included; the generation script requires the author-held `annotated_output_final.csv` and therefore cannot be executed from this repository alone. Qualitative examples and the reconstructed taxonomy table are withheld pending review of the original annotation guide and source-data redistribution terms.

## Resource measurements

Peak allocated and reserved GPU memory, epoch-level training metrics, evaluation-loss logs, and saved Notebook run metadata are included. The six uploaded GPU-calculator notebooks contain successful Papermill execution metadata. The LoRA duration was independently cross-checked against the Kaggle Version page; the other five saved-notebook durations have not each been separately screenshot-verified. Full Notebook duration, code-level timer scope, manuscript Training/Adaptation Time, and manuscript QA Runtime are distinct measures and are documented separately in `RUNTIME_MEASUREMENT_PROVENANCE.md`.

## Withheld materials

The prepared dataset, model weights, raw predictions with benchmark text, row-level human annotations, individual annotator files, qualitative examples, the reconstructed taxonomy table, and unverified legacy workbook RAM/Disk observations are not included in the public candidate.
