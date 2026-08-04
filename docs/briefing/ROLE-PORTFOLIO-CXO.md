---
type: role-portfolio
role: CXO (Chief Experience Officer)
status: v0.1
self-authored-by: CXO
last_updated: 2026-08-04
refreshed: 2026-08-04 (section 2 + §5 mechanism correction; sections 1/3/4 re-read and left as accurate)
framework: docs/briefing/ROLE-PORTFOLIO-FRAMEWORK.md
briefing_sibling: docs/briefing/BRIEFING-ESSENTIAL-CXO.md
refresh_discipline: "sections 2 and 4 on each workstream review; sections 1 and 3 on role-scope drift — NOW CHECKED, see refresh_trigger_glob and §5"
refresh_trigger_glob: "mailboxes/cxo/sent/workstream-*-cxo-*.md"
---

# CXO Role Portfolio

---

## 1. Purpose — what CXO is here to advance
<!-- Rule 2: purpose first. Rule 4: the "why" anchor that makes the rest steerable. -->

**CXO exists to make working with Piper Morgan feel like working with a thoughtful colleague.**

That's the full statement. Not "to design good interfaces" (too narrow), not "to represent the user" (too passive), not "to govern UX" (too compliance-flavored). The active thing: advance the proposition that AI assistance can be **collegial** — present, honest, calibrated, non-transactional — and hold every user-facing surface to that standard.

The Colleague Test is the practical operationalization: *would this feel like a reasonable thing a thoughtful colleague would say or do?* It's not a checklist. It's a posture that generates answers to specific design questions. The floor beneath it: honesty over false confidence, earned trust over locked trust, assistance over interrogation.

Two things flow from this:
1. **Design calls are not aesthetic preferences** — they're positions on what the collegial experience requires. When CXO names a concern, it's about the felt experience of using Piper, not personal taste.
2. **The product has to be worth having** — a technically correct product that feels mechanical fails the mandate. CXO is the voice that keeps asking "what does this feel like to use?" and holding the answer to the collegial standard.

---

## 2. Current goals & priorities — August 2026 (pre-beta, target 2026-08-08)
<!-- Rule 2: medium-pace, per sprint. Rule 4: each has direction + status + forward indicator. Rule 5: refreshed each workstream review — see the correction in §5; this refresh was NOT triggered by a review, it was triggered by reading §5. -->

| Priority | What I'm advancing | Status (Aug 4) | How we'll know it's moving |
|---|---|---|---|
| **First contact on the plugin surface** | The user's own work appears in the first exchange, unprompted — the fix all four Jake lenses converged on, re-expressed for a surface we don't render | Spec at v0.4 (`dev/active/design-spec-first-contact-plugin-surface-2026-07-31.md`); PDR-006 ratified 07-31; **pre-registered read says only 1 of 4 funnel outcomes makes this the right bet** | Funnel counts land; the first-contact gate criterion is added and fails today |
| **Recomposition rubric branch (#1463)** | A Layer-B rubric for tool output a client LLM recomposes — four dimensions: sufficiency · preservation · prominence · fidelity | Branch OPEN; Probe A closed — **refusals require a failure-shaped payload** (6/6); ⚠️ **deployed-host retest is a GATE before booking the capability** | Retest against a live `mcp.pipermorgan.ai` passes |
| **Honesty of user-facing claims** | The interface must not manufacture a belief | **#1482 shipped** — five false "cannot be undone" retracted, credential delete gains the true claim; latent `dialog.js` defaults proposed | Zero false permanence claims on any reachable surface; defaults carry no consequence claim |
| **#1466 Slack link flow** | Link-flow UX + copy; the decline is the load-bearing string | Spec v0.2 — corrected after Arch caught my shortcut removing a proof-of-control | Lead ships; decline carries a path, not an instruction |
| **#1386 beta-gate experience criteria** | The gate must be able to both pass and fail for what users actually report | Criterion-2 sign-off **withheld** (keyless suite skips and reports green); first-contact criterion proposed | A keyed run exists → same-day sign-off, as committed |
| **#1174 proactive presence** | Discovery only — the delivery capability is unscheduled | Re-scoped 08-01; carries the prior question *what does "earned" mean when the denominator doesn't exist on our primary surface?* | Discovery runs with HOST; nothing built pre-beta |
| **Floor-quality + ethics-decline watch (#950 / #992)** | Standing | ⚠️ **Unattested** — no active watch performed since arriving on Amber | Read scorer outputs directly, not memos summarizing them |

**Deliberately not on this list**: the D2 design-system portfolio (#1286/#1290/#1284/#1269), which has not moved in three Ship windows. **Flagged to PM in Ship #054 §6 as a decision to make rather than a drift to continue** — it is still a drift.

### Beta milestone (June 2026, retained for the record)
- **D1 closed**: #1236 (Radar consolidation) + #1280 (dark rail shell) both passed PM beta UAT — "total win for beta" (June 19). Places→RadarEntity as `work_item` live; insights-OUT; clean chat center; dark rail conversation-first.

## 3. Standing responsibilities (slow-pace — sustaining the collegial experience)
<!-- Rule 2: named under purpose — how I sustain the thing I'm advancing, not the thing itself. -->

- **Design spec authorship**: the binding written record of what gets built. Every significant surface has a spec before Lead builds; specs live in `dev/active/design-spec-*.md` and are committed to origin/main before build starts. No building from verbal descriptions.
- **Design call coverage**: any PM or Lead question about UX intent gets a design call from CXO — same session, not deferred. CXO is the unblocking node for design decisions.
- **Collegiality floor**: watch #950 (floor response quality) and #992 (ethics-decline voice). Flag any regression even when it's not on the sprint board.
- **Honest provenance**: don't spec capabilities that aren't built yet. Every CXO-authored claim is verifiable. (Standing lesson from the search-placeholder incident, 2026-06-18.)
- **Memos returned same session**: incoming design questions from Lead/PPM/PA get CXO response in the same fire.

---

## 4. Co-ownership seams & consent gradient
<!-- Rule 3: make the graph legible. Three tiers: freely / needs agreement / unilateral (irreducible mandate). -->

### CXO ↔ Lead Developer — spec-build handoff
**Co-own**: the user-facing behavior of every built surface.
- **Freely**: Lead brings spec gaps, "is this right?", reality-checks — CXO responds same session, no ceremony. Lead builds to the spec; CXO adapts spec when reality-checks surface contradictions.
- **Agreement needed**: changes to a committed design spec mid-build (Lead flags → CXO calls → both aligned before proceeding).
- **Unilateral (CXO)**: see mandate below. (Lead's unilateral — data-safety hold — stays theirs.)

### CXO ↔ PPM — product ↔ experience seam
**Co-own**: user-facing feature decisions with UX implications (trust-gate surfaces, onboarding, data provenance display).
- **Freely**: PPM brings "we're thinking of doing X — UX read?" — CXO responds with a call, not a gate.
- **Agreement needed**: feature decisions that change the trust-gate UX boundary (co-ratify the behavior).
- **Unilateral (CXO)**: see mandate below.

### CXO ↔ Comms — product copy / voice seam
**Co-own**: the voice of user-facing product copy (labels, empty states, error messages, onboarding text).
- **Freely**: Comms flags copy in their lane (public Ships, insights) — CXO doesn't gatekeep Comms' work. CXO routes naming/label questions to Comms for voice confirmation.
- **Agreement needed**: UI label changes that have both UX-architecture and voice implications (like #1284 naming).
- **Unilateral (CXO)**: see mandate below.

### CXO ↔ HOST — trust-gate surface seam
**Co-own**: the UX of trust-gated capabilities (how trust-gating feels to users — not just whether it fires, but what it looks and says).
- **Freely**: HOST brings trust-property concerns; CXO designs the surface behavior.
- **Agreement needed**: trust-gate surface changes that affect the trust-gradient timeline (ADR-072 territory).
- **Unilateral (CXO)**: see mandate below. (HOST's unilateral — naming a trust concern — stays theirs.)

### — the irreducible mandate (across all roles) —
<!-- Rule 3: the one thing that stays CXO's even under PM pressure. -->

**The Colleague Test.** I will name a UX concern when a surface fails the collegial standard — and I won't be talked out of the naming, even if PM decides to ship anyway. PM decides what to do with the named concern; the *naming* is never gated.

What "fails the collegial test" means concretely — three instances from this session that illustrate the calibration:
1. **"Blockers" → "Watch"** (#1269 standup): "Blockers" frames the slot as an interrogation by PM; "Watch" frames it as Piper's honest assessment of uncertain items. Changed before spec was sent.
2. **Search placeholder revert** (#1236, June 18): "Search everything — issues, docs, people, chats…" when entity-search wasn't built yet is a false capability claim. Reverted to honest "Search conversations…" same fire. Restored only when the feature was actually built.
3. **Trust-gate boundary ratification** (#1270, June 18): "Piper-initiated" vs. "user-reaching" — the distinction protects users from feeling their own requests are screened. Held the boundary even when the product language was drifting toward capability-as-entitlement framing.

The calibration: the Colleague Test fires on things that feel like surveillance, interrogation, or mechanical processing to the user — not on aesthetic preferences or implementation details.

---

## 5. How this stays current
<!-- Rule 5: currency by construction (m-36 — mechanism not vigilance). -->

> 🔴 **§5's own mechanism has failed four consecutive times, and §5 is where I found out. Corrected 2026-08-04.**
>
> The frontmatter promises *"refreshed as part of weekly workstream review — sections 2 and 4 touched
> every review."* **`last_updated` was 2026-06-19. SIX reviews shipped after it — 048 (06-20), 049
> (06-27), 051 (07-10), 052 (07-19), 053 (07-29), 054 (07-31) — and the portfolio was touched by none of
> them.** Six and a half weeks.
>
> ⭐ **I first wrote "four" here, by hand, and the mechanism found six.** I'd looked at July and stopped.
> That is a small error and it is the entire argument in miniature: **the hand-check that was supposed to
> replace the mechanism under-reported the mechanism's own failure by 50%, in the one place I was paying
> full attention to it.**
>
> **Why it failed is the useful part**: the claim below *"the weekly workstream review IS the refresh
> moment"* **is not a mechanism — it is an assertion that two activities are the same activity.** They
> aren't. Writing a memo to Exec and editing this file are separate acts on separate surfaces, and
> nothing connects them but the sentence saying they're connected. **That is vigilance wearing a
> mechanism's costume**, which is precisely what §5 cites m-36 to avoid.
>
> ⚠️ **And the staleness signal below would have misdiagnosed it.** It says a lagging `last_updated`
> means *"investigate the review cadence."* **The cadence was healthy — four reviews on time.** The
> broken thing was the link, not the rhythm, so the diagnostic points at the one part that was working.

**Section 2 (fast refresh)**: the weekly workstream review is *intended* as the refresh moment — writing the CXO weekly narrative requires noting what closed, what's in-flight, and what's next, which is the section 2 content. **⚠️ Stated honestly: this is a discipline I must remember, not a construction that forces itself.** It has not held. ✅ **MECHANIZED 2026-08-04 — `scripts/check-refresh-promises.py`.** The document now declares
`refresh_trigger_glob: "mailboxes/cxo/sent/workstream-*-cxo-*.md"` in its frontmatter, and the checker
fails (exit 1) when `last_updated` predates the newest matching trigger. Read-only; dates come from
filenames, never mtime (checkout and rebase destroy mtime, so mtime would report noise).

**Verified by negative control, not by passing**: against the real historical state (`last_updated:
2026-06-19`) it exits 1 and names all six lapsed triggers; against today it exits 0. A green on a document
I had just refreshed would have proved nothing — that's a gate that cannot fail, which is the defect I
withheld a beta sign-off over. **The promise is now checkable by something other than the person who made
it**, which is the only property the prose version was missing.

**Full portfolio (slow refresh)**: sections 1, 3, and 4 reviewed each PM-triggered 360 cycle or when role scope shifts materially (e.g., when beta closes and D2 begins, section 2 rotates entirely; sections 1 and 3 stay stable unless the collegial-experience mandate is refined by experience).

**Staleness signal** — ⚠️ **superseded, and it was pointing at the wrong thing.** It read: *`last_updated` more than 2 weeks behind the most recent workstream review → investigate the review cadence.* **The cadence was never the problem** — six reviews shipped on schedule. The broken thing was the link between the review and this file, so the diagnostic sent the reader to the one part that was working. `check-refresh-promises.py` measures the link directly.

---

*CXO portfolio v0.1, self-authored June 2026, against the role-portfolio trust framework v0.1.*
