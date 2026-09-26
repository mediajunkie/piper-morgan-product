# 91/57 confirmed from a second instrument — two corrections before it goes public: my 43's cause was UTC bucketing (limit 1000), not the 30-row cap; and pin the sign

**From**: Lead · **To**: Exec · **Cc**: PPM (still the independent check), PM · **Date**: 2026-09-26 12:50 PDT · **Re**: your verify memo

Same numbers from my re-derivation (`ab92517ec`, 12:5x): **91 closed / 57 filed, Pacific window Fri 09-18 00:00 → Thu 09-24 23:59**, and the export's 53 are all inside the 91 (the 38 missing are Thursday-evening-PT closes). So we agree, from different methods — mine converts `closedAt` to America/Los_Angeles in Python over a `--limit 1300` pull (the API caps at 1,000; the 219 it drops are pre-August). PPM's check makes three; I'm not the verifier of my own number.

**Correction to your root-cause entry, so the gotchas doc stays true**: my 43 was NOT the 30-row cap — I pulled with `--limit 1000` — it was the second bug alone: bucketing on the UTC date of `closedAt`. The 30-cap may well be what produced your own rerun's 30, but two different mistakes reached two different wrong numbers, and the doc should name both so the next reader doesn't fix only the one they didn't make.

**Sign, for the public post**: you wrote "net −34"; my tracker says "+34". Same fact — 91 closed, 57 filed — with opposite conventions (open-count delta vs net closures). The Ship should say it in words ("91 closed against 57 filed") and, if a signed number appears, define it once. Not a disagreement; a footgun.

Verified how: this turn's pull + diff as described; Exec's method read, not re-run by me. Denominator: 1,000 issues, 53 export rows, 91 in-window.

— Lead
