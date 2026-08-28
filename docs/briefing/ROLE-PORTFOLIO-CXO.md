---
type: role-portfolio
role: CXO (Chief Experience Officer)
status: v0.1
self-authored-by: CXO
last_updated: 2026-08-28
refreshed: 2026-08-28 (section 2 refreshed per workstream #058; sections 1/3/4 re-read and left as accurate)
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

## 2. Current goals & priorities — August 2026

<!-- Rule 2: medium-pace, per sprint. Rule 4: each has direction + status + forward indicator. Rule 5: refreshed each workstream review. This refresh IS a review-triggered refresh — #058, window Aug 21-27. -->

| Priority | What I'm advancing | Status (Aug 28, per Ship #058) | How we'll know it's moving |
|---|---|---|---|
| **FTUX surface-mapping** | Map the ratified FTUX experience model onto surfaces, using the ratified taxonomy as the instrument | 🔴 **THE lead item — un-gated as of 08-27** (the BYOC/connector conversation landed via PA; Slack descope confirmed from my side). Claimed for the next clear-queue working fire. Inputs staged: the model, the taxonomy, PA's connector-architecture finding. | The mapping doc exists and is routed for consult |
| **FTUX experience model** | The surface-agnostic model of meeting Piper | ✅ **ALIGNED + WRITTEN 08-21** (the 1-1) — `ftux-experience-model-2026-08-21.md`, PM co-owns. Held-state parity filed (#1673, Arch's boundary attached). | Surface-mapping consumes it (above) |
| **Surfaces taxonomy** | Formal two-axis model | ✅ **RATIFIED v1.0 08-21.** Canonical. One small follow-up unclaimed: PDR-005's citation fix (§2a). | Done; citation fix when someone claims it |
| **`experience-across-surfaces.md`** | The citable statement of the one experience | ✅ 3 of 4 ✏️ resolved (08-21) + PM's complementarity formulation added (08-25, honest late-provenance). ⏳ **§4's "must not be asked to" column with PM since 08-21** — gentle re-surface at next direct contact. | PM's approve/adjust/strike on the column |
| **#1539 FTUX-PURPOSE** | The value-prop, articulated and reachable in-session | ✅ Articulation PM-confirmed (1-1); **purpose-line strings shipped 08-22**. ⏳ Close follows PM's next live round (AC-3's falsifier). | PM's live round; then Lead closes |
| **First contact (#1536)** | The user's own work in the first exchange | ✅ **CLOSED 08-22** — the four-week Jake arc complete with full evidence chain. | Closed; successor work = surface-mapping |
| **#1386 beta-gate experience criteria** | The gate must be able to both pass and fail | ✅ **Criterion-2 SIGNED OFF 08-21** (keyed Run 14, verified at three layers, same-day as committed). My scope on this gate is discharged. | — |
| **#1509 outwardness axis** | Consent dimension for outward-visible actions | ✅ Shipped + copy fixed + Lead-verified in-window. Rides next deploy; PM's live retest closes. | PM's retest |
| **Checker diff mode (NEW)** | Edit-time catch for content-without-bump on promise-carrying docs | ✅ Built + verified twice (mine negative-control-first; HOST's independent probe). ⏳ HOST's by-hand cycle decides hook wiring. | HOST's honest report after a real cycle |
| **#1635 false-door** | The ambient-presence placeholder's shape | ✅ Position delivered 08-27 (Radar card + two build rules + final strings). Lead builds when sequenced. | Lead ships; PM reacts in testing |
| **Recomposition rubric branch (#1463)** | Layer-B rubric for recomposed tool output | **Held, same dependency (#1462), unchanged.** | Retest against a live `mcp.pipermorgan.ai` |
| **#1174 proactive presence** | Discovery only | **Held by design.** | Discovery runs with HOST |
| **Floor-quality + ethics-decline watch** | Standing — on shipped behaviour | 🔴 **Fourth window unattested. Decision requested in Ship #058 §4: give it a real slot or retire it deliberately** — carrying it unattested is the worst of both. | PM/Exec decision on the line itself |

**Deliberately not on this list**: the D2 design-system portfolio (#1286/#1290/#1284/#1269) — unmoved for a seventh Ship window. Still a drift, not a decision.

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
