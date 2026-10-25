# Draft: the plain-language section of the design-partner invitation

* **Status:** xian's draft, 2025-10-24 based on Comms' draft, 2026-10-19, nuilt from `terms-scaffold-for-xian-2026-10-16.md`, with facts rechecked today. **xian rewrites it in his own words**, then does his HALT pass. CXO reviews the wording. Due before the 10-23 checkpoint.
* **Under xian's 10-16 Option 2:** this goes in the invitation. No site page, no click-through. Counsel writes the legal layer for Production.
* **Left out on purpose (open facts):** any "we never train on your data" promise (Arch hasn't stated it); #2057 (project questions read as requests, still open); any undo or soft delete (#2021, open). The no-undo on to-do deletes goes on the known-issues list, not here.

---

## What you're agreeing to, in plain language

**Your work is yours.** What you put into Piper stays yours. We use it to run Piper for you. Your messages, uploaded files, AI provider key and connected-account access are encrypted when stored. Your to-dos, projects, lists and account details are stored but not encrypted by the app. It all lives on our hosting provider, Fly.io, in San Jose, California.

**Who sees it.** Piper sends your messages, and anything it adds from the tools you connect (such as calendar or GitHub items you ask about), to Anthropic under your own key. From there, Anthropic's own terms and privacy policy apply. Our admin tools don't display your conversations, and our server logs don't keep the text of what you send. The app has no analytics or ad tracking. [Do we need to mention Open AI keys? Will they be supported at the start of the beta? OK if not. I am just unsure.]

**Your key.** Piper runs on your own Anthropic key. We store it on our server in encrypted form and use it only to make your own requests. Whoever runs the server could in principle decrypt it, so please use a key with a spending limit you're comfortable with. [I run the server unless you mean Fly "runs" it? Are we trying to just remind them of a theoretical danger? It is oddly worded.] You can remove your key in Settings at any time, and that deletes it from our live database. Our encrypted backups can keep it for up to about five days. To cut off access completely, also revoke the key in Anthropic's console, so it stops working for Piper too.


**When Piper acts for you.** Piper checks with you before making most changes. If you tell it directly to do something, such as "Create a GitHub issue," Piper will do it right away, treating a plain instruction as the go. Piper always asks before it deletes something of yours. There's no undo yet, so take that question seriously!

**When something breaks.** We expect you'll hit rough edges. We'll include a short list of the most egregious known issues with this invitation. When you find something new, use Send feedback in Piper, or email alpha@pipermorgan.ai. Either way the message will be read by the team, including by me (xian) the human who owns this particular loop. [Does Send feedback exist yet? Should we explain how to do that?[

**Brief restarts.** Piper may restart briefly when we update it, usually at a quiet moment. You'll stay signed in, and your conversation will still be there. If a message gets no reply around the time of a restart, just send it again.

**If the database stops.** Recovery is automatic and usually takes 15 to 30 minutes. The alert reaches me either way.

**Leaving.** You can download your uploaded files, and what Piper has learned about how you work. Exporting your conversations and to-dos is the goal, and isn't built yet. There's no delete-account button yet either. If you'd like to delete your account, just email support@pipermorgan.ai and we'll delete your account and everything in it within 14 days. Deleting a single conversation inside Piper isn't possible yet. The roadmap includes the ability to put things in trash and to empty it for good yourself so we hope to get there before too long.

**Your invite code.** Your code works once, for one account. Please don't share it. If it leaks before you use it, tell us and we'll cancel it. Once used, it can't be taken back, because the account exists. We won't publish who our testers are, and we won't quote you without asking first.

**What this beta is.** *(xian picks ONE form on the morning the invitation goes, from PPM's one line. Never both.)*
- *Beta form:* Expect errors, and go carefully. Using your real work is OK.
- *Alpha form:* Piper isn't reliable yet. Please use test data, not your real work.

Before Production, we'll add [the list xian chooses from: deleting a conversation for good, deleting your account in the app, exporting conversations and to-dos, undo]. Today, the sections above describe what's true.

**Who it's for.** Piper Morgan is an assistant who gets it for product managers and for people making products who need the support of a product manager and don't have a human one at hand.

---

## Facts behind each paragraph (for xian's rewrite and CXO's review)

| Paragraph | Backed by | Rechecked today |
|---|---|---|
| Your work is yours | Arch 10-16 (encrypted by category); /privacy (Fly.io, San Jose; uploads encrypted, website `c8fbb15`); #2061 live | /privacy source read |
| Who sees it | /privacy (own-key providers, admin tools, logs); #2059 and #2060 closed; HOST 18:01 (`request_key.py`: tool context Piper adds goes in the same call under the partner's key). Names Anthropic only (PPM 17:46) | /privacy source read. "No one can read them" is **not** claimable: the decryption key is a server secret |
| Your key | HOST 18:01 code read (`user_api_key_service.py`: AES-256-GCM `encrypted_secret`, no plaintext write without the master key; `request_key.py`: key bound per request, keyless accounts refuse, no project-key fallback; `DELETE /api/v1/api-keys/{provider}` deletes the row and any keychain entry). Alpha encryption on: xian's 10-13 re-encrypt run (2 of 2 verified). Exec 17:50: these lines join HOST's pre-send checks, and no send goes without them | Code read only, no alpha read. **Open:** (1) a count of key rows with no ciphertext (PA or xian); (2) whether Fly Postgres backups keep a deleted key, and for how long (xian). CXO 18:07 edits applied: "deletes it from our database" (backups unread) and "so it stops working for Piper too" (we haven't read the provider's behaviour on revocation). "Anthropic" only until a served OpenAI run passes (PPM 17:46, CXO, HOST). xian 18:04 said yes to the test: a $10-capped key, a fresh wizard account run by Web, scored by PA. If it passes, "or OpenAI" goes back into "Your key" and "Who sees it" |
| When Piper acts for you | `collaboration_gate.py` 22-29 (any explicit imperative executes, not only GitHub); deletes confirm (Arch 10-16, not re-run per kind, so "something of yours", not "anything"); xian 10-18 (GitHub no-confirm goes in the invitation wording). Revised per CXO 14:42: cut "asks when a request is unclear" (#2057 contradicts it). CXO's example "add a project" left out, because CXO's served row on 10-18 showed adding a project asks one yes/no. **Rule named 15:01 (Lead, `classify_framing` run on the exact turns):** a bare imperative executes on any account, and a lead-in such as "Let's track this." makes the message compose, so it drafts first. That's why the example is quoted and says "on its own". CXO 15:02: keep it, and the draft-first behaviour stays through the beta start. **Confirmed on served alpha 10-20 (CXO 14:24, #2110 closed):** Web's quotes from alpha 3b7fbb46fb show both forms create, the bare form included ("Created issue #25, …") | Served check 10-20 (Web, quoted by CXO) |
| When something breaks | alpha@ reaches the team (HOST 10-16, `docs/ALPHA_KNOWN_ISSUES.md:143`); known-issues list (PPM) | #2096 (Send feedback page) admitted before partners (xian 14:4x, Exec's 14:35 ruling). **Check it's live on alpha before the invitation goes**, or cut "use Send feedback in Piper, or". xian 14:4x: "we can all see support@", so the Leaving paragraph's support@ is read |
| Leaving | **Uploads work without an OpenAI key (Web 18:04, served on alpha d1c64a92e3):** an Anthropic-only account uploaded a file and saw it listed, with no key message. So both upload lines stand. Chat can't reach an uploaded file (it answers with the Notion line, #2122), and PPM 17:46 says name no document-search features until #2122 has a class. `files.py` 571 (download) and 786 (`download-bulk`); `learning.py:803` (`/controls/export`); no conversation or to-do export (Arch); /privacy 14-day line; `erase_user.py` live (#2064) | Routes grepped today. Provider grants are reported, not revoked, so the draft doesn't promise revocation at GitHub etc. |
| Your invite code | `invite_token_service` (one redemption); `invite_admin_service.revoke_invite` (revokes ONE unused code; #2081 closed 10-19); no expiry | Code read today. "We'll cancel it" is backed by the admin revoke. No time limit is promised |
| What this beta is | PPM's 12:50 memo: today's reading is the beta form, and PPM sends the one line on the morning invites go | PPM's line on the day decides |

**Wizard note for the invitation's setup instructions** (separate from this section): **10-21 18:19:** CXO closed #2088 and #2089 at 15:32 on Web's served rows. The interim "code at step 3" line is gone. The setup instructions say the wizard asks for the invite code first, and name the first step "Invite" (the served strip: Invite, API Keys, Account, Projects, Complete). Not yet served: Create Account no longer asking for the code. That stays on Lead's pins, so recheck it on send morning.

**Restart line (added 10-22 18:19, CXO ruled 18:23):** CXO's wording. There is no clock time and no "once a day", because CIO's condition 3 (a promotion waits for 30 quiet minutes, 07:00–21:00) makes a fixed window untrue and nothing says restarts are daily. Sentence two rests on Web's staging row (8 of 8 turns across a deploy, sign-in and history intact), and sentence three stays conditional. It must not say a message sent mid-restart is saved or answered. **HOST, send morning:** check that the grant still waits for no chat in the last 30 minutes. If it doesn't, drop "usually at a quiet moment". The "Your key" backup sentence was accepted by CXO 18:23.

**Key backups (added 10-22 18:19):** PA 16:53, Fly metadata: alpha's Postgres has daily encrypted snapshots with 5-day retention, so a removed key can stay in a backup for up to about five days. The "Your key" line now says "live database" and names the backups. Still open: the count of key rows with no ciphertext (HOST or xian).

**Outage line (added 10-23 15:20, HOST ruled 13:19, edits accepted 15:23, first form true 15:48):** HOST's wording on PA's measurement (watch runs every 9 to 24 minutes, 12 runs over about 2.5 hours of one afternoon). Comms made two voice edits: the semicolon is now two sentences, and "reaches xian" is "reaches me", to match the draft's voice ("including me"). Keep "usually": a second fault within 24 hours stops and alerts instead of restarting. Never use test 3's two minutes, because a person dispatched that run. The interim line holds until #2146 is live, and xian names how fast. **Comms and HOST, send morning:** recheck the 15 to 30 minutes against the live watch cadence. If Arch and Lead change the cadence, the number changes with it. **10-23 15:48 (PA):** #2146 test 4 passed, so HOST's condition is met (pushed, reviewer removed, test 4 passed). The watch dispatched the restarter itself, and the database was healthy 9 min 15 s after the hold came off, about 4.5 min of that waiting for the schedule. The first form is now true. HOST still makes the send-morning pick. Keep "usually", because `stop24` refuses a second automatic restart within 24 hours. **17:02 (HOST):** HOST re-checked all five conditions directly and ruled "Comms: use that form", so the interim form (xian restarts it) is cut. Bring it back only if #2146 is rolled back. The stop24 refusal itself hasn't been served (Arch).

**Voice checks run on this draft:** no semicolons; no "honest", "quietly", "load-bearing" or "cohort"; no "never" promises except "can't be taken back" (a code fact).
