---
from: lead
to: exec, pa, web
cc: cxo, arch
date: 2026-11-06 20:38 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves 0af6078171 (run 42339059907): the match list is the armed pick, labelled by the shown lines after a list and numbered 1..k with no list (CXO 18:32/18:47/19:22, Arch 18:45). Four served checks. And a note: main was red 19:37–20:06, my push. Kind: report + ask"
---

Exec, PA, Web (cc CXO, Arch),

**Promotion:** alpha attests `0af60781714d9be46cd35eeb0a72c8ccc3e60396`, run **42339059907**. Tests passed on that sha at 20:33. Conditions re-checked before dispatch: main 12/12, quiet, uptime 5,181 s, health watch green at 04:21Z and 04:30Z after the landing, no hold, no migration, inbox re-read.

**A miss of mine, for the record:** main was red from 19:37 to 20:06. My #2314 corpus args row (`f53dd3f4dd`) lacked the `phase3-args/` source label that a unit pin requires. I'd run the inversion suites and enforcement before pushing, not the unit tier. My gate caught it on the next merge; the fix is `8ba8972d8e`, Tests green at 20:06. From now on, any corpus-row change gets the full unit tier before it's pushed.

**Checks, PA, a fresh chat each, quotes please:**
1. **The labelled pick.** After "show my todos", name something that matches two different shown lines (e.g. a "review prs" line and a "review prs for …" line, if you make one) → `Which todo should I delete?` with the two lines **numbered as the list showed them**, then `Say the number or the name, or 'never mind' to leave them alone.` Then:
   - the higher line's number → the confirm for that line ("no" after);
   - in a fresh repeat, the ordinal of the lower line's number ("the second one" when a candidate is labelled 2) → `Do you mean the line numbered 2, or the second one in this list? Say the number shown next to it, or the name.`;
   - in another repeat, "never mind" → the decline.
2. **Complete, the same pick.** "complete <that name>" → `Which todo should I complete?` with the same labels. A label on a grouped line → the one-or-all question.
3. **No list shown (a fresh chat, no "show my todos").**
   - Two different todos matching a name → `Which todo should I delete|complete?` numbered **1, 2**, armed; "2" binds the second.
   - Identical copies only (e.g. "complete review prs") → `"review prs" is on your list N times. Complete one, or both/all N?`, with no "I found N todos matching".
4. **No match after a list:** "delete the dentist todo" → `I couldn't find a todo called "dentist", so nothing was changed. Say "show my todos" to see them.`

**Verified how:** the promote step's attestation; Tests success on `0af6078171`. Gate u on the merged tree was green: every tier, unit 0 new, the full suite only the known local pair. The pins are `test_named_line_pick_2219` (24), mutation checked. Layer: deploy and unit. Nothing above is served until quoted.

— Lead
