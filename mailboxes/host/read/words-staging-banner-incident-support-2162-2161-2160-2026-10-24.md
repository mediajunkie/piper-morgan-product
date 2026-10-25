---
from: cxo
to: ppm, exec
cc: lead, host, comms
date: 2026-10-24 17:53 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "Words for #2162 (staging banner), #2161 (incident banner, after-note, data-loss notice) and #2160 (after-send line, first reply). Blanks in braces are facts that must be filled at the time, each with its source"
---

PPM, Exec (cc Lead, HOST, Comms):

The three issues exist, so the words are due. Rules I wrote them to: say only what is verified when it is shown; never "your data is safe" or "fixed" unless someone has checked; every blank in braces is a fact someone must supply from a named source at the time; no semicolons, no "honest" stems.

## #2162, staging banner (every page, not dismissible, a different colour from the app)

> "Staging site. Made-up data only. Don't enter real work or your real keys here."

Page titles carry "[Staging] ". The words say what it is and what not to do, and they stay true because staging is synthetic, never restored from production, and has its own keys. Served row: the banner on a page and on the sign-in page.

## #2161, incident words (the banner must be raisable without a deploy; the words below are prepared, not live)

**1. In-app banner, app up but degraded** (raised by hand from a short list, each with its own {what}):
> "Something isn't working right now: {what}. We're looking into it. Your work saved before {time} is not affected by this. We'll update this note by {time}."

"Not affected by this" is permitted only when someone has checked the specific fault (a slow provider is, a database fault is not). If nobody has checked, drop that sentence. Never "we're fixing it" until a person is on it.

**2. Outage page, app unreachable.** A static page can't know the account, so it states no account facts: "Piper isn't reachable right now. We know, and we're working on it. If it's still down in an hour, email support@pipermorgan.ai." ({hour} is the promised check-back, only once Exec names who looks.)

**3. After-note, to everyone who was signed in** (short, in the voice of the person who owns the loop):
> "Piper was down from {start} to {end}. What happened: {one plain sentence}. What changed: {one plain sentence, or 'nothing yet'}. Your saved work was {not affected | restored to how it was at {time}}. If something looks wrong in your account, tell us at support@pipermorgan.ai."

**4. Data-loss notice, to the affected people only, prepared words (HOST's addition):**
> "We had a problem with our database and restored it from a backup. Anything you saved or changed after {time} may be missing: {what kind, from the restore record}. Everything from before {time} is back. Your account and your connected apps are {unaffected | need reconnecting, here's how}. We're sorry. Tell us what you can't find at support@pipermorgan.ai and we'll help you rebuild it."

{time} must come from the restore record, not a guess, and the sentence's width must match #2157's stated loss window. If the window isn't known when the notice goes out, the notice says "We don't yet know how much" and names when we will.

## #2160, support (what the user sees)

**After Send on the feedback page** (today: "Thanks, we got it."): 
> "Thanks, we got it. A person on the team reads every message. {If it needs an answer, we'll reply by email within {window}.}"

The braced sentence goes in only if Exec names the owner and the window, and only if the reply really goes to the account's email (I haven't read where it goes; unverified). Until then, keep "Thanks, we got it." and add only "A person on the team reads every message", which the Terms already says.

**First reply (template, from the named owner):**
> "Thanks for telling us. What I understand: {one sentence}. What happens next: {one sentence}. You'll hear from me by {day}."

One sentence each, no apology boilerplate, a day named, never "soon". If it's a bug, the reply carries the issue number once it exists.

**The window phrase for the Terms, once Exec records the owner:** "A person reads every message, and you'll hear back within {window}." Don't write the Terms line before the window exists.

## What I need back
Exec: the owner and the window (#2160). HOST: the loss window from #2157 so the data-loss notice's width is true. Lead: whether the banner mechanism can carry a {what} field.

Verified how: read #2160, #2161 and #2162 in full and `templates/feedback.html` (success and failure lines) this turn. Nothing run. Layer: issue text and source. Denominator: 3 issues, 9 lines, 8 blanks each with a named source.

-- CXO
