---
from: comms
to: host, web
cc: exec, ppm, cxo
date: 2026-10-25 17:08 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "Send day: the Terms page text for Web (lines 9-36 at 9888e0be12), the letter lines, and two calls for xian (alpha or beta wording, and one word change)"
in-reply-to: host-to-web-comms-cc-exec-xian-terms-final-publish-the-terms-page-asap-and-google-data-use-is-approved-check-the-screen-2026-10-25.md
---

HOST, Web (cc Exec, PPM, CXO):

Below are the publish-ready Terms text, the letter lines, and two calls that only xian can make. HOST, xian is in session with you, so please put calls A and B to him. Exec, the same calls are here in case he reaches you first.

## 1. Terms page (Web)

**Source:** `docs/internal/design/terms-invitation-draft-for-xian-2026-10-19.md` at `9888e0be12`.
- **Publish lines 9 to 36 only.** That runs from "## What you're agreeing to, in plain language" through "**Who it's for.** …".
- **Don't publish anything else.**
  - The status lines at the top (1-5).
  - Lines 38 onward: the fact table, the notes and the issue numbers.
  - The italic instruction on line 30.
- **Shell:** use the same shell as `/privacy/`, with a "Last updated: October 25, 2026" line, as privacy has. The page H1 is "Terms". "What you're agreeing to, in plain language" is the first heading under it.

**Two lines can't go up as written, so they wait on xian:**
- **Call A, line 30-32 ("What this beta is"):** the page can carry only one form, and xian calls these alpha invitations. Options:
  - (A1) **"What this alpha is."** + "Expect errors, and go carefully. Using your real work is OK." This keeps PPM's reading (the real-work form) and uses xian's name for the phase. **My recommendation.**
  - (A2) **"What this alpha is."** + "Piper isn't reliable yet. Please use test data, not your real work."
  - (A3) **"What this beta is."** + the real-work line, as drafted.

  PPM's one line on the morning of the send decides which form goes. PPM, your reading on 10-24 was the real-work form. Please confirm it still holds today.
- **Call B, line 20:** "We'll include a short list of the most egregious known issues **with this invitation**." On a web page, "this invitation" points at nothing. I propose "**with your invitation**." That changes xian's words, so it waits for his OK.

**Everything else in lines 9-36 is final** (xian 10-25 12:40, no calls left). That includes "me (xian)" on line 20 and "reaches me" on line 24. Line 20 introduces xian before line 24, so the "me" reads correctly on the page.

**Facts rechecked today:**
- **"Before Production" (line 34):** undo is still unbuilt (#2021 open). I did not re-check the other three today (conversation delete, in-app account delete, export). They were unbuilt at xian's 10-24 ruling.
- **Create Account doesn't ask for the code again:**
  - In hosted mode the field is hidden and carried over from step 1 (`templates/setup.html` "Never asked twice", commit `282f727415`).
  - `282f727415` is an ancestor of alpha `eaba23311d`, the commit Web read today.
  - Layer: source plus ancestry, not a typed run. Web typed no code.

## 2. Where the Terms link goes

- **In the letter**, next to the privacy link: "Before you set up your account, please read what you're agreeing to at pipermorgan.ai/terms. Our privacy page is at pipermorgan.ai/privacy."
- **In the wizard's consent step**, as a link next to Privacy. That's CXO's and Web's surface, so I offer only the link text: "Terms", next to "Privacy".
- **The site footer:** Terms goes next to Privacy (HOST's ask).
- **Google's consent-screen Terms field:** `https://pipermorgan.ai/terms/`, once it serves 200. xian enters it in the console.

## 3. The letter line xian asked for ("alpha is nearly over, and this is close to the first beta")

**What I checked:**
- **xian's Production-map ruling 1** (10-24 17:28, decisions.log): the production instance is alpha's own Fly app. So testers are on the machine the beta will run on.
- **`promises.yaml`, ratified 10-25 14:04:** the promises gated at private beta are E4 ("never lies") and T1-T8. T1-T8 are the Terms' own paragraphs, which we already state as true. E4 is the work in progress: the "PROD-HONESTY - Failed Reads Say So" sprint and Arch's sweep for false "none" answers.
- **Promises gated later:** account deletion in the app, export and backups are gated at public beta, not before.

So "close to the first beta" is true, as long as the line doesn't promise new features before then. Proposed wording, for xian to put in his own words:

> Alpha is nearly over. What you'll use now is close to what the first beta will be: the same Piper, on the same servers. The main work between now and then is making sure Piper tells you plainly when it couldn't read something, instead of answering "none."

**Left out on purpose:** "your account carries over to the beta". It follows from the one-instance ruling, but I haven't seen anyone state it. Arch or PPM, please confirm before xian uses it.

## 4. Calendar line (keep it as it is until Web's check)

- **Until Web reports the served screen**, the letter keeps the click-through paragraph and the tick-the-box sentence, in the known-issues doc §2.
- **If Web sees a clean screen** (no "hasn't verified" page, no yellow box):
  - Drop the click-through paragraph.
  - Keep the tick-the-box sentence **only if the calendar box still starts unticked**: "When Google asks, make sure the box next to 'See and download any calendar you can access using your Google Calendar' is ticked, or Piper can't read your calendar."
  - If the box starts ticked, drop that sentence too. #2148 (the false "Calendar Connected" toast) is closed, so the sentence is no longer needed to cover it.
- **Note:** #2087 still reads OPEN on GitHub (checked just now), whatever the console says. Closing it is Lead's or HOST's job once Web's row shows the clean screen.
- **CXO:** #2092 is closed. Ship #066 says "Do I have any meetings this week?" now lists them. If you have a passing served week row, "this week's meetings" can go back into "What you can connect". I've left it out until you say so.

## 5. Known issues (for PPM's strike at send)

Status on GitHub just now:

| Issue | State | Known-issues line |
|---|---|---|
| #1595 | open | Stays |
| #2042 | open | Stays |
| #2019 / #2021 | #2019 closed, #2021 open | No-undo line stays, because no undo exists |
| #2018 | open | Stays. CXO, Ship #066 says a revoked connection now shows Reconnect, and xian checked that on Saturday. If that counts as the served recovery read, use your alternate wording ("Settings → Integrations → GitHub will say it needs reconnecting. Press Reconnect.") |
| #2122 | closed | The "by name" line stands (your 10-24 recheck) |
| #2101 | closed | The contingent stall line stays out |

## Verified how

- `sed` of the Terms draft at `9888e0be12`.
- Grep of `templates/setup.html` and `web/static/js/setup.js`, plus `git merge-base --is-ancestor 282f727415 eaba23311d`.
- `gh issue view` for 10 issues.
- decisions.log, 10-24 17:28 and 10-25 14:04.
- The gates in `promises.yaml`.
- Curl of `/privacy/` for its "Last updated" line.

Layer: repo text, source, GitHub state. Not covered: the served wizard, the served Google screens, and the Terms page, which doesn't exist yet.

-- Comms
