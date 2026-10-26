# #2018 recovery card: a dead GitHub connection, recovered from the UI alone

**For:** xian, with PA. **Build:** alpha `69d859ca5f` (or later; read the sha at the start). **Time:** about 15 minutes.
**Account:** xian's own alpha account (the one from card A1 on 10-17).
**Card by:** PA, 2026-10-26, on Lead's 12:48 memo.

## What this proves

#2018 is done when a user whose GitHub grant was revoked can do three things from the UI alone: see that it's broken, then reconnect (or disconnect, then connect), then see it working.

- **Reconnect is already proven.** Card A1 on 10-17 (alpha `118241587e`, your account) went revoke, "Needs reconnecting", Reconnect, working standup, 4 of 4: `dev/2026/10/17/controls/served-a1-xian-broken-grant-118241587e-2026-10-17.md`.
- **Disconnect, then Connect, has never been run on a dead grant.** It waited on #2172 (Disconnect claimed success when a copy failed to clear), which closed today. **This card runs that path.**
- **No console snippets this time.** "UI alone" is the bar. Use only the pages, the buttons and the chat box.

## Before you start (PA)

- Read `/health` and note the sha.
- If you have a personal access token (PAT) saved for GitHub on this account, say so first. With a PAT, the stale page reads "Connected via your personal token" plus the re-authorize warning (#2029). That's correct, but it isn't the no-token case #2018 is about.

## Steps

**1. Revoke (your hand, at GitHub).**
GitHub → Settings → Applications → Authorized OAuth Apps → Piper Morgan → Revoke.
Disconnect in Piper doesn't revoke at GitHub (#2178, Production), so this step stays yours.

**2. See it's broken.** Open alpha → Settings → Integrations.
- Expect the GitHub card to read **⚠️ Needs reconnecting**, "GitHub no longer accepts your connection.", with **Reconnect with GitHub** and no Test button. It should never say "Connected" or "Not configured".
- If it still says Connected, press **Test** (if shown). Expect "Test Failed: Your GitHub connection needs re-authorizing". The card reads GitHub only when something calls it.
- Then ask in chat: **"show my open pull requests"**. Expect a plain "needs re-authorizing" reply, not a list and not an empty "no PRs".

**3. Disconnect.** Settings → GitHub (`/settings/integrations/github`, or the card's link) → **Disconnect**.
- Expect a confirm dialog first. Note its words.
- Then expect one of two outcomes. Either "disconnected" with the page offering **Connect with GitHub**, or CXO's "incomplete" line naming what's left (a 503 from #2172's fix).
- **Either outcome is honest. Tell me which one you get, word for word.** A claimed success with a connection still shown would be the #2172 failure.

**4. Connect.** Press **Connect with GitHub** on that page.
- GitHub's own screens follow: the account chooser, Authorize, maybe a sudo confirm. They're GitHub's, not Piper's.
- Expect to land back on alpha with a success state.

**5. See it working.**
- Integrations: the GitHub card should read **Connected with your GitHub account.** Press **Test**: expect "Connected with your GitHub account. Checked just now."
- Chat: ask **"show my open pull requests"** again. Expect your real PRs, or an honest "none open".

**6. (Optional, if time) Reconnect on this build.** Repeat step 1, then use **Reconnect with GitHub** from the card instead of Disconnect, then step 5. This re-runs A1 on the new build. Skip it if we're past 15 minutes.

## What I need back

A screenshot or the exact words at steps 2, 3 (the dialog and the result), 4 (the page you land on) and 5 (the card, the Test toast, the chat reply). Note anywhere you had to guess where to go. Your bar from #2039 is user flow, IA and guessability.

## Pass, and what follows

- **Pass:** every expected line in steps 2 to 5 seen, with no console use and no help from PA beyond this card.
- PA posts the readings on #2018. CXO judges the words, and the issue closes with close-issue-properly.
- **Any miss:** PA files it, or reopens the child it belongs to, and #2018 stays open.
