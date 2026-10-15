---
title: Pagezy Reading Diagnostic
emoji: 📖
colorFrom: blue
colorTo: yellow
sdk: gradio
sdk_version: 5.22.0
python_version: 3.11
app_file: app/app.py
pinned: false
---

# Pagezy: Reading Diagnostic and N-ATLAS Evaluation

Pagezy is a prototype reading tutor and model-evaluation project focused on
Nigerian primary-school learners. It explores a practical question: when a
learner struggles with a passage, is the difficulty more consistent with
decoding the written words or understanding the passage?

The repository combines a small reading-comprehension demo with scripts and
recorded results for evaluating N-ATLAS and comparison language models. It is a
research and demonstration prototype, not a validated educational assessment or
a production service.

## The problem

Reading difficulties can have different causes and need different support. A
learner who understands a passage when listening but not when reading may need
support with decoding. A learner who has difficulty in both modes may need help
with vocabulary or comprehension.

Pagezy demonstrates this read-versus-listen framing with short passages,
multiple-choice questions, manually entered scores, and a simple diagnostic.
Sample audio assets are included, but the current UI does not play them. The
project also compares language-model outputs for educational prompts, with an
emphasis on grounding, age-appropriate language, cultural relevance, and safety.

## What is included

- A Gradio demo for reading passages, answering a question, entering
  read/listen scores, and viewing a heuristic reading-diagnostic result.
- A four-model comparison interface for N-ATLAS, a Pagezy QLoRA adapter, Qwen,
  and Llama.
- Scripts for preparing a SQuAD-derived training/holdout dataset, generating
  draft passages, generating audio, fine-tuning with QLoRA, and running a model
  sanity check.
- Evaluation code, sample datasets, prompts, audio assets, and recorded CSV
  results.
- Project documentation covering architecture, data, evaluation, safety,
  licensing, and deployment considerations.

## How it works

1. **Passage and question:** The demo loads a passage and its multiple-choice
   question from `data/passages.jsonl`.
2. **Read/listen comparison:** The demo asks the user to provide reading and
   listening scores using sliders. A threshold-based rule maps those scores to
   a decoding-gap, comprehension-gap, or on-track message.
3. **Answer feedback:** The demo checks the selected option and displays the
   passage's explanation or a generic hint.
4. **Model comparison:** The Model Arena sends the same hint-generation prompt
   to the fine-tuned N-ATLAS adapter, base N-ATLAS, Qwen, and Llama, then shows
   their responses, word counts, substring-grounding heuristic, and elapsed
   time.
5. **Offline evaluation:** The evaluation script runs each of those models on
   examples from the SQuAD-derived holdout data and writes per-example results
   to CSV.

The current demo does **not** measure a child's reading or listening ability
itself: the scores are entered manually. Its diagnostic is illustrative and
should not be used to diagnose a learner or make educational placement
decisions.

## Use the demo

1. Open the **Learn with Pagezy** tab.
2. Choose a story and read the passage. The included audio files are examples;
   the current UI does not include an audio player or capture spoken answers.
3. Select an answer to the passage question.
4. Set the reading and listening sliders to explore how the heuristic diagnostic
   changes, then choose **Check Answer** to see feedback.
5. Open **Model Arena** and choose **Run 4-Model Comparison** to compare model
   hints. The first run downloads and loads the models, so it can take several
   minutes and needs a supported GPU with enough VRAM.

The UI's read/listen scores are illustrative manual inputs, not measured quiz
scores. The standard learner demo uses a fixed hint; model-generated hints are
shown separately in the Model Arena.

## Architecture

```text
data/                  Passage corpus and SQuAD-derived train/holdout data
   |                            |
   v                            v
app/                   harness/ + scripts/
Gradio learning demo   Model comparison, evaluation, generation, fine-tuning
   |                            |
   +-------------+--------------+
                 v
              results/
       Recorded evaluation CSVs
```

The app and model workflows use Hugging Face Transformers for model loading and
generation. The Pagezy adapter is loaded with PEFT; the fine-tuning script uses
QLoRA with 4-bit quantization. Gradio provides the interface, while pandas and
the Hugging Face Datasets library support evaluation and data preparation.
`edge-tts` is used by the audio-generation script.

## Technology

- Python
- PyTorch
- Hugging Face Transformers, Hub, Datasets, and Accelerate
- PEFT and bitsandbytes for QLoRA / 4-bit model loading
- Gradio for the demo UI
- pandas and NumPy for evaluation data
- edge-tts for generating the included speech audio

Pinned Python dependencies are listed in [`requirements.txt`](requirements.txt).
The model workflows are intended for a compatible CUDA/Linux environment with
sufficient GPU memory. Model downloads may require accepting the relevant model
terms and, for N-ATLAS, access to the model repository.

## Repository layout

| Path | Purpose |
|---|---|
| `app/` | Gradio application and diagnostic logic |
| `assets/audio/` | Sample MP3s used by the demo |
| `data/` | Demo passages and SQuAD-derived train/holdout data |
| `docs/` | Architecture, evaluation, safety, licensing, and runbook documentation |
| `harness/` | Evaluation code and baseline evaluation notebook |
| `prompts/` | Passage, hint, and judge prompt examples |
| `results/` | Checked-in evaluation CSVs and a result-log template |
| `scripts/` | Dataset, passage, audio, inference, fine-tuning, and sanity scripts |

## Getting started

### Requirements

- Python 3.11–3.13 (as stated in the dependency manifest)
- Git
- A CUDA-compatible GPU and supported CUDA/PyTorch/bitsandbytes setup for the
  model loading, evaluation, and fine-tuning workflows
- Hugging Face access to any gated or restricted model repositories you use

The pinned PyTorch wheel and bitsandbytes support vary by operating system and
CUDA version. If installation fails, install the appropriate PyTorch build for
your platform using the official PyTorch instructions before installing the
remaining dependencies.

### Install and run the demo

From the repository root:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
python -m pip install -r requirements.txt
python app/app.py
```

The app loads its passage data and models at startup or when the Model Arena is
used. Model downloads can be large and may require authentication. The current
app calls `demo.launch(share=True)`, which creates a publicly accessible
Gradio share link; do not use it with private data.

### Run evaluation or utility scripts

Run commands from the repository root so the scripts can resolve their relative
data and output paths:

```bash
# Prepare 400 training and 100 holdout examples from SQuAD
python scripts/prepare-dataset.py

# Generate draft passages with N-ATLAS (writes data/draft_passages.jsonl)
python scripts/gen-passages.py --lang english

# Generate the sample audio files
python scripts/gen-audio.py

# Run the recorded holdout evaluation workflow
python harness/eval_finetuned.py
```

The fine-tuning workflow is in `scripts/fine-tune-qlora.py`; it expects the
training data above and a suitable GPU environment. Do not treat generated
passages as verified curriculum materials without an independent human review.

## Deploy to Hugging Face Spaces

The repository root README contains Hugging Face Spaces metadata: it selects
the Gradio SDK and points Spaces to `app/app.py`. To deploy:

1. Create a Space under your Hugging Face account or organization. Select the
   **Gradio** SDK and choose GPU hardware; this app is not configured for
   CPU-only inference.
2. Confirm your Hugging Face account has permission to download every model
   used by the Model Arena, including any gated repositories. If the Space
   needs authenticated downloads, add a read-access token as a Space secret
   named `HF_TOKEN` in **Settings → Variables and secrets**. Never put a token
   in a tracked file or in the README.
3. Add the Space as a Git remote and push the branch you want to deploy:

   ```powershell
   git remote add space https://huggingface.co/spaces/<account>/<space-name>
   git push space main
   ```

   Replace `<account>` and `<space-name>` with the values in the Space URL. If
   the `space` remote already exists, update it with `git remote set-url space
   https://huggingface.co/spaces/<account>/<space-name>` instead.
4. Follow the Space **Logs** tab through dependency installation and startup.
   After a successful build, open the Space and test both tabs.

The Model Arena loads quantized N-ATLAS (with the Pagezy adapter), Qwen, and
Llama weights into GPU memory. Choose hardware with enough VRAM for all three
models plus runtime overhead; a larger GPU may be needed depending on model
revisions and library behavior. CPU-only Spaces are not a supported target.
The Llama model may require separate access approval. A Hugging Face token
does not bypass model-gating requirements.

On every push, Spaces rebuilds the app environment from `requirements.txt`.
Review the build and runtime logs if the Space fails; common causes include
missing model access, insufficient GPU memory, or a PyTorch/bitsandbytes/CUDA
compatibility issue. The app currently launches Gradio with `share=True`, which
may also create a separate public Gradio share link; use the Space URL as the
canonical deployment URL and do not use the demo with private data.

For the full checklist and troubleshooting notes, see
[`docs/08_runbook_deployment.md`](docs/08_runbook_deployment.md).

## Data and evaluation

- `data/passages.jsonl` contains 20 demo passages in English, Pidgin, and
  Yoruba. Its records include both verified and unverified examples; check each
  record's `human_verified` field before reuse.
- `scripts/prepare-dataset.py` samples 500 records from the public SQuAD dataset
  and writes 400 training examples and 100 holdout examples.
- `harness/eval_finetuned.py` evaluates 20 holdout examples per model and saves
  per-example output to `results/2026-10-12_finetune_eval.csv`.
- `results/baseline_eval_results.csv` contains earlier baseline evaluation
  records. See [`docs/04_evaluation_rubric.md`](docs/04_evaluation_rubric.md)
  for the intended scoring dimensions and methodology.

These files are development evidence, not a controlled study. In particular,
the current fine-tuned evaluation uses a simple substring match for its
grounding indicator and phrase matching for refusals; those heuristics do not
establish factual correctness or child safety.

## Safety, privacy, and licensing

- The project is a prototype and its diagnostic is not a clinical or validated
  educational assessment.
- The app includes sample audio assets but does not currently play them. It
  uses manually selected answers and manually entered read/listen scores; it
  does not implement child-speech recognition.
- Do not submit personal or sensitive information to the demo. The app's
  current Gradio sharing setting exposes a public share link.
- This repository's code is offered under Apache-2.0; see [`LICENSE`](LICENSE).
  Third-party model weights, datasets, and generated audio may have separate
  terms. In particular, use of N-ATLAS is subject to Awarri's applicable
  research-license terms and attribution requirements. Verify those terms
  before deployment or redistribution.

See [`docs/06_safety_and_limitations.md`](docs/06_safety_and_limitations.md)
and [`docs/05_licensing_and_compliance.md`](docs/05_licensing_and_compliance.md)
for more detail.

## Documentation

- [N-ATLaS QLoRA model card](MODEL_CARD.md)
- [Project vision and scope](docs/01_vision_and_pivot.md)
- [System architecture](docs/02_system_architecture.md)
- [Data schema](docs/03_data_schema.md)
- [Evaluation rubric](docs/04_evaluation_rubric.md)
- [Safety and limitations](docs/06_safety_and_limitations.md)
- [Licensing and compliance](docs/05_licensing_and_compliance.md)
- [Deployment runbook](docs/08_runbook_deployment.md)
- [Release checklist](docs/10_release_checklist.md)

## License

The project code is licensed under Apache License 2.0. See [`LICENSE`](LICENSE)
and review any separate terms that apply to model weights, datasets, or audio
assets before using them.
