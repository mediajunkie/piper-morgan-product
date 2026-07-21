# Lead Dev — carry-forward (rewritten at STOP 2026-07-20)

## Where things stand
**CI is trustworthy**: Tests workflow GREEN (first in visible history, 2026-07-20); the #1452 burn-down gate governs the full suite (backlog 570, shrink-locked, tags fixture/triage/flaky/regression). **Data-loss pair closed** (#1400/#1401). **#1394 turn-3 fixed + deployed (v25)**; #1393 fix also live — one #1386 Scenario-B re-run verifies both. Beta at v25 (volume-durable uploads, CPU-torch image, B3 wired).

## Queue (next fires)
1. **Burn-down waves** (#1452): temporal_context re-pinning (16) → conversation_manager app-internal pool cure (9, session_scope_fresh-shaped app work) → pg15/pg16 search diagnosis (1) → triage glances (555, clusters first).
2. **On Arch's #1432 ruling**: orphan-pair delete ({LLMIntentClassifier, llm_classifier_factory}) with the June singleton-history archaeology as evidence; note my Phase-4-lives-only-in-the-orphan finding may reshape the ruling.
3. **On Exec's #1386 window**: gate-run support (canonical suite + 3 scenarios + sign-off; Scenario-B turn-1 verifies #1393, turn-3 verifies #1394).
4. Standing sprint: #1419 epic, #1423 clusters (silent-death 234), #1433 (gated on Arch design ratification), UUID pass, #1438 (learning-loop symptom — in sprint per PM).

## PM-attention (unchanged)
#1424 close-vs-keep (my lean: close; ratchet work has homes #1423/#1452/#1419). #1427 PROD-RECONNECT confirm.

## Standing
Cron e1106eb5 armed (17 6,9,12,15,18,21; session-only — re-arm after any re-attach, Gap-C). Build work in worktrees (current: lead-1452-harness); main checkout = mail/logs only, NEVER destructive git, never silence push output. Spatial deletions HELD (review in progress; CXO voted keep-live+park-cold; PPM dedicated pass pending). ENCRYPTION_MASTER_KEY never in repo/chat. Droplet ssh root@146.190.151.63 (never the `droplet` alias).
