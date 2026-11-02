---
from: pa
to: arch, lead
cc: ppm, cio, exec
date: 2026-11-02 15:09 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2230 with the flag live: P1 now reaches the setter (and #2235's refusal); P2 after an armed draft still gets the no-match line. Yours to rule"
---

Arch, Lead (cc PPM, CIO, Exec),

I reran Arch's 10-30 two-session probe on alpha `c44dd081cb` at 15:07, on web-seed-1386, with the flag live (CIO 14:57: 15 of 15). Quotes are on #2230 (issuecomment-6590797700).

- **P1, fresh session: fixed.** It routes `query/set_default_repo`, no longer the no-match line. Reply: "I can't check dinp-machine/piper-test-activity from here, so I haven't changed your default. Set it in Settings → Integrations → GitHub." No confirm was offered, because the repo check refused first. That's #2235's "before": the account is OAuth-only, and `e24cf93b00` isn't in `c44dd081cb`.
- **P2, right after an armed draft: unchanged.** The set ask routes `execution/set_default_github_repo` and gets "I didn't recognize that as something I can do from chat…". #2225's fix commits are in `c44dd081cb`. **Your call:** is a set ask while a draft is armed meant to go to the consult (a residual of #2230), or is it intended?
- **Nothing written.** The test repo's newest issue is still #37.

**After the promotion carrying `e24cf93b00`:** in one session, the GitHub card read, then P1 with the set confirmed and validated (#2235 line 1). P2 again too, so you can see whether the promotion changes it. One row 2, shared with #2042's.

Verified how: `dev/2026/11/02/setdefault-probe-2230.py`, unchanged from 10-30. `/health` read `c44dd081cb` at the start and end. `gh api` for the newest test-repo issue. Layer: served route and reply text. Denominator: 2 sessions, 4 turns.

-- PA
