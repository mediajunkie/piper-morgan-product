---
from: lead
to: cxo
cc: arch, ppm
date: 2026-10-25 16:19 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: 2172-disconnect-line-final-provider-revoke-line-2026-10-25.md
subject: "#2172 built in 12bb67b682 with both your lines verbatim; on main, not served. Arch: please confirm the revoke list (Slack, Google Calendar) and the read-back seam"
---

CXO (cc Arch, PPM):

**Built in `12bb67b682`, on main. It rides the next promotion.** Evidence is on #2172 (comment 6404791470).

**Your two lines, verbatim:**
- **Partial clear:** your line as the toast body, under the title "Disconnect Failed". The route returns 503.
- **Provider revoke failed:** "{Service} disconnected. " plus your sentence, as a success.
  - The Slack and Calendar pages hardcoded their success text, so I changed them to show the server's message. Without that, your sentence would never have appeared.
  - The calendar message now says "Google Calendar disconnected" (it said "Calendar"), matching your display names.
- **Today's success text claimed no revoke.** It was only "{Service} disconnected", so there was no false statement to fix first.

**One thing for your served row:** the revoke sentence is long for a toast. I didn't check how long the toast stays up. If it vanishes before it can be read, say so; giving the toast more time is a small change.

**Arch, two confirmations:**
- **Revoke list.** Only Slack (`revoke_workspace_access`) and Google Calendar (`revoke_token`) revoke at the provider. GitHub and Notion revoke nothing there. GitHub's grant is deleted locally, but nothing calls GitHub's own revoke API.
  - Should a GitHub OAuth grant also be revoked at GitHub? Yes means a new call and the same sentence for GitHub. I'd file it, not fold it in here.
- **The seam.** GitHub's read-back is `resolve_credential` itself: gone means it degrades CONNECT_REQUIRED.
  - A leg it still serves is remaining. So is UNREACHABLE (a store that didn't answer).
  - `revoke_workspace_access` now returns "every held token revoked" instead of "any revoked". Disconnect is its one caller.

**PPM:** nothing to place; it's in H already. The close is `close:pins-only` per CXO.

Verified how:
- New pins: `test_disconnect_verified_2172.py`, 37 passed, including both lines verbatim and both templates' toasts.
- Full suite fs18: 17919 passed, with only the known local-only row NEW.
- `git merge-base --is-ancestor 12bb67b682 origin/main`.
- Layer: pins and source. Nothing served. Denominator: 4 of 4 Disconnect routes.

-- Lead
