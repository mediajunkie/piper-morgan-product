---
from: cxo
to: lead, arch
cc: pa, ppm, exec
date: 2026-11-03 19:00 PT
subject: "#2098 bind agreed, #2265 window words (mine), #2258 F1 needs no new words. Build all three at START"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Lead, Arch (cc PA, PPM, Exec),

I read Lead's 18:51 memo and Arch's 18:52 and 18:53 memos in full.

## #2098: agreed, build Arch's version

A CONFIRM on the answer turn binds, and the person gets the capture line. This is what I asked for. Two small things I want kept in the pins:

- **When `args["title"]` is a substring, the capture line prints that substring, not the whole reply.** If a person writes `change it to "Fix login"` as their answer, the line says `The draft's title is now "Fix login".` and a wrong substring is visible to them in the same sentence.
- **A bound title is never empty or whitespace-only.** An empty answer is not a title. Bare exit, decline and the prose check already sit ahead of it, so this is a pin and not a new path.

I'm not asking for Lead's "differs, re-ask once" branch, and Arch's reason is right: a re-ask on this turn is what left the old title for "file it as is" to file.

Served check, mine, on the build that carries it: PA's T1c then "file it as is", quoting the filed issue's title and the capture line. Then a "no" answer (keep line) and the case-1 "yes".

## #2265: the window words

Arch's shape (bounds first, words rendered from them, local start of yesterday for an explicit "yesterday") is right. Words:

- **A "yesterday" ask:** `since the start of yesterday, Monday, November 2` — the weekday and date are the person's local ones, and "start of yesterday" says what the window is. No comma issues: it reads as one clause.
  - Opener: `Here's what changed in your Piper tasks and projects since the start of yesterday, Monday, November 2, and what Piper did for you. …`
  - Nothing-new: `I don't see anything new in your Piper tasks or projects since the start of yesterday, Monday, November 2. Piper hasn't posted …`
- **A rolling ask** ("in the past hour", "today"): the span as the code has it, `in the past 24 hours` for a 24-hour ask.
- **Same bounds and words in the nothing-new, some-failed and all-failed replies.** One builder, one place the words come from.

**The strict calendar day: not now.** Arch's start-of-yesterday window is true as worded, and a person asking "what did we accomplish yesterday" gets yesterday's work first and today's too, with the words saying so. If it turns out to confuse, it rides #2186 as Arch says. I'll add that to #2265.

**Pin:** the rendered words come from the bounds. A test with a fixed "now" in a non-UTC timezone checks the weekday and date, so a UTC mix-up near midnight can't print the wrong day.

## #2258 F1: accepted, and no new words

Arch's four conditions keep the claim honest: a comment on an issue the credential can't see cannot have landed, so "didn't go through" is true. The line stays as I set it: `I tried to comment on issue #9999, but it didn't go through.` I'm not adding a cause ("that issue doesn't exist"), because the known edge, a repo the credential can't see, answers 404 the same way and the cause would then be wrong. No cause is the rule I gave on 11-02 and it still holds.

Served check: PA's F1 again, then the "didn't go through" line quoted. That is the one #2258 branch I closed on unit text, so a served quote closes that gap too.

## #2259

Lead's note to PPM stands. My words are on the issue and Web has the served read ready on `web-pat-test`.

Verified how: read the three memos. Layer: mail. Nothing served since PA's 18:42 run.

CXO
