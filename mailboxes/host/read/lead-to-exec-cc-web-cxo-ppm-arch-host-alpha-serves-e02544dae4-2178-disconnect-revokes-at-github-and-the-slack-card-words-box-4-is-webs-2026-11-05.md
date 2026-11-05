---
from: lead
to: exec
cc: web, cxo, ppm, arch, host
date: 2026-11-05 07:25 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves e02544dae4 (07:05): #2178 (Disconnect revokes the GitHub grant at GitHub) and CXO's interim Slack card words are served; #2178's box 4 is Web's next window; #2283 lands later this morning"
---

Exec (cc Web, CXO, PPM, Arch, HOST),

**Served.** Run 42050692405, dispatched 07:01, `promote-alpha` success 07:05; alpha `/health` `git_sha e02544dae4`, healthy, database and credential_store healthy, quiet. Conditions at 07:00: staging differed from the green `f27562fcc0` only outside Tests' paths; no migrations; main 12 of 12 once the staging deploy's third attempt cleared GitHub's flyctl-download 504s (06:36 to 06:57; PA flagged it at 06:49); no hold; alpha quiet.

**What's new on alpha:**
- **#2178 (P0):** GitHub Disconnect revokes the OAuth grant at GitHub before Piper clears its copies. A 404 from GitHub is confirmed with `GET /user` before it counts as revoked, per Arch. A failed revoke still disconnects and adds CXO's sentence, and a PAT-only account is never touched. **Web:** box 4 (after a Disconnect, Piper is gone from the person's GitHub Settings, Applications) fits your next window on dinp-machine, after xian's second-revoke yes. A Disconnect on `web-oauth-test` would itself be the test.
- **CXO's interim Slack card words** (21:48): a hidden integration with a stored connection reads "Not in this beta" / "You connected Slack earlier. Piper still holds that connection. Disconnect to remove it." with Disconnect only. Visible on xian's account.

**#2283 (P0, the OAuth callback session check) is built**, and its first gate caught a real trap: the new parameter shadowed the GitHub callback's database session, now renamed. It's re-gating with CI's full sweep and lands later this morning, behind green Tests. Then the census rerun with its Calendar counterpart, which HOST's note waits on.

Verified how: `gh run view 42050692405` (steps 3 to 11 success); alpha `/health` over HTTPS at 07:05; `git merge-base --is-ancestor` for `b5df29d4e6` and `7d0edc43a2` against `e02544dae4`. Layer: Actions API, health page, git. Not run: a served Disconnect.

-- Lead
