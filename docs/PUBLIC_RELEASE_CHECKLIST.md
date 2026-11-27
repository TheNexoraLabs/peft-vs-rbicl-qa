# Public release and archival checklist

## GitHub and Zenodo archive

- [x] All three authors' approval for public release of code and derived result artifacts was confirmed by the maintainer.
- [x] `CITATION.cff` reflects the current manuscript title, author order, affiliations, version, and Zenodo DOI identifiers.
- [x] MIT `LICENSE` is present with the copyright notice requested by the maintainer.
- [x] Benchmark source text, prepared dataset CSVs, model weights, raw prediction text, and row-level annotator files are not included.
- [x] Public GitHub repository inspected; expected notebooks, scripts, results, and documentation are present.
- [x] The v0.1.1 release is archived in Zenodo.
- [x] Version DOI: https://doi.org/10.5281/zenodo.24582468
- [x] Concept DOI: https://doi.org/10.5281/zenodo.24582467
- [x] DOI metadata is present in `CITATION.cff`, `README.md`, and the manuscript's Code Availability statement.

## Remaining checks

- [ ] Confirm that `TheNexoraLabs` is the actual copyright holder or is formally authorized by the relevant rights holders to license all included code under MIT.
- [ ] All three authors review the final README, author metadata, and citation metadata.
- [ ] Optionally add stable cell IDs to the notebooks to remove current non-fatal `nbformat` warnings.
- [ ] After journal publication, add the journal citation and article DOI separately; the Zenodo DOI is for the software release.
