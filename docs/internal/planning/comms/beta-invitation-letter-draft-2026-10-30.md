# First beta invitation: letter draft (for xian, #1386 row 6)

**Drafted:** Comms, 2026-10-30 15:0x PT, after Exec's 14:52 relay ("xian announced at his talk today that private beta starts today").
**Built from:** the 10-26 alpha letter (`design-partner-invitation-send-ready-2026-10-26.md`), which partners have already received, and the known-issues list (`design-partner-known-issues-and-calendar-lines-2026-10-19.md` §1, PPM pre-check 08:04 10-30: all six hold).
**Placeholders:** `{NAME}`, `{CODE}` and `https://beta.pipermorgan.ai`. Never put a real name or code in this repo. Names and categories stay in HOST's roster.
**Not settled by this draft:** who gets it and when (xian's walk with HOST, in progress), and the four open points at the bottom.
**Row 6 path:** xian edits → CXO reads → PPM checks each known-issues line against GitHub at send and strikes any whose issue has closed served → xian's go on #1386.

---

**Suggested subject:** Your invitation to the Piper Morgan beta

## Who gets which version (HOST 15:03, from xian's walk. Counts only, names in HOST's roster)

| Version | Who | Count | Differs in |
|---|---|---|---|
| **1a** hands-on, new to the hosted app | practitioners plus one QA tester | 6 | opening, gets `{CODE}` |
| **1b** hands-on, alpha accounts in use | the two who used the hosted alpha (07-12 on) | 2 | opening, and "Getting in" says sign in as usual, no code |
| **1c** hands-on, invited 10-26 | the three sent the 10-26 alpha letter. Whether they redeemed is unread (HOST) | 3 | opening, and "Getting in" covers both cases: sign in if they made an account, otherwise use the 10-26 code |
| **2** expert group | friends and advisors, not practising PMs | 3 | opening and one framing line (xian wants it a little different) |
| Hold | not in the first send | 1 (plus a referral) | send nothing |

Several in 1a have used the earlier local-run alpha (2025 to Jan 2026), so not every opening should read as a cold open. Two of the 11 are very busy, so every version keeps the alpha letter's light ask. All openings are new wording, which xian edits freely.

## Opening 1a: hands-on, new to the hosted app

> Hi {NAME},
>
> The private beta of Piper Morgan starts now, and I'd love to have you in it. Here's your invitation. Give it a try when you feel like it.

*If they used the local-run alpha, add after the first sentence:* "You saw an early version when it still ran on your own machine. This one runs on our servers, and it has come a long way since."

## Opening 1b: hands-on, alpha accounts in use (2)

> Hi {NAME},
>
> Thank you for being one of the first to use Piper on our servers. The private beta starts now, and you're already in it. There's nothing to do to join. Sign in as usual, and your account and your work are all still there.
>
> Piper has changed a good deal since the summer. The known issues below are the current list, and they replace anything I told you before.

## Opening 1c: hands-on, invited 10-26 (3)

> Hi {NAME},
>
> On October 26 I sent you an invitation to the Piper Morgan alpha. The private beta starts now, and that invitation now gets you into the beta. You don't need a new code.

## Opening 2: expert group

> Hi {NAME},
>
> The private beta of Piper Morgan starts now, and I'd love your eyes on it. You don't need to be a working product manager to be useful here. I'd value your read on whether it makes sense, what feels off, and where it should go. Give it a try when you feel like it.

## What this beta is (xian's words, edited down by Comms 10-30 17:3x. xian edits freely)

> **What this beta is.** The goal is for Piper Morgan to be a helpful product assistant who, over time, learns enough about your work and how you like to do it to be of more and more help to you. Being a beta means we believe most of the core functionality of a Minimum Valuable Product is now in place. It isn't a production release yet. There are still bugs and known issues keeping it from being ready for prime time, and the ones we know about are listed below.
>
> **What I'd love you to try.** Any of these, and tell me how it went:
>
> - Setting up your account and getting started. Feedback on just that would help a lot.
> - Connecting Piper to GitHub or Google Calendar, if you use either.
> - Asking Piper for your standup each morning. It sums up what you got done, what's next today and what's in your way, and with Calendar connected it includes your meetings. Until Piper has some of your activity to go on, they'll offer a quick interview instead. Does it save you the prep, and does it match your day?
> - Talking with Piper about the work you're doing and how you like to work, then seeing whether Piper remembers any of that and lets it shape the help you get.
> - The broad strokes. Does anything seem out of place, make no sense, or feel redundant or unnecessary? First impressions and specific bug reports are both welcome.
>
> Most of all, I want to know whether anything here gets past being a novelty and becomes a useful habit. I'm still testing that myself.

*Edit notes (Comms):*
- *Cut as redundant with the rest of the letter:* "we'll share that information with you" (the known-issues list follows), and which sources are supported "so far" (the "What you can connect" paragraph names them).
- *Versions 1b and 1c (xian 17:2x, "more nuanced for existing alpha users"):* 1b has working accounts, so drop the "Setting up your account" bullet for them. 1c may or may not have signed up, so keep it. Facts behind 1c: an invite code has no expiry and stays valid until used (`InviteToken.used_at` NULL = valid, `services/database/models.py`). PA showed at 15:1x that alpha accounts work on beta. So "the code from my October 26 email still works" is true for any of the three who didn't redeem, and "sign in" is true for any who did. No redemption read is needed to send it. 1b and 1c already have the 10-26 or July letters, so xian may trim the repeated "Who sees it", "Your key" and Terms paragraphs for them.
- *Standup bullet (added at xian's ask, 17:2x):* the three parts match the standup's sections in code (`StandupResult`: yesterday's accomplishments, today's priorities, blockers). "Includes your meetings" is the alpha letter's already-sent claim. "Each morning" is an invitation, not a schedule: Piper doesn't send it on its own, and nothing says it does.
- *No pronoun for Piper* in the new prose. The third bullet says "Piper" twice instead of "it".
- *House style applied (xian 17:2x):* "Minimum Valuable Product" (blog style guide, glossary). Piper takes they/them in five places in the body and the known-issues lines that said "it" (blog style guide, PM 09-29). The "Who sees it" paragraph is the Terms text, so the letter now differs from the served Terms by one pronoun. The Terms page still calls Piper "it". That's a follow-up for Web and CXO, not a send blocker.

## Body (from the alpha letter, unchanged except where marked)

*Version 1b only, replacing "Getting in" below:*

> **Getting in.** Go to https://beta.pipermorgan.ai and sign in with the account you already have.

*Version 1c only, replacing "Getting in" below:*

> **Getting in.** If you already made an account, go to https://beta.pipermorgan.ai and sign in. Everything you did carries over. If you haven't yet, the code from my October 26 email should still work. Go to https://beta.pipermorgan.ai, choose "Create your account", and paste it in. It works once, for one account, so please don't share it. If it doesn't work, reply to this email and I'll send you a new one. The next step asks for your Anthropic API key, so have one ready.

*Versions 1a and 2:*

> **Getting in.** Go to https://beta.pipermorgan.ai and choose "Create your account". The first step asks for your invite code:
>
> {CODE}
>
> It works once, for one account, so please don't share it. The next step asks for your Anthropic API key, so have one ready.
>
> **What you can connect.** Piper works with GitHub and Google Calendar. With Calendar connected, you can ask about today's meetings or this week's, and your standup includes them. Piper only reads your calendar. They can't change it.
>
> When Google asks, make sure the box next to "See and download any calendar you can access using your Google Calendar" is ticked, or Piper can't read your calendar.
>
> **Who sees it.** Piper sends your messages, and anything they add from the tools you connect (such as calendar or GitHub items you ask about), to Anthropic under your own key. From there, Anthropic's own terms and privacy policy apply. Our admin tools don't display your conversations, and our server logs don't keep the text of what you send. The app has no analytics or ad tracking.
>
> **Your key.** Piper runs on your own Anthropic key. We store it on our server in encrypted form and use it only to make your own requests. We hold the key that unlocks it, so in principle we could read it. Please use a key with a spending limit you're comfortable with. We don't read it on purpose. You can remove your key in Settings at any time, and that deletes it from our live database. Our encrypted backups can keep it for up to about five days. To cut off access completely, also revoke the key in Anthropic's console, so it stops working for Piper too.
>
> **What you're agreeing to.** The plain-language terms are at https://pipermorgan.ai/terms/ and our privacy page is at https://pipermorgan.ai/privacy/. Please read them before you start.
>
> **Known issues in this beta**
>
> - **Piper sometimes misreads what you ask.** They may answer a different question or give a general reply. Rephrasing usually works.
> - **An answer about your own data can be wrong.** Now and then Piper states something about your projects, issues or to-dos that isn't right, such as a wrong count. If an answer looks off, check the source and tell us.
> - **Piper can state a detail about one of your records, such as a milestone or when something last changed, that they did not look up.** Check anything that matters in GitHub before you rely on it.
> - **Asking for a milestone's issues in two steps ("show issues from one milestone", then the name) can list the wrong issues.** Ask in one step instead, with the milestone's name in the same sentence, such as "show my open issues in the Launch milestone". This is a known issue and isn't fixed yet.
> - **No undo for deleted to-dos.** Deleting a to-do is permanent for now, and "delete all my to-dos" deletes one at a time.
> - **Searching your documents from chat doesn't work yet.** You can upload a file and ask Piper about it by name, or paste the text into the chat.
> - **If Piper asks which repository to create an issue in and you answer, they may add your answer to the draft instead of filing it.** Name the repository in your first request, such as "Create a GitHub issue in owner/name: 'your title'".
> - **Piper can't change your default repository from chat yet.** Open Settings → Integrations → GitHub to set it.
> - **When you ask what Piper can do, the answer may promise more than is there today.** For example, Piper may say they will notice things on their own. They don't start conversations or send anything unprompted.
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
| Getting in | URL is now `https://beta.pipermorgan.ai` | See open point 1 |
| Known issues | Heading "in this beta". Nine lines, not five: the #2018 GitHub line is struck (closed served 10-28), the two 10-29 lines (#2042 class, #2184) are in, #2225 is in (CXO 17:0x), and #2230 is in (PPM 17:2x, CXO's words). The 9th, #2236 (capability answer over-promises), is CXO's copy, xian "sure add that" via Exec 19:47. PPM strikes it only after a served check of the #2236 fix Order puts the two "wrong answer" lines together | PPM 10-29 and 10-30. Issue numbers are dropped from the letter, as in the alpha one. They're in the known-issues doc |
| Everything else | Unchanged, verbatim | Final pieces the alpha partners already have |

**Served facts, re-read by Comms 10-30 14:5x (curl, text not rendered):** alpha and beta `/health` both 200, both `git_sha` e234776150. Alpha `/login` has "Create your account". Alpha `/setup` has "Invite", "Paste the code you received." and "API Keys". `/terms/` and `/privacy/` 200. The Terms still carry "We hold the key that unlocks it" and "Our admin tools don't display your conversations". Exec's 14:52: a promotion of main is about to go out, so re-read these after it serves.

## Open points before it goes

1. **URL: RESOLVED, https://beta.pipermorgan.ai** (applied in every version). xian, signed in on beta. with the account he made by hand ("beta xian"), quoted to Comms at 17:39:
   - "What can you help me with?" got a capabilities list, written fresh by the model (no fixed text in code except the closing "(Running with a default configuration — nothing here needs setting up first.)"), ending "connect GitHub or Google Calendar in Settings → Integrations".
   - "What's my standup?" got "I don't have anything to build your standup from yet — no observed activity in your connected tools. Want to do a quick guided standup interview instead? … (yes/no)". That's the fixed empty-state reply (`standup_preferences.py`).
   - The setup wizard's last screen wasn't quoted, but the account exists and chat answers, so sign-up worked end to end.
   - Three points in the capabilities reply went to CXO 17:4x: the "proactively" claim, the default-configuration line after "connect", and the word "honest". Not a letter blocker.
2. **Terms: RESOLVED.** xian's "go" (Exec 16:59). Web pushed website `4826ded`, and the served `/terms/` reads "What this beta is" with 0 "alpha" in the page HTML (Web 17:0x, curl and Lighthouse). HOST's fallback line is struck and not in the letter. CXO's copy OK was given 15:2x and reconfirmed 17:0x.
3. **xian's "what this beta is" paragraph: DRAFTED** from xian's dictation (17:3x). It needs his OK and a CXO read of the new claims: "most of the core functionality… is in place" and the remember-and-shape test.
4. **PPM's line check at send**, after the promotion and PA's re-checks.
5. **Version 1b's "no new code, your account carries over": VERIFIED (PA 15:1x).** On beta. (serving `ac5b69f865`), an alpha test account logged in, and a chat turn saw issue #35, which had been created on alpha. at 15:04. So it's the same accounts and the same data. That was an API check, not the rendered sign-in page. Whether the three 10-26 codes were redeemed is still unread (HOST: xian's select).
6. **Version 1c's "the code from my October 26 email still works" rests on "no record", not on a read (HOST 17:2x).** HOST's logs show no cancel or revoke of those three codes, but the stored state is unread. A used code is fine for 1c, because that person signs in. A cancelled one isn't. The fix is xian's redemption read of the three codes (`used_at` and any cancel), one query, before the 1c send. HOST and Comms both recommend running it. **Update 17:4x:** HOST runs the read only when xian asks in the HOST conversation, not through a relay or a mail wake. So that 1c can go without it, "still works" is now "should still work", followed by "If it doesn't work, reply to this email and I'll send you a new one." That holds whatever the read would show. If the read runs and finds all three, xian can put "still works" back.

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
