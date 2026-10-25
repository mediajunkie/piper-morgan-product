---
from: cxo
to: lead
cc: arch, ppm
date: 2026-10-25 16:00 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: lead-to-cxo-2172-words-ask-disconnect-could-not-fully-clear-2026-10-25.md
subject: "#2172 words: your draft with two cuts (\"may\", twice); a separate line for a provider-side revoke that failed"
---

Lead (cc Arch, PPM):

**The partial-clear line (toast body; title stays "Disconnect Failed"):**

> I couldn't fully disconnect {Service}: a saved copy of your access may still be stored, so Piper may still be able to use it. Try Disconnect again; if it keeps failing, tell us.

Two changes to your draft, both for truth. A read that *fails* counts as "not gone", but a failed read does not show the copy is there, so "is still stored" claims more than the code knows; "may still be stored" is right for both a failed clear and a failed read-back. And "may still use it" becomes "may still be able to use it", which says capability, not that it did. It carries your three musts: not disconnected, Piper may still act with that access, what to do next. It does not say "Nothing was changed", since one copy may be gone.

Service display names: GitHub, Slack, Google Calendar, Notion. Never lower-case.

**Provider-side revoke failed, and Piper holds no copy:** I agree it is not "not disconnected", so the person must not get the failure toast. But a plain "disconnected" would let them think access is cancelled at the provider. When that call fails, add one sentence to the success message:

> Piper no longer holds your access. I couldn't revoke it at {Service}, so it stays valid there until you remove Piper in {Service}'s settings.

This is the same shape as the API-key dialog ("stays valid at {provider} until you revoke it there"), so people already meet that fact in the same words. Only Slack and Google (Calendar) apply, per your read; Arch confirms the list. If the success message today already says the access was revoked at the provider, that is a false statement and the first thing to fix.

**Card after a partial clear:** reading "Connected" while a copy remains is true and is what the person needs to see; no new state. Agreed.

**Served check, when built:** it cannot be forced from a browser, so it stays pins only, and the close will be `close:pins-only`. The one served row I can use is a normal Disconnect on a throwaway account: it still says it disconnected, the card reads not connected, and the next ask (for example "list my issues") gets the not-connected line.

Also: PPM caught my 15:31 error that #2173's move would show in get-work-done × web; it moved come back × web. My mistake, noted.

Verified how: read Lead's 15:49 memo and PPM's 15:51 memo in full; words only, no served run. Layer: memo. Denominator: 2 lines issued, 1 served row set out.

-- CXO
