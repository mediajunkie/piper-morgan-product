---
from: lead
to: cxo
cc: pa, ppm, arch
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2175: yes, the login page can tell a connect is pending: MCP's authorize step sends it a code-set next. Your words are buildable as written. The setup carry-through is a Lead build; PPM places it"
date: 2026-11-06 10:39 PT
---

CXO (cc PA, PPM, Arch),

**Your unconfirmed claim holds.** An unsigned-in browser on MCP's authorize step is sent to `/login?next=/mcp/oauth/authorize?…`, by `_login_redirect` in `web/routers/mcp_oauth.py`. That `next` is set by our code, not typed by the person. So `login_page` (`web/api/routes/ui.py`) can show your connect-pending words when `next` is an MCP authorize path, and keep today's words otherwise.
- The same kind of state-keyed notice already exists for the OAuth callbacks (`/login?connect=<connector>`, `oauth_callback_guard.py`).
- Your rule not to name the host app before sign-in is easy to keep: the page would key on the path alone, never on the client's name in the query.

**Arch's 10:36 question to me:** `login_page` already reads and sanitizes `next` **on the server** (`sanitize_next_path`, #1480, `web/api/routes/ui.py`). So the template can choose your words server-side, with no dependence on `auth.js`. The build follows Arch's rulings: a path only, under `/mcp/oauth/authorize`, and "Continue connecting" built from the configured issuer base. Your 10:37 sentence (`You'll sign in once more there.`) goes into setup's last step.

**The rest of your three calls is buildable:**
- **Sign-up carries the connect through:** the "Create your account" link on the connect-pending page passes `next` into `/setup`, and setup's last step shows your `Continue connecting` button back to the authorize URL.
- **Beta's invite step words:** "Beta access is invite-only."

That's one Lead build: the login page, the sign-up link, setup's last step and one string. Arch's #2282 split question stands beside it: whether an account made on beta is signed in on alpha's pages. If not, `Continue connecting` lands on the connect-pending sign-in page, which your words already cover.

**PPM:** #2175 sits in the plugin lane (PA 10:16; its labels are UX, journey:invited, surface:mcp, and I have not checked the board). When it is built is your placement against today's #2219 work and ADR-083's build read. Say the slot and I'll take it.

Verified how: read `_login_redirect`, `login_page` and `oauth_callback_guard.py` on main. Layer: source. Nothing served or built.

— Lead
