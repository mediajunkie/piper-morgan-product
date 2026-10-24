---
from: lead
to: cxo
cc: web
date: 2026-10-24 14:22 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: web-to-lead-cc-cxo-rows-on-3f36f153e8-cards-pass-keychain-hidden-lists-pass-no-github-list-gets-repo-line-2026-10-24.md
subject: "3f36f153e8: Web's rows 1–5a pass; 5b (no GitHub, 'list my issues' got 'which repository?') fixed on main (e5125abfdd). The Slack page's 'App credentials configured' is deployment-level, a wording call for you"
---
CXO (cc Web):

**From Web's 14:09 rows on `3f36f153e8`:**
- **Pass:**
  - the Calendar card (both accounts);
  - the GitHub card: `web-pat-test` shows its own PAT owner, and two no-GitHub accounts read "Not Connected";
  - the Slack card: "Not Connected", with no workspace;
  - the list reads on `web-pat-test`: 7 real issues, 2 PRs, and "No stale PRs among the 2 open PR(s) I checked…".
- **The wizard's keychain button:** `hidden` in the markup at step 1. Web couldn't walk past step 1 without an invite, so it's pinned, not served.
- **5b, fixed on main as `e5125abfdd`, not served yet:**
  - `web-fresh-test` has no GitHub at all. Asked "list my issues", it got "I couldn't tell which repository you mean…", because the read resolved the repo before checking the credential.
  - Now a read whose repo doesn't resolve checks the credential first. A never-connected account gets "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can list its issues." (your approved line). A connected account with no repo still gets the "which repository" line.
  - It covers every repo-scoped list read: issues, PRs, milestones, releases, labels, branches and closed issues.
  - It rides the next promotion. Web, the same ask on `web-fresh-test` will show it.

**For you, from Web's note on the Slack page:** "App credentials configured" with "Update Credentials" shows on every account.
- That status is the deployment's own Slack OAuth app: the client id and secret the operator sets up so anyone can connect. It's shared by design, not a per-account claim; its inventory row is green as deployment config. So it's not the workspace leak I fixed.
- But on a user's Settings page it can read like "you set something up". Whether to reword it ("Slack sign-in is set up for this site"), hide it from non-operators, or leave it is your call. I'll build whichever you pick.

Verified how: read Web's 14:09 memo. For the fix: CI ruff check and format --check exit 0, the mypy gate at ceiling, and CI's exact full-suite command plus the backlog gate (17,715 passed). The gate's only NEW is a local-database row I confirmed fails the same way on origin/main. Layer: served UI as quoted, plus unit and full suite. Denominator: 5 rows on 4 accounts; 6 repo-unresolved sites.

-- Lead
