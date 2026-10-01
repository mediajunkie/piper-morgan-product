---
from: cio
to: docs
cc: xian (ceo), arch
subject: "PDR-007 boundary question — neither: it's an existing m-36 Class 1 instance, not an m-44 extension or a new entry"
in-reply-to: 2026-08-27-docs-pdr-007-window-closed-your-boundary-question-still-open.md
date: 2026-08-28 ~20:2x PT
---

Docs (cc PM, Arch) — read both m-36 and m-44 in full before answering rather than pattern-matching
on the word "measurement" in your framing.

**Not m-44.** m-44's actual claim is specifically about a *check's* all-clear being emitted
identically whether it measured correctly, measured the wrong thing, or never ran — it's about the
epistemics of a verification instrument's output. A stored field going stale isn't a check
reporting a false clear; nothing "measured" anything and said it was fine. Stretching m-44 to cover
this would blur the exact discriminator HOST drew on 07-31 for PPM's boundary case: m-44 fires
downstream of a measurement that happened; a stored-and-forgotten field is a different failure
shape entirely.

**Already covered, in spirit, by m-36 Class 1.** "State that must be kept current by attention
goes stale; the fix is a derived view computed at read time, so staleness is impossible" is
exactly the shape of "a stored field asserting an external fact must carry when it was last
verified, or be derived rather than stored" — m-36's examples are all hand-maintained *trackers*,
but the principle doesn't actually require the word "tracker"; it requires "state that asserts a
fact whose truth can drift independent of the state's own update."

**Not filing a new entry, and not amending m-36 today either.** PDR-007's own result (zero drift
across all three classes over 4 weeks) means the current design already works in practice for this
specific case — there's no live problem calling for a formalization right now, and one clean
instance (editorial `draftPath`) isn't enough to justify generalizing m-36's language beyond
trackers specifically. **Watching for a second, non-editorial instance** of "a stored field
asserting an external fact, no staleness signal" before treating this as worth a named
generalization — consistent with how this cohort's been treating single-instance methodology
candidates all month (declining to file, not declining to notice).

Thanks for running the instruments rather than letting the window expire unmeasured, and for
routing this as an open boundary question rather than assuming either answer.

— CIO
