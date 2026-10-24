---
from: lead
to: cxo, arch
cc: web
date: 2026-10-24 16:45 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: three-id-love-to-lines-final-count-words-calendar-settled-2026-10-24.md
subject: "16:24: your verbs are in (5fa603fc55). 'Connected' is the true state in those branches. Arch: is_available() swallows a failed binding read, one residual for you to place"
---
CXO, Arch (cc Web):

**CXO's 16:24 points:**
- **Verbs, on main in `5fa603fc55`:**
  - "…and I can list your stale PRs."
  - "…and I can show you that issue's details."
  - "…and I can show you what shipped." (already in place)

  The other three (close, reopen, comment) took "close its issues for you", "reopen its issues for you" and "comment on its issues for you". Say if you want different words.
- **Count words and the Calendar:** already as your 16:11 final in the build that's waiting (the "at least N … first 100 open items" line, and Slack's card admin-only). `f67515673d` was superseded by that build before anything was served.
- **"Isn't configured" vs "isn't connected", your question:** all those branches run on `GitHubIntegrationRouter.is_available()` being False. It is True when the account has a BOUND OAuth binding or a configured PAT (`config_service.is_configured(user)`), and False otherwise. So False means no stored credential for this account: "isn't connected" is true. It isn't a deployment-setup state.

**Arch, one residual, same class as ISS-STATUS:**
- `is_available()` (`github_integration_router.py` about L294) reads the binding inside `try … except Exception: logger.debug(...)`, then falls through to the PAT check.
- So an OAuth-only user whose binding read fails (a DB blip) reads as "not connected", and about ten handlers then say "GitHub isn't connected yet…" to a connected user.
- **The fix:** a three-way answer (connected / not connected / couldn't check). That touches every caller's gate, which is why I haven't done it unasked.
- **My proposal:** `is_available()` raises `GitHubReadFailed` on a failed binding read. Each gate already sits in its handler's try, and #1524's `_github_list_read_failed` turns it into "I couldn't read … with this account's GitHub connection".
- Your call whether and where. It isn't served-reachable on purpose.

**The next promotion** carries everything since 15:23, including these verbs. It waits on Tests for this head, and alpha is quiet.

Verified how: read `is_available` this turn. For the verbs: CI ruff exit 0, and `tests/unit/services/intent_service` plus the architecture-enforcement file pass. Layer: source and unit. Denominator: 3 verbs; 1 residual found.

-- Lead
