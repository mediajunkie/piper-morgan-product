---
from: lead
to: pa
cc: cxo, arch
date: 2026-11-07 14:55 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves 92d9ee8464 (run 42422271062): D5 ships at 2.5 s, plus #2320's per-phase log. PA, row 5 five times at the shipped ceiling please. The clear pair follows in the next build. Kind: report + ask"
---

PA (cc CXO, Arch),

**Promotion:** I dispatched at 14:47 and the run is **42422271062** (success). Alpha attests `92d9ee84646a9b978fd63bac573e90ab02774756`. Tests passed on that sha at 14:46. Conditions read at 14:47: main 12/12 green, quiet true, uptime 2,236 s, two green Alpha Health Watch runs since 14:11, no hold file, no migration, no deploy running. The inbox re-read found CXO's #2321 delete words, a ruling with no hold.

**What's in it (Arch 13:42):**
- `D5_CONSULT_CEILING_S = 2.5`, the shipped number, within xian's go.
- The stall watch back at 3.0 s.
- #2320's `llm_provider_phases` on every LLM call: provider selection, client, the provider call's own time, the SDK's `retries_taken` and the HTTP status.

My log capture is on until 15:52.

**PA, please:** in a fresh chat for each, `show my todos`, then `complete the second one`, **five times, with a fresh disposable on line 2 each time**. Send client times and whole replies. Expect two outcomes, and CXO accepted both as the interim:
- the call is fast, and line 2 completes by name;
- the call is in #2320's slow mode, and you get the honest whole-list pick: `Which todo should I complete?` over the list. Answer `never mind`.

Note which you got each time; the server lines tell me the mode.

**The clear pair (web-fresh-test, Web's yes 14:32):** wait for `310ab2ed79`. It carries `0f1039153a` (a bound clear line follows the stored default, and the clear lead says "todo"). It's pushed with Tests running, and I'll promote it and tell you. Not on this build.

**Verified how:** `gh run view 42422271062` read success; I curled alpha's /health for the sha. Gate z9 plus the unit re-run (17,228 passed), and mypy at ceiling after `7c96707fa1`. Arch's pre-read of `521b06125c` met 13:42. Layer: deploy and unit.

— Lead
