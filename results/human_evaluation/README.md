# Human-evaluation outputs

This directory contains aggregate human-evaluation tables and figures derived from the author-held, adjudicated annotation source. The source annotation table and annotator-specific files are not redistributed in this repository.

## Evaluation sample

- 1,200 annotated model responses in total.
- 200 responses per system across six systems.
- The 200 response records per system correspond to 50 selected question instances from each of the four source datasets.
- The same 200 underlying question instances were used across the six systems; the sample-alignment diagnostic confirms matching input signatures, although model-specific sample identifiers differ.

## Human acceptability

Human acceptability is defined as `No error + F*`, following the manuscript. The detailed table reports the counts, percentages, and 95% confidence intervals. The confidence intervals were generated using dataset-stratified percentile bootstrap resampling (20,000 replicates; seed 42), as documented in the annotation-analysis materials.

## Annotator agreement

The aggregate agreement table reports 722 exact agreements among 1,200 paired ratings (60.17%) and an overall Cohen's kappa of approximately 0.397. Agreement statistics are descriptive and should be interpreted alongside the category definitions and adjudication procedure in the manuscript.

## Re-generation

`analysis/human_evaluation/generate_human_evaluation_outputs.py` generates the aggregate outputs from the author-held `annotated_output_final.csv`. That input and the individual annotator files are not redistributed, so the script is provided for transparency but cannot be run from the public repository alone.

The script normalizes legacy source labels `RAG` and `RAG+DeepSeek` to the manuscript's current names `RB-ICL` and `RB-ICL+DeepSeek`. No claim is made that retrieval correctness was independently verified. The reconstructed error-taxonomy output and qualitative example excerpts are withheld until they are checked against the original annotation guideline and source-data redistribution terms.
