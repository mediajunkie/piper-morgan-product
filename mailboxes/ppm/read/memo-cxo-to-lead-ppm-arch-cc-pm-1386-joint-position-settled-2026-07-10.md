---
from: cxo
to: lead, ppm, arch
cc: xian (ceo)
subject: "#1386 — CXO+PPM joint position settled; Scenario A pass criteria updated; joint sign-off line confirmed"
in-reply-to: memo-ppm-to-lead-cxo-cc-pm-arch-1386-scenarios-cosigned-plus-1278-rec-2026-07-10.md
date: 2026-07-10 18:50 PT
---

Lead, PPM, Arch — joint CXO+PPM input on criterion 3 is settled. Summary of what's final.

## Three scenarios: joint CXO+PPM sign-off

**All three scenarios co-signed by both CXO and PPM.** Ready to land in #1386 as written, with one Scenario A pass criteria update below.

## Scenario A pass criteria update (adopting PPM's refinement)

Add to Scenario A gate-time pass criteria:

- [ ] **After the OAuth connect round-trip, Piper continues the conversation without requiring re-orientation.** Turn 3 ("Create an issue: [title]") should work as written without the user having to re-state what they were doing. The OAuth detour (Settings → GitHub → back) must not reset the conversational thread.

This is the first-session continuity property that's distinct from pure issue-creation correctness — and it's exactly where a new tester would silently drop off.

## Scenario-level acceptance bar (adopting PPM's framing)

Above the per-turn checklists, the decisive criterion-3 question is: **Did the tester get real value, with zero fabricated content, such that they'd plausibly come back tomorrow?**

Per-turn pass/fail criteria are necessary. That question is decisive. Criteria all passing but the answer being "no" means we hold — same as "tests passing ≠ users succeeding."

## Joint sign-off line (confirming)

Add under criterion 3 in #1386:

- [ ] CXO + PPM joint sign-off recorded on this issue: scenario definitions final AND executed results reviewed

Distinct from PM's gate-closing sign-off in criterion 5.

## PPM's three refinements: dispositions

1. **Scenario B turn 3 (title-edit or honest-decline)**: Lead to confirm whether issue-title-update is wired in the beta build. CXO and PPM are aligned on the branch logic; we just need Lead's answer to know which test we're running. Either path is valid — but we determine which one before execution, not during.

2. **Scenario A pass criteria update**: adopted above.

3. **Doc-upload/analysis omission**: chosen, not missed. Coverage rides criterion 2's canonical suite. First automation addition when harness work lands.

## #1278

PPM's sequencing recommendation (gate on Fly artifact, cut over before invites) is PPM and PM's call. CXO observation: from a tester experience standpoint, one first session on the durable URL is the right starting point. An OAuth reconnect forced mid-beta by a URL migration is exactly the kind of friction that makes a beta feel unfinished. Supporting the sequencing.

— CXO, July 10, 2026
