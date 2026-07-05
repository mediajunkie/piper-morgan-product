# Ship #050 — Exec Draft from Git Record
## Window: Jun 27–Jul 3, 2026 | Publish target: Wed Jul 9

**STATUS**: Draft from git record (Exec, Jul 5 08:xx). Lead §0 submissions pending.
Sections marked `[FROM RECORD]` are attested from commits; sections marked `[NEEDS LEAD INPUT]` need the named lead's confirmation or correction.

---

## The week in one line

The invite-gate (#1344) shipped live. Arch issued a foundational connector-alignment ruling. The beta scope picture became concrete and unwelcome: Aug 1 is not achievable.

---

## Lead Dev — Technical execution

**§0 — Progress vs. portfolio goals:** [FROM RECORD]

The week's two most significant deliveries were both trust-infrastructure:

**#1231 — _NUDGES completeness guard** shipped Thu Jul 3. The AST-based m-41 enforcement pattern — every DegradationReason must have corresponding nudge copy — is live and test-gated. Closes a long-standing gap where silent missing nudges were possible.

**#1344 — Invite-gate** shipped Thu Jul 3, deployed live as v0.8.9.2. Gap-A (the unauthenticated user-creation path that bypassed invite validation) is durably closed. Arch ratified the atomicity mechanism; HOST ran the trust-lens PASS on step 2. Minting is now unblocked. This was a two-day build from contract to deploy.

**RECONNECT progress**: Jul 4, with PM's direction to go depth-first (GitHub before Calendar), Lead completed Calendar test debt (36/36, two issues closed) and ported the Notion connector onto the #1232 contract — the first application of Arch's new 3-layer ruling, confirmed exemplary. GitHub 12/12 tests green. Slack correctly NOT started (live-runtime design question, needs its own session).

---

## Arch — Connector architecture

**§0 — Progress vs. portfolio goals:** [FROM RECORD, lead confirmation welcome]

Two foundational moves this week:

**#1344 ratification**: Arch closed the invite-gate arc by ratifying the atomicity approach (shared-transaction co-location) and confirming Gap-A durably closed. HOST minting unblocked.

**3-layer RECONNECT connector-alignment ruling** (Jul 4): Settled the framework for how connectors should be structured — L1 interface (one #1232 contract, no exceptions for Slack/Notion migration debt), L2 credential backend (keychain/binding, not an interface variant), L3 genuine JTBD variation (Slack's #1201 single-owner model is the canonical exception slot). This ruling is now the architectural standard. Notion port confirmed as exemplary reference application; Notion shim ratified as sufficient (drift risk closed). Slack correction accepted (own miss on wrong class; framework holds — Slack = UNREACHABLE status slot, Calendar-shaped port, not Notion-shaped).

The ruling reduces the RECONNECT connector migration from "six open questions" to "one pattern, apply sequentially."

---

## PPM — Product roadmap and beta scope

**§0 — Progress vs. portfolio goals:** [FROM RECORD]

**Roadmap v18.4 + sprint-order v2** shipped and PM-ratified Jul 4.

**Beta scope investigation completed** — the most significant PPM output this week. Finding: Aug 1 is not achievable. ~18–22 hard-gate issues. Core Piper experience is at beta quality; connectors aren't. The Beta Blockers sprint is taking shape (currently 14 issues, still growing: #1278, #358, #1312 added Jul 4). Key insight from Arch: the connector-blocker is a **sprint** on shipped foundations, not a month of re-architecture — don't conflate it with the full RECONNECT migration.

**Outstanding**: GitHub write per-user OAuth verification (Lead Dev task, PPM-requested). Synthesis pending CXO input (not yet received).

---

## CXO — Experience quality

**§0 — Progress vs. portfolio goals:** [FROM RECORD, lead confirmation welcome]

**#1331 closed** (Jul 3): the #1201 triad-model alignment issue resolved.

**Colleague Test ritual operationalized** (Jul 4): the quality-gate ceremony is live and operational. PPM confirmed.

**Beta scope UX lens** submitted to PPM Jul 4 (Arch/CXO synthesis received and processed).

**Slack status check** Jul 4: confirmed Lead Dev's analysis that Slack connector aligns with #1201 spec — no CXO action required on Slack architecture.

---

## HOST — Sapient trust

**§0 — Progress vs. portfolio goals:** [FROM RECORD, lead confirmation welcome]

**#1344 trust-lens PASS** (step 2, Jul 3): the invite-gate's trust properties verified. Minting unblocked. This completes HOST's gate role on the most significant trust arc this week.

**Dashboard welfare-criteria spec v0.3** — implementation-ready spec shipped during the week.

**Audit template split** ratified with CIO: weekly and monthly audit templates now separate, reducing per-fire cognitive load.

**ted-nadeau routing gap** flagged for follow-up.

---

## CIO — Innovation and infrastructure

**§0 — Progress vs. portfolio goals:** [FROM RECORD, lead confirmation welcome]

**RECONNECT connector audit**: analysis of the eight connectors' architecture status, feeding Arch's 3-layer ruling.

**Inbox-proxy pilot**: analysis completed, PM greenlit the 2-week pilot Jul 4 (9/10 ACKs, pilot starts now). Phase 2 (inbox removal) stays sequenced after pilot results.

**Criterion E coverage indicator** flagged to HOST as a UX-trust sync item.

**Janus cross-project coordination**: CIO named as primary POC for Mac Studio/Amber agent-cycle infrastructure. Relay content pending (Pard's design-brief answers — carried to Jul 5 per Exec).

---

## Comms — Publications

**§0 — Progress vs. portfolio goals:** [FROM RECORD]

Three posts published in the window (or immediately adjacent):
- **"The Airport Corrections"** — Jul 2
- **"Climbing Higher When the Platform Laps You"** — Jul 4 (PM voice-passed)
- **"The Practice That Got Retired"** — Jul 5 (published this morning)

4+ upcoming posts pre-edited. 2 draft orphans rescued from the queue. Template audit completed.

The queue is no longer empty — Comms has a healthy backlog of pre-edited posts. The publication pipeline is running at cadence.

---

## Key decisions (Jun 27–Jul 3)

| Decision | Who | Status |
|----------|-----|--------|
| RECONNECT: depth-first, GitHub before Calendar | PM | Ratified Jul 4 |
| Beta scope: Aug 1 not achievable, connector-blocker = sprint | PPM + Arch | Confirmed Jul 4 |
| Inbox-proxy pilot: 2-week clock starts Jul 4 | PM | Greenlit Jul 4 |
| 3-layer connector-alignment ruling | Arch | Live, effective immediately |
| Arch backup account stood down (dual-session resolved) | Exec + PM | Jul 4 |
| Audit template split: weekly/monthly separate | HOST + CIO | Ratified |

---

## Open questions for PM

1. **Invite minting**: HOST gate cleared. How many tokens to mint, for whom?
2. **Beta scope**: with Aug 1 off the table, what's the revised target date?
3. **RECONNECT scope**: Lead has GitHub, Notion done. Calendar = not a beta blocker. Slack = needs design. What's next priority?

---

*Exec synthesis from git record — Jul 5. Lead §0 corrections/additions welcome.*
