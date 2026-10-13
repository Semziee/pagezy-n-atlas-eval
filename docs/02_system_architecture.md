# System Architecture

## Overview

The repository contains a Gradio application, standalone model/data scripts,
and recorded evaluation artifacts. The current application has a reading-demo
tab and a separate, on-demand model-comparison tab.

```text
data/passages.jsonl ───────────────► app/app.py
                                         │
                                         ├─ Learn with Pagezy
                                         │    passage, quiz, manual scores
                                         │    heuristic diagnostic
                                         │
                                         └─ Model Arena (on demand)
                                              N-ATLAS + PEFT adapter
                                              Qwen 2.5 3B
                                              Llama 3.2 3B

scripts/prepare-dataset.py ────────► data/train_400.jsonl
                                  └► data/test_100.jsonl

scripts/fine-tune-qlora.py ────────► local adapter directory
harness/eval_finetuned.py ────────► results/2026-10-12_finetune_eval.csv
```

## Application

`app/app.py` reads `data/passages.jsonl` when the app starts. Its **Learn with
Pagezy** tab displays a passage and one question, checks the selected option,
and uses manually entered reading/listening sliders to produce a heuristic
message. It does not use the quiz response to calculate the slider scores.

The **Model Arena** loads model weights when first run. The Pagezy adapter and
base N-ATLAS share the same base model object; Qwen and Llama are loaded as
additional models. The function generates a hint for a fixed wrong option for
each model and reports response text, word count, elapsed time, and a substring
match against the correct answer. It does not render a precomputed leaderboard
from the CSV files.

The app uses 4-bit bitsandbytes quantization and explicit CUDA device placement.
Model comparison therefore needs compatible GPU hardware and enough VRAM for
all loaded weights and inference. Refer to the [deployment runbook](08_runbook_deployment.md)
for Space requirements.

## Data and scripts

- `data/passages.jsonl` is the app's demo corpus. Its records use `read_text`,
  `quiz`, `age_group`, `language`, and related fields; see the
  [data schema](03_data_schema.md).
- `scripts/prepare-dataset.py` samples SQuAD records into training and holdout
  JSONL files.
- `scripts/fine-tune-qlora.py` trains a PEFT LoRA adapter using the training
  file and a 4-bit base model.
- `harness/eval_finetuned.py` runs model generation on a subset of the holdout
  file and writes per-example CSV rows.
- `harness/rubric.py` contains a simple response-scoring helper. The current
  evaluation script does not call it.
- `scripts/gen-passages.py` writes draft model-generated passages. Review drafts
  before using them as learning materials.
- `scripts/gen-audio.py` creates sample MP3 assets. The current app UI does not
  play these files.

## Model and dependency stack

The model workflows use PyTorch, Hugging Face Transformers and Datasets, PEFT,
Accelerate, and bitsandbytes. Gradio provides the UI; pandas and NumPy support
evaluation data. The exact dependency versions are pinned in
[`requirements.txt`](../requirements.txt).

## Outputs and reproducibility

The checked-in CSV files are examples of recorded evaluation runs. The
evaluation workflow writes `results/2026-10-12_finetune_eval.csv`, which can
replace the existing file when rerun. Preserve results before running workflows
that overwrite them. Model revisions, generation settings, hardware, and
runtime versions can affect outputs; the current scripts do not provide a
complete experiment-tracking system.
