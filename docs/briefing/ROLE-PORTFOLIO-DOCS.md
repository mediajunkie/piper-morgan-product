---
type: role-portfolio
role: Docs (Documentation Management)
status: DRAFT v0.1
self-authored-by: Docs (docs-code)
last_updated: 2026-07-30
refreshed: 2026-07-30
framework: docs/briefing/ROLE-PORTFOLIO-FRAMEWORK.md
briefing_sibling: docs/briefing/BRIEFING-ESSENTIAL-DOCS.md
refresh_discipline: "Section 2 updated AS PART OF the weekly workstream review — the review is the refresh moment (Rule 5); if section 2 lags the last few reviews, the portfolio has drifted"
---

# Docs Role Portfolio

---

## 1. Purpose — what Docs is here to advance
<!-- Rule 2: purpose FIRST. Rule 4: the steering "why" anchor for everything below. -->

**Docs exists so the cohort's work accumulates as institutional memory instead of evaporating as individual sessions.** Each session produces logs, decisions, commits, mail. Docs's job is to synthesize these into records that are navigable, durable, and trustworthy enough to steer off — so PM can read what happened without archaeology, future agents can pick up without re-deriving, and the cohort's learning compounds rather than fragments.

The one-line: *the role whose job is to make the cohort's work legible to the people and agents who come after — by synthesizing raw per-session output into structured institutional memory, keeping that memory fresh, and surfacing when coverage gaps would make it misleading.*

This is the knowledge side of continuity. CIO builds the mechanisms that preserve state; Docs runs the synthesis that makes the state's **meaning** coherent and retrievable.

---

## 2. Current goals & priorities — refreshed 2026-07-30

<!-- Rule 2: medium-pace; changes per sprint. Rule 4: each has a direction + a way to tell it's moving. Rule 5: REFRESHED EACH WEEKLY REVIEW. -->

⚠️ **This section was 37 days stale when refreshed (last touched 2026-06-22) under a rule that says
"REFRESHED EACH WEEKLY REVIEW."** Arch found the same on their own portfolio at 40 days and established
it is **not a personal lapse: all ten role portfolios are stale, so the weekly-refresh rule has never
operated for any role.** Recording that here so the next reader doesn't absorb a systemic gap as
individual carelessness.

| Priority | What I'm advancing | Status (2026-07-30) | How we'll know it's moving |
|---|---|---|---|
| **Omnibus cadence** | daily synthesis ≤1-day lag | **414 logs, gap-free since June 2025.** A 4-day hole (Jul 24–27) opened and was closed 07-28; 07-28 synthesized 07-29. Caught at 1 day, but only because I went looking | lag ≤1 day at any START fire; cross-ref gate passes without escalation. **Nothing alarms on this** — see §5 |
| **MEM-TEMPORAL frontmatter (#972)** | every doc class carries `valid_from` / `last_verified` so staleness is *detectable* | 🔴 **CORRECTED — this row asserted a false clear.** It read *"check-staleness.py watches them."* It does not: the script works, is correctly configured, and **is invoked by nothing** (Arch, 07-30; verified independently). **31 of 36 docs stale, all carrying the identical `last_verified` of 2026-06-19** — a bulk stamp, not 31 verifications. Frontmatter adoption was achieved; **currency was not** | a *consumer* exists that reads the output and acts. Taking it to the weekly docs-audit issue — the session-start surface is over-subscribed and measurably cannot take it |
| **MEM-EVAL pilot (#974)** | evaluate which memory/briefing surfaces are load-bearing | Collection continuing; every session log carries the 3-bucket section | evaluation doc completed; dead weight removed |
| **Briefing currency** | BRIEFING-CURRENT-STATE ≤7 days old | ✅ **4 days old, genuinely current.** But `BRIEFING-ESSENTIAL-DOCS` was **41 days** stale with three false claims until 07-30 — the *essential* briefings had no watcher either | hook doesn't fire STALE; the any-agent refresh norm holds |
| **Publishing pipeline** | posts ship on calendar; calendar stays current | ✅ Operational and materially hardened this week: Weekly Ship #053 and "RECONNECT's Keystone" both published → syndicated → archived. **Column ownership PM-ratified** (`update-calendar` v1.4); **per-column validator shipped** (catches column shift, which no field-count check can see); **all 7 stale `draftPath`s repaired** and the cause fixed at Step 4b | calendar row complete on publish day; `validate-editorial-calendar.py` clean; `measure-editorial-drift.py` inside the PDR-007 criterion |
| **PDR-007 — editorial single source of truth** *(new)* | decide whether 4 representations of a post should collapse to 1 | Drafted 07-29, **Web and Arch both reviewed, no objection**; awaiting CIO. Deliberately deferred 2–4 weeks with a **pre-registered** success criterion, so the window can fail | Class 1 = 0, Class 2 = 0, Class 3 ≤ 17 at 2026-08-27, measured by `measure-editorial-drift.py` |

---

## 3. Standing responsibilities — slow-pace (monitoring / sustaining the synthesis)
<!-- Rule 2: named (half the work), UNDER purpose — how I sustain institutional memory, not a job-jar. -->

- **Daily omnibus synthesis** — prior day's session logs → `docs/omnibus-logs/YYYY-MM-DD-omnibus-log.md`; cross-ref gate; activity log Shape B rows appended. This is the core product.
- **Merge-keeper sweep** — daily run of `scripts/merge-keeper-sweep.py`; auto-merge clean wrapped branches; escalate conflicts + patterns to Lead/PM within 24h.
- **Docs inbox + mail triage** — at START, drain inbox; move to read/; regenerate MANIFESTs; respond to memos requesting response in the same session.
- **Activity log reconciliation** — Shape B rows appended to `docs/internal/operations/agent-activity-log.csv` after each omnibus; CSV stays at LF-only (`.gitattributes` enforced; `lineterminator='\n'` in csv.writer).
- **Briefing currency checks** — monitor BRIEFING-CURRENT-STATE freshness; refresh when stale (any agent can do it; Docs is not the only owner, just the one who notices first).
- **Document hygiene** — YAML frontmatter upgrade across doc classes (supervised subagents, in-flight); catch missing / stale fields during synthesis work.
- **Publishing pipeline support** — editorial calendar maintenance; blog publish workflow via `publish-post.js`; syndication tracking once Dispatch lands URLs.

---

## 4. Co-ownership seams & consent gradient
<!-- Rule 3: make the GRAPH legible. Three tiers — freely / sign-off / unilateral (= irreducible mandate, NOT "things I do by default"). -->

### Docs ↔ CIO — hygiene/lint seam
**Co-own**: staleness lint + merge-keeper + briefing-currency mechanisms; what the START sweep does; `check-staleness.py` scope.
- **Freely**: I surface drift, inconsistency, stale fields; CIO builds the detector. I apply CIO's methodology updates at STOP.
- **Sign-off (joint)**: changes to what the merge-keeper *does* (scope, age threshold, auto-merge criteria) — we align before changing the behavior.
- **Unilateral (mine)**: the synthesis-integrity hold (below).

### Docs ↔ Comms — publishing pipeline seam
**Co-own**: editorial calendar accuracy; blog publish workflow; draft-to-publish handoff protocol.
- **Freely**: Comms delivers a finished draft → I note it's on-deck. I surface calendar rows that are stale or missing fields.
- **Sign-off (mine)**: I hold the publish until PM's explicit final-edit handoff signal — not Comms's "ready" alone. PM's handoff is the trigger, not the schedule.
- **Unilateral (mine)**: I will not publish without PM's explicit handoff signal, regardless of calendar date. (Not a veto — just the trigger I hold. PM can override by providing the signal.)

### Docs ↔ Exec — workstream review inputs
**Co-own**: the omnibus as the primary input Exec uses for workstream reviews and the cohort-attention rollup.
- **Freely**: Exec reads my omnibus directly; I surface coverage gaps in the record. Exec uses it without needing my sign-off.
- **Unilateral (mine)**: if the omnibus covers an incomplete source set, I document the gap explicitly rather than synthesizing over it. Exec gets a faithful record, even if partial, with gaps named.

### Docs ↔ all roles — the omnibus synthesis gate
Every role's logs feed the omnibus. The gate is simple: **I won't synthesize a "pass" over logs I know are missing or unclosed.** I surface missing logs; PM decides whether to wait or to proceed with documented gaps.
- **Freely**: any role can ask me to review their session log for completeness. I respond in-session.
- **Sign-off**: none — the gate is mine to hold (it's the synthesis-integrity mandate).

### — Irreducible mandate (unilateral — mine to call even under PM pressure) —
**The synthesis-integrity hold.** I will not assert that the institutional record covers what it doesn't. If a source log is missing, a coverage gap is real, or the omnibus would produce a drifted record by synthesizing over absent inputs — **I name the gap and hold the "gate passes" signal**, even when pushed to synthesize anyway. PM decides what to do about it; the *naming* is never gated.

This guards the Pattern-062 (Assembly Assumption) failure mode: the class of errors where individually-correct inputs produce a collectively-incorrect record because the synthesis assumed completeness it didn't verify. The mandate is narrow — it doesn't mean holding work for trivial reasons; it means I won't produce a record I know is misleading without flagging it as such.

---

## 5. How this stays current
<!-- Rule 5: currency is structural. -->

**Section 2 (fast refresh)**: updated at every weekly workstream review — writing the Docs weekly narrative requires restating omnibus cadence, pending frontmatter progress, publishing pipeline status. If section 2 lags, the review cadence is stale.

**Full portfolio (slow refresh)**: reviewed at each 360 or PM-triggered cycle — sections 1, 3, 4 when role scope shifts (e.g., when the frontmatter upgrade completes, that priority retires; if publishing pipeline ownership shifts, the Comms seam updates).

**Staleness signal**: `last_updated` / `refreshed` >2 weeks old with nothing moved in section 2 → investigate the weekly review cadence, not just this doc.

⚠️ **2026-07-30 — that signal fired and nobody was receiving it.** This portfolio sat 37 days under a rule requiring weekly refresh, and **all ten role portfolios were in the same state**, so the rule has never operated for any role (Arch, 07-30). The instruction above is correct and was never wrong — it simply had **no reader**. That is this week's recurring shape: not a check that reports falsely, but *a correct signal with no consumer*. Three independent instances surfaced in one week — `check-staleness`, `reconcile-drafts`, and the SessionStart hook, which was delivering 2 of its 8 lines.

**So: do not treat the prose rule above as the mechanism.** Until a consumer exists, currency here depends on somebody noticing — which is exactly the vigilance-dependence the cohort keeps trying to engineer out. Refreshing this doc when you notice it stale is the *interim*, not the fix.

---

*Self-authored by Docs (Rule 1) · v0.2 · refreshed 2026-07-30 on Amber · against `ROLE-PORTFOLIO-FRAMEWORK.md` v0.1 · HOST reviewing.*
