# 08 — Runbook: Environment & Deployment

## Development (Google Colab — the default)
1. New notebook → Runtime → Change runtime → T4 GPU.
2. `!pip install -r requirements.txt` (transformers, accelerate, bitsandbytes, gradio, evaluate, langchain, datasets).
3. Upload repo via `!git clone <your-repo>` or Colab's GitHub integration.
4. Set secrets via Colab's Secrets sidebar (HF token) — never in code, never in git.
5. Run harness: `!python harness/run_eval.py --models n-atlas qwen llama --n 10`.

## Demo Hosting (Hugging Face Spaces)
- Space type: Gradio SDK. Entry point: `app.py` at repo root.
- Free CPU tier is enough IF hints are cached (`results/cache/`); request GPU upgrade otherwise.
- Env vars (HF token) set in Space Settings → Repository secrets.
- Post-deploy smoke test (incognito): one passage → audio → answer → hint → diagnostic.

## Recovery Procedures
| Situation | Procedure |
|---|---|
| Colab session dies mid-eval | Results are append-only JSONL-safe: rerun with `--resume`; never overwrite `results/` |
| Judge prompt needs a fix | Bump version, re-run FULL eval, keep both result files, note version in each |
| Space exceeds 1,000 users | Never happens (no accounts/analytics); if a post goes viral, note it and reference the license cap — good problem |
| Token leaked | Revoke immediately, rotate in Colab Secrets + Space secrets, grep repo history, force-push cleaned history |
