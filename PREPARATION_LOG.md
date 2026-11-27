# Preparation log

## Research materials reviewed

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
- Added the shared inference and scoring notebooks; the maintainer confirms that this same workflow was used across all six configurations by selecting the appropriate final checkpoint for each run.
- Added `.gitignore` rules to prevent raw prediction/scoring CSVs and raw annotation files from being committed.

## Evaluation and statistical analysis

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
- Removed the unsupported statement that retrieval correctness was established. Qualitative examples and the reconstructed error taxonomy are withheld pending review of source-data terms and the original annotation guideline. Raw annotation-level files are not redistributed.

## Resource measurement provenance

- Preserved full Notebook Papermill run metadata, internal code-level timers, and manuscript timing values as distinct measures.
- The LoRA Run All duration (03:48:12) was independently confirmed against the author's Kaggle Version page. Other saved Notebook metadata records are successful but have not each been independently screenshot-verified.
- Legacy Excel hour entries could not be mapped to the same saved Notebook versions; they are not treated as the source of full-run duration.
- Peak allocated/reserved GPU memory and PEFT training/evaluation logs are included.

## Public GitHub repository status (2026-11-27)

- Repository: https://github.com/TheNexoraLabs/peft-vs-rbicl-qa
- The public tree contains 87 files (86 files covered by `FILE_MANIFEST.sha256`; the manifest does not hash itself).
- All expected top-level folders, eight notebooks, result files, documentation, `CITATION.cff`, and `LICENSE` were verified in the public GitHub tree.
- The local release archive matched all 86 SHA-256 manifest entries with no missing or mismatched entries at the time of the v0.1.1 release.
- All eight notebooks passed current `nbformat` validation; a non-fatal missing-cell-ID warning remains.
- Python source files compiled; relative Markdown links resolved; a best-effort scan found no common token/key patterns.
- The maintainer reports that all three authors approve public release of the code and derived result artifacts.
- The MIT copyright line is `TheNexoraLabs`; the maintainer should ensure the organization is the actual copyright holder or is authorized by the rights holders to issue this license.

## Zenodo archival status (2026-11-27)

- GitHub-to-Zenodo integration is enabled for `TheNexoraLabs/peft-vs-rbicl-qa`.
- GitHub release `0.1.1` was archived successfully.
- Version DOI: https://doi.org/10.5281/zenodo.24582468
- Concept DOI (all versions): https://doi.org/10.5281/zenodo.24582467
- Both DOI identifiers are recorded in the repository `README.md` and `CITATION.cff`.
- The manuscript's Code Availability statement and software bibliography entry cite the exact software version 0.1.1.

## Remaining maintenance items

- Confirm that `TheNexoraLabs` is the legal copyright holder or is formally authorized by the relevant rights holders to issue the MIT license for all included code.
- Have all authors review the final README, author metadata, and citation metadata.
- Optionally add stable cell IDs to the eight notebooks to silence the non-fatal `nbformat` warnings.
- The `FILE_MANIFEST.sha256` file corresponds to the archived v0.1.1 snapshot; a later maintenance commit on `main` may differ from that immutable Zenodo version.
- After journal publication, add the article's own publication DOI and final journal citation separately. The Zenodo DOI identifies the research software, not the article.


## Q1 QA inference timing verification (2026-11-27)

- Inspected the four notebooks in the maintainer-supplied `loader-llamas.rar` archive.
- Each notebook contains 300 saved answer outputs and a successful Papermill run (`exception = null`). No empty answer was found in any of the four 300-answer outputs.
- Mapped the files by exact row-wise comparison of the extracted answers with each model-specific Q1 `predicted_answer` column: loader-llama3-1 = DoRA (300/300); loader-llama3-2 = DoRA+DeepSeek (300/300); loader-llama3-3 = LoRA (300/300); loader-llama3-4 = LoRA+DeepSeek (300/300). The best competing-system match was lower (280/300 for the Llama pairings and 292/300 for the DeepSeek pairings).
- Used the saved execution metadata of the complete PEFT generation cell for the four fine-tuned systems. All PEFT outputs correspond to the 300-row Q1 primary set, not the 280-row Q2 sensitivity set.
- Used saved Jupyter execution metadata for the cell containing the 300-question query loop for all six systems. For RB-ICL, the cell intervals are cross-checked against the explicit internal time.time() timers (differences below 0.30 seconds); both notebooks report zero prompt-budget fallbacks.
- Replaced the former QA runtime values in the manuscript table with the Q1-aligned loop/cell measurements. Full Notebook Run All durations are preserved as a separate measure.
- Updated the manuscript's RB-ICL Token F1/runtime table, runtime discussion, measurement-convention appendix, and computational-cost figure.
- Added cleaned QA inference run-record notebooks with outputs cleared, execution metadata retained, and personal Google Drive checkpoint-download cells removed.
- Rebuilt the computational-cost workbook and SHA-256 manifest utility. No new model training, inference, or annotation was performed during this audit.
