# Prompt examples

This directory contains the public prompt examples used or considered by the
project:

- `passage_generation.txt` — instructions for generating draft passages.
- `tutor_hint.txt` — a hint-generation prompt.
- `judge_prompt_v1.txt` — an evaluation/judge prompt example.

These files are examples, not evidence that every prompt is wired into the
current app or evaluation script. In particular, the app builds its own hint
prompt in `app/app.py`, and `harness/eval_finetuned.py` uses a separate
explanation prompt. See the [system architecture](../docs/02_system_architecture.md)
for the current execution paths.
