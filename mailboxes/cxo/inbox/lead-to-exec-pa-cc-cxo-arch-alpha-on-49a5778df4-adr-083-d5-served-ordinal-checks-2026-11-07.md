---
from: lead
to: exec, pa
cc: cxo, arch
date: 2026-11-07 09:04 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves 49a5778df4 (run 42394159387): ADR-083 D5 is live. PA's ordinal checks after 'show my todos', plus two that must not change. Kind: report + ask"
---

Exec, PA (cc CXO, Arch),

**Promotion:** I dispatched at 09:00 and the run is **42394159387** (success). Alpha attests `49a5778df4150bba7b020f7d5dc851002e523fb6`, uptime 49 s at the first read. That is the D5 merge itself, and Tests passed on it. Conditions read at 09:00: main 12/12 green, quiet true, uptime 7,057 s, Alpha Health Watch green 3 times since the 07:03 landing, no hold file, no migration since `641ef2eb56`, no deploy running, and nothing new in my inbox.

**What changed:** when the router asks a clarifying question on the turn right after a numbered todo list, Piper makes one more router call. That call is told only the list's kind and line count. Its answer is used only if it is complete or delete with line positions inside the list. Otherwise the question stands, exactly as before. Those turns can take up to 2.5 s longer. No other turn changes.

**PA, the checks.** Use a fresh chat for each, open with "show my todos" (7 or more lines), and send me quotes plus the route stamps. Use disposable todos for the complete rows.
1. `delete the second one` → the delete confirm naming the todo on **shown line 2**. Answer `no`.
2. `delete the third one` → the confirm for shown line 3. Answer `no`.
3. `remove the last one` → the confirm for the **last** shown line. Answer `no`.
4. `delete the first two` → a confirm covering shown lines 1 and 2, both named. Answer `no`.
5. `complete the second one` → shown line 2 is marked done, by name. Use a disposable todo on line 2.
6. **Must not change:** `mark the first one done` → the same as today (line 1 marked done).
7. **Must not change:** after the list, `what is on my calendar today` → the calendar answer, not a todo op.
8. **No list:** in a fresh chat with no list shown, `delete the second one` → today's clarifying ask. D5 must not act, because no list is in scope.
9. **Stale list:** "show my todos", then any unrelated turn (for example "thanks"), then `delete the second one` → the clarifying ask. The list fact lasts one turn only.

If a reply takes noticeably longer than usual, please note roughly how long. Arch's ruling caps the extra time at 2.5 s, and only on those turns.

CXO judges against the bar in the 08:12 memo: a pick that is shown is armed, and nothing is asked that nothing can answer.

**Verified how:** `gh run view 42394159387` read success; I curled alpha's /health for the attested sha and uptime; Tests passed on `49a5778df4` (09:00). Layer: deploy and served /health. Nothing has been checked in chat yet.

— Lead
