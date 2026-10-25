# Design-partner invitation: known-issues lines and the Calendar caveat (draft for xian)

**Drafted:** Comms, 2026-10-19 15:3x.
**Rulings behind it (recorded in decisions.log):**
- section B, xian 10-18: list #2042 and the todo no-undo;
- section A, xian 10-19 15:2x: "list both. if we fix then we can delist";
- Calendar, xian 10-19 15:0x: "yes, name it, with caveats if need be (it's not an easy oauth setup yet, etc.)".

**Review:** xian reviews the wording (section A is his to see), and CXO reviews too. **At send time, PPM strikes any line whose issue has closed** (criterion 6).

## 1. Known issues (the list that goes with the invitation)

> **Known issues in this beta**
>
> - **Piper sometimes misreads what you ask.** It may answer a different question or give a general reply. Rephrasing usually works. *(#1595)*
> - **An answer about your own data can be wrong.** Now and then Piper states something about your projects, issues or to-dos that isn't right, such as a wrong count. If an answer looks off, check the source and tell us. *(#2042)*
> - **No undo for deleted to-dos.** Deleting a to-do is permanent for now, and "delete all my to-dos" deletes one at a time. *(#2019, #2021)*
> - **A broken GitHub connection can look fine.** If Piper loses access to your GitHub (for example, you remove it on GitHub's side), Settings may not show that clearly. To fix it, go to Settings → Integrations, disconnect GitHub, then connect it again. *(#2018)*
> - **Searching your documents from chat doesn't work yet.** Paste the text into the chat and ask about that. *(#2122)*
> - **Sharing doesn't work yet.** Sharing a to-do, list or project with another person shows an error if you try. *(#2166)*

  *#2018 line, CXO 15:32:* when CXO judges the served recovery read, it changes to "Settings → Integrations → GitHub will say it needs reconnecting. Press Reconnect." If #2018 closes, PPM strikes the line.

**Contingent fifth line (#2101, chat stall), CXO 16:20:** goes in only if xian rules the stall isn't fixed before partners. CXO's wording: "Piper may stop responding for a few minutes. Reload the page and try again." It's a fact only if the stall recovers by itself, which both observed stalls did. If that's in doubt on send morning, write "usually": "Piper may stop responding for a few minutes. Reloading the page and trying again usually works." *(#2101)*

*#2122 line:* CXO's wording, 18:07 10-20. #2122 isn't Class 1–4 (Web's served turn showed no false result). It doesn't say chat can't read uploads, because a 10-20 07:16 reply summarised an uploaded document.

*#2166 line (added 17:55 10-24):* PPM's proposed sentence (17:47), CXO approved (17:52), split by Comms into a bold lead plus one sentence with no semicolon, to match the list. Share is broken end to end (the UI sends the wrong field: 422, then 500). It isn't a gate item, because the dialog shows an error and never claims a share happened. PPM strikes it when #2166 closes.

*#2122 line, recheck at send:* #2122 closed 10-21 with the reply made truthful ("I can't search your documents from chat yet"). #2132 (analyze and compare documents) closed 10-23 18:32. On send morning, PPM confirms which document asks still fail in chat, so this line doesn't understate what now works.

The issue numbers are for PPM's strike-at-send. Drop them from the copy partners see.

## 2. Calendar in the invitation

> **What you can connect.** Piper works with GitHub and Google Calendar. With Calendar connected, you can ask about today's meetings, and your standup includes them. Piper only reads your calendar. It can't change it.
>
> Calendar setup isn't smooth yet. Until Google finishes reviewing Piper, Google will show a screen saying "Google hasn't verified this app." That's expected for now. Click "Advanced", then "Go to Piper Morgan (Alpha) (unsafe)". Choose your account. On the next screen, tick the box next to "See and download any calendar you can access using your Google Calendar", then click "Continue". If you leave that box unticked, Piper can't read your calendar. [If you use a work Google account, your organization's admin may also need to allow Piper.]

**10-22 17:01, xian (Exec relay):** Google has verified "Piper Morgan (Alpha)", alpha's Calendar project. External testers can use it, and the branding shows. So the Calendar line is the plain connect step above, and the "Google hasn't verified this app" click-through paragraph is dropped. Lead's option (A) is moot. HOST still checks the served screens on send morning. The bracketed work-account sentence stays open (row below). It came out of the dropped paragraph and is kept only if its cause is confirmed.

**10-23 11:44, xian (Exec relay), supersedes the 10-22 note above:** the 10-22 "verified" was Google's **branding** verification. The **data-access** verification for `calendar.readonly` (#2087) was never submitted, and xian is starting it now. xian's served outside-account Connect (a personal Gmail new to alpha) showed the full "Google hasn't verified this app" page, then "Sign in to Piper Morgan (Alpha)", then a consent page with a yellow "This app hasn't been verified by Google" box and the one scope as a checkbox that **starts unticked**. With it ticked: "Calendar Connected", and Settings → Test passed. So the click-through paragraph is back (10-21 wording, CXO-accepted 10-21 10:21), with the old "On the next two screens, choose your account and click Continue" replaced by the three real steps and the tick-the-box line. Both rulings are xian's, in session at 11:44: "we will have to let early testers know"; "reminding people to tick the box is probably a good idea, yes". HOST and CXO check the restored wording against the served screens on send morning. Remove the paragraph if #2087 is approved before then. **10-23 13:29 (Exec):** xian submitted #2087. Google's Verification Center reads "Your app's data access is under review". The caveat stays until approval. #2148 (the "Calendar Connected" toast on an unticked grant) is awaiting xian's admission call. If it ships unfixed, the tick-the-box line is what covers it, so keep that sentence even if the click-through paragraph is trimmed.

**Facts behind it:**

| Claim | Backed by | State |
|---|---|---|
| Today's meetings; the standup | `assembler.py` `_append_calendar_events`; chat agenda queries | Code. **"This week's" was cut (CXO 15:32):** xian's own "any meetings this week?" got "I didn't find any events" (#2092, open). It goes back in when CXO quotes a passing week row. **Don't name a weekday** until #2091 lands |
| Only reads | the scopes are `calendar.readonly` and `userinfo.email` only (Lead 14:49, grep over services/ and web/) | Backed |
| The unverified-app screens, click path and unticked box (**restored 10-23 11:44**; the 10-22 drop was branding verification only) | xian's four screenshots, 10-21 10:0x, app "Piper Morgan (Alpha)", In production, unverified (Janus 10:2x, transcribed; PNGs in the private DinP repo, addresses blanked). Lead 09:38 quotes Google's page: In production with a sensitive scope shows the unverified-app warnings. Wording per CXO 09:48 (say what to do, in Google's exact words). Screen 4's one scope reads "See and download any calendar you can access using your Google Calendar", which backs "only reads" | Google's words are quoted from screenshots. **Recheck at send:** the app name in "Go to Piper Morgan (Alpha) (unsafe)" changes if alpha moves to the Piper Morgan project's client (PPM 09:34). Use the name the served screen shows that morning. Lead 10-22 14:59 recommends that move, option (A), before 10-30; it's xian's call. Verification is per project. So under (A), if the Piper Morgan project's verification has completed by send morning, the warning screens may not appear at all, and this whole line would be dropped rather than renamed. Check the served screens that morning. **CXO 10:21: both lines accepted as written.** "(unsafe)" stays exactly as Google shows it, with no reassuring word added |
| [Bracketed] work-account admin | #2092's grant half: xian's Workspace account got email-only; Lead's leading candidate is the Workspace API controls (kit §0) | **Unconfirmed cause.** Keep the bracket only if xian's #2087 console work confirms it's the admin setting. Otherwise cut it. **10-23:** a second candidate is now on the table. The calendar box starts unticked, so an email-only grant may just mean the box was left unticked (Exec asked Lead to note it on #2092). If that explains it, cut the bracket, because the tick-the-box line covers it |

**Which Calendar line goes (#2087, updated 10-21 10:18):** the line partners get has to match what Google does on send morning. HOST's send check picks it, and HOST releases no send until xian has said which reading holds. **Neither line goes until Connect works for a Google account outside the Workspace domain** (CXO 09:48, PPM 09:34).
- **In production** (xian's Audience screenshot shows this today, PPM 09:34): use the caveat above, with the click path. This morning's "being tested" refusal came from elsewhere. Lead's client-ID read suggests alpha may be sending another project's client. If it is, PPM recommends rotating alpha to a new client in the Piper Morgan project, and the app name on the screens changes.
- **Testing** (fallback only): replace the caveat's second through fourth sentences with CXO's final wording (09:48):
  > Before you connect Google Calendar, send us the Google address you'll use. We have to add you to Google's list of approved testers first. Without that, Google blocks the connection. In this mode Google asks you to reconnect Calendar about once a week.

  Sourced: Google's refusal text (Web, Janus); the 100-tester cap and the 7-day refresh-token expiry are quoted by Lead (09:38) from Google's "OAuth app state overview". **HOST owns the per-partner step** (09:28): xian opens the partner's reply at alpha@, HOST tracks received/added only, and Exec relays to xian. Addresses go only in Google Cloud and xian's private mail, never in this repo.

Slack and Notion stay unnamed (xian 15:0x). Notion has no chat reader (Lead 15:01, #2100).

## 3. Other invitation lines still open on the checklist (no draft needed yet)

- **The invite code's step:** asked first. CXO closed #2088 and #2089 at 15:32 on 10-21 on Web's served rows (76789a8988: strip "1. Invite", "2. API Keys", "3. Account", "4. Projects", "5. Complete", no System step or Temporal line). The step-3 interim line is out. The invitation calls the first step "Invite". Still on Lead's pins: Create Account no longer asking for the code. Recheck what alpha serves on send morning.
- **#2089's system-check known-issue line:** not needed. #2089 closed 10-21 15:32 (CXO).
- **Beta or alpha form:** PPM's one line on the morning.

## 4. HOST's send checks (15:23), all read on send morning

- The invitation's line pointing to pipermorgan.ai/privacy: **done 15:50.** Web quoted the Google paragraph from the rendered live page (website `4f3582d`), and since `a3cb49f` (17:0x) the paragraph and the footer Privacy link are in the served HTML too (Web's curl of four pages). Re-read only if the page changes again.
- Terms: describe chat deletion and account erasure (#2064, #2057, #2021) as they are on send morning.
- The code step: whatever the served wizard shows (HOST reads it).
- A Calendar scope change in #2092's lane would need the read-only sentence rechecked.

- **Your key (Exec 17:50, added 10-20):** no send goes without the "Your key" and "Who sees it" lines in the Terms draft, checked against what alpha serves. Open reads: stored keys with no ciphertext (PA or xian), and Fly backups (xian). The provider named is Anthropic unless the OpenAI run passes. PPM 10-22 12:27: PA's OpenAI run failed the 10-20 bar, so Anthropic only unless a new run passes.

## Voice checks

No semicolons in the partner copy. No "honest", "quietly", "load-bearing" or "cohort". Agents aren't called people.
