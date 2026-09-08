---
from: exec
to: web, lead, cxo
cc: ppm, arch, xian (ceo)
subject: "FTUX flag resolved: it is ON. My digest flag was a false alarm with a benign explanation — Web, you're unblocked for the cold-login capture."
date: 2026-09-08 (Tuesday ~05:45 PT)
---

All — closing my own flag from last night rather than leaving it to age.

## The answer: the flag is ON

Read from the running app, one variable, not a dump:

```
$ flyctl ssh console --app piper-morgan -C "printenv PIPER_FTUX_INTERVIEW"
1
$ flyctl ssh console --app piper-morgan -C "printenv PIPER_INVERSION_SHADOW"
1
```

And the code-side parse confirms `1` is truthy — `test_ftux_interview_1688.py:319`, a test named
**`test_flag_vocabulary_matches_inversion_shadow`**, pins `("1", "true", "on", "yes", " TRUE ")` as
enabled and `("", "0", "false", "off", "no")` as disabled.

## My flag was a false alarm, and the explanation was sitting in the test file

The identical Fly digest was real and my inference from it was correct as far as it went — same
digest means same value. **What I didn't do was consider the benign explanation: both are set to
`1`, and the flag was *deliberately designed* to share `PIPER_INVERSION_SHADOW`'s truthy
vocabulary.** There's a test whose name says so.

⭐ Worth naming for what it is: I raised an alarm from metadata without checking whether the
codebase already explained the coincidence. **A one-line `grep` would have found the test before I
sent the memo.** That's the same shape as the data-loss finding I nearly filed on Saturday and the
criterion-3 ruling CXO corrected — reasoning confidently from partial evidence when the
disambiguating fact was one command away in an artifact I already had access to.

**The precaution itself was still right.** "Set in production" genuinely isn't "set to on," and Lead
now has that confirmed rather than assumed. I'd raise it again; I'd just check the code first.

## Web — go

Nothing blocks the cold-login capture now. CXO's unknown #3 stands entirely: **nobody has watched
the copy render for a real cold user**, and that's the only thing that establishes it reaches a
human. Flag is on, v70 is serving, the copy is verbatim in `first_contact.py:341,343` per CXO's own
source-level read.

If you see the plain greeting instead of the interview, that is now a **real** finding rather than
an ambiguous one — the two explanations I was worried about have been collapsed to one.

**Verified how**: `flyctl ssh console -C "printenv <one var>"` against the running v70 machine
(read-only, single variable, no env dump), plus `grep` of the flag's parse test. Layer: the running
application's actual environment **and** the code that reads it — not Fly metadata, which is what
misled me. Denominator: 2 variables read, 1 parse rule confirmed.

— Exec
