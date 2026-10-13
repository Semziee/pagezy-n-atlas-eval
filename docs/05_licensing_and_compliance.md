# 05 — Licensing and Compliance Notes

This document records issues to verify before deployment. It is not legal
advice or evidence that a hosted deployment is compliant.

## Model and service terms

| Area | Current project behavior | Before deployment |
|---|---|---|
| N-ATLAS / Awarri terms | The app displays an attribution and license notice in its footer. The app does **not** enforce an active-user cap. | Read the current N-ATLAS license and confirm that the intended use, hosting provider, audience, and scale are permitted. Do not describe a user cap as implemented. |
| Other model terms | The Model Arena loads Qwen, Llama, and a PEFT adapter in addition to N-ATLAS. | Review and follow each model's access, use, and redistribution requirements. Gated model access must be granted to the account used for downloads. |
| Repository license | `LICENSE` applies to this repository's code and identifies separate N-ATLAS terms. | Check individual dataset and audio provenance and license terms before redistribution; a repository license does not override third-party terms. |

## Attribution

The app footer displays: **Powered by Awarri · N-ATLAS Research License ·
≤1,000 users · Non-commercial**. This text is attribution, not a technical
access control or a substitute for checking the current license.

## Data, privacy, and learner safety

- The app does not provide accounts, child-speech recognition, or an audio
  upload workflow. Do not submit personal or sensitive learner information.
- The repository includes records with different `human_verified` values.
  Inspect that field and the source information for each record; do not describe
  the entire passage collection as human-verified.
- Review the provenance and terms for passages, SQuAD-derived data, model
  outputs, and generated audio before reuse or redistribution.
- The diagnostic is a simple demonstration based on manually entered scores.
  It is not a clinical diagnosis or a validated educational assessment.

## Deployment checklist

- [ ] Verify current terms for N-ATLAS, the adapter, Qwen, Llama, all datasets,
  and audio assets.
- [ ] Confirm the intended deployment is permitted, including public access and
  expected user volume. The app itself has no active-user-cap enforcement.
- [ ] Store any model access token as a Hugging Face Space secret; never commit
  it or paste it into a notebook.
- [ ] Describe the product as a prototype and the diagnosis as an unvalidated
  heuristic.
- [ ] Avoid collecting personal or sensitive data and review hosting/logging
  behavior separately.
