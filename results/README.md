# Results

This directory contains per-example numerical evaluation metrics for the six evaluated systems. Generated answer text and source benchmark text are not redistributed.

## Evaluation-set naming

- `primary_300/`: the original 300-example held-out test set used for the paper's primary evaluation.
- `overlap_filtered_280/`: the 280-example subset used for the paper's overlap sensitivity analysis after removing the same 20 context-overlap examples from every system.
- `summary_metrics_long.csv`: aggregate metrics from the supplied summary files, in long format.
- `sample_manifest.csv`: stable sample IDs and membership flags for the two evaluation sets.
- `training_logs/`: epoch-level training and evaluation-loss logs for the four PEFT configurations.
- `resource_usage/peak_gpu_memory.csv`: peak GPU-memory measurements for all six configurations.
- `resource_usage/runtime_measurement_sources.csv`: side-by-side comparison of author-reported Kaggle Run All values, saved-notebook Papermill durations, code-level timers, and manuscript timings. These sources do not yet match.
- `resource_usage/papermill_run_metadata.csv`: timestamps and full execution durations recorded in the six uploaded saved Notebook files.

## Columns in per-example result files

Each file contains `sample_id`, `source_dataset`, `split`, and per-example numerical metric columns. `sample_id` identifies a test item using the SHA-256 procedure documented in `scripts/add_sample_ids.py`. Generated predictions, benchmark context, questions, and reference-answer text are omitted to avoid redistributing source dataset content.

## Important

Runtime sources are intentionally separated. The author identifies the workbook values as whole Kaggle Run All durations. However, the six uploaded saved Notebook files also carry Papermill start/end/duration metadata, and those full-notebook durations are substantially longer than the workbook values. The workbook has therefore been withheld from this public release candidate until its values can be matched to the exact Kaggle Notebook versions/runs. See `docs/RUNTIME_MEASUREMENT_PROVENANCE.md`. Code-level timers are separately reported with their measurement boundaries. Peak allocated GPU-memory values match the manuscript table.


Statistical-analysis outputs are under `results/statistical_analysis/`. Human-evaluation aggregates are under `results/human_evaluation/`. Raw annotation-level files and benchmark context/question/reference text are not redistributed.

Per-example metric files intentionally omit generated answer text and source benchmark text. See `docs/STATISTICAL_REPRODUCIBILITY_CHECK.md`.
