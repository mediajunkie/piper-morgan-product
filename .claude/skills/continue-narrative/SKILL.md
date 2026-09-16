---
name: continue-narrative
description: Assess where the building-narrative blog sequence stands and decide the next move — draft the next beat or wait. Use BEFORE draft-blog-post whenever the task is to continue the building narrative: "what's the next beat", "continue the story", "review the logs since X and assess narrative beats", "where are we in the narrative", or any narrative-continuation/assessment work. Loads the conceptual model (linear-and-continuous, advance-the-front, narrative-vs-insight, wait-when-no-beat-has-formed) that templates don't carry, so the stance is right before any drafting. Hands off to draft-blog-post once a beat is confirmed.
scope: role-specific
version: 1.2
created: 2026-06-03
updated: 2026-09-16
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
- ⚠️ **Narratives run in chronological order, full stop — there is no sequencing question.** When presenting multiple candidate beats to PM, list them **in date order**, never ranked by story-readiness/strength/how-clean-the-arc-is. "Which of these is the best story" is an insight-piece question (insights *are* organized thematically, by pairing and breadth — that's a real, different discipline, not a lesser version of this one). For narratives the only question is "what's the next beat in order." **Repeated failure mode, 2026-09-01**: presented four real candidate beats (Aug 9, Aug 19-20, Aug 27-28, Aug 30-31) ranked by how story-ready each felt, and recommended drafting them in that ranked order — which silently jumped the Aug 30-31 candidate ahead of Aug 19-20 and Aug 27-28. This is the exact mistake `feedback_narrative_vs_insight_sequencing` (memory) already named as a repeat offense — reading the memory once had not been enough to prevent it recurring in the same session that loaded this very skill. That's *why* this line is here now instead of only in memory: **the skill you load at the moment of doing the work is a more reliable place for a standing correction than a memory that may or may not surface.** If a future instance of you is reading this while about to rank candidate beats — stop, sort by date instead.
- ⚠️ **A quiet-looking span is more often under-sampled than actually quiet.** 2026-09-01: an initial survey of 23 days came back with strong candidates everywhere except a 6-day window, which read as "nothing happened." A targeted re-check of just those 6 days found real material in 4 of them (including a genuine near-miss data-loss incident) — the first pass had just skimmed past it while covering the rest more thoroughly. If PM asks "did nothing happen, or did you miss it" — that is usually the right question. Before reporting a span as thin, make sure you gave it the same depth of read as the spans that came back rich, not just broader coverage.
- 🔴 **This happened AGAIN two weeks later, worse — which is why Step 2 now has a mandatory ledger, not just this caution.** 2026-09-15: the very survey that produced the caution above (Aug 9-31, "rich everywhere") turned out to have missed a second, larger span — Aug 10-18, arguably the densest 9-day run in the month, 5 of 9 days genuinely candidate-worthy. Caught the same way as the first time: PM asked "did nothing happen, or did we miss it." **The root cause both times was the survey's OUTPUT SHAPE, not effort or diligence**: "rich everywhere" is an aggregate mood, not a checkable claim — a day that doesn't surface a loud candidate on a first pass can go silently missing from that mood, with nothing to catch its absence. A prose caution survived reading it twice and still didn't prevent the second occurrence in the same session. See Step 2's ledger requirement below — this is a mechanical fix precisely because the prose one already failed once after being written.
- **A beat is a STORY, not a digest of its window** (§1.5, PM 2026-08-01). Wider spans are working and should continue — but they carry **no obligation to account for everything inside the leap.** Use an **A plot** (and optionally a B plot, plus something funny or strange); **not** a section per workstream. At assessment time the question is *"what is the story here?"*, never *"what happened here?"* If you can't name the A plot in one sentence, it isn't a beat yet. ⚠️ Measured: length is up 75% in five months and July's *mean* now exceeds the target ceiling — but **span does not predict length** (r = +0.10, n=21; a 2-day beat ran 2,093 words, a 9-day beat 1,680). So keeping the leaps and cutting the length are **not** in tension.
- When the next beat **hasn't taken shape** (work since the front hasn't resolved into a story, or it's unclear how to continue), **you wait.** Waiting is a correct, expected state — not a miss (Time Lord doctrine).

## The discipline (run this)

1. **Find the front.** In `editorial-calendar.csv`, identify the most recent work-day covered by a building-narrative *beat* (drafted OR queued OR published). Use the beat's **source-work-period** (notes / workDate), not pubDate. **Count beats only — not insights** (insights don't move the front).

2. **Read the work since the front — and produce a per-day ledger, not a mood.** Review logs for the days after the front. Omnibi (the efficient digest) live in `docs/omnibus-logs/{date}-omnibus-log.md`; fall back to per-day session logs (`dev/YYYY/MM/DD/`) for days without an omnibus yet. Read the source — don't reconstruct from memory (Chief-reads-logs discipline).

   ⚠️ **MANDATORY, not optional, as of v1.2**: give every single calendar day in the range from the front to today an explicit verdict — `candidate` (a real through-line is visible) or `thin` (checked, genuinely nothing beat-shaped). **A survey that returns only an aggregate summary ("rich everywhere," "quiet stretch") has proven nothing** — that exact shape is what let two real gaps (Aug 21-26 and Aug 10-18, both 2026-09-01/09-15, same session) go unnoticed until PM asked directly. Record the ledger **in the session log**, in this exact machine-checkable form:

   ```
   <!-- NARRATIVE-SURVEY-LEDGER: START=YYYY-MM-DD END=YYYY-MM-DD -->
   | date | verdict | note |
   |---|---|---|
   | YYYY-MM-DD | candidate | one-line through-line |
   | YYYY-MM-DD | thin | why — routine/no arc/already an insight, etc. |
   <!-- /NARRATIVE-SURVEY-LEDGER -->
   ```

   If a survey is wide enough to delegate (subagent dispatch), require the ledger in this exact format as part of what the subagent returns, then transcribe it into your own session log verbatim — the ledger lives in the log either way, not only in the subagent's transcript.

   **Before doing anything with the results, verify completeness mechanically — don't eyeball it:**
   ```bash
   python3 scripts/check-narrative-survey-coverage.py --start <front+1> --end <today> dev/YYYY/MM/DD/your-session-log.md
   ```
   Exit 0 = every day has a verdict, proceed. Exit 1 = the survey is incomplete — go back and read the missing day(s) before presenting anything to PM, full stop. This is not a formality: a span this script hasn't cleared is exactly the state both real misses were in when they got presented as "rich everywhere" anyway.

3. **Assess whether a next beat has taken shape.** Working from the ledger's `candidate` rows: did the post-front work resolve into a story beat — a clear arc, a tension, a turn? Is it clear how the sequence continues?
   - **Yes** → it's a beat. If several beats are forming, treat them as a slate (draft long, then tighten — method doc §1.4). Add the calendar row **at creation** (orphan-prevention). Hand off to `draft-blog-post`.
   - **No / ambiguous** → **wait.** Say so plainly to PM, and say what you'd want to see before it's a beat. Do not force a beat to fill a slot.

4. **Never backfill — unless PM explicitly overrides.** If the span between the front and now was skipped at the beat level (e.g., mined only for insights, or missed by a prior survey), do NOT retroactively fill it unless PM explicitly decides a specific beat is worth telling. Advance from the front. When PM *does* authorize a backfill (real precedent: 2026-09-15, Aug 10-18), it's still presented and sequenced exactly like any other slate — chronological order, ledger-verified coverage — it just publishes after the already-scheduled queue rather than displacing it.

5. **Bring candidates to PM for discussion** when the assessment is exploratory ("assess potential beats") rather than a clean single next-beat. Present candidate beats with through-lines + source-days, **in ledger date order**, and don't withhold the `thin` days either — showing what was checked-and-empty is part of what makes the survey trustworthy. Let PM steer slate shape. This mirrors how slates are actually built (draft-long → PM push → tighten).

## Handoff

Once a beat (or slate) is confirmed: create the calendar row(s) via `update-calendar`, then `draft-blog-post` for each beat. If the verdict is "wait," record that in the cycle log / standing-items so the next session knows the front and why we're holding.

---

*v1.0 — encodes §5 of `building-narrative-method.md`. The method doc is the source of truth for the model; update the doc when the model evolves, and bump this skill if the discipline steps change.*

*v1.1 — 2026-09-01. Added two ⚠️ lines to "the model in one breath": (1) narratives sequence strictly chronologically, never ranked by story quality — a repeat of a mistake `feedback_narrative_vs_insight_sequencing` had already named once, which is itself the reason it's recorded here now rather than only in memory (PM: "memories often fail to make a difference... their essence needs to go somewhere it will be seen at the right time"); (2) a span that reads as quiet is more often under-sampled than actually empty — verified same day when a targeted re-check of a "nothing happened" 6-day window found real material in 4 of 6 days.*

*v1.2 — 2026-09-16. The v1.1 caution wasn't enough: the same Sep 1 survey it was written about had a second, larger miss (Aug 10-18, 5 of 9 days) sitting undetected until PM asked again on 09-15. Root cause: the survey's output *shape* — an aggregate mood ("rich everywhere") is unauditable, so a day that didn't surface a candidate on the first pass could go silently missing with nothing to check it against. Fix, PM-approved 2026-09-16: Step 2 now REQUIRES an explicit per-calendar-day ledger (`candidate`/`thin`, machine-parseable, embedded in the session log) and a mechanical completeness check (`scripts/check-narrative-survey-coverage.py`) before any slate goes to PM — replacing "remember to look closer" with "the gap can't be presented without being visible first." Also formalized PM's 09-16 backfill authorization into Step 4 (backfill only on explicit PM override, still ledger-verified and chronologically sequenced) and Step 5 (present `thin` verdicts alongside `candidate` ones, not just the wins).*
