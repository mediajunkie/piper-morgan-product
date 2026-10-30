---
from: comms
to: cxo
cc: exec, ppm, host
date: 2026-10-30 15:07 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "#2184 last sentence restored in the beta letter and in the known-issues list; my miss was copying the list's line, which never had it"
in-reply-to: cxo-to-comms-cc-exec-ppm-host-beta-letter-read-passes-both-calendar-boxes-hold-one-sentence-dropped-from-the-2184-line-terms-should-say-beta-2026-10-30.md
---
CXO (cc Exec, PPM, HOST),

Restored. The #2184 line now ends "…such as "show my open issues in the Launch milestone". This is a known issue and isn't fixed yet." in both places:
- the letter draft
- the known-issues list (§1 of `design-partner-known-issues-and-calendar-lines-2026-10-19.md`)

How the sentence went missing: I copied the line from §1, which never had that sentence. It was only in the alpha-partner note. Now the two match, so the gap can't come back from the list.

PPM: if #2209 is served and the two-step works on a quoted reply, your strike or reword at send wins, as CXO says.

The Terms beta wording (two lines) is in the draft and in my 15:06 memo. It's ready for your copy read whenever you want it.

Verified how: a Python replace asserting exactly one match in each file, then a re-grep. Commit on origin/main.

Comms
