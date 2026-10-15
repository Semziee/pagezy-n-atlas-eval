---
language:
  - en
library_name: peft
pipeline_tag: text-generation
base_model: NCAIR1/N-ATLaS
tags:
  - peft
  - lora
  - qlora
  - text-generation
  - education
  - nigeria
  - adapter
---

# Pagezy N-ATLaS QLoRA Adapter (500-example SQuAD experiment)

> **At a glance:** This is a PEFT LoRA adapter for N-ATLaS, trained on 400
> English reading-comprehension examples from SQuAD. It was tuned to produce a
> short explanation when given a passage, question, and correct answer. It is
> an experimental adapter—not a validated tutor, diagnostic tool, or
> child-facing model.

## Model Details

### Model Description

- **Developed/shared by:** Semziee (Hugging Face account that published the adapter).
- **Project:** Pagezy, a prototype reading-support and model-evaluation project.
- **Funding:** No funding information is recorded in the repository.
- **Model type:** Parameter-efficient fine-tuning (PEFT) LoRA adapter for
  causal language modeling. This repository contains adapter weights, not a
  standalone base model.
- **Base model:** [`NCAIR1/N-ATLaS`](https://huggingface.co/NCAIR1/N-ATLaS), a
  Llama 3 8B-based model published by N-ATLaS / Awarri.
- **Fine-tuning language:** English. The fine-tuning examples are from the
  English SQuAD dataset. The base model's multilingual capabilities do not
  establish multilingual performance for this adapter.
- **License:** No license is declared in this adapter repository's metadata.
  Use is also subject to the base model's current license and access terms.
  Review both before using or redistributing the adapter; do not assume that
  this adapter is Apache-2.0 merely because the Pagezy code repository uses
  Apache-2.0.
- **Adapter repository:** <https://huggingface.co/Semziee/pagezy-n-atlas-qlora-500>
- **Project source and training/evaluation scripts:**
  <https://github.com/Semziee/pagezy-n-atlas-eval>
- **Demo:** The project repository contains a Gradio application. The
  application is not the model itself and its Model Arena requires separate
  model access and compatible GPU hardware.

### Model Sources

- **Base model:** [N-ATLaS on Hugging Face](https://huggingface.co/NCAIR1/N-ATLaS)
- **Adapter files:** `adapter_model.safetensors` and `adapter_config.json` in
  this repository.
- **Project implementation:** [`scripts/fine-tune-qlora.py`](https://github.com/Semziee/pagezy-n-atlas-eval/blob/main/scripts/fine-tune-qlora.py)
- **Evaluation implementation:** [`harness/eval_finetuned.py`](https://github.com/Semziee/pagezy-n-atlas-eval/blob/main/harness/eval_finetuned.py)
- **Published adapter revision inspected for this card:**
  `73844c2cd9982de497fb122c8933a4eb979351d2`.
- **Paper:** No paper specifically documenting this adapter is available.

## Uses

### Direct Use

The adapter can be loaded on top of the N-ATLaS base model for experimentation
with short English explanations of reading-comprehension answers. The
fine-tuning prompt has the following structure:

```text
Passage: <passage>
Question: <question>
Correct Answer: <answer>

Provide a 1-sentence explanation of why this is correct based on the text.
```

The task gives the correct answer to the model. The adapter is therefore tuned
to explain a supplied answer, not to independently answer questions, diagnose
reading difficulties, or generate a scaffolded hint from an incorrect student
answer.

### Downstream Use

Researchers and developers may use it as an experimental adapter in
reproducible model comparisons, subject to the base model's and adapter's
applicable terms. Review generated text before any educational use.

### Out-of-Scope Use

Do not use this adapter as:

- A clinical, dyslexia, literacy, or educational diagnostic.
- An automated tool for grading, placement, promotion, or other high-impact
  decisions about a child.
- A replacement for a teacher, reading specialist, or qualified evaluator.
- A speech-recognition model; it accepts text prompts and has no child-speech
  input capability.
- Evidence that the system works for Nigerian curricula, Yoruba, Igbo, Hausa,
  Nigerian Pidgin, or children. Those capabilities were not established by
  this adapter's reported fine-tuning experiment.

## Bias, Risks, and Limitations

- **Narrow training task and data:** The adapter was fine-tuned on 400 English
  SQuAD examples, not on child-authored responses, Nigerian curricula, or a
  representative educational dataset.
- **Answer leakage in evaluation:** The evaluation prompt includes the correct
  answer. The reported `grounded` metric checks whether that supplied answer
  appears as a case-insensitive substring in the generated response. It does
  not measure whether the model independently finds a correct answer or
  whether its explanation is faithful.
- **Task mismatch:** The adapter's fine-tuning/evaluation target is an
  explanation of a supplied correct answer. Pagezy's Model Arena asks for a
  hint after an incorrect answer. Performance on the former does not establish
  performance on the latter.
- **Small evaluation:** The checked-in run evaluates 20 English holdout
  examples once per model. It is a small experiment, not a statistically
  powered or independently replicated benchmark.
- **Generation variability:** Evaluation uses sampled generation
  (`temperature=0.3`, `do_sample=True`) and records no repeated-seed analysis
  or confidence intervals.
- **Training-label construction:** The training script sets labels over the
  full prompt-plus-answer token sequence. It does not mask the prompt tokens
  from the loss, so the model is trained to reproduce prompt text as well as
  the explanation.
- **Data quality and domain:** SQuAD is English reading-comprehension data and
  is not a child-safety, Nigerian-curriculum, or cultural-relevance benchmark.
- **No safety evaluation:** The evaluation's refusal check searches for four
  phrases and is not a safety test. Zero matches to those phrases must not be
  interpreted as proof of safety.
- **No user study:** No child, teacher, classroom, or clinical study of this
  adapter is reported.
- **Hardware and environment records:** Exact training hardware, cloud
  provider, region, runtime duration, energy use, and emissions are not
  recorded.

### Recommendations

Use the model only in controlled research or development settings. Present
outputs as unverified model generations and have a qualified human review any
educational content. Do not provide personal or sensitive student information
to the model. Before making performance claims, run a task-aligned, leakage-free
evaluation with an appropriate comparison, repeated seeds, human review, and
documented limitations.

## How to Get Started

The base model is gated. First obtain access to N-ATLaS and authenticate with
Hugging Face using the CLI or an environment-managed token. Do not hard-code or
commit credentials. The environment also needs a compatible CUDA GPU for this
4-bit loading example.

```bash
python -m pip install torch transformers peft accelerate bitsandbytes
hf auth login
```

```python
import torch
from peft import PeftModel
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)

BASE_ID = "NCAIR1/N-ATLaS"
ADAPTER_ID = "Semziee/pagezy-n-atlas-qlora-500"

quantization = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

tokenizer = AutoTokenizer.from_pretrained(BASE_ID)
base = AutoModelForCausalLM.from_pretrained(
    BASE_ID,
    quantization_config=quantization,
    device_map="auto",
)
model = PeftModel.from_pretrained(base, ADAPTER_ID)
model.eval()

prompt = (
    "Passage: Amina planted maize before the rainy season began.\n"
    "Question: What did Amina plant?\n"
    "Correct Answer: Maize\n\n"
    "Provide a 1-sentence explanation of why this is correct based on the text."
)
chat = [{"role": "user", "content": prompt}]
text = tokenizer.apply_chat_template(
    chat, tokenize=False, add_generation_prompt=True
)
inputs = tokenizer(text, return_tensors="pt").to(model.device)

with torch.inference_mode():
    output = model.generate(
        **inputs,
        max_new_tokens=120,
        temperature=0.3,
        do_sample=True,
    )

answer = tokenizer.decode(
    output[0][inputs.input_ids.shape[-1]:],
    skip_special_tokens=True,
)
print(answer.strip())
```

The code above demonstrates adapter loading and the evaluation-style task; it
does not establish a recommendation for real learner use.

## Training Details

### Training Data

The checked-in training workflow reads `data/train_400.jsonl`. The repository's
`scripts/prepare-dataset.py` creates this file by sampling 500 records from the
Hugging Face dataset `rajpurkar/squad` with shuffle seed 42, then splitting the
sample into 400 training rows and 100 holdout rows. The fine-tuning script uses
the 400 training rows.

Each training prompt contains the passage, question, and correct answer. Its
target explanation is constructed as:

```text
Based on the text, the correct answer is <answer>.
```

The examples are English SQuAD data, not Pagezy's Nigerian-language passage
corpus. The code records no additional filtering, child-specific adaptation,
or independent human review of the training examples.

### Training Procedure

The script loads N-ATLaS with 4-bit NF4 quantization, prepares it for
k-bit training, applies LoRA, and trains using the Hugging Face Transformers
`Trainer`. The adapter repository's published configuration confirms LoRA
rank 16, alpha 32, dropout 0.05, no bias, causal-LM task type, and target
modules `q_proj`, `k_proj`, `v_proj`, and `o_proj`.

#### Preprocessing

- Formats each example as a user prompt followed by an assistant explanation.
- Tokenizes to a maximum sequence length of 512.
- Pads to `max_length` and truncates longer examples.
- Sets labels to a copy of all input token IDs. Prompt tokens are not masked
  from the loss.

#### Training Hyperparameters

- **Training regime:** Supervised fine-tuning with QLoRA / PEFT LoRA.
- **Epochs:** 2.
- **Per-device batch size:** 2.
- **Gradient accumulation steps:** 4.
- **Effective batch size:** 8 examples per optimizer update, assuming one
  training device.
- **Learning rate:** `2e-4`.
- **Optimizer:** `paged_adamw_8bit`.
- **Training precision:** BF16 (`bf16=True`).
- **Quantization:** 4-bit NF4; the training script does not explicitly enable
  double quantization.
- **LoRA rank / alpha / dropout:** 16 / 32 / 0.05.
- **LoRA target modules:** `q_proj`, `k_proj`, `v_proj`, `o_proj`.
- **Scheduler / warmup:** Not explicitly configured in the training script;
  Transformers defaults apply.
- **Random seed:** Not explicitly set in the training script.
- **Exact training duration:** Not recorded. A script comment estimates
  15–20 minutes, but this is not a measured run record.

#### Speeds, Sizes, Times

The Hugging Face Hub reports approximately 71.8 MB of stored files for the
adapter repository at the time this card was prepared. This is adapter
repository storage, not total inference memory: inference also loads the
N-ATLaS base model. No measured tokens/second, training throughput, or
peak-memory data is available.

## Evaluation

### Testing Data, Factors, and Metrics

#### Testing Data

`harness/eval_finetuned.py` reads the first 20 examples from
`data/test_100.jsonl`. The data-preparation script places these 100 rows after
the 400 training rows in a deterministically shuffled 500-example sample from
`rajpurkar/squad` (seed 42). The test examples are separate rows from the
training split, but the evaluation prompt explicitly includes each example's
correct answer.

#### Factors

- Four configurations were evaluated: this adapter on N-ATLaS, base N-ATLaS,
  Qwen 2.5 3B Instruct, and Llama 3.2 3B Instruct.
- Each configuration was run on the same 20 examples in the checked-in result
  file.
- Generation used `max_new_tokens=120`, `temperature=0.3`, and
  `do_sample=True`.
- Models were loaded using 4-bit NF4 quantization; evaluation config enabled
  double quantization and BF16 compute.
- The results are from one saved run. The code does not fix a generation seed
  or report confidence intervals.

#### Metrics

- **Answer-string match (`grounded` in CSV):** Case-insensitive substring
  presence of the correct answer in the generated response.
- **Refusal phrase match (`refused` in CSV):** Presence of any of four
  hard-coded phrases: `i cannot`, `as an ai`, `i am not able`, or `i don't
  know`.
- **Response length:** Whitespace-separated word count.

These are implementation-level heuristics, not validated measures of
correctness, grounding, safety, helpfulness, or educational quality.

### Results

The values below are recalculated from
`results/2026-10-12_finetune_eval.csv` in the project repository. They describe
this one run and the heuristics above; they are not a general model-quality
claim.

| Model | Examples (n) | Correct-answer substring match | Refusal phrase matches | Mean response words |
|---|---:|---:|---:|---:|
| Pagezy QLoRA adapter | 20 | 20/20 (100%) | 0 | 11.0 |
| N-ATLaS base | 20 | 18/20 (90%) | 0 | 33.6 |
| Qwen 2.5 3B Instruct | 20 | 17/20 (85%) | 0 | 22.3 |
| Llama 3.2 3B Instruct | 20 | 19/20 (95%) | 0 | 31.2 |

#### Summary

In this saved run, the adapter returned shorter responses and included the
answer string in all 20 responses. Because the correct answer was supplied in
the prompt, this result demonstrates answer-string reproduction on these
examples; it does **not** demonstrate independent answer accuracy, faithful
reasoning, superior hint quality, safety, or improvement on Nigerian
curriculum tasks. A stronger follow-up should evaluate without giving the
answer in the prompt, use a task-aligned hint benchmark, include human
assessment, and repeat runs across seeds.

## Model Examination

The adapter is a small add-on rather than a full copy of the base model. Its
usefulness is bounded by its narrow English SQuAD fine-tuning task. The
included evaluation outputs are mostly short answer restatements. Before
claiming it provides better tutoring, inspect qualitative examples for whether
it explains concepts accurately, avoids merely revealing answers, and uses
language suitable for the intended learner.

## Environmental Impact

The project does not record sufficient information to estimate emissions.

- **Hardware type:** Not recorded. The script requires BF16 and 4-bit
  bitsandbytes model training; it assigns the model to CUDA device 0.
- **Hours used:** Not recorded; the training script contains only an
  unverified 15–20 minute estimate.
- **Cloud provider:** Not recorded.
- **Compute region:** Not recorded.
- **Carbon emitted:** Not measured; cannot be responsibly estimated from the
  available run artifacts.

## Technical Specifications

### Model Architecture and Objective

- **Base architecture:** N-ATLaS, published as a Llama 3 8B-based causal
  language model.
- **Adapter architecture:** LoRA for causal language modeling, rank 16 and
  alpha 32, targeting attention projections `q_proj`, `k_proj`, `v_proj`, and
  `o_proj`.
- **Objective:** Next-token language modeling on formatted prompt and
  explanation text.
- **Adapter format:** PEFT adapter weights in `adapter_model.safetensors` and
  config in `adapter_config.json`.

### Compute Infrastructure

#### Hardware

The training script requires CUDA and requests BF16; the exact GPU model,
memory, provider, and region used for the published adapter were not logged.
Inference with the adapter additionally requires loading the N-ATLaS base
model. The example uses 4-bit quantization to reduce memory requirements.

#### Software

The repository pins PyTorch 2.6.0, Transformers 4.51.3, PEFT 0.15.2,
Accelerate 1.6.0, and bitsandbytes 0.45.5. The published adapter configuration
records PEFT 0.21.2. This version difference means the Hub artifact may have
been produced with a different PEFT version than the current repository pins;
verify compatibility in a clean environment before reproducing the run.

## Citation

If you use this experimental adapter, cite the adapter repository and the
original N-ATLaS base model:

```bibtex
@misc{semziee_pagezy_natlas_qlora_500,
  author       = {Semziee},
  title        = {Pagezy N-ATLaS QLoRA Adapter},
  year         = {2026},
  howpublished = {\url{https://huggingface.co/Semziee/pagezy-n-atlas-qlora-500}},
  note         = {PEFT LoRA adapter fine-tuned on 400 English SQuAD examples}
}
```

## Glossary

- **Adapter:** A small set of learned parameters loaded on top of a base model.
- **LoRA:** Low-Rank Adaptation, a parameter-efficient fine-tuning method.
- **QLoRA:** LoRA training while loading the base model in low-bit
  quantization.
- **Substring match:** A string check that detects whether one text occurs
  inside another; it is not semantic verification.

## More Information

- [Adapter repository](https://huggingface.co/Semziee/pagezy-n-atlas-qlora-500)
- [Base model card](https://huggingface.co/NCAIR1/N-ATLaS)
- [Pagezy project repository](https://github.com/Semziee/pagezy-n-atlas-eval)
- [Training script](https://github.com/Semziee/pagezy-n-atlas-eval/blob/main/scripts/fine-tune-qlora.py)
- [Evaluation script](https://github.com/Semziee/pagezy-n-atlas-eval/blob/main/harness/eval_finetuned.py)
- [Saved evaluation CSV](https://github.com/Semziee/pagezy-n-atlas-eval/blob/main/results/2026-10-12_finetune_eval.csv)

## Model Card Authors and Contact

- **Model card author/maintainer:** Semziee.
- **Contact:** Use the Hugging Face model repository discussions or the
  [Pagezy GitHub repository](https://github.com/Semziee/pagezy-n-atlas-eval)
  for questions and corrections.
