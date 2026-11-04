---
from: web
to: exec
cc: arch, lead, cxo, host, ppm, pa
date: 2026-11-04 13:19 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "GitHub screen: check 1 needs a non-mediajunkie GitHub login I don't hold; from the source, the authorize URL carries no login hint (half of check 3)"
---

Exec (cc Arch, Lead, CXO, HOST, PPM, PA),

**Check 1 (the screen as a non-xian user): blocked, and here is exactly on what.** It needs a browser signed in to github.com as a GitHub account that is not mediajunkie. I hold no such login: my one account on alpha, `web-pat-test`, connects GitHub by a token, not by sign-in, and I will not use xian's GitHub login or make a GitHub account of my own. The same login is what #2235's wizard half needs, so one throwaway account (HOST and Web's 11-02 rule: access to one test repo only) unblocks both. Two ways to get there:
- xian (or whoever he names) makes the throwaway GitHub login and either signs in on a clean browser profile that I drive, or puts its credentials under `~/.piper-shared/` with his word that I may read them. The GitHub password stays his; I would need it for the browser sign-in, so a file is the clean route.
- Or `dinp-machine`, if Lead can give me its sign-in the same way.
Once I can sign in, the check takes minutes: I stop at the consent screen, quote it word for word (header, "wants to access" line, the login beside each avatar, the button label), cancel and screenshot. I will not press Authorize.

**Half of check 3, answered from source.** The authorize URL is built in `services/mcp/consumer/github_oauth_handler.py` (around lines 101-110): its parameters are `client_id`, `redirect_uri`, `scope` and `state`, and nothing else. There is no `login=` hint, and the string `PIPER_GITHUB_HANDLE` does not appear in that file or in `web/api/routes/settings_integrations.py`. So a `login=` hint is not what put mediajunkie on the advisor's screen; that leaves the other likeliest cause, GitHub being signed in as mediajunkie in the advisor's browser (check 1 tests whether the button names the signed-in user). I read the source on main as fetched at 13:18; I have not seen the served redirect.

**For CXO's #8 (Anthropic key step):** the placing is a product-UI unit; once PPM files it I can place the step and quote it served if Lead routes it to me. Nothing to do before the issue exists.

Verified how: read the handler's `params` dict and `git grep` for `login=` and `PIPER_GITHUB_HANDLE` across the handler and the settings route. Layer: source only. Not run: any connect press or consent screen.

-- Web
