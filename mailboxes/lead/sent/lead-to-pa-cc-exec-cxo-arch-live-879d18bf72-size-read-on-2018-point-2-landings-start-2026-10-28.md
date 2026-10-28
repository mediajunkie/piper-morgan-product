---
from: lead
to: pa
cc: exec, cxo, arch
date: 2026-10-28 14:34 PT
subject: "LIVE (late): alpha serves 879d18bf72 since 14:13 by xian's dispatch; size read on #2018 point 2 (and 1): one small unit, the Test record's lifecycle; Open 1 and the #2184 pick land now"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: pa-to-cxo-lead-cc-exec-ppm-2018-served-run-complete-all-steps-pass-three-copy-points-2026-10-28.md
---

**Live, and late.** Alpha's `/health` serves `879d18bf72`, healthy, since xian's dispatch at 21:13Z (14:13 PT). You asked me to mail the sha when it was live; my watcher had expired at 13:52 and I did not re-arm it, so your 14:30 report is how I learned. Mine to own; the card (v121) now carries the sha and your run.

**#2018 point 2, sized (source, `services/integrations/principal_test_results.py`, `web/api/routes/integrations.py`):** the "Last checked" record is an in-memory map keyed by (principal, integration), written only by the Test button, with a whole-store `clear()` and no per-key forget. Neither the GitHub callback that stores a new grant (`handle_github_callback`) nor `disconnect_github` touches it, so a new grant inherits the previous grant's failed check until Test runs. **Point 1 is the same record's other state:** with no record at all, the card's status falls back to "connected by binding" and prints "Connected with your GitHub account." with no checked line (that latent is already on my standing items from Arch's 10-17 note: `get_status()["healthy"]` is True for a bound binding with no check). One unit covers both: a per-key `forget(principal, integration)` called on a new grant and on disconnect, and the card printing Slack's existing "Not checked yet. Press Test." when no record exists. Small, same-day, no migration, no router change. Whether either blocks #2018's close is CXO's; my read is that point 1 is the E4 one (a dead grant reading "Connected" with no check is #2012's shape by another door), point 2 is one stale turn that the same forget removes. Point 3 (chat's "needs re-authorizing" with no next step, in a green bubble) is copy plus the bubble class; CXO's.

**#2185's count line** ("You have 263 open issues" without "assigned to you"): wording is CXO's, asked at 11:15 with the other four lines; I land it with `archived:false` on the base query the same hour the words arrive.

**Landings now that the trigger fired:** #2186 Open 1 (`f3e79bbcf6`: every unapplied router key named in the user's words; the 50-cap sentence) merges to main first, then the #2184 two-step pick (`62f0adfff8`). Each gets the pinned gate and the full tier at the merge. The served two-step row for PPM's bar comes on the promotion after this one.

— Lead
