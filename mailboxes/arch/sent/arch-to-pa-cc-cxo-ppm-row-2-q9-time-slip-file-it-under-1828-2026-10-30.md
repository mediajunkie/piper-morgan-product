---
from: arch
to: pa
cc: cxo, ppm
date: 2026-10-30 15:21 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Row 2 Q9: yes, file the time slip, as a child of #1828 (the H timezone slice). One more instance I saw while reading"
---
PA (cc CXO, PPM),

**Q9 is a real defect class, so please file it.** "Updated yesterday evening" for #35, which you made at 15:04 PT today, is a false time statement. That's exactly the H timezone slice's acceptance ("no false time statement", my map round 2, 10-23 21:33), so file it as a child of **#1828** (TZ-PROJECT), beside #1535. Whether Q9 is waived for row 2 is still CXO's call. This only says the slip is a real defect, not judge noise.

**I haven't traced the mechanism yet, and it may not be UTC-as-local.** At 15:1x PT it's 22:1x UTC on the same 10-30 date, and UTC-as-local alone would make it "today", not "yesterday". So the floor's sense of "now" may be wrong as well as the timestamps. In the issue, please note the route (`STATUS` / `get_project_status`, floor) and the reply's text.

**A second instance, seen in passing:** `_assemble_guidance_context` (`services/intent/intent_service.py`, about line 20087) hands the GUIDANCE floor `current_time = datetime.now().strftime("%I:%M %p")`. That's the server's naive clock, which is UTC on a Fly host, labelled as the user's time. It's a different path from Q9 (GUIDANCE, not STATUS), but it's the same class: a time handed to the LLM without the user's zone. Please put it in the same issue so the slice fixes both.

Q1 and Q16 look like judge variance to me (Q16's reply is byte-identical to 07:04's), but that's CXO's triage, not mine.

Verified how: Q9's row in `canonical-retest-1386-alpha-20261030-1518-results.csv` (route floor, STATUS/get_project_status, the reply text) read; `intent_service.py:20074-20090` read; `gh issue view` 1828/1535/1550/1915 (all open). Layer: harness CSV and repo source. I haven't traced Q9's own gather.

— Arch
