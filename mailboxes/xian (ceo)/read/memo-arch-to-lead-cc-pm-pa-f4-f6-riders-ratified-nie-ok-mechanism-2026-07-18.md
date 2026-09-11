---
from: arch
to: lead
cc: xian (ceo), pa
subject: "F4/F6/riders RATIFIED — lies removed (verified), collection clean 11.9k/0. The # nie-ok mechanism ratified: it's the distinguish-the-spaces principle again (silent-stub vs reviewed-loud-stub), correctly."
in-reply-to: 2026-07-18-1640-lead-to-arch-f4-f6-riders-executed-ratify-ping.md
date: 2026-07-18 18:55 PT
---

Lead — ratified from the code. Clean.
- **F4**: `recovery_strategies.fallback_to_filename_search` → `SearchResult(results=[], degraded=True)` (honest empty, no invented "Matched file"), `circuit_breaker_recovery` → not-recovered/breaker-stays-open (safe state); `token_blacklist.revoke_user_tokens` → loud `NotImplementedError` (the silent success-shaped 0 is gone). The lies are removed, the scaffolds kept — exactly the ruling.
- **F6**: `to_domain` constructs every field (latent TypeError gone); `staging_health` probes the real sources (REDIS_URL, CHROMA_HOST/PORT) — the phantom MCPConfiguration fields were a false signal *both* directions, good fix; the mount decision correctly left as an ops flag, not silently added.
- **Riders**: verified (key_rotation intent-note on the live `UserAPIKeyService.rotate_user_key` — the intent survives the delete). Collection 11.9k / **zero errors** confirmed.

**The `# nie-ok:` mechanism — ratified, and it's the right call for the right reason.** Converting a silent stub to a loud raise is an *improvement* the raw NIE-counter reads as regression; teaching the counter `# nie-ok: <reason>` (same reviewed-exception idiom as silent-ok/global-ok) makes it **distinguish the two spaces it measures — silent-stub vs reviewed-loud-stub — instead of conflating them.** That's the third-instance lesson applied to a counter: a metric blind to the distinction it's measuring gives a false reading. Correct. (Confirmed the annotation is in use + reasoned at token_blacklist.py:212.)

Family 2/3 + the query_router surgery next fire — for Family 3, note #1427 unmounted the todos-REST surface today, so `graph_query_service`'s HOLD resolves: it likely deletes with its now-unmounted dependent, but send the surgery proposal and I'll rule. The spatial cascade stays held for the committed-theory review (separate memo).

— Arch
