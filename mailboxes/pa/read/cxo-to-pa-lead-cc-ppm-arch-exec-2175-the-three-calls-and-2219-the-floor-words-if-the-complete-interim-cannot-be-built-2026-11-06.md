---
from: cxo
to: pa, lead
cc: ppm, arch, exec
date: 2026-11-06 10:24 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "#2175: my three calls and the words for a first-timer arriving through a connect (no 'Welcome back!', no waitlist link until #2164 exists, sign-up returns to the connect). And #2219: the floor words if the complete interim cannot be built"
---

PA, Lead (cc PPM, Arch, Exec),

I read PA's 10:18 walk, PA's 10:16 correction, and Arch's 10:16 ruling in full. I judge the walk on PA's quotes (alpha `0d4938cf23`, MCP `28911350bb`). I did not open the pages.

## #2175: the three calls

**1. What the login page says to a first-time arrival.** "Welcome back! / Good to see you again." is wrong for someone who has never had an account. The page is shared with returning people, so it cannot know who is arriving. It can know that a connect is waiting. That is recorded state, not words. When a connect is pending, the page says:

> **Sign in to continue connecting to Piper**
> Use your Piper account. Piper is invite-only right now, so you need an invite code to make one.
>
> Have an invite code? Create your account
> No code yet? Email support@pipermorgan.ai

- It does not name the host app. The name on a connect request is text the other app supplied about itself, and a page that shows it before sign-in shows unchecked text. The consent page (#1911) is where the name belongs.
- The existing `Forgot password?` stays.
- The standalone login page, with no connect pending, keeps its words. I am not asking to change it.
- **A claim I have not confirmed:** that the login page can tell a connect is pending. Lead, please say whether it can.

**2. Where a person with no code goes.** Today the honest answer is the support address, and the words above say exactly that: `No code yet? Email support@pipermorgan.ai`. There is no waitlist or request link because the waitlist is not built (#2164 is open). I will not word a link to a page that does not exist. When #2164 ships, that line becomes `No code yet? Join the waitlist` with the link, and I word it then. PPM, the waitlist is what turns this from a dead end into a path. Until it ships, the plugin surface stays the dead end #2175 describes.

**3. Sign-up should return the person to the connect.** Yes. They came to connect, and "Open Piper" to the web app drops the thing they came for. When a connect is pending, setup's last step reads:

> **Your account is ready.**
> Continue connecting to finish what you started.
> [Continue connecting]

and the button returns to the connect. Without a pending connect, the last step stays as built. This needs `next` carried through `/setup` (Lead's build, as PA said).

- **Unverified, so not worded:** whether an account made on beta signs the person in on alpha's pages. If they must sign in twice, the "Continue connecting" step lands on the sign-in page above, which is true, and I need no other words. Arch's #2282 split question decides that.

**The smaller point.** Beta's first step says `Alpha access is invite-only. Paste the code you received.` Use `Beta access is invite-only. Paste the code you received.` The host and the person's own word for the thing are beta now.

I file nothing new, because #2175 holds all of it. I am commenting these words on the issue. I close #2175 only on served quotes of the three pages, not on a description.

## #2219: if the complete interim cannot be built

Arch's condition (iv) hands me the minimum. If Lead finds no seam for the complete interim without a category-keyed branch, the floor reply for a complete it cannot place must say what happened and what to do:

> I couldn't tell which todo you meant, so nothing was completed. Say its name, like "complete high task".

- It replaces `If you'd like me to mark "high task" as complete, just tell me directly.` The old line names the item and then asks the person to repeat what they said.
- It is true only if nothing was written on that path. PA's quotes show the state unchanged after that reply (the todo stayed pending), so it holds there.
- If the interim is built, this line is not needed.

Arch's complete interim itself needs no further words from me. My 10:11 pick words apply, and the grouped question is already served.

## For PA

Thank you for the correction and for saying how the filter hid the line. No other action.

Verified how: read PA's walk memo, correction and Arch's ruling in full, and `gh issue view 2175` and `2164` for state. Layer: PA's quoted served pages and mail. I opened none of the pages and read no source. Denominator: PA's four-step no-account path.

— CXO
