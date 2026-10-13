# 07 — IP Strategy: Sellable at $1M, Copy-Resistant at $0

## The Core Insight
The repo is **not** the asset. Anyone can clone a Gradio app in a weekend. The
asset is three things copying cannot reproduce:

1. **The operating manual** (this kit) — process as IP. Companies buy the *system*,
   not the code.
2. **The verified data flywheel** — human-verified passages, and later the
   child-speech corpus. Data with provenance compounds; clones start at zero.
3. **The evaluative judgment** — the frozen rubric, judge prompt, and the
   discipline of logged, honest results. Reputation compounds too.

## The Three-Layer Fence

| Layer | What's in it | License / Visibility |
|---|---|---|
| **L1 — Open (the honey)** | Repo structure, day plans, harness code, Gradio app, sample data (20 passages), rubric *concept*, all docs except this one | Public, Apache-2.0. Optimized to be forked, starred, and quoted. |
| **L2 — Visible but owned** | Full methodology docs, architecture rationale, demo video, pitch narrative | Public but © you; registered as your work. Hard to copy *well* because it requires taste. |
| **L3 — Closed (the moat)** | `prompts/` (final system prompts), judge-prompt weights, `data/passages_full.jsonl` (40–60 verified), scoring thresholds after tuning, deployment configs/secrets, Phase-2 corpus plan | **Private repo `pagezy-core`.** Never committed here. |

## Mechanics of the Fence (do these on Day 4)
- [ ] Private repo `pagezy-core` created; L3 items live there. Public repo contains only a `prompts/README.md` saying "prompts maintained privately; contact for licensing."
- [ ] `.gitignore` blocks: `*.env`, `secrets/`, `data/passages_full.jsonl`, `prompts/final/`, `results/private/`.
- [ ] `scripts/where_am_i.py` verifies the fence: fails CI-style if any L3 path is tracked by git.
- [ ] Watermark: every passage contains one subtle "canary" sentence pattern unique to your corpus (documented only in `pagezy-core`) — proves copying later.
- [ ] Copyright header in every source file: "(c) 2026 <Your Name>. Apache-2.0 for code; methodology proprietary."

## Why This Still Wins the Competition
Judges see a fully working, documented, compliant system (L1+L2). Everything
required to *run and evaluate* the demo is public. What's private is the
*production* layer — exactly the boundary any acquirer expects. A company can
clone the demo; they cannot clone 60 verified passages, the tuning know-how, or
the credibility trail in `results/`.

## The Sale Narrative (for later, when this becomes a product)
"We're not selling code. We're selling a validated diagnostic methodology, a
compliance-first deployment pattern for national AI stacks, and a data flywheel
that improves with every school onboarded. The demo is the receipt; the manual is
the product."
