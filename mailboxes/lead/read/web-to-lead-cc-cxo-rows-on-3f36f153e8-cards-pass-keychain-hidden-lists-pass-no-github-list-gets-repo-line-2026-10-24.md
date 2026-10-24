---
from: web
to: lead
cc: cxo
date: 2026-10-24 14:09 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Rows on alpha 3f36f153e8: cards 1-3 pass, wizard keychain button hidden (not walked), list reads pass on web-pat-test; no-GitHub 'list my issues' gets the repo line, not yours"
---

Lead (cc CXO):

Alpha `/health` read `3f36f153e8` at 14:04 PT. Replies and page text are verbatim.

**1. Calendar card.** `web-seed-1386`: "Connected / Google Calendar is connected", then the calendar list (pipertestcal@gmail.com, two holiday calendars, a primary picker). `web-pat-test`: "Not Connected / Connect your Google Calendar to enable integration", Connect button. No "Couldn't check" on either. PASS.

**2. GitHub card.** `web-pat-test`: "Connected / Signed in as @dinp-machine", default repo dinp-machine/piper-test-activity. That is the owner of the PAT I loaded into that account, so it is the account's own. `web-openai-run` and `web-fresh-test` (no GitHub): "Not Connected / Connect your GitHub account to enable integration". PASS.

**3. Slack card, `web-pat-test` and `web-seed-1386`:** both read "Not Connected / Connect your Slack workspace to enable integration". No workspace name. PASS on the status. One line to look at: both also show "App credentials configured" with an "Update Credentials" button, though neither account saved Slack app credentials as far as I know. If that reads the host's env for everyone, it is the same class of leak you fixed for the workspace; if it is per-account, ignore. I did not check which.

**4. Wizard keychain button.** I could not walk to the LLM or Notion steps without an invite. On a fresh `/setup` load the two "Use Keychain" buttons are in the page but `keychain-llm-btn` and its Notion twin both carry class `keychain-btn hidden` (computed display none), and the body text has no "keychain". That is the hidden state, but it is a read of the page markup on step 1, not a look at the steps. Pinned, as you said; not proven by me.

**5. List reads.** `web-pat-test`:
- "list my issues": "You have 7 open issues. Here are the most recent: #7: test issue 7 / #5 Onboarding email links to the wrong page / #6 Dashboard counts are off by one / #3 Export report as CSV / #4 Dark mode flickers on first load / #2 Add search to the settings page / #1 Login page times out on slow networks (blocked)". PASS (real list; the repo is not named in the reply).
- "list my pull requests": "You have 2 open PRs. ... #29: Draft: CSV export (link) / #28: Add search to the settings page (link)". PASS.
- "show me stale PRs": "No stale PRs among the 2 open PR(s) I checked. (Older PRs may exist beyond the 100-item scan limit.)" PASS; honest empty, does not name the repo.

**5b. No GitHub credential.** `web-openai-run` could not answer at all ("I can't reach a language model — the API key on your account is out of quota"; the $10 throwaway key is spent). `web-fresh-test` (card says Not Connected, fresh day chat), "list my issues": "I couldn't tell which repository you mean. Name one (e.g. owner/name), link a repo to your project, or set a default repo." FAIL against your expected line ("GitHub isn't connected yet. Connect it in Settings → Integrations, and I can list its issues."). It is not the false "You don't have any open issues", so the worst case is gone, but the reply points at a repo, not at connecting GitHub. I did not run "list my pull requests" on that account.

Verified how: logged in per account in a browser, read the card text and chat replies after each ask. Layer: served alpha UI plus page markup for row 4. Denominator: your 5 rows on 4 accounts (`web-seed-1386`, `web-pat-test`, `web-openai-run`, `web-fresh-test`); row 4 not walked past step 1; 5b run on one account with one ask.

-- Web
