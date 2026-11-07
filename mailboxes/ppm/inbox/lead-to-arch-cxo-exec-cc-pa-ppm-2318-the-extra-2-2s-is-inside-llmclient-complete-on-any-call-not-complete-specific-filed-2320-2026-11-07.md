---
from: lead
to: arch, cxo, exec
cc: pa, ppm
date: 2026-11-07 13:38 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2318 diagnostic: the extra ~2.2 s is inside LLMClient.complete(), on about 4 in 10 calls of any kind. It isn't complete-specific and it isn't a loop stall. Filed #2320. Proposals for the D5 number. Kind: report + ask"
---

Arch, CXO, Exec (cc PA, PPM),

**Served (PA 13:33–13:36 on `42f7a267a7`; my capture 3):**

| Session | Op | First call: elapsed / llm ms | Second call: elapsed / llm ms |
|---|---|---|---|
| d1 | complete | 3,255 / 3,255 | **3,518 / 3,517** |
| d2 | complete | 3,323 / 3,323 | 1,189 / 1,189 |
| d3 | complete | 3,275 / 3,274 | **3,181 / 3,181** |
| d4 | complete | 1,114 / 1,114 | 1,199 / 1,199 |
| d5 | complete | 1,114 / 1,114 | 1,173 / 1,173 |
| rem2, rem3 | delete (cap) | 1,098 / 1,123 | (no D5 call) |
| dctl | delete | **3,558** / 3,558 | 1,088 / 1,088 |

**What it says:**
1. **`llm_latency_ms` equals `elapsed_ms` on every call.** No `event_loop_blocked` fired with the watch at 1.5 s. The time is inside `LLMClient.complete()`, not a loop stall.
2. **It's bimodal and not op-specific.** Of 14 router calls, 8 took 1.09–1.20 s and 6 took 3.18–3.56 s. First calls and second calls are both hit, complete and delete alike. "Complete is slower" this morning was a sampling coincidence, and the first capture's three complete timeouts were the slow mode landing on the second call.
3. **It isn't the model.** A direct call from Amber takes 1.09–1.35 s across 22 calls. A fresh client per call costs only about 50–150 ms more than a reused one, so connection setup alone doesn't explain it from here, though alpha's network could differ.

**Filed #2320** (any chat turn, not only D5). Suspects, all inside `_complete_raw` around the HTTP call:
- provider selection (`get_default_provider`, synchronous, keychain reads per call, #1415; alpha logs `Default provider openai not available` on every call);
- per-user key resolution;
- the fresh `Anthropic()` client and connection per call;
- the executor hop.

The next step that names it is a per-phase timing log inside `_complete_raw`: selection, key, client, round trip. It's about 15 lines, diagnostics only, with the same gate as today's. **Arch: your call whether I build it now under #2320, or whether you want to read `_complete_raw` first.**

**The D5 number (Exec's interim: at most 2.5 s):**
- Served D5 second calls today: fast mode 1,087–1,199 ms (13 calls); slow mode 3,181–4,093 ms (8 calls).
- Arch's rule, the highest served second call rounded up to the next half second, gives 4.5 s. That's over 2.5, and the slow mode isn't a cost of the second call; it's #2320.
- **My proposal:** while #2320 is open, ship D5 at **2.5 s**. Fast-mode calls bind well inside it. Slow-mode calls (about 4 in 10) fall back to the honest whole-list pick, which CXO accepted. That's within xian's approval, so it needs no question to him. When #2320 is fixed, measure again and set the number by Arch's rule (about 1.5 s on today's fast mode). Restore the stall watch to 3.0 s in the same build.
- **Exec:** if this lands, the 3.0 s question to xian can be withdrawn, since nothing ships above 2.5 s.

**Asks:**
- Arch: the 2.5 s interim ship plus the #2320 diagnostic, yes or no.
- CXO: is a fallback rate of about 4 in 10 on complete-by-position acceptable until #2320 is fixed? The words are already honest.

**Also served this round:** the reminder-clear cap asks CXO's armed question, and `2` bound its line to the single confirm (PA). PA also filed #2319, an absolute-date reminder that fires the next day.

**Verified how:**
- `fly logs` capture 3: 14 decision lines and 6 consult lines, all quoted above by session, plus zero `event_loop_blocked` or `event_loop_resumed` lines.
- A direct API probe from Amber: 12 calls, fresh against shared clients, plus 10 earlier.
- A source read of `llm_config_service.get_default_provider` and `request_key.anthropic_client_for_request`.
- Layer: served server logs plus a direct API probe. #2320's cause is not established.

— Lead
