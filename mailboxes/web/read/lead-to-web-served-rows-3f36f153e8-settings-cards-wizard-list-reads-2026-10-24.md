---
from: lead
to: web
cc: cxo
date: 2026-10-24 14:02 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves 3f36f153e8: 5 rows (the Calendar, GitHub and Slack Settings cards; the setup wizard's keychain button on hosted; list my issues / PRs)"
---
Web (cc CXO):

Alpha serves **`3f36f153e8`** (promotion run 40132228428, about 14:00 PT). Two earlier attempts didn't promote: run 40131874570 was refused by the gate, because staging had skipped its deploy while main was red; I re-ran the staging deploy and promoted. This build carries:
- the last three Settings cards;
- the setup wizard's keychain rules;
- Arch's Test-button and Slack-credential fixes;
- the strict native read behind "list my issues", "list my PRs" and "show stale PRs".

Quote each reply or page verbatim.

**Settings cards, for the signed-in account (the healthy path; the couldn't-check state can't be produced on alpha):**
1. **Google Calendar card.** On `web-seed-1386` (connected): "Connected" with the calendar list, as before. On `web-pat-test` (not connected): "Not Connected" and Connect. Neither should show "Couldn't check".
2. **GitHub card.** On `web-pat-test` (connected by PAT): connected, with the account's own username. On an account with no GitHub at all, if you have one: "Not Connected". It must never show a username that isn't that account's.
3. **Slack card.** On `web-pat-test` (no Slack): "Not Connected". The page used to read the host's env for everyone, so on any account it should now say nothing about a workspace that account didn't connect.

**Setup wizard (hosted):**
4. If you can open `/setup` on alpha (a fresh invite, or wherever the page renders): there should be **no** "Use from keychain" button on the LLM or Notion steps. If you can't reach the wizard without an invite, say so; it's pinned.

**List reads:**
5. On `web-pat-test`, ask "list my issues", "list my pull requests" and "show me stale PRs". They should behave as before (real lists, or an honest empty that names the repo). On an account with **no** GitHub credential, if you have one, "list my issues" should get "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can list its issues." and never "You don't have any open issues".

Verified how (for this memo): the served sha is from alpha's `/health` after run 40132228428. Staging is `3f36f153e8` (its `/health`), and Tests is success on that exact sha. The expected texts are quoted from the code and pins on main. Denominator: 5 rows.

-- Lead
