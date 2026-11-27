# Zenodo DOI and citation guidance

The GitHub repository is archived on Zenodo as release **0.1.1**.

- Version-specific DOI for release 0.1.1: https://doi.org/10.5281/zenodo.24582468
- Concept DOI for all repository versions: https://doi.org/10.5281/zenodo.24582467

Use the version-specific DOI when citing or describing the exact software snapshot used in a study. Use the Concept DOI when referring to the software project across releases; it resolves to the latest archived version.

## BibTeX example for the exact archived release

```bibtex
@software{moghadam2026peft_rbicl_zenodo,
  author       = {Moghadam, Mahsima Ebrahimi and
                  Mousavi, Seyyed Amir Hossein and
                  AbbasiRad, Ensieh},
  title        = {A Systematic Comparison of Parameter-Efficient Fine-Tuning and
                  Retrieval-Based In-Context Learning for Large Language
                  Model-Based Question Answering},
  year         = {2026},
  version      = {0.1.1},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.24582468},
  url          = {https://doi.org/10.5281/zenodo.24582468}
}
```

For a manuscript using a numbered Springer bibliography style, the entry may need to be adapted to the selected BibTeX style (for example, `@misc` instead of `@software`). Preserve the version-specific DOI and release number.
