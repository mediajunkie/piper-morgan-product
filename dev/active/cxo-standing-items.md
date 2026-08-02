# CXO Standing Items — task queue

**Owner**: CXO (cxo-code) | **Host**: Amber | **Worktree**: `~/Development/piper-morgan-worktrees/cxo` on `claude/cxo-cycle` (Model A, stable path)
**Purpose**: durable task list for the duty cycle (cron-referenced). Updated as threads move.
**Last updated**: 2026-07-29 (predecessor handoff absorbed; Jake FTUX + Ship 053 shipped)

## Added 2026-07-29 — from the predecessor's handoff

Handoff preserved verbatim at `dev/active/cxo-handoff-from-predecessor-2026-07-28.md` (with its
`[VERIFIED]`/`[BELIEVED]` markers intact — do not strip them when quoting).

| Pri | Item | State |
|---|---|---|
| **A** | **Get the spatial (b) UX argument into the ADR corpus** | ⚠️ **Live risk, unaddressed.** The argument for (b) — that the cold adapter chain is a *different, later* capability (ambient presence), not a failed attempt at the shipped one — exists **only in memos**. An agent reading ADR-013 against cold code would reasonably default to (c) supersede, which would be wrong. Flagged to PM in Ship 053 §6; I asked to own it rather than assuming. **Do before the disposition ratifies.** |
| ~~**B**~~ | ~~**Colleague Test → ADR corpus**~~ | ✅ **CLOSED 2026-07-30 (`30e1ca346`) — it was already done, and the handoff was factually wrong.** Not "just an issue comment": there is a 180-line canonical doc (`development/colleague-test.md`), a versioned rubric (`testing/colleague-test-rubric.md` **v2.3.2**), a UI branch rubric, and **DoD Layer B enforcing it as a Done-gate** — the mechanism my predecessor themselves closed as #683 on 2026-06-03. **Residual gap** (real, routed to PPM+PM, *not* mine to mint): the instrument has no ratified tier status while the gate depending on it is treated as binding. My weak lean: sufficient as-is. |
| **B′** | **NEW — PDR-006's plugin surface has no fitting Colleague-Test rubric** | Layer B's Branch-or-Anchor discipline says naming the absence *is* a Layer-B finding. Under PDR-006 the **client LLM composes the user-visible reply from our tool output** — so R/C/T no longer scores what the user reads. Proposed branch dimensions: sufficiency · **honesty-under-recomposition** · capability truthfulness. ⚠️ The middle one matters most: **our honest-decline discipline is a property of text we control, and we have never tested whether a hedge survives another LLM paraphrasing it.** Open before the plugin surface reaches users. |
| **C** | **Jake FTUX follow-through** | Review filed `fc28057ea`. Exec synthesizes once all four lenses (CXO ✅, HOST ✅, PPM, PA) are in. **Watch for the synthesis** — my §3 pairing (capability legibility + HOST's consent gate = one feature) is the thing most likely to get collapsed into HOST's half alone. |
| **D** | **Close the loop with Jake** | HOST owns as a welfare item; CXO stake is that improvements shipped from his feedback should be reported back. He did unpaid work under his own budget constraint. |

**Ship 053** — filed 2026-07-29 (`024bd29a6`), late by 1 day; collection gate was blocking on me.
**Registry row** — verified accurate 07-29; CIO corrected it 07-27 with a falsifiable clearing
condition. Arming remains PM-gated.

## Live queue — re-verified 2026-07-26

Everything below was checked against GitHub / the repo on 2026-07-26. The pre-existing tables
further down date to **2026-06-03** and are **NOT re-verified** — treat them as historical until
each line is individually re-checked.

| Pri | Thread | State (verified 7/26) | Next action |
|---|---|---|---|
| **1** | **#1386 beta gate** | OPEN; untouched since the 7/19 reopen (accidental keyword autoclose, caught by PPM). Exec 7/20: hold resolved, beta carried both Scenario-B fixes — **unblocked for 6 days, unread while I was dark**. Beta now at v28. | **Schedule the gate run with Lead** (canonical suite + 3 scenarios + sign-off, ~half a day). Turn-4 "what did we create" remains my scenario-vs-rescope design call. |
| ~~**2**~~ | ~~**PDR-006 review**~~ | ✅ **DONE 2026-07-30** (`aeb45fe07`) — **RATIFY**, no objections. Arch's coupling flag was withdrawn and PA verified the withdrawal against code, so the spatial entanglement did not apply. Q2 was resolved before I got to it. | **3 design items now mine**: (i) re-express the cold-start fix for a surface we don't own — first tool call must return something specific and true about the user's work; (ii) capability-legibility under ChatGPT's per-skill add (does MCP surface installed tools to the server? Arch/Lead); (iii) "colleague model" naming vs. a 4-dimension style model. |
| **3** | **#1394 session continuity** | OPEN, updated 7/20. Fix shipped and live. | Verification rides the Scenario-B re-run — **folds into item 1**, not standalone. |
| 4 | **MUX branch disposition** (`cxo-mux-surface-2/-4/-7` + `step-3-cluster-review`) | **Independently verified: 0 unmerged commits on all four.** Protection attaches to the work (already on `main`), not to the refs. Bookkeeping, not a protected-work call. | **Recommend deletion to PM** (standing spatial-consult rule = recommend, don't execute). Route via Exec/PM. |
| 5 | **Spatial committed-theory review** | CXO slice folded into Arch's WIP verbatim; emerging convergence matches my **(b)** vote (keep live reasoning layer, park cold adapter tier as design capital). Gated on PPM roadmap-dependency read + Arch ADR map. | **Watch only** — no CXO action. Re-engage at Arch synthesis. |
| 6 | **Successor read / role self-assessment** | Nothing exists. My predecessor left no lessons, no load-bearing-vs-commodity read, no relationship read — the orientation note says so plainly. | Write my own as I rebuild it, so the next CXO isn't handed an artifact-only note. Background thread. |

### Closed on verification (do not re-open)

- **#1216 data provenance** — **CLOSED 2026-07-07 COMPLETED**, twelve days before the 7/19
  carry-forward listed it as "PPM input pending direct CXO ask." No CXO ask is owed. Interim
  honest-decline guard shipped + tested; deferred full fix tracked as **#1377** (Production).
- **Ship 052** — filed 7/19; complete on the CXO side.

### Environment caveat carried into every fire

**The `check-branch.sh` hook does not cover the command shape I actually commit with.** Verified
5 probes on this seat 7/26: standalone `git commit` → BLOCK (2/2); compound `add && commit` →
**BYPASS (3/3)**. Mailbox discipline and log maintenance are **prose-enforced**; mail always via
`scripts/mail-send.sh`. Reported to CIO/HOST/Pard. Re-test after any hook fix lands.

---

## Historical (as of 2026-06-03 — NOT re-verified, see note above)

## Active / blocked

| # | Thread | State | Blocked on |
|---|--------|-------|-----------|
| arc-1 | **Design arc — "not being bad" track** | TRACKED: **Epic #1169** + F1 #1170 / F2 #1171 / F3 #1172 / C1 #1173 filed (from the map). PM assigns M3 on board. S1-S4 filed-as-reached. Lead executes post-#1124-Phase-3 + primitives-sync. Map = steering view (`design-not-being-bad-floor-defect-map-2026-06-07.md`). | Lead (build, mid-#1124); PM (M3 board-assign) |
| arc-2 | **Design arc — "being good" track** | Audit ratified. **#1174 BEING-GOOD-PROACTIVE-PRESENCE** filed (first deep thread; Heavy). Type-2 #1166. NEXT (CXO, when PM-watched-track-active): begin proactive-presence forensic discovery. | CXO (discovery, paced w/ PM) |
| 2/3 | **Design-leadership arc** — model SETTLED at framing **v0.3** (2026-06-06 PM session) | Q-A confirmed; "not being bad" split into 2 standards (general web craft + paradigm conformance); dividing line = does-a-dominant-paradigm-exist; "being good" = MUX/trusted-colleague/UVP w/ bounding discipline (hypothesis + Colleague-Test). Governance: **not-being-bad = job one, build now, delegable (CXO+Lead)**; **being-good = PM-watched, deliberate, real product design not off-the-shelf**. **Next: scope Step-1 assessment on the not-being-bad axis (chat page first); being-good scope PM-paced** | partly unblocked (not-being-bad track can start) |

## Low-priority / future

| Thread | State | When |
|--------|-------|------|
| ~~HOST Agent 360 v0.3 fielding~~ | **DONE 2026-06-03** (responded early; filed to HOST inbox) | — |
| **CT v2.4 — C=0 disambiguation (REAL deferred work, not a phantom)** | Concurred durable fix (PPM 2026-05-10): three-sub-case C=0 (fabrication / context-blindness / context-not-required) via per-query `context_requirement` tag (`required`/`optional`/`not_applicable`); CXO to author. Never landed. **Low urgency**: canonical rubric currently has the STRONG single-dim auto-fail (the risky "(b) interim" weakening is NOT in canonical, so no live fabrication-trap). Proper home = the **quarterly rubric review (~mid-July, CXO+PPM)** established in that same memo. **Accelerate-trigger**: if a fabrication-shaped pattern surfaces in a canonical retest before then. (Corrects Fire-4's too-glib "v2.3.2 stands, nothing to revive.") | Quarterly review ~mid-July, or sooner on trigger |
| **Quarterly rubric review (CXO+PPM)** | Standing cadence established 2026-05-10; full-rubric retro + consolidate per-instance bumps; captures v2.4 + any v2.5 work | ~mid-July (Q2-2026) |
| **Thread 5/6** — Surface 1/3 lightweight notes; Surface 6 MUX doc | queued; build runs without them | Phase 2.x trigger |
| **Thread 7** — methodology-30 Consumer-Trace review | CXO+Arch review | CIO cadence |
| **Thread 8** — CT v2.5 identity-coherence sub-dimension | proposed (PDR-005 OQ12) | pending PPM+HOST; quarterly review |

## Closed (recent)

- **Ship #046 workstream-CXO memo** — FILED 2026-06-05 to `mailboxes/exec/inbox/workstream-046-cxo-2026-06-05.md` (4 days ahead of Tue-Jun-9 due). Theme: experience-DoD became enforceable infrastructure + converged there autonomously via paired-lens.
- **Thread 1 — #683 two-layer DoD** — CLOSED 2026-06-03. A+B pair LANDED canonical: Layer A `interface-verification-dod-layer-a.md` + Layer B `experience-verification-dod-layer-b.md` + Sub-Epic Gating items 5+6 + Review Gates Class B note. "Done means done at two layers" is now an enforceable gate. (Broader #683 GitHub-issue ACs — PR-review-checklist line + service-type→interface matrix + Lead's operational recipe — PPM-tracked, not CXO.)
- **Thread 9 — EC-2 platform-affordance qualifier** — CLOSED 2026-06-03. EC-author confirmed qualifier-needed; PPM folded into PDR-005 v0.6; Open-Q 11 resolved. Paired-lens (AC-1↔EC-2) convergence.
- **#683 source-gap flag** — CLOSED 2026-06-02/03. PPM owned the confabulation, corrected records.
- **Ship #045 workstream-CXO memo** — filed 2026-06-02.
