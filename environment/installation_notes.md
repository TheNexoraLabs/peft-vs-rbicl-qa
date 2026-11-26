# Installation notes transcribed from the final-run notebooks

These are the principal pinned packages explicitly installed in the notebooks. The original notebooks use Kaggle-oriented install cells; retain the CUDA/PyTorch compatibility of the selected runtime when reproducing the experiments.

## PEFT notebooks (LoRA / DoRA)

- `torch==2.10.0+cu128`
- `xformers==0.0.35`
- `unsloth==2026.5.4`
- `transformers==4.56.2`
- `trl==0.22.2` (installed with `--no-deps` in the notebook)
- `triton==3.6.0`
- `pip3-autoremove` (utility installed by the notebook)

## RB-ICL notebooks

- `torch==2.10.0`
- `torchvision==0.25.0`
- `xformers==0.0.35`
- `unsloth==2026.5.4`
- `transformers==4.56.2`
- `triton==3.6.0`
- `llama-index==0.12.44`
- `llama-index-vector-stores-chroma`
- `chromadb==1.0.13`
- `huggingface_hub==0.36.2`
- `llama-index-llms-huggingface==0.5.0`
- `llama-index-embeddings-huggingface` (no version pin in notebook)

This file is a transcription of explicit installation commands, not a fully solved dependency lockfile. Do not treat it as a guaranteed portable `pip install -r` file.

## Shared QA inference and scoring

The shared inference notebook uses the same Unsloth/Transformers stack listed above. The scoring notebook additionally imports `evaluate`, `rouge-score`, `bert-score`, `sentence-transformers`, and `sacrebleu`. The original scoring notebook uses unpinned lower-bound package specifications; this is a transcription of the supplied workflow, not a lockfile.
