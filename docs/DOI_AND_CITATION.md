# Zenodo DOI and citation guidance

The current GitHub software release (**v0.1.2**) is archived on Zenodo.

- **Version-specific DOI for v0.1.2:** https://doi.org/10.5281/zenodo.24597976
- **Concept DOI (all versions):** https://doi.org/10.5281/zenodo.24582467

The previous archived release (**v0.1.1**) remains available with its own immutable version-specific DOI:

- **Version-specific DOI for v0.1.1:** https://doi.org/10.5281/zenodo.24582468

## Which DOI should I cite?

Use the version-specific DOI when citing or describing the exact software snapshot used in a study. For work based on release v0.1.2, cite **10.5281/zenodo.24597976**. Use the Concept DOI when referring to the software project across releases rather than to one exact snapshot.

## BibTeX example for the current release (v0.1.2)

```bibtex
@software{moghadam2026peft_rbicl_zenodo,
  author       = {Moghadam, Mahsima Ebrahimi and
                  Mousavi, Seyyed Amir Hossein and
                  AbbasiRad, Ensieh},
  title        = {A Systematic Comparison of Parameter-Efficient Fine-Tuning and
                  Retrieval-Based In-Context Learning for Large Language
                  Model-Based Question Answering},
  year         = {2026},
  version      = {0.1.2},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.24597976},
  url          = {https://doi.org/10.5281/zenodo.24597976}
}
```

For a manuscript using a numbered Springer bibliography style, the entry may need to be adapted to the selected BibTeX style (for example, `@misc` instead of `@software`). Preserve the version-specific DOI and release number.
