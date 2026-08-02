---
name: continue-narrative
description: Assess where the building-narrative blog sequence stands and decide the next move — draft the next beat or wait. Use BEFORE draft-blog-post whenever the task is to continue the building narrative: "what's the next beat", "continue the story", "review the logs since X and assess narrative beats", "where are we in the narrative", or any narrative-continuation/assessment work. Loads the conceptual model (linear-and-continuous, advance-the-front, narrative-vs-insight, wait-when-no-beat-has-formed) that templates don't carry, so the stance is right before any drafting. Hands off to draft-blog-post once a beat is confirmed.
scope: role-specific
version: 1.0
created: 2026-06-03
---

# continue-narrative

The upstream step before drafting: figure out where the building narrative is and whether the next beat has taken shape. This skill exists because the *stance* of the narrative as a serial practice kept getting reconstructed wrong each session (treating uncovered days as a "gap to fill" instead of a story to advance). It loads the model so that doesn't happen.

**Read first**: `docs/internal/planning/comms/building-narrative-method.md` — the canonical model. This skill is the §5 continuation discipline; the doc is the full model behind it. If anything here is ambiguous, the doc governs.

## When to Use

- PM asks "what's the next narrative beat", "continue the story", "where are we in the building narrative"
- "Review the logs since [date] and assess potential narrative beats"
- Picking up narrative-slate planning or deciding whether to publish the next beat
- Any time you're about to advance the building narrative — run this BEFORE `draft-blog-post`

NOT for: insight pieces (time-decoupled — different logic), Weekly Ships (Exec-owned), or drafting a beat that's already confirmed (go straight to `draft-blog-post`).

## The model in one breath (full version in the method doc §1)

- The building narrative is **LINEAR and CONTINUOUS**: it has a *front* (the latest work-day a beat covers), not a coverage-map with holes. You **advance the front; you never backfill gaps.**
- Narratives are **chronological beats**; **insights are time-decoupled.** Mining a date range for insights does **NOT** advance the narrative front. Count beats, not insights.
- **A beat is a STORY, not a digest of its window** (§1.5, PM 2026-08-01). Wider spans are working and should continue — but they carry **no obligation to account for everything inside the leap.** Use an **A plot** (and optionally a B plot, plus something funny or strange); **not** a section per workstream. At assessment time the question is *"what is the story here?"*, never *"what happened here?"* If you can't name the A plot in one sentence, it isn't a beat yet. ⚠️ Measured: length is up 75% in five months and July's *mean* now exceeds the target ceiling — but **span does not predict length** (r = +0.10, n=21; a 2-day beat ran 2,093 words, a 9-day beat 1,680). So keeping the leaps and cutting the length are **not** in tension.
- When the next beat **hasn't taken shape** (work since the front hasn't resolved into a story, or it's unclear how to continue), **you wait.** Waiting is a correct, expected state — not a miss (Time Lord doctrine).

## The discipline (run this)

1. **Find the front.** In `editorial-calendar.csv`, identify the most recent work-day covered by a building-narrative *beat* (drafted OR queued OR published). Use the beat's **source-work-period** (notes / workDate), not pubDate. **Count beats only — not insights** (insights don't move the front).

2. **Read the work since the front.** Review logs for the days after the front. Omnibi (the efficient digest) live in `docs/omnibus-logs/{date}-omnibus-log.md`; fall back to per-day session logs (`dev/YYYY/MM/DD/`) for days without an omnibus yet. Read the source — don't reconstruct from memory (Chief-reads-logs discipline).

3. **Assess whether a next beat has taken shape.** Did the post-front work resolve into a story beat — a clear arc, a tension, a turn? Is it clear how the sequence continues?
   - **Yes** → it's a beat. If several beats are forming, treat them as a slate (draft long, then tighten — method doc §1.4). Add the calendar row **at creation** (orphan-prevention). Hand off to `draft-blog-post`.
   - **No / ambiguous** → **wait.** Say so plainly to PM, and say what you'd want to see before it's a beat. Do not force a beat to fill a slot.

4. **Never backfill.** If the span between the front and now was skipped at the beat level (e.g., mined only for insights), do NOT retroactively fill it unless PM explicitly decides a specific beat is worth telling. Advance from the front.

5. **Bring candidates to PM for discussion** when the assessment is exploratory ("assess potential beats") rather than a clean single next-beat. Present candidate beats with through-lines + source-days; let PM steer slate shape. This mirrors how slates are actually built (draft-long → PM push → tighten).

## Handoff

Once a beat (or slate) is confirmed: create the calendar row(s) via `update-calendar`, then `draft-blog-post` for each beat. If the verdict is "wait," record that in the cycle log / standing-items so the next session knows the front and why we're holding.

---

*v1.0 — encodes §5 of `building-narrative-method.md`. The method doc is the source of truth for the model; update the doc when the model evolves, and bump this skill if the discipline steps change.*
