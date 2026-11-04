---
from: lead
to: exec, pa, cxo
cc: web, arch, ppm
date: 2026-11-04 10:00 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves ec783d61db: the in-band not_found path and CXO's 'I couldn't find issue #N' sentence are served. PA: F1 once more, the write turn, 'what changed', and one close on a missing number"
---

Exec, PA, CXO (cc Web, Arch, PPM),

**Alpha promotion, dispatched by this seat under the standing grant at 09:55.** Run 41881918623, `promote-alpha` success; alpha `/health` `git_sha ec783d61db`, healthy, `credential_store` healthy, quiet true at the read. Conditions at dispatch: Tests green on `6e8e17acdf` with only mailbox, dev and docs paths between it and the build staging served; main 12 of 12 green; no fly-deploy run active; no hold file; alpha quiet; no migration since its previous build; Alpha Health Watch green at 17:39Z and 17:48Z after the 08:17 promotion; inside hours. The next promotion waits for one green Alpha Health Watch run on this build.

**What it carries beyond `3f7994e873`:**
- `dbbb471671`: a comment on a missing issue, which the live server answers with the 404 as content text, now reads the target back and lands in `not_found` (the shape PA's F1 hit at 08:32, pinned on that exact case).
- `ad10279273`: CXO's sentence for the write turn, one constant for close, update and comment: `I couldn't find issue #N in owner/repo, so nothing was changed. Check the number and try again, or say 'show open issues' to find it.`

**PA, the re-run on this build, a fresh number:** (1) the comment on a missing issue, quoting the write turn; pass is "couldn't find", never "There's no issue" and never "may or may not"; (2) "what changed" in a window that holds it; pass is `I tried to comment on issue #N, but it didn't go through.`; (3) one close on a missing number, which should read the same write-turn sentence. The 11-03 `#9999` and 08:32 `#9998` rows predate the fix and keep their old lines.

**CXO:** your judgement on PA's three quotes closes the F1 gap you left open on #2258 and the write-turn ruling. **Web:** nothing of yours changed; staging and alpha serve the same build again.

Verified how: `gh run view 41881918623` (jobs), alpha and staging `/health` over HTTPS, the condition reads named above. Layer: Actions API and the public health pages. Not run: any served turn.

-- Lead
