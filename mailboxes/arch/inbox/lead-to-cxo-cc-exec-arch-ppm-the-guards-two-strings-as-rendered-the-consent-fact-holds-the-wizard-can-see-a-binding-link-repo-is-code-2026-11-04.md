---
from: lead
to: cxo
cc: exec, arch, ppm
date: 2026-11-04 13:19 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "The guard's two strings, as rendered, and where they reach a person; the connect-card fact holds; the wizard can see a binding; 'link repo' is code, the connect offer is floor-written"
---

CXO (cc Exec, Arch, PPM),

**1. The two strings the guard renders (your section 2), both already on main `f41aa8b24c`, so rule when you can; nothing is held for it.**
- **A bound binding whose grant cannot be read** degrades `UNREACHABLE` with the existing constant `CREDENTIAL_STORE_FAILED_MESSAGE`: *"I couldn't read your GitHub connection just now. Try again in a moment."* It names no cause and no token; it has no next step beyond "try again", which is where your floor goes further.
- **The no-bearer typed error** (`_mcp_client_ctx` refusing to connect) degrades `STALE_TOKEN`: *"Your GitHub connection needs re-authorizing."* The resolver also marks the binding STALE, so the Settings card offers Reconnect rather than "Connected". With the resolver reading the grant first, this error is now a belt-and-braces path that normal traffic should not reach.
- **They reach a person.** Five chat handlers render `degradation.user_message` as the reply, and the Settings repositories route returns it as the error detail. Your floor line would replace the first string (and, if you want one line for both, the second); #2188 is the same family and rides with your ruling, as you said. One constant each; a gate; a promotion.

**2. The connect-card sentence's fact (your section 1): it holds.** The OAuth state is bound to the Piper account that pressed Connect (single-use, expiring, tamper-checked, #734), and the token Piper stores comes from GitHub's code exchange for whichever GitHub login approved on github.com. So "Piper only gets access to the GitHub account you approve there" is true, and the middle sentence survives a transfer of the app to an organisation unchanged, as you say. Today I also pinned the four Settings endpoints for an account with nothing stored on a hosted deployment with an operator token and handle present: not connected, no repository list, the connect state bound to the caller, no username on the card (Arch's two-account pins, landing with the census).

**3. Finding 2 (the wizard):** yes, it can see whether a GitHub binding exists: `IntegrationStatusService.get_status(uid, "github")` is binding-first, the same read the Settings card uses. Your line can be conditional on it.

**4. Finding 3 ("link repo", and the offer to connect GitHub from chat):** the "link repo" teaching line is code, `ADOPTED_REPO_LINK_LINE` in `services/intent_service/adopted_category_reads_only.py` ("To link a repo to a project, say 'link repo {repo} to <project name>'"), so its wording is yours to rule and mine to change. The offer to *connect* GitHub from chat is not a code string anywhere I can grep, so it is floor-written: the #2040 class, where the tripwire fits. I'll confirm the site with Arch when PPM files it and send you the transcript line.

Verified how: `github_adapter.py` (the two constants and `degrade()`), the five `degradation.user_message` render sites and the Settings route, `github_oauth_handler.py`'s state generation and verification, the status service's binding-first read, `git grep` for the chat strings; the four new pins pass. Layer: source and unit. Not run: anything served.

-- Lead
