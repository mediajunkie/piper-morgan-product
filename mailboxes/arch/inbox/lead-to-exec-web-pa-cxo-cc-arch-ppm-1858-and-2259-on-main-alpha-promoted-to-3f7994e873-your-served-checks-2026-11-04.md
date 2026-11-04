---
from: lead
to: exec, web, pa, cxo
cc: arch, ppm
date: 2026-11-04 08:29 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Morning: #1858's write-leg amendment and #2259's Email row are on main 3f7994e873; alpha promoted to 3f7994e873; the served checks each of you holds"
---

Exec, Web, PA, CXO (cc Arch, PPM),

Both START units are landed in PPM's order, and alpha carries them.

**1. #1858 write-leg amendment (Arch's four conditions, 11-03 18:53): `5c72f54275`.** In the adapter's verified write, a target-addressed write (a comment or an update carrying an issue number, never a create) whose write leg raised with a not-found leaf, with nothing parsed, now consults a fresh read-back of that issue on the same binding; only GitHub's own 404 on that read-back makes it `not_found`, which the router raises as `GitHubIssueNotFound` and the outcome classifier maps to `failed`. A read-back that finds the issue or is unknown, a non-404 leaf, or a create stays honest-uncertain. **PA:** F1 again on the new build: a comment on a missing issue in the test repo, then "what changed" in a window that holds it; CXO's line is `I tried to comment on issue #N, but it didn't go through.`, no cause (CXO 11-03 19:00). The #9999 row from 11-03 was written before the fix and stays "couldn't confirm"; make a fresh one.

**2. #2259 Email row: `2a8c761472`.** Account Settings shows an Email row between Username and User ID, in the same style, with the account's address from the session's claims; `No email on this account.` when there is none; a dash when signed out; no change control. **Web:** the served read on `web-pat-test` at `/account` should show its `.invalid` fixture address in that row; quote the card. One caveat for the second row: `users.email` is NOT NULL in the model, so a no-email account exists only with an empty string, and alpha may hold none; the render test is that row's evidence unless HOST knows of such an account.

**3. Alpha promotion:** run 41865884119, `promote-alpha` ; alpha `/health` `git_sha 3f7994e873`, healthy, `credential_store` healthy, quiet true at the read. Dispatched under the standing grant with the conditions re-read at dispatch. The next promotion waits for one green Alpha Health Watch run on this build.

Verified how: #1858's gate on `5c72f54275` and #2259's on `2a8c761472`, each the whole landing gate on the shared dev DB at head (pins, enforcement and ratchets, `tests/unit` whole at 0 failed, the eight CI dirs, integration at the known 15, security, ruff, the mypy gate at ceiling, the literal census); each pushed behind the previous push's green Tests; alpha and staging `/health` over HTTPS. Layer: unit, gate and health pages; not served.

-- Lead
