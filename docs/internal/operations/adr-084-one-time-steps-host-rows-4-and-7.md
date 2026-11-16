# ADR-084 one-time steps: HOST's rows 4 and 7

Written 22:09 PT 2026-11-15 by HOST for Exec's 01M7HF64B8 (pre-written, so xian's yes is followed by a paste). **Nothing here runs or is shown to xian as approved until he says yes to ADR-084.** CIO's file for the other rows may be a separate one; fold these in or link them, whichever Exec prefers. Rows follow the ADR's "What xian does, once" numbering.

Rule for every step below: a password, a 2FA code or a token is typed by xian into the provider's own page or a hidden prompt. It is never typed or pasted into a seat's session, a mail, a log or a file in the repo.

---

## Row 4: the test GitHub machine account (create, bound in the org, connect, then install)

**Status: PARTLY NOT READY.** The "connects it on the second seat account" part needs that beta account to exist. The ADR does not say who creates it (Lead's seed script, or Web). Arch or Lead: name the owner and tell Exec. Until then, steps 1 to 3 can be done; steps 4 to 7 wait.

**Why a machine account:** GitHub's terms (Section B.3, read 11-15) allow one free machine account beside a personal account, and forbid a second personal one. A human must create it.

1. **Create the account.** At github.com/signup, in a browser window where you are NOT signed in to your own GitHub (a private window is enough). Username: `<machine-account-name>` (your choice; it will be public, so not your name or a tester's). Use an email address you control that is not your main one. Then turn on 2FA with an authenticator app; **keep the 2FA secret in your own password manager, nowhere a seat can read.** Put in the profile bio: "Machine account for Piper Morgan test automation." *(Recommended, not something GitHub's terms require as far as I read.)*
   - **You should see:** the new account's empty dashboard.
2. **Bound it in the org.** Signed in as yourself: github.com/organizations/pipermorgan/settings/member_privileges, set **Base permissions** to **No permission**. Then github.com/orgs/pipermorgan/people, **Invite member**, enter the machine account's username, role **Member** (never Owner). Accept the invitation while signed in as the machine account. Then Teams, create a team `seat-test`, add the machine account, and give the team access to the **test repositories only** (`piper-test` and the second private test repository). Nothing else.
   - **You should see:** the account listed under People as Member, and the team's Repositories tab listing only the test repositories.
   - Also check: the account is not a collaborator on `mediajunkie/piper-morgan-product` or any repository of yours (each repository's Settings, Collaborators).
   - **One thing I have not read:** whether this account counts as a paid seat. Look at github.com/organizations/pipermorgan/settings/billing and tell Exec what the seat count line shows.
3. **Do not install the App yet.** The order matters: connect first, install second, with PA's read in between (the "installed nowhere" line can be read once only before the first install).
4. *(waits on the beta account)* **Connect.** In the dedicated seat browser (only once row 10 has loaded it; before that, any browser window you sign in and out of) sign in to beta as the **second seat account** (you type its password at beta's login page). Settings, Integrations, GitHub card, press Connect. GitHub asks you to sign in: sign in as the **machine account** (you type its password and the 2FA code). On GitHub's authorize page, read the App name and the permissions list before pressing Authorize; it should be the one Piper App (client ID `Iv23…tj64`).
   - **You should see:** beta's GitHub page saying "✓ Connected with GitHub", no token form.
   - Tell Exec "connected, not installed". **Stop here until PA's zero-install read is done.**
5. **Install, after PA says go.** On beta's GitHub repositories section press "Install on GitHub". On GitHub choose the `pipermorgan` account, **Only select repositories**, pick `piper-test` only, Install.
   - **You should see:** beta's repository list showing `piper-test` and nothing else.
6. **Sign out of GitHub** in that browser (so the profile does not keep the machine account signed in).
7. **Seat checks afterwards (names and counts only):** Web reads the repository section as the seat account; PA reads the connector (expect only `piper-test` items); HOST reads what the account holds and records it.

**If it fails or looks wrong:**
- Authorize page shows another App name, extra permissions, or asks for access to all repositories: **do not press Authorize**; tell Exec.
- Undo, in this order: beta Disconnect button on the GitHub page (clears the stored token); GitHub, the machine account's Settings, Applications, revoke the App; remove the install on the `pipermorgan` org's Installed GitHub Apps; remove the machine account from the org.
- 2FA lost: GitHub's account recovery for the machine account only; nothing else of yours depends on it.

---

## Row 7: the MCP app deploy token and its GitHub environment

**Status: NOT READY.** Waits on **#2384** (the job and the secret's exact name) and on **Lead stating what a Fly deploy token for this app can do beyond deploying** (HOST runs no fly; I have not verified whether such a token can run commands inside the app, which would make it production-database reach). The names below are placeholders until #2384 fixes them.

1. **Create the environment.** github.com/mediajunkie/piper-morgan-product, Settings, Environments, **New environment**, name `<environment-name from #2384>`. Under **Deployment branches and tags** choose **Selected branches and tags**, add **main**. (This is what stops a branch pushed with an edited workflow from reading the secret.)
   - **You should see:** the environment page showing the branch rule "main".
2. **Create the token and copy it without showing it.** In Terminal, any folder:
   `fly tokens create deploy -a piper-morgan-mcp -x <lifetime> | pbcopy`
   *(exact command and expiry flag: Lead confirms before this goes on the card; HOST has not run it.)* It must name the app `piper-morgan-mcp` and **no other app, never an organization-wide token.** The token goes to your clipboard and nothing prints.
3. **Store it.** On the environment page, **Add environment secret**, name `<secret-name from #2384>`, paste, save. Then clear the clipboard: `pbcopy < /dev/null`.
   - **You should see:** the secret's name listed, "Updated now". The value is never shown again.
4. **Tell Exec the date and the expiry** you chose (HOST's custody row takes both; no value).
5. **Seat check afterwards (names only):** `gh api repos/mediajunkie/piper-morgan-product/environments/<environment-name>` shows the branch policy; the same path with `/secrets` lists secret names. If the seat's access is refused, that is fine; Lead reads the first dispatch's output (sha and release only).

**If it fails or looks wrong:**
- `fly tokens create` offers or defaults to a wider scope: stop and tell Exec; do not store it.
- Undo: delete the secret and the environment on GitHub; in Terminal `fly tokens list -a piper-morgan-mcp` and revoke the token's entry (Lead gives the exact revoke line).
- Token seen anywhere in clear (a session, a log, a mail): revoke the same day and create a new one.
