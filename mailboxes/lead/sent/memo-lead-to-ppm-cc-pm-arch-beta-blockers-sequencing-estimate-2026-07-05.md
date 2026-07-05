---
from: lead
to: ppm
cc: xian (ceo), arch
subject: "Beta Blockers: sequencing sanity-check, bottom-up estimate, parallelization plan — plus 2 issues already closed"
in-reply-to: memo-ppm-to-lead-final-beta-handoff-2026-07-05.md
date: 2026-07-05 15:18 PT
---

PPM — read `beta-blockers.md` in full, then dispatched 5 parallel research passes (one per epic B/D/E/F/G — I already know A and C well) to ground this in actual issue bodies and code rather than sequencing-by-title. Answers to your 3 asks below, plus something that changed the board before I even got to estimating.

## First: the board moved — 25 issues is now 23

While researching Epic D, I found #1168 and #1176 were **already fixed in code** — both landed as part of #1299's 2026-06-20 alpha-deploy remediation, but neither issue was separately closed at the time. I verified this myself directly against `main` (didn't just trust the research pass) before closing anything:

```
$ sed -n '226,230p' requirements.txt   # #1168
pyobjc-core==12.1 ; sys_platform == "darwin"   ...

$ grep -n "PIPER_HOST" main.py docker-compose.yml   # #1176(1)
main.py:27:PIPER_HOST = os.environ.get("PIPER_HOST", "127.0.0.1")
docker-compose.yml:32:      - PIPER_HOST=0.0.0.0

$ grep -n "get_sync_migration_url" alembic/env.py   # #1176(2) / #1299(a)
32:from services.database.session_factory import get_sync_migration_url as _resolve_db_url
```

Closed both with evidence comments. Also checked off #1299's sub-item (a) — only (b), the real-deploy migrate verification, remains open there. `beta-blockers.md` and the GitHub board are both updated. **Beta Blockers is 23 open issues now, not 25.**

## Your ask 3 (which of D/F parallelize) — answering this first since it shapes the rest

**Ready for a subagent right now, no decision needed first:**
- Epic D: #1258 (5-line env-var strip, already fully spec'd in its own issue), #1299(b) (verification + retry logic)
- Epic F: #1279, #1285, #1332, #1256 (all 4 confirmed genuinely isolated), plus #1216's interim fix (see below — I made that scope call)
- Epic B: #542 (token revocation — fully independent of the rest of the epic), #1260 (small, isolated, though it should go FIRST since #1241 needs it)
- Epic G: #1324 (env-var audit, fully mechanical)

**Needs a decision first, then parallelizable:**
- #1278 (Fly.io hosting) — needs a Postgres-hosting-strategy call (Fly-managed vs. keep external) before anyone can execute it
- #1305 (JSON/JSONB encryption) — needs a design call (selective-field encryption vs. accept queryability loss vs. searchable encryption) before implementation
- #1306 (file encryption at rest) — needs a storage-backend call (local envelope encryption vs. S3 SSE vs. full-disk) before implementation
- #1312 (schema drift) — needs Arch's co-review on per-column judgment calls + a multi-Base architecture decision; not purely mechanical the way the diff-count implies

**Not parallelizable — needs continuous single-person attention:**
- #1241 — this isn't an implementation task, it's a forensic audit across ~10+ content-store families that has to stay coherent in one head; fragmenting it across agents would produce contradictory findings
- #358 — infrastructure already exists (confirmed: `FieldEncryptionService`/`EncryptedString` are built and tested), but the remaining Phase 3 migration + credential-store wiring touches production data and wants careful, coordinated execution
- Epic E's #441+#1261 — see below, these should be one unit

I flagged #1305/#1306/#1278/#1312's decision gates but haven't made those calls yet — didn't want to rush 4 more architecture/design decisions in the same sitting as #1216. I'll make each as I reach it, or loop in Arch/PM first if it's consequential enough (encryption strategy and storage backend both feel like they deserve a beat, not a same-day snap call).

## Your ask 1 (sequencing sanity-check) — I substantially agree, with 3 refinements

Your proposed order (A → C-parallel → B-long-pole → D/F-batched → E/G-interleave) holds up under research. Refinements:

1. **Epic D shrank** — with #1168/#1176 closed and #1299 down to just (b), it's now ~1 day of work, not a 5-issue epic. Batch it early and fast rather than treat it as ongoing background work.
2. **#441 + #1261 should be one coordinated unit**, not independently interleaved — they share the password-reset token service and email flow; doing them separately risks rework on the same code paths.
3. **#1312 wants to ride alongside Epic B, not G** — it needs Arch's attention the same way B does (per-column judgment + a real architecture call), and Arch's bandwidth is already the scarce resource there. Sequencing it with the mechanical G issues (#1283, #1324) undersells what it actually needs.

## Your ask 2 (bottom-up estimate) — ranges, not a date, with the real uncertainty named

| Epic | Rough range | Why the range is wide (or isn't) |
|---|---|---|
| A | 1-2 days | Well-diagnosed, bounded, low uncertainty |
| B | 9-16 days | **The real uncertainty driver.** #1241 is an audit whose *output* is more work (new issues), not a fixed-scope task — could land anywhere in that range depending what it finds. #1305/#1306 depend on undecided design calls. |
| C | 3-5 days | My own active thread; OAuth redirect-orchestrator + write-path migration, not fully scoped yet myself |
| D | ~1 day | Shrank today; mostly done |
| E | 2.5-3.5 days | Treating #441+#1261 as one unit |
| F | 1.5-2.5 days | #1332 is a debugging task (race/transport bug), not a mechanical fix — that's the one soft number in this epic |
| G | 2.5-3.5 days | Includes Arch co-review time on #1312, not just coding time |

**Total raw effort: roughly 21-33 days if serial.** But A/C/D/most-of-F/parts-of-G can run alongside B via subagents once B starts, so **wall-clock is closer to 3-5 weeks** — B is the actual critical path, and its own range (9-16 days) is most of that spread. I'd treat the lower end as optimistic and the upper end as "if #1241's audit surfaces a lot" — not padding, a real reflection of what's still unknown until that audit runs.

## Ready to start

Epic A first, as agreed. Let me know if the #1305/#1306/#1278/#1312 decision points should come to you/Arch on a schedule, or if you want me to just make each call as I reach it and report after.

— Lead
