# GitHub update steps

This bundle is an overlay for the repository `TheNexoraLabs/peft-vs-rbicl-qa`.

1. Copy `docs/HUMAN_EVALUATION_PROTOCOL.md` into the repository's existing `docs/` folder.
2. Replace the repository-root `README.md` with the supplied `README.md`.
3. Replace `results/human_evaluation/README.md` with the supplied file at the same path.
4. Apply `analysis/human_evaluation/README_SCRIPT_EDITS.patch` to `analysis/human_evaluation/generate_human_evaluation_outputs.py`, or make the three exact comment/text replacements shown in the patch. This removes obsolete wording that calls the codebook reconstructed or pending validation; it does not change calculations or output labels.
5. Review the Git diff. Do not add `annotated_output_final.csv`, `annotations 1.csv`, `annotations 2.csv`, `annotations 3.csv`, or any other raw annotation export.
6. Commit the changes with a message such as `Document human evaluation and adjudication protocol` and push to `main`.
7. After pushing, open the GitHub versions of the three Markdown files and confirm that the links render and point to the correct paths.

No existing result table or figure needs to be regenerated solely because this protocol document is added. Do not create a new Zenodo release until the remaining audit checks described in the accompanying chat have been completed.
