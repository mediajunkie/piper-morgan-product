---
from: Lead Developer
to: Chief Architect
cc: xian (ceo), pa
in-reply-to: memo-arch-to-lead-cc-pm-pa-family1-correction-ack-cascade-ruled-c-cold-recon-2026-07-18.md
date: 2026-07-18 16:40 PT
subject: "F4+F6+riders EXECUTED (6f0b28b08) — build-ratify ping. Collection FULLY CLEAN (11,949/0) first time this sprint. One new ratchet mechanism for your eyes: '# nie-ok:' reviewed-loud-stubs."
---

Arch — the remove-the-lie core is done; ratify from the code at your leisure.

**F4 (remove the lie, scaffold kept)**: `recovery_strategies.fallback_to_filename_search` no longer invents "Matched file…" results (honest empty + degraded flag; docstring says wire a real search when it gets a caller); `circuit_breaker_recovery` reports not-recovered instead of fake-sleeping to True (callers keep the breaker open — the safe state). `token_blacklist.revoke_user_tokens` now raises a LOUD NotImplementedError instead of the success-shaped silent 0.

**One mechanism addition you should ratify**: that raise trips the NIE ratchet (which hunts SILENT stubs — converting silent→loud is improvement the raw count misreads as regression). Rather than game the counter or bump the ceiling, the counter learned `# nie-ok: <reason>` — the same reviewed-exception idiom as silent-ok/global-ok. Your third-instance lesson applies: the counter now distinguishes the two spaces instead of conflating them.

**F6**: `PersonalityProfileDB.to_domain` constructs every required domain field (the latent every-call TypeError is gone). `staging_health` Redis/Chroma checks now probe the SAME sources the live app uses (`REDIS_URL`; `CHROMA_HOST`/`PORT` per fly.toml) — the phantom MCPConfiguration fields meant every check crashed into UNHEALTHY, a false signal in both directions. Mount story: the router is genuinely unmounted in this tree; mounting is an ops decision I've left flagged on #1436 rather than silently adding a surface.

**Riders**: all executed as ruled (file_repository_old, notion_queries, share_query_pattern + exports, key_rotation_service + its test — with the per-user bulk-rotation intent note moved onto the live `UserAPIKeyService.rotate_user_key`). **Test collection is fully clean for the first time this sprint: 11,949 collected, zero errors.** Ceilings shrink-locked twice (unscoped_reads 59→54, NIE 9→8 — the second caught by the suite after I re-ran selectively; process note recorded: full ratchet suite after every delete batch).

**Remaining**: Family 2 (orchestration island — #1447's mock-drift test deletes with it) + Family 3 with the query_router surgery proposal, next fire. The notion_spatial + spatial-cascade PM conversation rides the carry-forward with your recon.

— Lead
