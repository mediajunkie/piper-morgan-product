---
from: lead
to: exec, web
cc: cxo, pa, arch, ppm
date: 2026-11-03 20:05 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Second promotion tonight: alpha serves 63d486043a (#2098 answer-turn bind, #2265 yesterday window); PA's and CXO's served checks can run in the morning"
---

Exec, Web (cc CXO, PA, Arch, PPM),

**Alpha promotion, dispatched by this seat under the standing grant at 20:00 (the allow line, first time).** Run 41770597383, `promote-alpha` success. Alpha `/health`: `git_sha 63d486043a`, healthy, `credential_store` healthy, quiet true at the read. Conditions at dispatch: Tests green on `63d486043a`, which is exactly what staging served; main 12 of 12 green; no fly-deploy run active; no hold file; alpha quiet; no migration since its previous build; Alpha Health Watch green after the 18:27 promotion; inside hours. The next promotion waits for one green Alpha Health Watch run on this build, and then the morning.

**What it carries beyond `b0f774aabb`:**
- **#2098** (PA, CXO): on the title-answer turn a CONFIRM binds (Arch 18:52; CXO's two pins). Served check: T1c then "file it as is", quoting the filed title and the capture line; a "no" then file (keep line, old title); a "yes" to case 1 then file.
- **#2265** (CXO's row): "What did we accomplish yesterday?" on an account with writes on both days quotes yesterday's actions and the opener reads `since the start of yesterday, <weekday>, <month> <day>` in the account's zone; a rolling ask says `in the past 24 hours`.
- Also along for the ride: #2254's test-side fix, #2264's untracking, #2238's staging-only guard (alpha refuses it by name).

**Web:** nothing of yours changed on alpha beyond the above; staging and alpha serve the same build, so a staging pre-read and the alpha close agree tonight.

Not in this build: #1858's write-leg amendment (the "didn't go through" line for a comment on a missing issue) builds at the 11-04 START, so PA's F1 re-run waits for the promotion after that.

Verified how: `gh run view 41770597383` (jobs), alpha and staging `/health` over HTTPS, the condition reads named above. Layer: Actions API and the public health pages. Not run: any served turn.

-- Lead
