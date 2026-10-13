# 06 — Safety & Limitations (Ship This Publicly — It Builds Trust)

## Known Limitations (The Honest List)
1. **No child-speech ASR in V1.** N-ATLAS ASR lacks comprehensive Nigerian
   children's speech data and degrades in noise. Therefore V1 uses audio
   *playback* (TTS / pre-recorded MP3) and human-entered answers.
2. **Diagnostic is a screening signal, not a clinical diagnosis.** Output language
   to parents: "Your child shows a pattern consistent with a decoding gap — we
   recommend a teacher assessment." Never "Your child has dyslexia."
3. **LLM hints can be wrong.** Every hint is generated live; the harness measures
   hint quality (rubric) but no guarantee attaches to a single hint.
4. **1,000-user cap** on the free N-ATLAS tier by design.
5. **20–60 passages** is a demo corpus, not curricular coverage.

## Safety Controls Implemented
- Safety dimension in rubric with **auto-fail** and a `results/safety_flags.md` log (see `docs/04`).
- Input is multiple-choice only in V1 — no free-text child input reaches the LLM.
- No personal data collected (see `docs/05`).
- Judge-prompt frozen; human spot-check on ≥20% of eval outputs.

## Phase 2 Roadmap (the part judges remember)
1. Crowdsource child speech via school partnerships (with consent frameworks) —
   this competition's visibility is the recruitment channel.
2. Fine-tune N-ATLAS ASR on that corpus → closes a **documented national gap**.
3. Expand corpus to full primary curriculum; add teacher dashboard.
4. Governance: child-data consent, model cards, external red-team of hint safety.
