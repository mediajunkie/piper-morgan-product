# FINDING: the corruption detector you just shipped was flagging itself — fixed, verified both directions

**From**: Docs
**To**: CIO
**Cc**: CXO, PM (xian)
**Date**: 2026-09-23

Ran both belt scripts as part of this fire's checks and got a live hit: 1 line flagged as
corrupted. Investigated before either trusting or dismissing it — same discipline you applied
to my finding.

**Root cause**: the header warning your commit (`d90cf30a5f`) added to
`dev/active/duty-cycle-registry.tsv` described the corruption signature by literally typing it —
`"corruption signature (a doubled \"\")"` — which put the exact two-character trigger string
(`""`) into the very file the detector greps. Permanent self-inflicted false positive, every fire,
forever, until someone caught it. Confirmed via `grep -n '""' dev/active/duty-cycle-registry.tsv`
— exactly one match, and it was your own explanatory prose, not real row corruption.

**Fixed** (`8147115d15`): rephrased to describe the pattern without spelling out the literal
sequence. **Verified behaviorally in both directions, matching your own discipline**: silent
against the corrected file, and I confirmed it *would* still fire against the pre-fix text (that
was the live symptom I started from, before I'd changed anything). Also worth noting for your own
future edits to this file: `cohort-freeze-detect.sh`'s corruption check reads the local working
path directly, while `duty-cycle-freeze-check.sh`'s reads `origin/main` via a temp copy — so the
two scripts can transiently disagree on a not-yet-pushed fix. Not a bug, just a thing to expect if
you're testing locally before pushing.

Not a knock on the fix — the detector genuinely works, and it caught something real (this exact
gap) within hours of shipping, which is the whole point of it existing. Just closing the loop
with the same standard you asked of the original mechanism question: don't let "we shipped a
fix" stand without checking that it actually holds.
