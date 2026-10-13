# Project Vision and Scope

## Problem

Reading difficulties can have different causes. A learner who understands a
passage when listening but struggles to read it may need different support from
a learner who has difficulty understanding it in either mode.

Pagezy explores a read-versus-listen framing for this problem using passages
with questions and a simple diagnostic message. Its intended audience is
Nigerian primary-school learners, but the current repository is a prototype,
not a validated tool for real learner assessment.

## Current prototype

The repository includes:

- A Gradio reading demo with sample passages, a multiple-choice question,
  manually entered reading/listening scores, and a heuristic result.
- A separate Model Arena that compares hints from N-ATLAS with a Pagezy PEFT
  adapter, Qwen 2.5 3B, and Llama 3.2 3B.
- Scripts for passage generation, SQuAD-based data preparation, QLoRA
  fine-tuning, audio generation, and model evaluation.
- Recorded CSV evaluation outputs and project documentation.

The score sliders are not derived from quiz performance. The app has no
speech-input workflow, and its current UI does not play the repository's sample
audio files. Review the [system architecture](02_system_architecture.md) and
[safety limitations](06_safety_and_limitations.md) for implementation detail.

## Design choices

- **Keep the scope demonstrable.** The app shows a basic reading workflow and
  separates it from model comparison.
- **Keep generated content identifiable.** Model-generated passages are drafts
  until independently reviewed.
- **Report what the evaluation actually measures.** Current grounding and
  refusal signals are string-matching heuristics, not validated safety or
  factuality metrics.
- **Treat licensing as a deployment requirement.** N-ATLAS and other model
  licenses apply separately from this repository's license. The app does not
  enforce a user cap.

## Possible future work

Potential next steps include adding actual audio playback, deriving score inputs
from assessment interactions, having educators review and validate the
diagnostic, improving the evaluation methodology, and documenting a deployable
model configuration. Any use of children's speech or personal data would
require appropriate consent, privacy safeguards, and governance review.
