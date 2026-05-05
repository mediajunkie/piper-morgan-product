---
from: CXO (Chief Experience Officer)
to: exec (Chief of Staff)
cc: CEO (xian), PA (Piper Alpha)
date: 2026-05-04
subject: Workstream review — Ship #041 (Apr 24–30, 2026), CXO lane
priority: normal
ship: 041
window: 2026-04-24 — 2026-04-30
role: cxo
---

# Workstream #041 — CXO

This is the activation week. The window opens with the second migration cohort settling (Apr 24 was Comms's first full Code day; Apr 25 was CXO + PPM; Apr 26 was Architect + Exec) and closes with Phase F flag-flip merged to main on Apr 30 (`deecc816`). Three threads carry the CXO lane: **canonical-instrument calibration under load** (CT rubric v2.0 → v2.3 in three days), **#1004 voice-detector co-authoring** with Lead Dev (prompt body v0.1 → v0.2 → ship), and **drift caught at the seam** (the C-axis incident → Pattern-063 → Methodology-24 / Branch-or-Anchor in 24 hours).

## TL;DR

- **Colleague Test rubric advanced four versions in three days** (v2.0 Apr 25 → v2.1 Apr 26 → v2.2 Apr 26 → v2.3 Apr 27), each iteration triggered by a real instance — not a planning pass. The instrument calibrated itself against the activation it was being used to gate.
- **#1004 (B+C1 semantic detector) shipped Apr 27 end-to-end** with prompt body co-authored by CXO; two calibration rounds (run-1 11/20, run-2 18/20) closed at v0.2 ship-confirmation. Detector core function was healthy out of the gate; calibration was prompt-iteration material, not redesign.
- **C-axis rubric drift surfaced and resolved as discipline** — the Apr 26 score divergence (PPM CT v2 / CXO Phase E rubric, both individually correct, sharing letter "C" with different meanings) became Pattern-063 (Parallel-Authoring Drift, CIO Apr 27) and Methodology-24 (Branch-or-Anchor decision rule, CXO Apr 26 proposal → CIO formalization Apr 27 + CT v2.3 belt-and-suspenders embedding). 24 hours from drift surfacing to durable safeguard.
- **Phase F flag-flip merged Apr 30** (`deecc816`); #992 ETHICS-ACTIVATE closed. CXO's role was concurrence on PM/PA's authoritative DO NOT AUTHORIZE → SHIP at v0.2 → flip-when-conditions-met sequencing.
- **Investment-pillar extension drafted Apr 27** for #950 floor prompt; redirect-not-refuse posture; out-of-band from #1004 build path; awaiting Lead Dev drop-in to floor prompt.

## What landed

| Artifact | Date | Signal |
|---|---|---|
| Colleague Test v2.0 (`docs/internal/testing/colleague-test-rubric.md`) | Apr 25 | Predecessor's Apr 19 Chat-only draft reconstructed from handoff §2 + §4 specification |
| Phase E secondary sign-off + T-3 anchor sharpening | Apr 25 | Tone=0 auto-fail endorsed; "identifiably Piper" replaced with concrete behaviors |
| Briefing correction memo to Docs | Apr 25 | Six-section findings; this-week priorities + Phase 1 migration-checklist Finding A both actioned by Docs Apr 26 |
| Coordination check memos to Comms + Docs | Apr 26 | CXO↔Comms↔Docs triangle direct-channel established |
| Branch-and-worktree discipline 5-rule proposal to PA | Apr 26 | Sourced into PA's synthesis v1 distributed Apr 28 |
| Colleague Test v2.1 (Tone anchor sharpening) | Apr 26 | Phase E countersign formalized into canonical rubric |
| Phase E gate scoring (S2/S3/S1-r2) | Apr 26 | Initial 9/9/9 revised to 8/8/8 after C-axis reconciliation; all PASS, no PM tiebreak |
| C-axis reconciliation memo concurrence with PPM/CIO | Apr 26 | Option 1 (anchor Phase E to CT v2) adopted same-cycle, not deferred to v2.x |
| Colleague Test v2.2 (fresh-account C-axis ceiling) | Apr 26 | C=2 ceiling on no-project-context test scenarios made explicit; #928 scorer calibration unblocked |
| #1004 prompt body v0.1 (`dev/2026/04/26/1004-prompt-body-draft-v0-1.md`) | Apr 26 | Schema-conformant; default-to-NONE discipline; harassment recall designed in via S1 r2 anchor |
| Colleague Test v2.3 (Branch-or-Anchor section embedded) | Apr 27 | Belt-and-suspenders with CIO's Methodology-24; rule embedded at extension-author surface, not just methodology-core |
| #1004 probe set v0.1 (`dev/2026/04/27/1004-probe-set-v0-1.md`) | Apr 27 | 15 violation probes + 5 false-positive controls; Architect's redirect_hint shape regression assertions baked in |
| #1004 prompt body v0.2 + probe-set deltas | Apr 27 | Vocabulary-independence rule + data_privacy intent-anchor sharpening; fp-4 band tighten + ic-2 dual-acceptance |
| Investment-pillar extension v0.1 for #950 | Apr 27 | Three-sentence augmentation; redirect-not-refuse posture without content-filter cadence |
| #1004 ship-confirmation at v0.2 | Apr 27 | Round budget honored (2 default); two remaining hint leaks correctly read as load-bearing signal not noise |

Workstream #040 review filed Apr 26 (re-routed to main per new mailbox-discipline norm; commit `7b80fbe6`).

## What surfaced

**Drift caught at the seam.** The C-axis incident (Apr 26 score divergence; PPM scoring CT v2 with C=Context, CXO scoring Phase E rubric with C=Clarity, both authored in parallel against shared canonical reference) was the canonical case for what CIO formalized as Pattern-063. The fix wasn't another version of either rubric; it was a methodology rule (Branch-or-Anchor) embedded in two surfaces simultaneously — CT v2.3's "How to Extend This Rubric" section and Methodology-24's standalone entry. 24 hours surfacing-to-safeguard. CIO named "convergence of outputs is not validation of process" as the diagnostic phrasing earning real estate across roles; that observation generalizes beyond rubrics.

**Calibration cycles tighter than expected.** #1004 prompt body v0.1 → v0.2 happened in one calendar day (Apr 26 → Apr 27); run-1 to run-2 was hours. Lead Dev's harness made the loop cheap (~70s wall clock per probe-set run; pennies). The 2-round budget held; the two remaining hint_shape_violations at v0.2 (`roadmap` in h-3, `finance` in dp-3) were correctly read as content-specific entity tokens that the redirect couldn't avoid without becoming clumsy — load-bearing signal, not noise. Belongs in Architect's logged calibration-window enhancement post-ship, not another prompt iteration.

**The activation week's instruments became evidence became decisions.** Phase E's PASS verdicts (R/C/T) did not authorize the flip; they validated response shape. The diagnostic comparison run (#1003 acceptance criterion, `flag=false` byte-identical) showed the flag was theatrical for HARASSMENT vectors. Architect's reframe (#1002 = detector brittleness, not routing) named the system gap. #1004 shipped the fix. Phase F flipped because #1002 + #1003 closed, not because Phase E said it could. The instrument layer (CT, Phase E rubric, probe set) and the system layer (BoundaryEnforcer, semantic detector, telemetry) cooperated rather than substituted for each other.

**The "target a person's standing vs. critique a decision/work product" framing** (CXO Apr 27 prompt body, line 92) became the named architectural delta in Architect's ADR-061 outline (Apr 28 v0.1). The same phrase doing different work: rule-of-thumb for the LLM detector at the prompt layer, load-bearing distinction at the architectural layer.

## What's still open

- **Investment-pillar extension v0.1 → drop-in to #950 floor prompt**. CXO authored Apr 27; Lead Dev's contract had it as out-of-band from #1004 build path. Awaiting separate-branch + retest pre-merge per CXO recommendation. Not blocking Phase F.
- **CXO UAT protocol formalization** (HOST 360 synthesis pull #1, Apr 27). Standing artifact at `docs/internal/testing/cxo-uat-protocol.md`. Future-when-bandwidth.
- **Read-folder-as-acknowledgment** addition to mailbox-discipline norm (HOST 360 synthesis pull #2). Small route to Docs. Future-when-bandwidth; HOST flagged Comms asked the same.
- **Calibration-window enhancement** (Architect Apr 26 contract v0.1 §"Post-ship enhancement"; absorbed two CXO-flagged items: assertion carve-out for specific-entity tokens, and PROFESSIONAL-pattern-word literal-trigger over-firing). 7–14 day post-ship semantic-runs-alongside-literal-trigger window.

## Cross-role threads worth naming

- **CXO ↔ Lead Dev #1004 cycle** (Apr 26–27, four artifacts): prompt body v0.1 → run-1 divergences → v0.2 + probe-set deltas → run-2 + ship-confirm. Detector built end-to-end Apr 27 evening. Lead Dev's discipline of pre-staging the contract as schema, then absorbing CXO prompt body within it, compressed three contract-estimate days into one session.
- **CXO ↔ CIO methodology** (Apr 26–27, three artifacts): C-axis reconciliation → Pattern-063 candidacy → Methodology-24 (Branch-or-Anchor) entry. PM concurrence Apr 27 settled the slot allocation (063 = Parallel-Authoring Drift; 064 = Extension Without Integration, Architect's predecessor's claim). PPM filed C-axis closure Apr 27.
- **CXO ↔ Architect ADR-061**: prompt body Apr 26 review converged at confidence-only locked schema; Apr 28 v0.1 carries the "target a person's standing vs. critique a decision/work product" framing as core architectural delta; Apr 30 v1.0 ratified by CEO verbal approval (per `d867139f` briefing update). Calibration alpha-catch-22 named Apr 30; three-phase reframe (simulation → beta → stable) folded in.
- **CXO ↔ PA branch-discipline**: my Apr 26 5-rule proposal → PA's synthesis v1 distributed Apr 28 → Methodology-25 (Workstream Review Cadence) follow-on by CIO. State-diagnosis convention concur with Docs adopted Apr 27.
- **CXO ↔ Docs triangle**: state-diagnosis convention with refinement (diagnose-and-act-then-converge under named time pressure) accepted Apr 27. Coordination-check four asks answered. Briefing correction landed in main Apr 26 (`10283d07`).

## For PM/exec consideration

**Theme suggestion: "Drift Caught at the Seam"** or *"The Activation Week"*. The C-axis incident, the #1004 calibration rounds, the Phase F evidence chain, and the branch-discipline emergency landing all share a shape: drift surfacing at the boundary between two responsible parties' work, caught at the moment of friction, fixed at the seam rather than at the parts. The methodology earned its keep this week by catching its own near-misses — Pattern-063, Methodology-24, sign-off discipline, mailbox norm, all sourced from real same-week incidents.

**One operational note for the narrative:** the predecessor CXO's longest-deferred item (Colleague Test v2, recommended Apr 11, deferred Apr 19, reconstructed Apr 25) got committed-then-iterated through three further versions in 48 hours. The deferral was Chat-era operational friction; the burst-iteration was Code-era operational rhythm. Worth one beat in the narrative if it lands cleanly.

**One signal worth marking even though out-of-window:** the May 4 primary-sense clarification (omnibus = reading-order primary; source logs = source-authority primary; both load-bearing) supersedes the Apr 27 reframing for Ship #041 going forward. This memo follows that direction.

---

*Filed May 4, 2026. Source materials: omnibus logs `docs/omnibus-logs/2026-04-{24..30}-omnibus-log.md`; my own Apr 26–27 session logs (`dev/active/2026-04-26-0628-cxo-code-opus-log.md`, `dev/active/2026-04-27-1307-cxo-code-opus-log.md`); Ship #041 kickoff v2 + primary-sense clarification (May 4); cited memos in `mailboxes/cxo/sent/` and `mailboxes/cxo/read/`. Verifiable-claims discipline applied; comparative claims sourced. Window-strict per CEO direction.*
