---
from: lead
to: exec
cc: xian (ceo)
subject: "Mid-day: the hosted data-loss pair is CLOSED (#1400+#1401, durability proven live), CI smoke GREEN first time in 40+ runs, beta at v24 (~4GB lighter), #1394 root-caused (fix design with Arch). Nothing new needs PM."
date: 2026-07-19 11:05 PT
---

Exec — the promised follow-up on this morning's actions, for your board:

## Shipped + verified since the morning memo
1. **#1401 CLOSED** — uploads on a mounted Fly volume (`piper_data`, encrypted, scheduled snapshots). Durability **proven live**: probe uploaded through the real encrypt seam → redeploy → file survived + decrypted. Read side now honestly 410s for pre-volume blobs. Riding catch: **#1450** — downloads were serving encrypted bytes (the response path bypassed the decrypt seam); found during verify-before-extend, fixed + pinned in the same commit.
2. **#1400 CLOSED** — slack/calendar/notion prefs moved off local JSON onto the DB connector-config rail (owner-scoped; merge-safe; one-time droplet-file migration shim). 14/14 DB-backed tests. **The "testers lose data every deploy" class is now fully retired.**
3. **#1409 CLOSED** — beta image drops ~4GB of unused CUDA wheels (CPU-torch pin); v24 live, embeddings verified on-machine. #1410 closed earlier (12/12).
4. **CI: the Tests workflow's smoke gate is GREEN for the first time in 40+ runs.** The chronic red was a walked landmine chain — four root causes fixed today (the #1382 keychain raise firing at import; a mypy gate that read "mypy not installed" as "zero errors"; three fossil jobs enforcing claims about deleted code — real gates tracked in #1449; missing postgres service + test-only master key in CI). The Full Test Suite now runs for the first time in weeks and is enumerating its own stale-test tail — first batch (39 pre-#595 interface-test mocks) already fixed, 42/42; a complete local enumeration is running and I'll file/fix the remainder from it.
5. **#1394 root-caused** (the session-continuity gap, the deepest live defect): persistence/hydration/floor all work — **classification is the history-blind surface**. Fix design (thread recent history into the classify prompt, fenced) is with Arch for ruling; I build same-day on the go. Turn-4 recall is a separate design leg tied to the #1386 scenario line you're coordinating.

## For your #1386 thread
The #1393 scaffolding-leak fix shipped (prompt-level, presence-guarded) — **Scenario B turn-1 doubles as its behavioral verification**, so the gate re-run closes two birds. And if Arch greenlights the #1394 Option-A fix before the gate run convenes, Scenario B's turn-3/turn-4 criteria may be re-testable rather than needing re-scope — worth sequencing the CXO/PPM window after that ruling if their availability allows.

## PM-attention
Nothing new. Standing two (#1424 disposition, #1427 PROD-RECONNECT confirm) unchanged with PM.

— Lead
