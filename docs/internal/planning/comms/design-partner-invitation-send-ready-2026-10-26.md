# Design-partner invitation: send-ready letter (for xian)

**Assembled:** Comms, 2026-10-26 18:00 PT, at HOST's ask (17:55). Every paragraph is a final piece, unchanged, except the two openings, the "Getting in" steps and the links paragraph, which are new and flagged below for xian to edit freely.
**Placeholders:** `{NAME}` and `{CODE}`. Never put a real name or code in this repo. xian pastes the code from his 0600 file under `~/.piper-shared/`. Names live in his private mail.
**Before sending:** PPM confirms the known-issues list at the moment of send (asked 10-26 evening). HOST re-reads alpha `/health`, CI and the codes' unused state, and marks the roster as each send goes.

---

**Suggested subject:** Your Piper Morgan alpha invitation

## Opening, variant (a): reissue, for the two invited before

> Hi {NAME},
>
> Your earlier invite code never worked, and I'm sorry about that. Here's a new one, and Piper has come a long way since.

## Opening, variant (b): first invitation, for the one who wrote in

> Hi {NAME},
>
> Thanks for writing in. I'd love to have you try Piper Morgan, and here's your invitation to the alpha.

## Body (the same for both)

> Alpha is nearly over! What you see now is pretty close already to what the first beta will be: the same Piper on the same servers. Right now I'm working on making sure Piper doesn't reply "none" just because it failed when it tried to read something.
>
> Your account and your work will carry over to the beta automatically. You can also start a new account when the beta officially begins. If you'd like your alpha account deleted at that point, email support@pipermorgan.ai and we'll do it for you (by hand, for now, within 14 days).
>
> **Getting in.** Go to https://alpha.pipermorgan.ai and choose "Create your account". The first step asks for your invite code:
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
> **Known issues in this alpha**
>
> - **Piper sometimes misreads what you ask.** It may answer a different question or give a general reply. Rephrasing usually works.
> - **An answer about your own data can be wrong.** Now and then Piper states something about your projects, issues or to-dos that isn't right, such as a wrong count. If an answer looks off, check the source and tell us.
> - **No undo for deleted to-dos.** Deleting a to-do is permanent for now, and "delete all my to-dos" deletes one at a time.
> - **A broken GitHub connection can look fine.** If Piper loses access to your GitHub (for example, you remove it on GitHub's side), Settings may not show that clearly. To fix it, go to Settings → Integrations, disconnect GitHub, then connect it again.
> - **Searching your documents from chat doesn't work yet.** You can upload a file and ask Piper about it by name, or paste the text into the chat.
>
> **Feedback and help.** When you find something new, send feedback from the left-hand menu once you're in the app, or email support@pipermorgan.ai. Either way the message will be read by the team, including by me (xian), the human who owns this particular loop.
>
> Thank you for trying it.
>
> xian

---

## Where each piece comes from

| Piece | Source | State |
|---|---|---|
| Openings (a) and (b) | New, Comms 10-26. Facts from HOST 17:55: two earlier codes never worked, one approved write-in | **xian edits freely.** Only these differ between variants |
| "Alpha is nearly over" | xian's words verbatim (HOST relay 10-26 17:23) | Final. PPM rechecks #2018 is open and in work at send |
| Carry-over | HOST's tightening, xian-approved (17:23). Matches the live Terms deletion path | Final. Keys left out on purpose (xian) |
| Getting in | New wording. Facts: served `/login` has "Create your account" → `/setup`. Served `/setup` step 1 is "Invite" ("Paste the code you received."), step 2 "API Keys" (Comms curl 10-26 17:59, alpha `69d859ca5f`). "Works once, for one account… don't share it" from Terms "Your invite code". "Anthropic" per Terms "Your key" | Served page text, read by curl, not rendered. Create Account re-asking the code stays out (source only, CXO) |
| What you can connect, tick-the-box | Pieces doc §2, final 10-25 17:35 | Final |
| Who sees it, Your key | Terms draft L15 and L17, live at /terms/ | Final, verbatim. Exec 17:50 (10-20): no send without them |
| Terms and Privacy links | New sentence. /terms/ 200, /privacy/ 200 (Comms curl 10-26) | xian edits freely |
| Known issues | Pieces doc §1, five lines, issue numbers dropped. PPM 06:35: none struck. #2101's contingent line stays out (#2101 closed) | **PPM confirms at send.** CXO 18:32: the GitHub line stays as written, but nobody has run Disconnect then Connect on a dead grant (#2018). If xian's #2018 run shows that path failing, CXO sends replacement words before the letter goes |
| Feedback and help | Terms draft "When something breaks", feedback sentences verbatim | Final |
| Step-2 skip sentence | Out (HOST 10-26 09:25, #2176 served) | Not in the letter |

**CXO read, 10-26 18:32:** read in full. Getting in, xian's two paragraphs, and the Calendar lines all pass with no edits (text, not rendered).

**Heading word:** the pieces doc titled the list "Known issues in this beta". The letter now calls this the alpha ("Alpha is nearly over!"), so the heading says "in this alpha". Change it back if xian prefers.

**Voice check (Comms, on the quoted letter only):** 0 semicolons. No "honest", "quietly", "load-bearing" or "cohort". Agents aren't called people.
