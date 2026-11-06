---
from: web
to: lead, cxo, pa
cc: ppm, arch, exec
date: 2026-11-06 13:13 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Served read on beta 765a2bc4f1: Settings groups, project words, Edit gone and the sign-in words all pass. The #2286 approval note I could not see, because both accounts I may use are connected"
---

Lead, CXO, PA (cc PPM, Arch, Exec),

Beta's `/health` reports `765a2bc4f1`. I read it signed in as web-seed-1386 (not an admin), in a browser, at 13:13 PT. Quotes are from the rendered page.

1. **Settings (#2273).** Four groups in this order, each with its cards: "Connect Piper to your tools" (Integrations, Projects, LLM API Keys, Connected apps); "About you" (Account, Preferences, Personality, Learning & Patterns); "Privacy and trust" (Privacy & data, Transparency); and the last group, which reads **"Advanced"** for this non-admin and holds only the Advanced card. Integrations is first. Its words: "Connect your tools, such as GitHub, and check that each one is working." Clicks: Settings is one click from the app; the Integrations page is two; the GitHub row is on that page, with "Connected as dinp-machine. Not the right account? Disconnect, then connect again."
2. **Project page (#2272).** On "Mobile Redesign" (no repository linked) the button is "Link a repository" and the empty state reads: "No repository is linked to Mobile Redesign yet." On "Piper Test Activity" (one linked) the buttons are "Link a repository" and "Unlink". The Unlink dialog (`Unlink {repo} from {project}?`, "This only removes the link in Piper. The repository itself is not changed.") I read in the served script and did not press, as PA asked me to leave the link in place. The link dialog is still a dropdown of registered repositories labelled "Repository (owner/name)", as CXO accepted.
3. **Projects list (#2271).** Each row has Remove only. No Edit. The only "coming soon" left in the served page is a code comment.
4. **Sign-in (#2267).** The email `Web-Seed-1386@TEST.invalid` (wrong case) with the right password signed in. A wrong password gave: "That email and password didn't work. Check both and try again, or use Forgot password."
5. **GitHub approval note (#2286). Not read on a page.** Both accounts I am cleared to use (web-seed-1386 and web-oauth-test) are connected, and the page swaps the Connect group for "✓ Connected with GitHub." once connected, so the note is not on screen for them. The note is in the served HTML of the GitHub settings page ("GitHub will ask you to approve Piper Morgan. Its page names the account that owns the app, which is Piper's and not yours, and says which of your GitHub accounts it wants to access. Check that account is the one you mean. Piper only gets access to the account you approve there."), so the words are served. Seeing it above "Connect with GitHub" needs an account that is not connected. I will not disconnect these two, since they hold the grants other checks use. Lead or PA: say if a not-connected account exists, or if xian wants one of these disconnected for the read.

Verified how: browser sign-in on beta, rendered DOM reads of /settings, /settings/integrations, /projects and two project pages; the served HTML and script for items 2 and 5. Layer: rendered pages on the deployed build, not source. Denominator: 5 of Lead's 5 web items; 4 read on the page, 1 (the note) read in the served HTML only. I did not press Unlink, Disconnect or any write.

-- Web
