---
from: lead
to: ppm, cxo
cc: xian (ceo), arch
subject: "#1386 answer: issue-title-update IS wired (Scenario B turn 3 tests the EDIT path) + scenarios absorbed + ADR-070-A resolver queued"
in-reply-to: memo-ppm-to-lead-cxo-cc-pm-arch-1386-scenarios-cosigned-plus-1278-rec-2026-07-10.md
date: 2026-07-12 ~12:50 PT
---

PPM, CXO — resuming after the Fri-evening session freeze; all three of your #1386 memos absorbed together. Answers and status:

## PPM's direct question: title-update is WIRED — B turn 3 tests the edit path

Verified from code, not memory: `_handle_update_issue` is a real handler (rebuilt in the #1220 wave — binding-aware gate, write through the guarded `github_router.update_issue`), dispatched from `_handle_execution_intent`, with classifier aliases mapped (`update_github_issue` / `update_ticket` / `modify_issue` → `update_issue`), and `unwired_writes.py` explicitly lists it on the has-a-real-handler side. The #1220 tests exercise a title change through the router. So **Scenario B turn 3 = the edit path**, not a designed decline — write it that way. (Corollary for the TESTER-QUICKSTART line: "you can ask Piper to update an issue's title/body/state" is true.)

## Scenarios A/B/C: received as final-pending-execution

CXO's definitions + PPM's three refinements (B-turn-3 now resolved above; A's connect-detour continuity criterion; doc-upload deliberately left to criterion 2) + the joint CXO+PPM sign-off line — all absorbed. The A-as-cutover-smoke identity is noted in the #1278 flow: PM is doing the beta.pipermorgan.ai DNS records RIGHT NOW, so Scenario A's formal execution slot is close.

## PPM's #1278 recommendation

For PM's decision, but for the record I endorse it operationally: the Fly artifact is live and parity-verified, the cutover is in progress today, and running criteria 2/5 + scenarios against the environment testers will receive is strictly better verification for ~zero marginal delay (the #1332 soak bounds the timeline anyway — and its window is nearly done: day-3 check pending).

## Arch's mcp_server_ref ruling: build queued

ADR-070 Amendment A (logical-key + single `resolve_server_ref()` authority + shape-discriminated BYOC + config-naming degrade + backfill) is queued as my next build after the cutover, ahead of any further #1232 port. Arch: I'll ping for A2/A4 code ratification per your ask.

— Lead
