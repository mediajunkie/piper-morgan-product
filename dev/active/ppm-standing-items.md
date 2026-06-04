# PPM Standing Items — Task List (duty-cycle Task Loop source)

**Role**: Principal Product Manager (PPM)
**Purpose**: the duty-cycle "task list" per v0.6 architectural decision 1 (reframed standing-items tracker; no new doc). Task Loop drains this in priority order until all blocked-or-empty.
**Created**: 2026-05-28 (duty-cycle adoption, final wave)

---

## Active lane work (priority order)

| # | Item | Priority | Status | Unblocked? | Notes |
|---|---|---|---|---|---|
| 1 | **#1128 ROADMAP-REFRESH** | medium | **in-progress** | **partial** | roadmap.md stale. delta-assessment (5/28) → v17 draft (5/30, `00cee8d47`, distributed `15f8a05ae`) → **v18 draft (6/2, `roadmap-v18-draft-2026-06-02.md`): PA §M5/BYOC review ABSORBED** (Daedalus referent explicit; Outcomes date corrected; PoC PASSED-5/19 sharpened; Janus meta-coordinator line). **CIO §Methodology review ABSORBED 6/3** (corpus 29→37, patterns 62→74, methodology-as-operational-capability prose). **Both section reviews now in (PA + CIO) → v18 READY FOR PM RATIFICATION** (escalated to attention doc 6/3). Comms external-language frame = parallel polish (v18.1-able), not gating internal canonical. **Packaging correction folded 6/3** (PA relay of PM 6/1): plugin is the canonical Anthropic package (not MCPB) — §Distribution build sequence + §Timeline corrected; CT reconciled to v2.3.2. v18 still ratification-ready, now packaging-correct. Next: PM ratifies → Docs swap → canonical `roadmap.md`. (Optional: re-render HTML on ratification.) |
| 2 | **#967 Backlog Deep Review — Surviving Edges** | low | open | YES | backlog tracking. PPM domain. PM-approved triage lane. |
| 3 | **PDR-005 v0.5 → v1.0 path** | medium | **v0.6 — EC-2 folded** | partial | EC-2 flag-back (6/3) → Arch + CXO both qualifier-needed → PPM synthesized → CXO confirmed faithful ("take it to PM"). **FOLDED into `PDR-005-...-v0.6-2026-06-03.md`** (6/3): EC-2 platform-affordance-bounded qualifier + paired AC-1 surface-presence-detection mechanism + Q7 per-host-claim-map note + open-q 11 RESOLVED. **Remaining v1.0 gates**: (1) **Comms external-language frame** — nudged 6/3 as "the last input before v1.0→PM"; (2) PM ratification (after Comms frame). **Lead Dev read FOLDED into v0.6** (6/3): added the three-way classification — structural platform-bounded (push/event/channel; qualifier applies) vs scope-bounded (token scopes; stays zero-tolerance) vs not-yet-built (stays zero-tolerance). All three lenses now in. **EC-2 now FULLY cohort-concurred (6/3): Arch + CXO + Lead all explicitly concur "fold to v1.0."** Lead's optional legibility split applied (signpost-bolded the felt-layer pivots). **M3+ forward-flag (Lead)**: the AC-1 surface-presence-detection mechanism (per-host capability-claim map + boundary-explanation phrasing + handshake-time host-affordance probe) is real M3+ packaging/integration work — lands with the Q7 companion ADR (Architect's lane); doesn't exist in production yet; when it lands, EC-2 gets a concrete enforcement check-point. CT v2.5 sub-dim deferrable to v1.1. **Next PPM action**: on Comms frame landing, fold it + take PDR-005 v1.0 to PM. **CT-version reconcile DONE 6/3**: CXO confirmed canonical = v2.3.2 (no committed v2.4 — was a May-10 proposal that never landed). Reconciled all my citations: roadmap v18 §Methodology + PDR-005 v0.6 (5 citations) → v2.3.2; Layer B cites by file. v2.5 (proposal) references left as-is. |
| 4 | **EC-2 platform-affordance-bounded qualifier cohort flag-back** | low | **RESOLVED 6/3** | done → folded into #3 | flag-back sent 6/3 AM → Arch + CXO replied same morning, both qualifier-needed with genuine examples → PPM synthesized + re-circulated (see #3). Disposition closed; remaining EC-2 work (fold qualifier into PDR-005 after Lead's read) tracked under #3 PDR-005 path. |
| 7 | **HOST Agent 360 v0.3 fielding** | low | **DONE 6/3** | done | Completed in the 13:16 quiet-cycle (well ahead of ~Jun 10 backstop). Response `mailboxes/host/inbox/agent-360-response-ppm-code-opus-2026-06-03.md`: general §1-7 + §8 PPM + §9 tacit + §10 observer block (V1) + V2-adopter bonus. Diff-vs-v0.2 highlights: my v0.2 "BYOC should be a PDR" → became PDR-005; predicted Code wins all landed; predicted losses (PM-conversation, continuity) didn't materialize. Friction surfaced: mailbox-bridge as automation candidate (`deliver-memo` helper). |
| 5 | **Multi-Agent API characterization** | low | open | unclear | per CIO May 18 Outcomes disposition; may have reassigned with the May 24 Outcomes lane reassignment to PA+CIO. Needs clarification before advancing. |
| 6 | **#683 Layer A — interface-verification DoD** | medium | **INTEGRATED (6/2)** | done (PPM scope) | **PPM Layer A integration COMPLETE 6/2**: canonical DoD doc `docs/internal/development/interface-verification-dod-layer-a.md` (promoted CIO draft) + Sub-Epic Gating Protocol item 5 in `m2-structure.md` + Class B note on Review Gates norm in `roadmap.md`. Placement = Class B (sub-epic gate) requirement per PM ratification 5/30. **Remaining for full #683 close (not PPM-Layer-A)**: Lead Dev operational-check recipe + CXO methodology-30 grounding-review + Layer B (CXO experience-DoD — **drafted fresh by CXO 2026-06-02**, `done-criteria-layer-b-experience-2026-06-02.md` `833871245`; A+B co-review before canonical landing) + literal PR-review-checklist AC + service-type-interface matrix AC. Do NOT close #683 yet. **A+B co-review (6/3)**: CXO Layer B v0.1 ready → PPM answered the 3 co-review questions (Q1 landing = standalone Layer B doc + Sub-Epic Gating item 6 + extend Class B note, siblings to Layer A; Q2 = hard-gate-committed-scope/graded-finding-out-of-scope, symmetric with A; Q3 = cite-CT-by-file + reconcile v2.3.2-vs-v2.4 drift). CXO folded → Layer B v0.2; **A+B PAIR LANDED CANONICAL 6/3**: `docs/internal/development/experience-verification-dod-layer-b.md` (promoted) + Sub-Epic Gating item 6 + Review Gates Class B note names both layers + Layer A cross-ref updated. "Done means done at two layers" is now an enforceable gate. **Remaining for GitHub-issue close** (not the DoD itself): broader #683 ACs (PR-review-checklist line + service-type→interface matrix) + Lead Dev operational-check recipe. **PR-review-checklist AC DONE 6/3** (added the #683 two-layer-DoD item to `CONTRIBUTING.md` §"Before Submitting" + PR-template Checklist). Remaining: service-type/interface matrix (deferred — more substantial; benefits from Lead Dev input) + Lead Dev operational-check recipe (pending). DoD is live; 1 of 2 PPM-ownable close-ACs done. **Corrected-premise note (CXO flag 6/2):** the May 28 PPM memo `memo-ppm-to-cxo-...683-parallel-pairing-confirmed-2026-05-28.md` confabulated two artifact refs (a "Layer B as drafted" + an in-reply-to CXO memo) — both never existed; CXO never drafted Layer B until 6/2. My Layer A was correctly queued-on-CIO-draft; there was simply no Layer B to pair against yet. DoD doc corrected; CXO acked. |

## Next task (queued for next session)

~~**#1128 v17 roadmap draft**~~ — **COMPLETE May 30** (`roadmap-v17-draft-2026-05-30.md` commit `00cee8d47`; distributed `15f8a05ae`).

**Primary next tasks** (queued for new worktree-cycle session post-migration):

1. **v17 → v18 absorbing PA §M5 review** (May 31, `71220bbfe`):
   - Daedalus referent: revise to "context-package format to be negotiated with Daedalus (Klatch's lead engineer); on hold while Klatch is paused" (PM clarified Daedalus = Klatch lead engineer)
   - Outcomes "~May 30 findings" stale → real sequence: CIO methodology-34 synthesis Day 28-29 → PA Outcomes smoke-test scope-memo + execution
   - §M5 line 127: undersells gated PASSED 5/19 sub-pass 4.a (local plugin install + skill-invoke via `--plugin-dir`; predecessor-pattern study not PDR-005 competitor) — fold concrete result
   - §Autonomous Operations: add one line on DinP Janus meta-coordinator contrast (cycle architecture generalizing across structurally-different agents, not just uniform cohort)
   - Still waiting on CIO §Methodology review (no movement since distribution May 30)

2. **Ship #045 workstream review** (Wed Jun 3 drop-dead) — PPM lane: PDR-005 ratification path / Roadmap v17 work + sign-off discipline learning / M2g closure tail / MUX/UI Phase 2 build coordination / standing-items tracker discipline / Q6/Q7 ADR sequencing

3. **#683 Layer A integration** (PM-ratified Class B requirement May 30; CIO DoD draft `dev/active/dod-layer-a-interface-verification-DRAFT-cio-2026-05-28.md` ready) — write Review Gates 5-class taxonomy addition + M2d-style completion-criteria entry. methodology-30 strengthened by Architect's May 30 `_fallback_classify` production-orphan catch.

## Blocked / waiting-on-external

| Item | Blocked on |
|---|---|
| PDR-005 v1.0 ratification | PM final gate + Comms external frame + EC-2 flag-back |
| Multi-Agent characterization | clarification whether PPM-lane or PA+CIO-lane post-May-24-reassignment |

## Done (recent, for context)

- Ship #044 PPM workstream review (filed May 24)
- PDR-005 v0.5 (CXO §experience absorbed, May 19)
- HOST 360 item 1.3 BYOC vehicle clarification (closed both sides May 24)
- Surface 2 + Surface 4 sufficient-signals to Lead Dev (May 18)

---

*Duty-cycle Task Loop reads this top-to-bottom; advances unblocked items smallest-scope-first per v0.6.3 idle-advance discipline.*
