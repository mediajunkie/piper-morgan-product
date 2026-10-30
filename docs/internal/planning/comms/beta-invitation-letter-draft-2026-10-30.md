# First beta invitation: letter draft (for xian, #1386 row 6)

**Drafted:** Comms, 2026-10-30 15:0x PT, after Exec's 14:52 relay ("xian announced at his talk today that private beta starts today").
**Built from:** the 10-26 alpha letter (`design-partner-invitation-send-ready-2026-10-26.md`), which partners have already received, and the known-issues list (`design-partner-known-issues-and-calendar-lines-2026-10-19.md` §1, PPM pre-check 08:04 10-30: all six hold).
**Placeholders:** `{NAME}`, `{CODE}` and `{URL}`. Never put a real name or code in this repo. Names and categories stay in HOST's roster.
**Not settled by this draft:** who gets it and when (xian's walk with HOST, in progress), and the four open points at the bottom.
**Row 6 path:** xian edits → CXO reads → PPM checks each known-issues line against GitHub at send and strikes any whose issue has closed served → xian's go on #1386.

---

**Suggested subject:** Your invitation to the Piper Morgan beta

## Who gets which version (HOST 15:03, from xian's walk. Counts only, names in HOST's roster)

| Version | Who | Count | Differs in |
|---|---|---|---|
| **1a** hands-on, new to the hosted app | practitioners plus one QA tester | 6 | opening, gets `{CODE}` |
| **1b** hands-on, already in the alpha | the two 07-12 hosted-alpha users and the three 10-26 invitees | 5 | opening, and "Getting in" says sign in with their account, no code (see open point 5) |
| **2** expert group | friends and advisors, not practising PMs | 3 | opening and one framing line (xian wants it a little different) |
| Hold | not in the first send | 1 (plus a referral) | send nothing |

Several in 1a have used the earlier local-run alpha (2025 to Jan 2026), so not every opening should read as a cold open. Two of the 11 are very busy, so every version keeps the alpha letter's light ask. All openings are new wording, which xian edits freely.

## Opening 1a: hands-on, new to the hosted app

> Hi {NAME},
>
> The private beta of Piper Morgan starts now, and I'd love to have you in it. Here's your invitation. Give it a try when you feel like it.

*If they used the local-run alpha, add after the first sentence:* "You saw an early version when it still ran on your own machine. This one runs on our servers, and it has come a long way since."

## Opening 1b: hands-on, already in the alpha

> Hi {NAME},
>
> Thank you for trying the alpha. The private beta starts now, and you're in it. You don't need a new code. Your account and your work carry over.

## Opening 2: expert group

> Hi {NAME},
>
> The private beta of Piper Morgan starts now, and I'd love your eyes on it. You don't need to be a working product manager to be useful here. I'd value your read on whether it makes sense, what feels off, and where it should go. Give it a try when you feel like it.

## What this beta is (xian's paragraph, not drafted)

*Slot for your own words. The alpha letter's "Alpha is nearly over!" paragraph doesn't fit a beta letter, so it's out. Prompts, if useful: what a tester can expect day to day, how rough it still is, and what you most want them to try. Keep it to what is true today (no promised fix dates).*

## Body (from the alpha letter, unchanged except where marked)

*Version 1b only, replacing "Getting in" below:*

> **Getting in.** Go to {URL} and sign in with the account you already have.

*Versions 1a and 2:*

> **Getting in.** Go to {URL} and choose "Create your account". The first step asks for your invite code:
>
> {CODE}
>
> It works once, for one account, so please don't share it. The next step asks for your Anthropic API key, so have one ready.
>
> **What you can connect.** Piper works with GitHub and Google Calendar. With Calendar connected, you can ask about today's meetings or this week's, and your standup includes them. Piper only reads your calendar. It can't change it.
>
> When Google asks, make sure the box next to "See and download any calendar you can access using your Google Calendar" is ticked, or Piper can't read your calendar.
>
> **Who sees it.** Piper sends your messages, and anything it adds from the tools you connect (such as calendar or GitHub items you ask about), to Anthropic under your own key. From there, Anthropic's own terms and privacy policy apply. Our admin tools don't display your conversations, and our server logs don't keep the text of what you send. The app has no analytics or ad tracking.
>
> **Your key.** Piper runs on your own Anthropic key. We store it on our server in encrypted form and use it only to make your own requests. We hold the key that unlocks it, so in principle we could read it. Please use a key with a spending limit you're comfortable with. We don't read it on purpose. You can remove your key in Settings at any time, and that deletes it from our live database. Our encrypted backups can keep it for up to about five days. To cut off access completely, also revoke the key in Anthropic's console, so it stops working for Piper too.
>
> **What you're agreeing to.** The plain-language terms are at https://pipermorgan.ai/terms/ and our privacy page is at https://pipermorgan.ai/privacy/. Please read them before you start.
>
> **Known issues in this beta**
>
> - **Piper sometimes misreads what you ask.** It may answer a different question or give a general reply. Rephrasing usually works.
> - **An answer about your own data can be wrong.** Now and then Piper states something about your projects, issues or to-dos that isn't right, such as a wrong count. If an answer looks off, check the source and tell us.
> - **Piper can state a detail about one of your records, such as a milestone or when something last changed, that it did not look up.** Check anything that matters in GitHub before you rely on it.
> - **Asking for a milestone's issues in two steps ("show issues from one milestone", then the name) can list the wrong issues.** Ask in one step instead, with the milestone's name in the same sentence, such as "show my open issues in the Launch milestone". This is a known issue and isn't fixed yet.
> - **No undo for deleted to-dos.** Deleting a to-do is permanent for now, and "delete all my to-dos" deletes one at a time.
> - **Searching your documents from chat doesn't work yet.** You can upload a file and ask Piper about it by name, or paste the text into the chat.
>
> **Feedback and help.** When you find something new, send feedback from the left-hand menu once you're in the app, or email support@pipermorgan.ai. Either way the message will be read by the team, including by me (xian), the human who owns this particular loop.
>
> Thank you for trying it.
>
> xian

---

## What changed from the alpha letter

| Piece | Change | Why |
|---|---|---|
| Openings | New: 1a, 1b and 2 (HOST's groups, 15:03) | Three groups, and not every opening is a cold one |
| "Alpha is nearly over" | Out, replaced by a slot for xian | It describes the alpha |
| Carry-over paragraph | Out, folded into opening 1b as one sentence | Only the five alpha people have accounts that carry over |
| Getting in | URL is now `{URL}` | See open point 1 |
| Known issues | Heading "in this beta". Six lines, not five: the #2018 GitHub line is struck (closed served 10-28), and the two 10-29 lines (#2042 class, #2184) are in. Order puts the two "wrong answer" lines together | PPM 10-29 and 10-30. Issue numbers are dropped from the letter, as in the alpha one. They're in the known-issues doc |
| Everything else | Unchanged, verbatim | Final pieces the alpha partners already have |

**Served facts, re-read by Comms 10-30 14:5x (curl, text not rendered):** alpha and beta `/health` both 200, both `git_sha` e234776150. Alpha `/login` has "Create your account". Alpha `/setup` has "Invite", "Paste the code you received." and "API Keys". `/terms/` and `/privacy/` 200. The Terms still carry "We hold the key that unlocks it" and "Our admin tools don't display your conversations". Exec's 14:52: a promotion of main is about to go out, so re-read these after it serves.

## Open points before it goes

1. **Which URL?** beta.pipermorgan.ai and alpha.pipermorgan.ai serve the same build today. *Exec 15:01:* PA runs one fresh sign-up on beta. with the re-checks on the promoted build. If it passes, Exec recommends "beta." to xian. If not, "alpha." stays. HOST 15:04 would watch it with xian present. *PA 15:1x:* beta. serves the promoted build, `ac5b69f865`. The fresh sign-up spends a single-use code, so it needs xian's hands. PA has given him the steps. Until it's run, the letter keeps "alpha.".
2. **The Terms page still says alpha.** HOST 15:04 recommends changing it before the first send. The proposed wording is below. Who edits the served page, and whether it needs a version bump, is xian's and Web's call. If xian sends first, HOST suggests one plain line in the letter: "Our Terms page still uses the word alpha. Everything in it applies to the beta."
3. **xian's "what this beta is" paragraph.**
4. **PPM's line check at send**, after the promotion and PA's re-checks.
5. **Version 1b's "no new code, your account carries over": VERIFIED (PA 15:1x).** On beta. (serving `ac5b69f865`), an alpha test account logged in, and a chat turn saw issue #35, which had been created on alpha. at 15:04. So it's the same accounts and the same data. That was an API check, not the rendered sign-in page. Whether the three 10-26 codes were redeemed is still unread (HOST: xian's select).

## Terms page: proposed beta wording (for xian and Web, HOST 15:04 asked for it)

Source: website `src/app/(public)/terms/page.tsx`, read at origin/main 506a65c. "Alpha" appears in exactly two places. Nothing else changes, because the trust content is the same.

| Where | Now | Proposed |
|---|---|---|
| Page description (meta) | "What you are agreeing to when you use the Piper Morgan alpha: …" | "What you are agreeing to when you use the Piper Morgan beta: …" |
| Section heading | "What this alpha is" | "What this beta is" |
| That section's body | "Expect errors, and go carefully. Using your real work is OK." | Unchanged. It's still true |
| "Last updated" | October 25, 2026 | The date Web ships it |

The "Before Production, we'll add…" paragraph under that heading still reads true for a beta, so it stays.

**Voice check (Comms, on the quoted letter only):** 0 semicolons. No "honest", "quietly", "load-bearing" or "cohort". Agents aren't called people.
