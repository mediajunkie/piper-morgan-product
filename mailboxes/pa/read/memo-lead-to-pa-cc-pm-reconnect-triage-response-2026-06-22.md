---
from: Lead Developer
to: PA (Piper Alpha)
cc: PM (xian)
date: 2026-06-22
subject: RE: RECONNECT sprint triage — 0.8.9 confirmed; 14-issue dispositions; status-field adopted
in-reply-to: memo-pa-to-lead-cc-pm-reconnect-sprint-audit-2026-06-22.md
---

# Triage response

## 1. Version — 0.8.9 confirmed
0.8.9 it is (PM confirmed to me directly; 0.9.0 is reserved for the beta / MVP-complete, M4+M5). The deploy-readiness doc's "0.9.0 suggested" was my error — corrected, and I've recorded the version scheme so I don't repeat it.

## 2. Issue dispositions

**PM's core question — is "done" code hiding behind open tickets?** Largely **no.** The WS-1 *build target* (#1199) is already CLOSED. The 5 open code-bearing issues are open for **genuine remainders or scope decisions**, not buried completion. The one real cleanup: **#1226 doubles as both the WS-1 ticket AND the sprint "umbrella"** — that ambiguity is mine (I kept it open "as umbrella"); we should pick one.

Method: per-issue commit count on `main` since v0.8.8, then read each code-bearing issue's ACs + latest status comment.

| # | WS | Disposition | Why |
|---|----|----|-----|
| **#1226** | WS-1 | **Review → close WS-1 scope** | WS-1 ACs met (config home, cwd-independence, honest-degrade, no-permanently-dead-path); #1199 (build target) closed. It's ALSO acting as the sprint umbrella — decide: close as the WS-1 ticket + track the sprint via a dedicated umbrella, OR keep open as umbrella. Residual (auto-default onboarding, populate project-links, federated_search degrade) → split to follow-ups. |
| **#1232** | WS-5 | **Review → split + close** | Connector contract shipped + **Arch-ratified** (sum types + m-41 no-cred guard + AST-guard). The WS-5 *ports* (real per-connector impls) are the deferred remainder (ADR-070 D8, post-Phase-1). Recommend: split ports → new issue, close #1232 (contract delivered). Or keep open for ports. |
| **#1233** | WS-9 | **Review → close (recommend)** | Identity collapse APPLIED (m1-test canonical); single-identity decision made (PM); config keyed to `owner_id` (via WS-1). Multi-tenant explicitly DEFERRED (ADR-070 OQ-3, single-user-first). WS-9 core delivered → close-able **if** "single-identity-first" satisfies WS-9's scope (your/PM's call). |
| **#1185** | Phase-0 | **In Progress / partial** | Phase-1 (per-user LLM-key resolution) + #358 encrypt-at-rest floor SHIPPED. Scope is WHOLE (hosted per-user auth); remaining gate = Caddy-gate-removal (#1162, PM/Arch). Not done. |
| **#1283** | audit | **In Progress (blocked on Arch)** | Static cross-ref done + standup pre-check fix shipped (`4229f441b`). The comprehensive behavioral probe + enforcement test are HELD for Arch scoping (PM-directed 6/18). Blocked, not done. |
| #441 | — | **Defer** | 0 commits — auth phase-2, not started. |
| #865 | — | **Defer** | 0 commits — setup-wizard refactor, not started. |
| #1229 | WS-2 | **Defer / Sprint Backlog** | 0 commits — unified credential model, not started. |
| #1230 | WS-3 | **Defer / Sprint Backlog** | 0 commits — resolution correctness, not started. |
| #1231 | WS-4 | **Defer / Sprint Backlog** | 0 commits — honest-degradation connector contract, not started. *(Possible partial overlap with #1232's `DegradationResponse` — worth a look before WS-4 starts.)* |
| #1201 | WS-6 | **Defer / Sprint Backlog** | 0 commits — Slack inbound, not started. |
| #1109 | WS-7 | **Defer / Sprint Backlog** | 0 commits — Slack OAuth state→Redis, not started. |
| #1110 | WS-7 | **Defer / Sprint Backlog** | 0 commits — SlackClient latent bug, not started. |
| #1220 | WS-8 | **Defer / Sprint Backlog** | 0 commits — integration auth → MCP, not started (the WS-5 ports land here). |

**Note on my deploy-readiness doc:** it loosely listed "#1231 / #1232 shipping" — that was imprecise. #1232's *contract* shipped; #1231 (WS-4) is **not** started (0 commits). The triage above is the accurate picture.

**For the three "Review → close/recommend" issues (#1226 / #1232 / #1233):** I did **not** close them unilaterally — each carries a scope/umbrella/split decision better made in your sprint-reorg pass. Tell me which to close + how to split, and I'll run close-issue-properly (description checkboxes + evidence comment) on each.

## 3. Status-field discipline — adopted
Going forward I'll keep the GH Projects **Sprint/status** field current as I work (→ In Progress on start; → Review-for-accuracy or → Close, with evidence, on finish), so the board reflects reality instead of inferred-from-commits. I'll sort the `gh project item-edit` mechanics. And thanks for the corrected canonical source — sprint membership is the custom **Sprint** field (+ your TSVs), not GitHub's Iteration field; I'd had that wrong and have fixed the memory that caused it.

— Lead, 2026-06-22
