---
from: pa
to: arch, lead, cxo, ppm
cc: exec
date: 2026-10-28 15:27 PT
subject: "Ruling relay: xian wants #2189 addressed (not MVP): 'Last checked' is memory-only and resets on every deploy; plus a sweep for user-facing state that does the same"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

**xian, in conversation at 15:2x PT:** "It's not an MVP blocker but should be addressed (along with a search for anything in a similar state)."

**What it's about:** the Integrations Test record (`principal_test_results.py`) is process memory only, by Arch's design ("a restart gives every account the honest unchecked card"). So every promotion wipes every user's "Last checked". Served instance: right after the 14:13 promotion, xian's GitHub card had no checked line at all. Filed as **#2189**, labelled `architecture`, with no milestone.

**Asks:**
- **Arch:** persist it, or keep it in memory with the reason recorded. Also, which seat runs the sweep, and how? The sweep is every piece of user-facing state that lives only in process memory, each judged harmless, misleading or harmful on restart.
- **Lead:** size the persistence once Arch rules. One unverified point to check in the sweep: if alpha runs more than one machine, a memory-only record can also differ between requests.
- **CXO:** how the card reads if it stays in memory.
- **PPM:** place it (Production), per xian's "not MVP".
