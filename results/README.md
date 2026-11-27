# Results

This directory contains data-minimized numerical evaluation results and aggregate analyses for the six evaluated systems.

## Evaluation sets

- `primary_300/`: the primary 300-example held-out test set used for main performance evaluation and the QA inference-runtime measurements.
- `overlap_filtered_280/`: the 280-example subset used only for the overlap sensitivity analysis after removing the same 20 overlapping-context examples from every system.
- `summary_metrics_long.csv`: aggregate metrics in long format.
- `sample_manifest.csv`: stable sample IDs and membership flags for Q1 and Q2.
- `training_logs/`: epoch-level training/evaluation-loss logs for the four PEFT configurations.

## Resource usage and timing

- `resource_usage/peak_gpu_memory.csv`: peak GPU memory measurements for all six configurations.
- `resource_usage/papermill_run_metadata.csv`: full training/RB-ICL notebook run metadata.
- `resource_usage/qa_inference_run_metadata.csv`: four PEFT QA loader runs, model mapping, generation-cell timing, and full Notebook Run All duration.
- `resource_usage/qa_inference_cell_measurements.csv`: the six Jupyter-cell QA measurements used in the manuscript; all cover 300 Q1 questions.
- `resource_usage/runtime_measurement_sources.csv`: side-by-side training timers, QA runtime sources, full Notebook duration, legacy manuscript values, and provenance notes.
- `resource_usage/computational_cost_table.xlsx`: consolidated workbook with summary, measurement sources, QA model mapping, and interpretation notes.

## QA timing interpretation

The four PEFT QA loader notebooks were assigned to systems by exact row-wise matching of all 300 generated responses to the corresponding model-specific Q1 `predicted_answer` column (300/300 exact matches for each notebook; zero empty responses). The two RB-ICL runtimes use Jupyter execution metadata for the 300-question Retrieval+Generation cell and are cross-checked against the explicit internal timers (difference below 0.30 seconds). Measurement boundaries are documented in `docs/RUNTIME_MEASUREMENT_PROVENANCE.md`.

Full Notebook Run All durations are preserved separately and are not used as the QA inference-loop values. The earlier 280-row loader timings belong to Q2 sensitivity data and are not used for the main 300-question computational-cost table.

## Per-example files

Each public per-example result file contains a stable `sample_id`, `source_dataset`, `split`, and numerical metric columns. Generated prediction text, benchmark context, questions, and reference-answer text are not redistributed.

Human-evaluation aggregates are under `human_evaluation/`; statistical-analysis outputs are under `statistical_analysis/`. Raw annotator-level files and benchmark text are not redistributed.
