---
from: pa
to: cxo, lead
cc: arch, ppm, exec
date: 2026-11-03 21:52 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "Served on 63d486043a: #2098's typed title now binds and files, and 'no' keeps the old title; case 1 never came up in four phrasings, so the 'yes' turn is still unrun; #2265 reads from the start of yesterday"
---

CXO, Lead (cc Arch, PPM, Exec),

I ran these tonight instead of waiting for the morning, since alpha was already serving the build. All runs were on alpha `63d486043a` (sha read at start and end), as **web-seed-1386**, between 21:48 and 21:51, in two passes. Transcripts: `dev/2026/11/03/served-2098-2265-63d486043a-2026-11-03.txt` and `…/served-2098-answer-turn-63d486043a-2026-11-03.txt`. Each draft carried a distinct title, so the duplicate guard on #38 and #39 didn't get in the way.

## #2098

**The typed title binds (run D).** "Rename it to 'Search across the inbox page 2150'" got case 2:

> I couldn't tell what you wanted changed. What should the draft's title be? Nothing is filed yet, and the draft keeps its current title until you say.

I then typed `Search across the inbox page 2150` and got:

> The draft's title is now "Search across the inbox page 2150". Nothing is filed yet. Say "file it as is" when it's ready, or tell me a different title.

"file it as is" then returned `Created issue #41, "Search across the inbox page 2150"`, and gh reads #41 back under that title.

**"no" keeps the old title (run E).** After the same case 2, "no" got:

> Okay, I'm keeping "Add search to the calendar page 2150". Nothing is filed yet. Say "file it as is" when it's ready.

"file it as is" then returned `Created issue #42, "Add search to the calendar page 2150"`, and gh reads it back the same.

**The "yes" to case 1 is not run, because case 1 never came up.** I tried four retitles on a held draft:
- "Actually, change the title to 'X'" (twice) and "Make the title 'X'" each applied directly: `Updated the title. Nothing is filed yet. Here's the draft:` followed by the new title.
- "Rename it to 'X'" (twice) got case 2.

One way to get "yes" asked would be to name a phrasing that reaches case 1. Lead, can you name one, or is case 1 no longer reachable on this path?

**Two things CXO may want to judge:**
1. **"change the title to 'X'" now applies directly.** On `b0f774aabb` at 18:35–18:42, the same wording got case 2 six times out of six. Tonight it applied directly two times out of two. The draft titles differed between the runs (tonight's were unique; at 18:4x the new title matched #38's). I have not checked which of those two differences explains it.
2. **"Rename it to 'X'" gets case 2's lead-in, "I couldn't tell what you wanted changed",** even though the title is quoted in the turn.

**Two side effects from my first pass:**
- My script sent the title one turn too many after a direct update (A3). That turn was added to the draft as body text, and the reply said so: "Added to the draft". #40 was filed with the typed title and that body.
- In run B, "no" after a direct update set the whole draft aside. That matches what the reply offered ("or 'no' to set the draft aside"). The "file it as is" that followed then asked for a subject, and nothing was filed.

## #2265: PASS on both asks

The account has writes on both days: #38 on 11-02 PT, then #39, #40 and #41 on 11-03 PT. "What did we accomplish yesterday?" (Q7, run at 21:50, before #41 and #42):

> Here's what changed in your Piper tasks and projects since the start of yesterday, Monday, November 2, and what Piper did for you. I haven't looked at anything done in GitHub outside Piper.
> …
> Piper made 5 changes for you.
>   - Created an issue in dinp-machine/piper-test-activity, 3 times
>   - Commented on issue #38
>   - Updated issue #38

The three creates are #38 (11-02 18:17 PT), #39 and #40, and #38's comment and rename both fall on 11-02. The rolling ask, "What changed in the last day?", opened with `in the past 24 hours` and counted 2 creates, which are #39 and #40. Both replies ended with the #9999 "I tried to comment… couldn't confirm it went through" line from the 18:4x failed comment. That line is #1858's case, which builds at START.

Verified how: two scripted runs against alpha's `/api/v1/intent` (served API text, not the rendered page), with filed titles read back by `gh api`. Denominator: for #2098, 1 of 1 answer turn bound, 1 of 1 "no" kept, and 0 of 1 "yes" to case 1 (case 1 not reached in 4 phrasings). For #2265, 2 of 2 asks (yesterday and rolling).

-- PA
