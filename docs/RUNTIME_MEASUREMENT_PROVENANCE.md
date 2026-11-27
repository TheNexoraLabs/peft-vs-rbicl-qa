# Runtime Measurement and Computational Cost

## 1. Evaluation Scope

All six experimental configurations were evaluated using the same 300-question primary test set (Q1). Runtime measurements are reported as observed wall-clock durations from the saved Jupyter Notebook execution metadata and explicit code-level timers.

Three distinct measurements are reported:

- Training/adaptation time for the four parameter-efficient fine-tuning (PEFT) configurations.
- QA inference-cell runtime for all six configurations.
- Full QA Notebook execution duration (Run All), reported separately from the inference-cell runtime.

These measurements represent different execution scopes and should not be interpreted interchangeably.

## 2. Training and Adaptation Time

Training/adaptation time is measured using the explicit code-level timer implemented in the final GPU-calculator notebooks for the four PEFT configurations.

The timer starts immediately before the construction of the `SFTTrainer` and stops after model training, model and tokenizer saving, memory cleanup, and CUDA synchronization have completed.

Therefore, the reported duration includes trainer initialization and the subsequent training and model-saving operations. It does not represent the full execution time of the training Notebook.

RB-ICL configurations do not involve parameter fine-tuning; consequently, their training/adaptation time is reported as N/A.

## 3. QA Inference Runtime

QA inference runtime represents the wall-clock execution time of the Jupyter cell responsible for processing the complete 300-question Q1 test set.

The measurement is obtained from the saved Jupyter execution metadata, using the interval between `iopub.execute_input` and `iopub.status.idle` for the relevant execution cell.

For the PEFT configurations (LoRA and DoRA), the measured cell includes prompt construction, tokenization, text generation, decoding, per-answer console output, and final DataFrame display.

For the RB-ICL configurations, the measured cell covers the complete 300-question retrieval-and-generation loop. Model loading and vector-index construction are performed before this cell and are therefore excluded from its runtime.

Consequently, these values represent observed QA pipeline execution times rather than isolated GPU decoding times. The different execution boundaries should be considered when interpreting runtime differences between PEFT and RB-ICL systems.

## 4. Runtime Measurements

The following table summarizes the computational measurements for all six experimental configurations.

| Experimental Configuration | Training / Adaptation Time | QA Inference-Cell Runtime | Mean Time per Question (s) | Full QA Notebook Run All |
|---|---:|---:|---:|---:|
| LoRA | 03:45:31.81 | 00:24:27.63 | 4.8921 | 00:27:18.59 |
| DoRA | 08:45:31.08 | 00:32:36.86 | 6.5229 | 00:35:17.63 |
| LoRA + DeepSeek | 04:12:31.93 | 01:46:28.58 | 21.2953 | 01:49:17.20 |
| DoRA + DeepSeek | 09:02:31.80 | 01:52:34.56 | 22.5152 | 01:55:55.00 |
| RB-ICL | N/A | 00:10:52.47 | 2.1749 | 00:19:06.66 |
| RB-ICL + DeepSeek | N/A | 00:21:33.98 | 4.3133 | 00:29:56.53 |

All QA inference-cell runtimes correspond to the same 300-question primary evaluation set.

Mean time per question is calculated as:

\[
T_{\mathrm{mean}} =
\frac{T_{\mathrm{QA}}}{300}
\]

where \(T_{\mathrm{QA}}\) is the measured QA inference-cell duration in seconds.

## 5. Full Notebook Execution Duration

Full Notebook Run All duration represents the total elapsed time required to execute the corresponding QA inference Notebook from the beginning to the completion of its cells.

For the four PEFT configurations, these measurements correspond to the respective full QA loader Notebook executions. For the two RB-ICL configurations, they correspond to the final GPU-calculator Notebook executions.

Unlike the QA inference-cell measurements, full Notebook durations also include operations performed outside the main inference loop, such as environment setup, model loading, dataset preparation, and other Notebook execution steps.

These durations are therefore reported as a separate measure of end-to-end Notebook execution time and are not substituted for QA inference runtime or training/adaptation time.

## 6. GPU Memory Usage

Peak allocated GPU memory was recorded for all six configurations using the corresponding GPU memory logs.

The reported peak allocated memory values are:

| Experimental Configuration | Peak GPU Allocated Memory (GB) |
|---|---:|
| LoRA | 11.622 |
| DoRA | 13.106 |
| LoRA + DeepSeek | 11.866 |
| DoRA + DeepSeek | 13.350 |
| RB-ICL | 7.171 |
| RB-ICL + DeepSeek | 7.414 |

These values represent the maximum GPU memory allocated during the corresponding experimental runs.