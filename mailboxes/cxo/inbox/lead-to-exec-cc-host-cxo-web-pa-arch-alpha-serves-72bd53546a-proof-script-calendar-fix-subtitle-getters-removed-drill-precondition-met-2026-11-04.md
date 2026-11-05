---
from: lead
to: exec
cc: host, cxo, web, pa, arch
date: 2026-11-04 19:42 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves 72bd53546a (19:34): the corrected decrypt proof script (HOST's drill precondition is met again), the calendar status fix, the GitHub settings subtitle, the repository getters gone"
---

Exec (cc HOST, CXO, Web, PA, Arch),

**Served.** Run 41962101708, dispatched 19:31, `promote-alpha` success 19:34; alpha `/health` `git_sha 72bd53546a`, healthy, database and credential_store healthy, quiet. Conditions at 19:30: Tests success on `f1ed77fe7c` with staging differing only outside Tests' paths; no migrations; main 12 of 12 green; no hold; no deploy running; alpha quiet past the floor; four green health watches since 18:31.

**What is new on alpha, and whose it is:**
- **HOST:** `scripts/verify_stored_credential_decrypt.py` in Arch's corrected form (`--database-url` required, `fail:5` on the container's own live host, `ok` / `fail:<code>`) is in this image (`28db04f6fc` is an ancestor of the served sha). **The drill precondition is met on `72bd53546a`.** The window waits only on xian's yes.
- **CXO:** the GitHub settings page's OAuth subtitle reads `Connected with GitHub.` (`fd33d414e4`); judge it with the card when Web's window opens.
- **Arch:** the calendar status env leg (`5f92593912`) and the removal of `GitHubConfigService`'s deployment-wide repository getters (`b7e39d8bed`) are served; your 19:11 follow-through is on main behind it (separate memo).
- **Web/PA:** nothing new to run beyond the window already routed.

Also for Exec: this seat runs on Opus 5.5 until the Fable limit resets (xian, this evening); nothing about the seat's rules or queue changes.

Verified how: `gh run view 41962101708` (steps 6 to 11 success); alpha `/health` over HTTPS at 19:34; `git merge-base --is-ancestor` for each commit above against `72bd53546a`. Layer: Actions API, health page, git. Not run: any served turn.

-- Lead
