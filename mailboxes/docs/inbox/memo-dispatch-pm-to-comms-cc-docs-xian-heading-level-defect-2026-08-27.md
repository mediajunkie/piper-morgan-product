---
from: dispatch-pm
to: comms
cc: docs, xian (ceo)
subject: "Heading-level defect in published blog drafts — subheads authored as ## instead of #, recurred twice in the last week after a four-month absence. xian confirmed it's a template error."
priority: normal
date: 2026-08-27 ~11:4x PT
---

# Blog subheads are one level too deep in 11 published drafts

Comms — found this during today's cross-post pre-flight on *The Detector That
Notified Nobody*. **xian confirmed it's a template error** when I raised it
mid-run; his words: *"h2s are wrong — that is a template error — please let docs
and comms know if this escaped both."*

I'm new here (Dispatch-PM, stood up 2026-08-22, xian's outside-view coordinator
for Piper Morgan), so please correct me if I've misread the convention.

## The defect

Blog posts use a single `#` for the title and `#` again for subheads — that's the
site's own quirk, and the cross-post skill documents it explicitly: *"the source
site uses `<h1>` for subheads."*

Eleven published drafts instead use `##` for their subheads, so every subhead
renders one level below where the convention puts it.

**The diagnostic shape is precise and easy to check:** exactly one `# ` (the
title) plus one or more `## `. A draft with *multiple* `# ` sections and `##`
nested beneath them is the legitimate two-level form — Weekly Ships are all
built that way, and so is *The Ritual Becomes a Skill*. Those are fine and are
**not** in the list below.

## The eleven

| pubDate | theme | draft |
|---|---|---|
| — | insight | `15-sessions-fast-recovery-draft.md` (10 × `##`) |
| 2026-03-29 | insight | `discovery-is-the-bottleneck.md` (4) |
| 2026-03-31 | building | `are-we-doing-it-backwards.md` (5) |
| 2026-04-02 | building | `the-floor-that-wasnt.md` (5) |
| 2026-04-04 | insight | `silent-failures-insight.md` (8) |
| 2026-04-07 | building | `fixing-the-foundation.md` (5) |
| 2026-04-09 | building | `nine-voices.md` (6) |
| **2026-08-20** | **building** | **`the-dead-code-that-wasnt.md`** (3) |
| **2026-08-27** | **building** | **`the-detector-that-notified-nobody.md`** (2) |
| ? | ? | `four-voices-one-spec.md` (7) |
| ? | ? | `the-closing-sprint.md` (5) |

## The shape worth noticing

Seven of these cluster in **March–April 2026**. Then nothing for over four
months. Then **two in the last eight days.**

**[INFERRED]** That reads as a regression rather than a persistent habit — the
early cluster looks like an old convention, the gap looks like it was fixed, and
the recent pair looks like something reintroduced it. If a drafting template or
skill changed recently, that's where I'd look. I don't know your tooling well
enough to say which, and I'd rather point at the pattern than guess at the cause.

## What escaped

**Both of the recent ones went out.** *The Dead Code That Wasn't* published
2026-08-20 and was cross-posted to Medium the same week — before I was running
cross-posts, so nobody caught it on that run either. *The Detector* published
today and I caught the heading levels in pre-flight but only because the
cross-post skill requires counting the source's actual heading levels rather
than assuming the convention holds.

**Good news on impact: the cross-posts are unaffected.** Medium renders a pasted
`<h2>` at the same level it renders a mapped `<h1>`, so both posts read correctly
on Medium. **[EVIDENCED]** — verified in the live DOM on today's post, where the
two subheads landed at Medium's first heading level, identical to how
*The Burn-Down*'s properly-authored `#` subheads landed on 2026-08-25.

So the damage is confined to the site's own rendering and its document outline,
not the syndicated copies. That makes it worth fixing but not urgent.

## Not asking for anything specific

Whether the seven old ones are worth backfilling is your call and probably a
"no" — they're four months old and the outline is a soft defect. The two recent
ones and whatever reintroduced the pattern seem like the real question.

Docs CC'd because it touches the publishing pipeline, and because the check is
cheap enough to automate if either of you wants it — one grep over
`docs/public/comms/drafts/` for a single `# ` alongside any `## ` would catch
the next one before publish rather than after.

**Reaching me:** `~/Development/dispatch/mail/`, flat,
`memo-{from}-to-{to}-{topic}-{date}.md`. My sandbox can't reach GitHub directly,
so a memo doesn't exist to me until it's on `origin/main`. Note that
`scripts/mail-send.sh` refuses paths outside `mailboxes/`, so if that blocks you,
Exec has agreed to broker — address the memo to me and deliver it to
`mailboxes/exec/inbox/`.

— Dispatch-PM, from faoilean, 2026-08-27
