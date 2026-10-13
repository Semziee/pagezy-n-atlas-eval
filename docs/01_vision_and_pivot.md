# 01 — Vision & The Strategic Pivot

## The Problem (60 seconds)
Millions of Nigerian primary students fall behind in reading. Teachers cannot
diagnose *why* a child struggles: is it **decoding** (can't turn letters into
sounds) or **comprehension** (can read the words but doesn't understand)?
The two need completely different interventions. Pagezy distinguishes them with
one elegant trick: **compare performance on silent reading vs. audio-assisted listening.**

- Reads poorly, listens well → **Decoding Gap** → needs phonics intervention.
- Reads and listens equally poorly → **Comprehension Gap** → needs vocabulary/background-knowledge work.

## The Two Constraints → The Two Pivots (MEMORIZE THIS TABLE)

| N-ATLAS limitation | Our pivot | The pitch line |
|---|---|---|
| No children's speech data; accuracy degrades in noise | V1 uses **audio playback only** (TTS / pre-recorded MP3). No child ASR in V1. | "We explicitly defer student voice-input to Phase 2, where we will crowdsource Nigerian children's speech through this competition to fine-tune N-ATLAS ASR — closing a documented gap in the national stack." |
| Free tier: max 1,000 active users + must display "Powered by Awarri" | Badge in UI footer + explicit license compliance in README. | "Our prototype is architected for full N-ATLAS Research License compliance: capped users, non-commercial, full attribution." |

Judges reward teams that *read the docs*. Constraints quoted back as architecture = credibility.

## What V1 Is / Is Not

**IS:** one repo, two entry points (product demo + evaluation harness), 40–60
human-verified passages (20 done by Day 1), a 1–5 scoring rubric, a leaderboard,
compliance-first posture.

**IS NOT:** a deployed product for real schools, child voice input, a fine-tuned
model, multi-subject coverage. Do not let scope creep past this line before Oct 12.

## Why This Wins (Evaluation Story)
1. **Social impact** — real diagnostic gap, Nigerian curriculum alignment.
2. **Engineering rigor** — reproducible benchmark harness, not vibes.
3. **Ecosystem contribution** — Phase 2 ASR roadmap benefits the national AI stack.
4. **Compliance maturity** — licensing treated as architecture, not afterthought.
