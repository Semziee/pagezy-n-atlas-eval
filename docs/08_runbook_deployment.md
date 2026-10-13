# Deployment and Usage Runbook

This guide describes the repository as it exists today. Pagezy is a prototype;
deploying it does not make its diagnostic or model outputs validated for
educational or clinical use.

## Local setup

Use Python 3.11–3.13, as specified in `requirements.txt`. Install and run from
the repository root:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app/app.py
```

The UI opens in a browser. Model weights are downloaded from Hugging Face when
the Model Arena is first run. Model loading and inference require a compatible
CUDA GPU; this repository is not configured for CPU-only model inference.
Check model terms and account access before downloading restricted weights.

## Using the application

### Learn with Pagezy

1. Select a story from the passage dropdown.
2. Read the passage and select one of its answer options.
3. Adjust the reading and listening score sliders, then select **Check Answer**.
4. Read the answer feedback and heuristic diagnostic.

The sliders are manual inputs: the app does not calculate scores from quiz
answers or listen to a learner read. Although sample audio files are included,
the current UI does not play them. The ordinary quiz feedback uses the
passage's explanation for correct answers and a fixed hint for incorrect
answers.

### Model Arena

1. Select a passage.
2. Select **Run 4-Model Comparison**.
3. Compare the generated hints and the word-count, heuristic grounding, and
   elapsed-time columns.

The first run downloads and loads the model weights. The app loads base
N-ATLAS plus the Pagezy PEFT adapter, Qwen 2.5 3B, and Llama 3.2 3B. This needs
a CUDA-compatible GPU with enough memory for all models and runtime overhead.
The grounding column is a substring check, not a factuality evaluation.

## Hugging Face Spaces deployment

The root `README.md` includes Space metadata configured for Gradio, Python 3.11,
and the `app/app.py` entry point. Keep that metadata accurate if the entry point
or pinned Gradio version changes.

### Prerequisites

- A Hugging Face Space created with the **Gradio** SDK.
- GPU hardware with sufficient VRAM for the three model weights used by the
  Model Arena, in addition to application/runtime overhead. The exact minimum
  depends on the model revisions and runtime; if models fail to load with CUDA
  out-of-memory errors, select a larger GPU.
- Model access for `NCAIR1/N-ATLaS`, `Semziee/pagezy-n-atlas-qlora-500`,
  `Qwen/Qwen2.5-3B-Instruct`, and `meta-llama/Llama-3.2-3B-Instruct`.
  In particular, Llama may require accepting its terms and approval on the
  Hugging Face account.
- If the Space needs authentication to download private or gated weights, a
  read-access token saved as the Space secret `HF_TOKEN`. A token cannot grant
  access that the associated Hugging Face account does not have.

Never commit a token to Git or place one in source code, notebooks, logs, or
documentation. Set it through the Space's **Settings → Variables and secrets**
page.

### Publish from the Git checkout

Authenticate with the Hugging Face CLI using the account that owns the Space,
then add the Space repository as a Git remote:

```powershell
hf auth login
git remote add space https://huggingface.co/spaces/<account>/<space-name>
git push space main
```

Replace the placeholders with the account and Space name from the Space URL.
If the remote is already configured, update it instead of adding it again:

```powershell
git remote set-url space https://huggingface.co/spaces/<account>/<space-name>
```

Spaces builds the app from the files pushed to the Space repository. Review the
Space's **Logs** tab while dependencies install and the app starts. After the
build succeeds, test the Space URL in a fresh browser session:

- Open both app tabs.
- Load the reading demo, change passages, submit correct and incorrect
  answers, and confirm the diagnostic responds to slider values.
- Run the Model Arena and confirm all four output columns and timing/grounding
  rows populate.
- Check the logs for authentication, CUDA, model-loading, and memory errors.

The application currently calls `demo.launch(share=True)`. Consequently, a
Space may also create a separate Gradio share link. Treat the Hugging Face Space
URL as canonical, and do not enter private information into either endpoint.

## Evaluation and data scripts

Run commands from the repository root:

```powershell
# Generate a reproducible 400/100 split from SQuAD
python scripts/prepare-dataset.py

# Generate draft passages with N-ATLAS
python scripts/gen-passages.py --lang english

# Generate the sample MP3 files
python scripts/gen-audio.py

# Run the holdout model comparison
python harness/eval_finetuned.py

# Fine-tune with QLoRA (requires the prepared training set and supported GPU)
python scripts/fine-tune-qlora.py
```

Review generated passages before using them with learners. Dataset generation
may overwrite checked-in train and holdout files; evaluation writes its CSV to
`results/2026-10-12_finetune_eval.csv`. Preserve or back up results you need
before rerunning workflows that overwrite them.

## Troubleshooting

| Symptom | Check |
|---|---|
| Model download returns 401/403 | Confirm the Space secret is named `HF_TOKEN`, the token has read access, and the account has access to each gated model. |
| CUDA out of memory | Select a GPU with more VRAM; the Model Arena loads multiple models in one process. |
| bitsandbytes or CUDA import/load error | Check that the Space hardware, PyTorch wheel, CUDA runtime, and pinned bitsandbytes version are compatible. |
| Space reports missing data | Confirm `data/passages.jsonl` is present in the Space repository and the app is launched from the repository root. |
| App builds but first Arena run is slow | Model weights are downloaded and loaded on first use; check Space logs and allow the load to finish. |
| Space still shows an older version | Confirm the push reached the Space's `main` branch and inspect its build logs. |

## Operational and safety notes

- V1 has no child-speech recognition and does not collect spoken answers.
- The reading/listening scores are user-entered; output is only a heuristic
  demonstration, not an assessment or diagnosis.
- Do not collect or submit identifying or sensitive learner data.
- The app source does not implement an active-user cap. Confirm license terms
  and deployment obligations independently; documentation is not enforcement.
- Model weights, datasets, and audio may have terms separate from this
  repository's Apache-2.0 code license.
