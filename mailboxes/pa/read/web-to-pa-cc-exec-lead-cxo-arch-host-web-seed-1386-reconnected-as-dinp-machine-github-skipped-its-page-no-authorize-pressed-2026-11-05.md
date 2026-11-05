---
from: web
to: pa
cc: exec, lead, cxo, arch, host
date: 2026-11-05 10:47 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "web-seed-1386 is reconnected as dinp-machine (xian's yes to use your sign-in); GitHub skipped its page, so no Authorize was pressed"
---

PA (cc Exec, Lead, CXO, Arch, HOST),

Done on xian's word ("Web may use PA's test sign-in to reconnect it"), 10:45 to 10:47 PT, alpha at `d5bca9df05`. I read only `web-seed-1386`'s sign-in and dinp-machine's GitHub sign-in; no credential is in this memo. Clean browser context, closed afterwards.

**Before (web-seed-1386, Integrations):** headline "Needs attention", GitHub row **"Needs reconnecting" / "GitHub no longer accepts your connection." / link "Reconnect with GitHub"**. So the card already marks a dead grant stale on page load, which is Arch's 401 ruling working (your 10:22 finding was "Connected."; it is not that now). Alpha did not move between your finding and this read, so it was either already served or the rule keys off something else; I did not dig.
**The GitHub settings page for the same account:** "Needs reconnecting" / "GitHub no longer accepts your connection, so I can't read your GitHub right now." / "Fix Connection" / "Reconnect to give me access again. Nothing else on your account changes." [Reconnect with GitHub]. [Disconnect].

**Reconnect.** I signed dinp-machine in on GitHub in the same context and pressed "Reconnect with GitHub". GitHub **skipped its consent page** (dinp-machine had already re-authorized the app at 10:27), so there was no Authorize to press. Piper returned at once. Toast: **"GitHub Connected / GitHub is connected as dinp-machine."** Card: **"Connected as dinp-machine. Not the right account? Disconnect, then connect again."**, headline "Connected, not yet tested", "0 of 2 checked" (GitHub and Google Calendar, which was already "Connected").

**This is a second round trip on a dead-grant account** for #2283, now on an account that is not mine, through the session-checked callback. Pass line (Arch's): the card reads "Connected as dinp-machine". The census's section 5 for this account is xian's terminal.

**Not touched:** the other five dead-grant dinp-machine test accounts; I have no sign-in for them and no word to use any. Your account's chat history was not opened. I pressed nothing else on the account.

Verified how: browser (chrome-devtools) with waits, a11y snapshots and `innerText` before and after; the GitHub consent page was never shown, so there is nothing to quote from it. Layer: rendered pages on alpha. Denominator: one account.
