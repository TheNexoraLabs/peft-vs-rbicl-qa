# Preparation log

## Source materials reviewed

- Six final GPU-calculator training/RB-ICL notebooks and their saved execution metadata.
- Six primary and six overlap-filtered per-system evaluation CSVs, corresponding summaries, training/evaluation logs, and GPU-memory logs.
- The cost workbook and the author's Kaggle Version-page confirmation for the LoRA Run All duration.
- Statistical-analysis script and outputs.
- Human-evaluation aggregate outputs, generation script, license file, and citation draft.
- Shared QA inference and scoring notebooks.

## Code and notebooks

- Cleared saved outputs and execution counts from public notebook copies.
- Removed token-like commented strings from PEFT notebooks.
- Removed a Google Drive download cell that referenced checkpoints from a previous failed run.
- Parameterized model, dataset, prediction-output, and scoring-output paths using environment variables while retaining Kaggle fallback paths.
- Added the shared inference and scoring notebooks; the author confirms that this same workflow was used across all six configurations by selecting the appropriate final checkpoint for each run.
- Added warnings and `.gitignore` rules to prevent raw prediction/scoring CSVs and raw annotation files from being committed.

## Automatic evaluation and statistics

- Confirmed six aligned primary evaluation sets of 300 examples and six aligned sensitivity sets of 280 examples. The 280-example sets are exact subsets with the same 20 examples removed across all systems.
- Confirmed the primary and sensitivity Token F1 means match the manuscript to four decimal places.
- Replaced context/question-based public matching with stable SHA-256 sample IDs and removed generated prediction text and benchmark source text from public per-example result files.
- Re-ran the paired statistical script from compact metric files: 70 primary comparisons and 10 interaction analyses. The primary tables reproduce the archived results within floating-point precision. Interaction bootstrap intervals are deterministic after sorting sample IDs; small CI-bound changes are documented.

## Human evaluation

- Added aggregate human-evaluation tables, plots, and sample-alignment diagnostics.
- The aggregate set contains 1,200 responses: 200 per system and 50 source questions per dataset per system.
- Human acceptability is reported as `No error + F*`, with dataset-stratified 95% percentile bootstrap confidence intervals (20,000 resamples; seed 42).
- Agreement summary: 722 exact agreements out of 1,200 (60.17%); overall Cohen's kappa approximately 0.397.
- Updated legacy RAG labels to RB-ICL in public output tables. The source-label normalization remains in the generator for backwards compatibility.
- Removed the unsupported statement that retrieval correctness was established. Qualitative examples and the reconstructed error taxonomy are withheld pending review of the source-data terms and original annotation guideline. Raw annotation-level files are not redistributed.

## Resource measurement provenance

- Preserved full Notebook Papermill run metadata, internal code-level timers, and manuscript timing values as distinct measures.
- The LoRA Run All duration (03:48:12) was independently confirmed against the author's Kaggle Version page. Other saved Notebook metadata records are successful but have not each been independently screenshot-verified.
- The legacy Excel hour entries could not be mapped to the same saved Notebook versions; they are not treated as the source of full-run duration.
- Peak allocated/reserved GPU memory and PEFT training/evaluation logs are included.

## Public repository status (2026-11-26)

- The repository was pushed to the public GitHub repository: https://github.com/TheNexoraLabs/peft-vs-rbicl-qa
- The published tree contains 87 files (86 files covered by `FILE_MANIFEST.sha256`; the manifest does not hash itself).
- The public tree was checked after upload. All expected top-level folders, eight notebooks, result files, documentation, `CITATION.cff`, and `LICENSE` are present.
- The local release archive matched all 86 SHA-256 manifest entries with no missing, mismatched, or unexpected files.
- All eight notebooks passed current `nbformat` validation; the validator emitted a non-fatal warning that cell `id` values are absent. This may be cleaned up in a later maintenance commit.
- The three Python scripts compiled successfully, relative Markdown links resolved, and a scan for common token/key patterns found no matches in the release files. These checks reduce risk but are not a guarantee that every possible secret has been identified.
- The maintainer reports that all three authors approve public release of the code and derived result artifacts.
- The MIT license copyright notice is set to `TheNexoraLabs` at the maintainer's instruction. The organization name should be used as copyright holder only if it is the actual rights holder or is authorized by the rights holders to issue the license.
- The LoRA Run All duration (03:48:12) was independently confirmed against the author's Kaggle Version page. Other saved Notebook metadata records are successful but have not each been independently screenshot-verified.
- No training, inference, or human re-annotation was performed during repository preparation. The statistical analysis was re-executed locally from the compact public metric files.

## Remaining archival steps

- Enable the repository in the Zenodo GitHub integration.
- Create the first GitHub release only after the Zenodo integration is enabled, then verify that Zenodo archives it and issues a DOI.
- Add the DOI and final software citation to `CITATION.cff`, the manuscript's Code Availability text, and the corresponding bibliography entry once the Zenodo record exists.
