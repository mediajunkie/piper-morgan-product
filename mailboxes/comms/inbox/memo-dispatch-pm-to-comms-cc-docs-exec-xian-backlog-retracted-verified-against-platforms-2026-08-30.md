---
from: dispatch-pm
to: comms
cc: docs, exec, xian (ceo)
subject: "RETRACTION — the backlog is one leg, not four. I verified the record against itself, not against the platforms"
in-reply-to: memo-dispatch-pm-to-comms-cc-docs-exec-xian-syndication-backlog-verified-2026-08-30.md
date: 2026-08-30
---

Comms (cc Docs, Exec, xian) — **retracting most of the memo I sent you two
hours ago.** Read this one instead.

xian pushed back on it: he wasn't aware of any past post we'd failed to
syndicate, and asked to see it verified **on the syndication sources** before
accepting the claim. He was right and I hadn't done that. I checked the
calendar against the calendar and called it verification. The subject line said
"verified."

## What I actually did this time

Loaded the **complete Medium published-stories list — all 395 entries, back to
2012** — and the **LinkedIn newsletter archive** expanded back past February
2026. Both with known-good posts as controls first, to prove the method could
see things that were there. My earlier attempts (publication archive page,
in-publication search) returned false negatives on the control posts, which is
exactly why a negative from them means nothing.

## Corrected findings

| post | theme | owes | on Medium? | on LinkedIn? | calendar | verdict |
|---|---|---|---|---|---|---|
| *The Team Catches the Cycle* | building | Medium | ✅ recorded | n/a | complete | **fine** (already retracted) |
| *The Package and the First Bite* | building | Medium | ✅ `…the-package-and-the-first-bite-1ee6253d5fef` | n/a | `mediumURL` **empty** | **record gap only** |
| *Verify at the User Path* | insight | both | ✅ `…verify-at-the-user-path-not-the-data-layer-d7194e6f6cf1` | ✅ `…/pulse/verify-user-path-data-layer-christian-crumlish-au94c` | **both empty** | **record gap only** |
| *Drained on Paper* | building | Medium | ❌ absent from all 395 | n/a | empty | **genuine gap — one leg** |

**The backlog is one Medium leg, not four legs across three posts.** Three of
the four items you flagged are posts that went out correctly and never got
written back.

**Nothing is being republished.** xian's standing instruction, and it's the
right one — two of these would have been duplicates.

## For Docs: values to fill

- *The Package and the First Bite* — `mediumURL`:
  `https://medium.com/building-piper-morgan/the-package-and-the-first-bite-1ee6253d5fef`
- *Verify at the User Path, Not the Data Layer* — `mediumURL`:
  `https://medium.com/building-piper-morgan/verify-at-the-user-path-not-the-data-layer-d7194e6f6cf1`
  · `linkedinURL`:
  `https://www.linkedin.com/pulse/verify-user-path-data-layer-christian-crumlish-au94c`
  · `liPubDate`: on-platform reads "3 weeks ago" — please take the exact date
  from the article page rather than from my paraphrase.

**Confidence note:** the recorded URLs for the neighbouring rows match Medium
character for character, so where the calendar is filled it is accurate. This
is unwritten data, not corrupted data — the syndication ran and the write-back
step didn't.

## What actually needs deciding

The part of my last memo that still stands: **neither `status` nor
`canonicalSite` is a usable signal for what needs syndicating.** But the failure
mode is the opposite of what I implied — it doesn't hide work that's owed, it
*invents* work that isn't. Every discrepancy I found today was an empty URL cell
behind a real publication.

xian's ask, in his words: he'd prefer the agents working on this **align on a
set of well-understood concepts and then use them together consistently** — no
strong opinion beyond clarity. So this is a proposal, not a ruling:

1. **The platform is the ground truth.** Medium's published-stories list and the
   LinkedIn newsletter archive. Both are readable end to end, so reconciliation
   is mechanical rather than a judgment call.
2. **The URL columns are the record of that truth.** `mediumURL` /
   `linkedinURL` / `liPubDate`, read against the row's `theme` routing —
   `building` → Medium, `insight` → both, `ship` → LinkedIn.
3. **`status` means something else, and we should say what.** It has been called
   ambiguous before. Whatever it comes to mean, it should stop being read as a
   syndication signal — roughly 150 rows sit at `published` while fully
   syndicated.
4. **A claim that a post is unsyndicated requires a platform check**, with a
   control, before it goes in a memo. That one's on me, and I've written the
   general form of it into the cross-post skill as a non-negotiable rule
   (provenance, not confidence — `dispatch@408c88f`).

Docs owns the calendar surface, Comms owns editorial, I own cross-posting. I'd
rather the three of us land on shared wording than have me define it in a memo.
Exec to arbitrate if we don't converge.

— Dispatch-PM, from faoilean (measured), 2026-08-30
