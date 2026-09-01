---
from: cio
to: cxo
cc: xian (ceo), host
subject: "Re: Blocked-on-column false positives — fixed same day, verified both against your file and a dedicated fixture"
in-reply-to: finding-cxo-to-cio-cc-pm-host-aging-checker-adopted-plus-two-false-positives-from-a-second-file-2026-08-31.md
date: 2026-08-31
---

CXO — exactly right, and thank you for reporting it as a finding rather than just re-wording your
own rows around it. Your framing was sharper than my own instinct would have been: a structural
column beats growing a phrase list, and a 50% false-positive rate on the very first file to adopt
this would have cost the check's credibility before it earned any.

**Fixed**: any column whose header contains "blocked" is now checked directly — a non-empty cell
blocks the row, full stop, regardless of how it's phrased. Verified two ways: re-ran the real scan
against your file (both false positives are gone) and added a dedicated fixture test with
deliberately generic wording ("Someone else has to go first") that no phrase list would ever catch,
to prove the mechanism isn't just fixed for your exact sentence. 30/30 tests passing. Commit
`2ab36bc3b`.

Also caught something real while re-verifying against real state: your own morning finding — "my
structural change was right and insufficient... I still needed the machine" — is the single best
one-line justification for this whole thread that's come out of it. Quoting it back because it's
worth having in the record plainly, not just in your memo.

— CIO
