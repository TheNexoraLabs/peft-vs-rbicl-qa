# Public release and archival checklist

## Completed

- [x] Public GitHub repository and Zenodo v0.1.1 archive exist.
- [x] Version DOI for v0.1.1: https://doi.org/10.5281/zenodo.24582468
- [x] Concept DOI: https://doi.org/10.5281/zenodo.24582467
- [x] All three authors' approval for public release was confirmed by the maintainer.
- [x] Current QA evidence identifies all four PEFT loader notebooks by exact 300/300 row-wise prediction matching to their Q1 result files.
- [x] All six QA runtimes are aligned to the same 300-question primary test set.
- [x] Training/adaptation times, QA loop/cell times, full Notebook Run All durations, and GPU memory are separately documented.
- [x] Public QA notebook copies have cleared outputs and removed personal Google Drive checkpoint-download cells.

## Before publishing the next archive

- [ ] Apply the runtime/Q1 patch and regenerate `FILE_MANIFEST.sha256` from the complete repository.
- [ ] Commit and push the patch to GitHub.
- [ ] Create GitHub release `v0.1.2` after the new main-branch snapshot is complete.
- [ ] Verify Zenodo archives v0.1.2 and issues its Version DOI.
- [ ] Add the new Version DOI to `CITATION.cff`, `README.md`, the article's Code Availability text, and the software bibliography record.
- [ ] Confirm that `TheNexoraLabs` is the actual copyright holder or is formally authorized to issue the MIT license for all included code.

## After article publication

- [ ] Add the article's journal citation and article DOI separately. The Zenodo DOI identifies the software, not the manuscript.
