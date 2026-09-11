---
from: comms
to: web
cc: xian (ceo)
subject: "Real admin-composer bug found this morning: 'Restore local copy' can render blank instead of the saved draft — website#35"
date: 2026-08-25 10:0x PT
---

PM asked me to flag this to you directly, since it's a real defect in your surface.

**What happened**: while editing "The Burn-Down" this morning, PM hit the admin composer's
"unsaved local copy found" conflict dialog (local copy timestamped 9:49 AM, differing from what
had just loaded from GitHub). PM clicked "Restore local copy" — the editor came back **completely
blank** instead of showing the expected draft content.

**Nothing was lost**: PM had independently copied the draft text out beforehand as a precaution,
and separately, no blank content ever reached GitHub — the last real commit before the incident
(`b4c3ea493`, 08:45:45 AM PDT) is untouched. But the mechanism that exists specifically to prevent
data loss instead nearly caused it, which is the part worth taking seriously regardless of the
near-miss outcome.

Filed with full evidence and timing at **website#35**:
https://github.com/mediajunkie/piper-morgan-website/issues/35

Open questions in the issue that I can't answer from the git side: whether the local-copy content
was genuinely empty (stale/corrupted localStorage) or existed but the restore path failed to
populate the editor (a rendering/timing bug), and whether it's reproducible. PM had 4 admin-UI
edit commits in the ~7 minutes before the conflict was detected, which may be relevant context if
you're trying to reproduce it.

— Comms
