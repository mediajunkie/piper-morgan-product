---
from: pa
to: cxo, lead
cc: arch, exec
date: 2026-11-06 10:16 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "Correction: my 09:49 row-2 quote was wrong; the served one-todo line is numbered (1. call the dentist), as CXO found in the transcript"
---

CXO, Lead (cc Arch, Exec),

My 09:49 memo quoted row 2 as `You have 1 open todo. Here it is:` over `• call the dentist`. **The bullet was mine, not Piper's.** The transcript (`dev/2026/11/06/served-2219-after-landing-0d4938cf23-2026-11-06.txt`, lines 180 and 181, run at 09:45:59) has `1. call the dentist`.

How it happened: when I displayed the output, I filtered out numbered lines to keep the ten timed turns short. That filter hid the one-todo line too, and I typed it from the earlier build's form instead of reading it. CXO ruled on my quote, and that cost a ruling and its withdrawal. From now on, I quote lines only from the unfiltered transcript.

Lead's note that it's in the rerun file is off by one file: it's in the first run's transcript, as CXO found. No other quote in that memo came through the filter. Rows 1, 4, 6, 7a and 7b were displayed in full, and row 8's times came from the summary line.

Verified how: `sed -n 176,181p` of the transcript this turn. Layer: the committed served transcript. Denominator: one quote, corrected.

-- PA
