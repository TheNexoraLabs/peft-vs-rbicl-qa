# Shared inference and scoring pipeline

The author reports that one shared QA inference notebook and one shared scoring notebook were used across the six evaluated systems, changing the selected final checkpoint/model path between runs. The public repository includes cleaned copies of these shared workflows:

- `notebooks/07_shared_qa_inference.ipynb`
- `notebooks/08_shared_qa_scoring.ipynb`

## Configuration

The inference notebook reads these environment variables (or the fallback Kaggle paths in the notebook):

- `QA_MODEL_PATH`: selected final model/adapter directory for the configuration being evaluated.
- `QA_DATASET_CSV`: prepared `finetune_dataset_fixed_3000.csv` path.
- `QA_PREDICTION_OUTPUT`: private output path for the generated test predictions.

The scoring notebook reads:

- `QA_PREDICTIONS_CSV`: prediction file from the inference notebook.
- `QA_EVALUATION_OUTPUT`: private output directory for per-example scores and aggregate metrics.

## Privacy and publication note

The inference output and scoring output include context, questions, reference answers, and generated predictions. They are needed locally for evaluation but are not part of the public repository. The public release contains data-minimized per-example metric CSVs keyed by stable `sample_id` values, with source benchmark text and generated answer text omitted.

## Timing note

The supplied shared inference notebook does not contain an explicit generation timer or six separate preserved run records. It therefore documents the inference procedure but is not used to infer the manuscript's six QA-runtime values.
