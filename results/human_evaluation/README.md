# Human-evaluation outputs

This directory contains aggregate human-evaluation tables and figures derived from the author-held, adjudicated annotation source. The source annotation table and annotator-specific files are not redistributed in this repository.

## Evaluation sample

- 1,200 adjudicated model-response records in total.
- 200 responses per system across six systems.
- 50 records per system from each of the four source datasets.
- The same 200 underlying question instances were evaluated across all six systems; the sample-alignment diagnostic compares input signatures, while model-specific response IDs may differ.

## Annotation and adjudication

Two annotators independently labeled each response under blinded initial-annotation conditions. A third reviewer (the supervising advisor) then examined both initial labels and the accompanying record information and assigned the final adjudicated label in `final_error_code`. The third reviewer is therefore an adjudicator, not a third independent rater.

Inter-annotator agreement is calculated only from the two pre-adjudication ratings: 722 exact agreements among 1,200 paired ratings (60.17%) and Cohen's kappa of approximately 0.397.

The complete protocol, operational error-code definitions, acceptability rule, and interpretation notes are documented in [`docs/HUMAN_EVALUATION_PROTOCOL.md`](../../docs/HUMAN_EVALUATION_PROTOCOL.md).

## Human acceptability

Human acceptability is defined as `No error + F*`, following the manuscript. The detailed table reports counts, percentages, and 95% confidence intervals. Confidence intervals use dataset-stratified percentile bootstrap resampling (20,000 replicates; seed 42), as implemented in the analysis script.

## Re-generation

`analysis/human_evaluation/generate_human_evaluation_outputs.py` generates the aggregate outputs from the author-held `annotated_output_final.csv`. That input and the individual annotator files are not redistributed, so the script is provided for transparency but cannot be run from the public repository alone.

The script normalizes legacy source labels `RAG` and `RAG+DeepSeek` to the manuscript's current names `RB-ICL` and `RB-ICL+DeepSeek`. No claim is made that retrieval correctness was independently verified.

The aggregate tables and figures do not expose benchmark context, questions, reference-answer text, model-generated answer text, or annotator notes.
