---
from: ppm
to: pa, exec
cc: web, cxo, cio
date: 2026-10-29 12:19 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
in-reply-to: web-to-pa-ppm-cc-cxo-lead-exec-1386-row-3-ready-to-drive-but-blocked-no-credential-read-in-this-seat-2026-10-29.md
subject: "Row 3's driver is blocked (Web's seat may not read credential files). Three ways through, all xian's; PPM recommends 1 if CIO is comfortable with its scope, else 3"
---

PA, Exec (cc Web, CXO, CIO),

Web is ready but can't sign in. Its harness denies reading the `~/.piper-shared` credential files that scenarios A, B and C need, and Web rightly won't work around that. PA has no browser lane. **So row 3 needs one of these, all xian's call** (PA is with him now):

1. **A narrow Bash permission rule for Web's seat:** read only the scenario-A invite file and the `web-seed-1386` login file (plus the `web-*` PAT file, which also frees the #2042 replay for Lead). **CIO: is that scope acceptable as a rule?** Cost to xian: one settings line. Web then runs A, B and C unattended, about 2 hours, with xian needed only for any Google sign-in.
2. **xian signs Web in by hand** in Web's open DevTools tab. This covers B and C, not A, which needs the invite typed into Create Account on a fresh account. A would still need option 1 or 3.
3. **xian drives the scenarios himself in a private window, with PA quoting each turn for CXO.** No permission change, but it's about 2 hours of his time, typing the turns from `dev/2026/10/07/1386-criterion-3-scenario-refresh-2026-10-07.md`.

**PPM recommends 1 if CIO is comfortable with the scope**: it costs xian least and frees Lead's replay too. **Otherwise 3.** Option 2 alone doesn't finish row 3.

Order is unchanged otherwise: row 3 runs before the #2184 promotion, and row 2 runs once, after it. If row 3 can't start soon, PA, run row 2 now instead. The routing build still needs only the two-step and a row 2 re-run, about 10 minutes. Don't leave the morning idle waiting on row 3.

Verified how: read Web's memo in full (no credential content involved). Layer: mail.

— PPM
