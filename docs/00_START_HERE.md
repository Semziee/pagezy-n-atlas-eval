# 🚨 START HERE — Read This First (Even If You Remember Nothing)

> **Purpose of this file:** If you have total memory loss, this document rebuilds
> your entire context in 15 minutes and tells you exactly what to do next.
> Do not skip it. Do not reorganize it. It is the root of the tree.

---

## 1. Who You Are (Reconstructed)

You are a builder/engineer entering the **N-ATLAS × Awarri competition** (submissions
close Oct 12, 2026). You are building **Pagezy**: a reading-diagnostic tool for
Nigerian primary-school students, powered by the N-ATLAS LLM. Your competitive
angle is engineering maturity: you are not just *using* the national AI stack —
you are *measuring and documenting* it, and your Phase 2 plan fixes a documented
gap in it (child-speech ASR).

## 2. The One-Paragraph Pitch (Say This Verbatim If Asked)

> "Pagezy V1 identifies whether a struggling student has a **decoding gap** or a
> **comprehension gap** using a read-vs-listen diagnostic. It runs on N-ATLAS LLM
> for curriculum-aligned question generation, with human-recorded/TTS audio, and
> ships with a reproducible evaluation harness benchmarking N-ATLAS against
> Qwen2.5-3B and Llama-3.2-3B. We defer child voice-input to Phase 2, where this
> competition's reach lets us crowdsource Nigerian children's speech to fine-tune
> N-ATLAS ASR — closing a documented gap in the national AI stack."

## 3. Golden Rules (Never Violate These)

1. **Depth beats breadth.** We ship a vertical slice, not a product.
2. **Every artifact has an owner file and a consumer.** Nothing is "just there."
3. **If it isn't written down in this repo, it does not exist.**
4. **Never fabricate results.** A failed eval honestly logged beats a fake one.
5. **The moat is methodology + data flywheel, not code.** Code is open; method is proprietary (see `docs/07_ip_and_moat.md`).
6. **Compliance is a feature.** The Awarri badge, the 1,000-user cap, the attribution — all visible, all deliberate.

## 4. The 15-Minute Restart Ritual

Read these **in this exact order**, checking items off as you go:

- [ ] `docs/00_START_HERE.md` (this file) — context rebuilt
- [ ] `docs/01_vision_and_pivot.md` — why we exist and why our constraints are strengths
- [ ] `docs/02_system_architecture.md` — how every part connects (the map)
- [ ] `docs/CHECKPOINTS.md` — which gate are we at? What is the *next unblocked task*?
- [ ] Today's day plan in `day_plans/` — do only today's box, nothing else

Then run the sanity script: `python scripts/where_am_i.py`
It prints current day, which checklists are incomplete, and the single next action.

## 5. Hard Deadlines

| Date | Deliverable |
|---|---|
| Oct 7 (Day 1) | Repo created, N-ATLAS access confirmed, 20 human-verified passages |
| Oct 8 (Day 2) | Harness v1 + diagnostic logic working end-to-end on 3 passages |
| Oct 9 (Day 3) | Gradio two-tab UI functional |
| Oct 10 (Day 4) | Compliance, licensing, safety docs, code polish |
| Oct 11 (Day 5) | 3-minute demo video recorded |
| Oct 12 (Day 6) | Deployed to HF Spaces + submission |

## 6. If Something Is On Fire

1. Check `day_plans/day_XX_*.md` → "Common Failures & Fixes" section.
2. Check `results/` for the last logged result — never redo work already logged.
3. Only then ask for help, quoting the exact checkpoint ID (e.g., `CP-2.3`).
