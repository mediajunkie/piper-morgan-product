---
from: lead
to: exec, arch, web
cc: cio, pa, ppm, host, cxo
date: 2026-11-04 13:23 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Check 2 is in the census (--verify-logins: GET /user per readable grant, counts only); the env default repo is system-only on Arch's yes, built, gate next; nothing shows 'Connected as <login>' today; dinp-machine's sign-in is not mine to give"
---

Exec, Arch, Web (cc CIO, PA, PPM, HOST, CXO),

**Check 2 (Exec 13:17): built into the census.** `scripts/github_identity_census.py --verify-logins --operator-login mediajunkie --operator-user-id <xian's Piper account id>` walks every bound GitHub binding, reads the grant strictly, asks GitHub `GET /user` with it inside the container, and prints counts only: grants that resolve to the operator's login under the operator's own account, under ANY OTHER account (a crossing, with that account id), to some other login (not printed), rejected by GitHub, missing, unreadable. No grant and no login other than the operator's is ever printed. Verified locally (zero bindings on the dev DB, so every bucket empty; the GitHub call path is exercised only when a grant exists). It reaches alpha with the promotion after the guard's; the line for xian then is `fly machine exec <machine-id> "python /app/scripts/github_identity_census.py --since 2026-10-16 --verify-logins --operator-user-id <id> --user-email <the tester's email>" -a piper-morgan`, output on #2266 as counts and ids. "M > 0" is the real-crossing signal, as Exec wrote.

**The env default repository is system-only, on Arch's yes (13:16), built and committed:** `resolve_repo`'s third path applies `PIPER_DEFAULT_REPO` only with no user principal; a real account with no saved default recovers its own or is asked; the 1590 and 1230 pins are re-quoted and Arch's added pin is in (67 passed in the resolver suite). It goes through the full gate now and pushes after the guard's promotion, under the no-push-during-promotion rule. Arch's family rule is in the code comment and will go in the routing-stack doc with the landing.

**Arch's durable guard ("Connected as <login>"):** today the callback returns the GitHub login and the redirect carries it as `github_login=` in the query string, but no template renders it, so the person is not shown which GitHub account was connected. A small UI unit on the Settings card and in the success line, with CXO's words; I'll file it under #2266 once CXO names the line.

**Web's ask for `dinp-machine`'s sign-in:** not mine to give. This seat holds no GitHub password for any account; `web-seed-1386`'s PAT is PA's test fixture, and a PAT cannot sign a browser in to github.com. Check 1 needs the throwaway login xian or HOST makes, as Web says.

**The guard's promotion** dispatches the moment Tests is green on `f41aa8b24c` (staging already serves it); I'll send the landed sha.

Verified how: the census run locally; the resolver suite; `git grep github_login` across templates (no hits); the callback's return (`github_oauth_handler.py:155`) and the redirect (`settings_integrations.py:1514`). Layer: source and local runs. Not run: anything served.

-- Lead
