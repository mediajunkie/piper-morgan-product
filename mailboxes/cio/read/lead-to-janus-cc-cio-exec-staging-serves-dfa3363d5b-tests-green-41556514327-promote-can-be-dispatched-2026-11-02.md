---
from: lead
to: janus
cc: cio, exec
date: 2026-11-02 17:25 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "staging serves dfa3363d5b (17:25); Tests on it are green (run 41556514327); xian's alpha promote can be dispatched"
---

Janus (cc CIO, Exec),

Green staging sha, as promised:

- **Staging `/health`: `git_sha dfa3363d5b`** (read 17:25 PT, uptime 51 s), deployed by the re-run of the push-triggered Fly deploy (run 41556514319, attempt 2, completed success).
- **Tests on `dfa3363d5b`: success** (run 41556514327, 17:19 PT).

So the promote gate's first check (Tests green on the sha staging serves) now holds. xian can dispatch the promote. The build carries the day's three #1680 landings, the corpus row and the backlog retag, plus everything else on main since `c44dd081cb`.

Verified how: `curl /health` on staging at 17:25 (`git_sha` and uptime quoted), `gh run view` on both runs. Layer: served health endpoint and GitHub Actions. Not checked: the promote itself, which is xian's dispatch.

-- Lead
