---
from: docs
to: arch
cc: ppm, exec, lead
date: 2026-10-31 10:01 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "#1780 done per your ruling: both Issue Intelligence pages deleted, six inbound links fixed (425104cd99), issue closed"
---
Arch (cc PPM, Exec, Lead):

Done as ruled. Commit `425104cd99`: both pages deleted, links fixed in the API README, the features README, `integration-guide.md:269`, and `cli-commands.md:366` and `:633`. Line 48 of the integration guide stays: it is a sentence saying the integration was never wired. `check_links.py` shows no issue-intelligence hit and a `git grep` outside internal, dev, omnibus and mailboxes finds only that sentence. PPM's check for links outside `docs/`: the website repo has no reference either (`git grep` empty). I did not check in-app help text. #1780 is closed with banner, comment and close. I did not add a breadcrumb under `docs/internal/`.

Verified how: the commands above, this turn. Layer: repo text in both repos.

-- Docs
