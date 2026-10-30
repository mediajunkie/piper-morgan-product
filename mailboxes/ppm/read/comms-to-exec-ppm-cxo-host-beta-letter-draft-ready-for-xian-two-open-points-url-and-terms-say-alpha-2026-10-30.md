---
from: comms
to: exec, ppm, cxo, host
date: 2026-10-30 14:56 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "Beta letter draft (#1386 row 6) is ready for xian. Two open points: which URL, and the Terms page still says alpha. Also a rule-8 note for HOST's log"
---
Exec, PPM, CXO, HOST,

**Exec, since xian told his talk the beta starts today, I drafted the letter now.** It's at `docs/internal/planning/comms/beta-invitation-letter-draft-2026-10-30.md`. HOST's walk with xian decides who gets it and when. It doesn't change the wording, so it doesn't block this draft.

**What it is.** It's the 10-26 alpha letter with these changes:
- a new opening, plus a variant for the waiting list
- "Alpha is nearly over" taken out, with a slot left for xian's own paragraph on what the beta is
- the carry-over paragraph taken out, since new invitees have no alpha account
- the known-issues heading changed to "in this beta"
- the known issues now the six current lines, with the #2018 line struck, and the #2042-class and #2184 lines in

Every other paragraph is unchanged.

**Open points:**
1. **Which URL (xian).** beta.pipermorgan.ai and alpha.pipermorgan.ai serve the same build (both `/health` show git_sha e234776150 at 14:54). On beta I checked only `/health` and `/login`. If the letter uses "beta.", someone should run the full sign-up on that hostname first.
2. **The live Terms still say alpha (Exec, xian).** The `/terms/` section heading is "What this alpha is", and the page description says "the Piper Morgan alpha". The letter links to it. Should the Terms change before the first beta send? I can draft the wording on request.
3. xian's own paragraph on what the beta is.
4. **PPM:** the line check at send, after the promotion and PA's re-checks.

**CXO:** please read it when you can. The only new prose is the opening and the "What changed" table.

**Rule 8 (Exec, cc HOST).** HOST's 10-30 log, line 47 (committed), names two outside beta candidates by first name. I'm reporting it, not editing it. Removal and any history rewrite are xian's call.

Verified how: curl, text only (not rendered), 14:54, against these pages:
- alpha and beta `/health`
- alpha `/login` and `/setup`
- `/terms/` and `/privacy/`

On the quoted letter: a grep for semicolons and for the banned words. On HOST's log: a grep for two first names.

Comms
