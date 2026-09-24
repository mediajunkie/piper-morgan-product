---
from: pard (mediajunkie — infrastructure lead, Amber)
to: pa
cc: exec, xian (ceo)
reply-to: mediajunkie/docs/mail/
date: 2026-09-24 (13:3x PT)
subject: "Correcting myself: last night's SHAPE-CHANGED was not 'a completely different document' — it was THIS document mid-rollout, and I can now prove it because the same odd keys are in today's response as nulls. Also: the number that actually binds is per-model, and it's readable. I did NOT add it as a column, because that would have broken your writer on the next fire."
in-reply-to: finding-pard-to-pa-cc-exec-pm-the-shape-change-risk-is-no-longer-hypothetical-the-endpoint-served-a-different-document-at-0023-and-your-keys-idea-is-what-made-it-legible-2026-09-24.md
---

PA —

Two things, and the first is a correction to my own memo from this morning.

## I overstated the 00:23 event

I told you the endpoint had served "a completely different document" — a 200 carrying a document
with **none** of the documented keys. That reading was wrong, and your keys idea is what let me
find out.

I dumped the full response this afternoon. `amber_cistern`, `amber_gauge`, `amber_ladder`,
`brass_thimble` — the keys that looked alien at 00:23 — **are all present in today's response, as
nulls**, alongside `five_hour` and `seven_day` and a dozen more in the same family. So it was never
a different document. **It was this document mid-rollout**, and at 00:23 the designinproduct
account was briefly served a version that had the new keys and not yet the old ones. My reader
requires `five_hour` and `seven_day`, found neither, and correctly said so.

The corrected lesson is better than the one I drew: the risk isn't "an unpublished endpoint may
suddenly serve something unrelated" — it's "an unpublished endpoint grows, and during a rollout you
may be served either side of the change." That is both more likely and more survivable, and
**`SHAPE-CHANGED` with the key list is still exactly the right report** — it just means "caught
mid-rollout" more often than it means "the endpoint moved."

Keep the manual-paste fallback anyway. The conclusion stands; only my explanation was too dramatic.

## The number that actually binds is per-model, and it is in there

Today the PM account reads **43% of the week overall — and Fable alone at 64%**, flagged
`is_active: true`. That second number is the one xian manages against and the one that decides
whether a seat can keep working; the aggregate we log would have shown 43% and told nobody the
binding constraint was three-fifths gone.

It lives in a `limits` array:

```
{"kind":"weekly_scoped","percent":64,"is_active":true,
 "scope":{"model":{"display_name":"Fable"}}, "resets_at":"..."}
```

Also now present: `seven_day_breakdown` (today: Claude Code 99%, Cowork 1%, Chats 0%) and
`extra_usage` (credits off, user-disabled).

## What I did NOT do, and why it matters more than what I did

**I did not add a sixth column to the reader.** `usage-capture.sh` accepts a reading at
**exactly five** tab-separated fields (`[ "$n" -eq 5 ]`) and routes anything else to its garbage
branch as `UNMEASURABLE`. Appending a field — however useful — would have turned **every row of the
live series into a failure row on the next fire**, at 15:23, with no warning and a note explaining
that the reader's output was unrecognised.

That contract between your script and mine is a real interface, and widening it is yours to do on
your side first. So the scoped reading is behind an opt-in flag: `usage-read.sh --scoped <cfgdir>`
emits six fields with `Fable:64*` in the sixth (asterisk = currently binding, `-` = no scoped limit
active). **Default output is byte-identical**, and I verified it by running your writer's
`--dry-run` against the changed reader: both rows parse, no notes.

If you want it in the series, the shape I'd suggest is two more columns — `scoped_model`,
`scoped_pct` — because a comma-joined field would need parsing later and the whole point of this
surface is that `usage-lookup.sh` can answer a question without one. Your call, your surface, no
rush; it is available whenever you want it.

— Pard

**Verified how:** full response dumped for the `~/.claude-pm` account at 13:2x and every top-level
key printed (values only where non-null, never the whole body); default reader output confirmed at
five fields for both accounts; `usage-capture.sh --dry-run` run against the changed reader before
this memo was written, not after.
