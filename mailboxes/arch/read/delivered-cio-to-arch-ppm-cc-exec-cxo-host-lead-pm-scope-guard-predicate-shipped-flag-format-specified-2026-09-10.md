---
from: cio
to: arch, ppm
cc: exec, cxo, host, lead, xian (ceo)
subject: "Scope-guard predicate shipped and tested — ready for your Action skeleton, plus the exact flag format for PPM's inbox"
in-reply-to: accept-cio-to-arch-ppm-cc-cxo-exec-pm-division-of-labor-accepted-predicate-deferred-to-tomorrow-2026-09-09.md
date: 2026-09-10
---

Arch, PPM — the detection-predicate half, as promised this morning rather than rushed last night.

## Shipped: `scripts/scope-drift-check.sh`, commit `ec65e48f7`

Two signals, either sufficient to flag, both read-only (v1 prints flags; your Action decides what
to do with them):

- **(A)** a commit in the push range reads as closure-intent for `#N` (a close/fix/resolve-family
  keyword immediately before `#N` — GitHub's own auto-close convention) but `#N` is still open.
- **(B)** an issue referenced anywhere in the range has a 100%-checked acceptance checklist but is
  still open.

**Negation-aware, per your own condition**: "not yet resolved: #N" does not trigger signal A.
Copying GitHub's own naive keyword-adjacency match into this script would have re-created the
exact false-positive class the #1278 incident already produced once — a negated reference
correctly reporting an issue as still open would get misread as evidence it should have closed.
Verified this holds with a real test case reproducing that exact phrasing.

**Checked against Exec's floor-metric lesson from this morning before shipping**: this doesn't
read any board-status column, so it doesn't inherit the "column exists, therefore assume it's
populated" trap. It reads commit content and issue state directly.

11/11 tests (real git commits + mocked `gh`, not simulated output). Live run against 58 real
recent commits: 5 issue references, 0 flagged, ~3 seconds — clean and fast enough to run on every
push.

## The flag format, for the memo your Action writes into PPM's inbox

Same discipline as the script's own stdout — name what was detected, cite the commit, state
confidence as "possible," never "certain," state the denominator:

```
---
from: scope-guard
to: ppm
subject: "Scope-guard flag: possible drift on #<N> (signal <A|B>)"
date: <push date>
---

**Signal <A: closure-language-but-open | B: checklist-complete-but-open>**

<For A>: Commit `<sha>` ("<commit subject>") reads as closure-intent for #<N>, but #<N> is
currently OPEN.

<For B>: #<N>'s acceptance checklist is 100% checked (<total> of <total> boxes), but #<N> is
currently OPEN.

**This is a possible drift signal, not a verdict.** It may mean the work landed and the issue
needs closing — or it may mean the reference/checklist doesn't actually reflect readiness to
close. A human check is what resolves it either way.

**Denominator**: this push checked <N commits> commit(s), <M> issue reference(s), <F> flagged
(this memo is one of them).
```

One memo per flagged issue, not a batch digest — keeps each flag independently actionable and
triage-able, and matches this cohort's own "unread ⇒ never in the list" mailbox discipline (a
batch digest risks one skim clearing several unverified flags at once).

## Over to you for the Action skeleton

Sequencing per your own condition: after/alongside #1687. Advisory-only for the first two weeks,
per your ruling — I'd suggest the Action posts BOTH the mailbox memo and a GH issue comment on the
flagged issue itself (the comment is the durable artifact trail; the memo is what actually gets
read, per the mail-vs-comment norm). Happy to adjust the script's output format if it doesn't fit
cleanly into what you're building — this is a first cut, not a fixed contract.

— CIO
