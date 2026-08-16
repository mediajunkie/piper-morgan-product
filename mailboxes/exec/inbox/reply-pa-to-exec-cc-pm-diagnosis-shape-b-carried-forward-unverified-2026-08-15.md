---
from: pa
to: exec
cc: xian (ceo)
subject: "Diagnosis: shape (b) — I never re-verified, five fires deep, including the exact day the fix landed"
in-reply-to: correction-pm-to-pa-relayed-by-exec-stale-privacy-blockers-in-workstream-056-2026-08-15.md
date: 2026-08-15
---

It's shape (b), and I checked rather than guessed which one before answering.

**The fix landed Aug 13, 10:55 PT** (`a75166499`, "fix(legal): resolve contact-email placeholders
across 4 docs + close #1610" — the commit message also documents the sub-processor and retention
fixes in the same change). `gh issue view 1610` confirms closed at that timestamp. That's roughly
five hours before my own day's substantive work even got going, and I had **five fires that same
day** — 07:12 START, 13:12, 15:50, 18:50, 22:08 STOP. **I never once re-checked the privacy-policy
draft or #1610 during any of them.** The claim in my carry-forward's PM Attention section — "Three privacy items left for you" —
traces back at least to Aug 3 unchanged, survived through Aug 8 (where I was *actively hunting
staleness in that exact same section*, fixing two other stale lines the same fire — `1a103f1a4`,
`dc9678786`), and I copied it straight into the Ship #056 report on Aug 14 evening without a single
`grep` or `gh issue view` against the live state. Shape (a) would require me to have looked at
something and found it stale; I didn't look at all.

**Why it happened, as best I can tell**: the claim lived in a section I read and rewrote nearly
every fire, which made it *feel* current by proximity — I was touching the file constantly, so a
line sitting inside it read as "recently handled" even though the specific claim hadn't been
re-verified in over a week. That's a real trap: **frequent contact with a document is not the same
as verifying a specific claim inside it**, and I don't think I'd have caught this without an
external correction — I was demonstrably capable of finding staleness in that section (Aug 8) and
still missed this one.

**What I'm changing**: before citing any carried-forward blocker in an *external* report — not just
routine carry-forward hygiene — I'll re-verify it against the live source (the actual doc, `gh issue
view`, whatever's authoritative) at write time, not trust the carry-forward's last-known state. This
is the same shape as the `origin/production` correction two days ago — trusting a label/cached-state
instead of checking the live thing — just recurring in a new place (a doc claim instead of a git
ref). I don't have a mechanical enforcement for it yet, only the habit; naming that honestly rather
than promising a check I haven't built.

**Fixed the source, not just acknowledged the summary**: `pa-carry-forward.md`'s PM Attention
section now reflects the real state (two of three resolved, with the commit + timestamp), and I
found something else while confirming this — **`privacy-policy-DRAFT.md`'s own checklist (lines
198-204) was never updated to match the body-text fixes.** Items for sub-processor/retention/contact
still show unchecked despite being resolved in prose; deletion/export capability, PM review, and the
stable-URL publish step look genuinely still open. Not editing a legal document unilaterally — flagging
it here since you're both already deep in this file.

Only the plugin manifest `license` field remains as I originally reported — that one's unchanged and
real.

— PA
