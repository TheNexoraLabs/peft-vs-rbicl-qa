# Public release and archival checklist

## Completed for the public GitHub repository

- [x] All three authors' approval for public release of code and derived result artifacts was confirmed by the maintainer.
- [x] `CITATION.cff` reflects the current manuscript title, author order, and affiliations.
- [x] MIT `LICENSE` is present with the copyright notice requested by the maintainer.
- [x] Benchmark source text, prepared dataset CSVs, model weights, raw prediction text, and row-level annotator files are not included.
- [x] The public repository was inspected after upload; the expected files and folders are present.
- [x] The 86 SHA-256 manifest entries were checked against the prepared release archive; no missing or mismatched entries were found.
- [x] All eight notebooks pass current `nbformat` validation (a non-fatal missing-cell-ID warning remains).
- [x] Python source files compile and README-relative links resolve.
- [x] A scan for common credential/token patterns returned no matches. This is a best-effort scan, not a guarantee that every possible secret is absent.
- [x] Timing provenance and reproducibility limitations are documented.

## Still required before the first DOI-backed release

- [ ] Confirm that `TheNexoraLabs` is the correct copyright holder or is formally authorized by the relevant rights holders to issue the MIT license for all included code.
- [ ] Connect GitHub to Zenodo and enable `TheNexoraLabs/peft-vs-rbicl-qa` in Zenodo.
- [ ] After enabling the integration, create the first GitHub release (suggested tag: `v0.1.0`, matching `CITATION.cff`).
- [ ] Verify that Zenodo successfully archives the release and issues a DOI.
- [ ] Add the DOI to `CITATION.cff` and update the manuscript's Code Availability statement and software bibliography entry.
- [ ] Optionally add stable cell IDs to the eight notebooks to silence the current non-fatal `nbformat` warnings.
