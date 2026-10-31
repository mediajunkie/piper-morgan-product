# Design-partner invitation: known-issues lines and the Calendar caveat (draft for xian)

**Drafted:** Comms, 2026-10-19 15:3x.
**Rulings behind it (recorded in decisions.log):**
- section B, xian 10-18: list #2042 and the todo no-undo;
- section A, xian 10-19 15:2x: "list both. if we fix then we can delist";
- Calendar, xian 10-19 15:0x: "yes, name it, with caveats if need be (it's not an easy oauth setup yet, etc.)".

**Surface, re-scoped 10-29 (PPM 13:10, #1386 criterion 6):** this list now goes with the **first beta invitation** (no sooner than 10-30, after xian's conversation with HOST). The 10-26 alpha letter is history. Criterion 6 ticks on the beta letter's final draft: GitHub and Calendar named with Calendar's caveat, CXO's #2184 line in, #2018's line gone. Comms sends PPM that draft when it's near final.

**Review:** xian reviews the wording (section A is his to see), and CXO reviews too. **At send time, PPM strikes any line whose issue has closed** (criterion 6).

## 1. Known issues (the list that goes with the invitation)

> **Known issues in this beta**
>
> - **Piper sometimes misreads what you ask.** They may answer a different question or give a general reply. Rephrasing usually works. *(#2195, the remainder of #1595, which closed by split 10-29; PPM 10-30)*
> - **An answer about your own data can be wrong.** Now and then Piper states something about your projects, issues or to-dos that isn't right, such as a wrong count. If an answer looks off, check the source and tell us. *(#2042)*
> - **No undo for deleted to-dos.** Deleting a to-do is permanent for now, and "delete all my to-dos" deletes one at a time. *(#2019, #2021)*
> - **Searching your documents from chat doesn't work yet.** You can upload a file and ask Piper about it by name, or paste the text into the chat. *(#2226. Retagged 10-30 from #2122, which closed 10-20 when the chat reply became honest. The gap itself is still open. PPM 15:1x)*
> - **If Piper asks which repository to create an issue in and you answer, they may add your answer to the draft instead of filing it.** Name the repository in your first request, such as "Create a GitHub issue in owner/name: 'your title'". *(#2225, CLOSED with the fix on main but not served. CXO 17:0x)*
> - **Piper can't change your default repository from chat yet.** Open Settings → Integrations → GitHub to set it. *(#2230. CXO's words, PPM 17:2x ruling. Strike at send only on PA's live confirm after Arch's ops flip)*
> - **When you ask what Piper can do, the answer may promise more than is there today.** For example, Piper may say they will notice things on their own. They don't start conversations or send anything unprompted. *(#2236. CXO's words, xian yes via Exec 19:47. Holds for a new account at `TrustStage.NEW` (Lead's read, CXO). Strike at send only after a served check of the #2236 fix)*
> - **Asking for a milestone's issues in two steps ("show issues from one milestone", then the name) can list the wrong issues.** Ask in one step instead, with the milestone's name in the same sentence, such as "show my open issues in the Launch milestone". This is a known issue and isn't fixed yet. *(#2184; last sentence restored per CXO 15:05 10-30)*
> - **Piper can state a detail about one of your records, such as a milestone or when something last changed, that they did not look up.** Check anything that matters in GitHub before you rely on it. *(#2042 class)*

  **#2225 line: moved into the list above, 10-30 17:0x** (Lead 16:5x: the wizard can finish with no repository, so it isn't rare. CXO 17:0x: "put my line into the letter and the known-issues list now"). PPM strikes it at send only if Lead's fix is served and a quoted reply shows the owner/name answer filing. #2225 is CLOSED with the fix on main but not served (Exec 17:0x). PPM is deciding how to keep items like this visible.

  *#2018 line: STRUCK 10-29 (PPM 09:51).* #2018 closed served 10-28 14:36, after xian's UI-only recovery run on alpha passed every step. xian 10-19: "if we fix then we can delist." The removed line read: "A broken GitHub connection can look fine. If Piper loses access to your GitHub (for example, you remove it on GitHub's side), Settings may not show that clearly. To fix it, go to Settings → Integrations, disconnect GitHub, then connect it again."

**PLACED 10-29 15:2x (#2184 line, above).** **Alpha partners too (xian 16:4x, PA relay 16:47):** the three alpha partners get a #2184 line. Comms proposed a short note rather than a `/try/alpha` section (to Exec 18:2x), and asked CXO whether the "MVP milestone" example should name the partner's own milestone instead. **Settled 18:3x:** CXO 18:31 accepted the placeholder and changed the beta line above to match (applied, first sentence unchanged). xian 18:33 (PA relay): "OK to send as is, yes". It goes as a short note from xian's own mailbox, and HOST holds the recipients in the gitignored roster. **Last sentence settled (xian 18:43, PA relay):** CXO's "This is a known issue and isn't fixed yet." ("I prefer CXO's version.") Final text is in PA's 18:4x relay. The recipients are the three 10-26 invitees in HOST's roster, sent from xian@. **Sent: not yet reported** (HOST 21:0x). When xian sends it, tell HOST the same day. Strike: PPM, when #2184 closes served. xian 13:02 (PA relay): #2184 leaves the MVP gate as a known issue (PPM option B, ledger 3 → 2, #2184 to Production, Sprint PUB). PA 13:05: the line goes in the first **beta** invitation. Strike it when #2184 closes on a served pass. History of the staging: **Contingent line (#2184, two-step milestone ask), CXO 09:50 10-29, via PPM 09:51:** was to go in on the next partner surface once today's promotion is live **without** the #2184 routing fix (its fix waits on xian's key decision). CXO's wording, verbatim:

  *(Superseded wording, CXO 09:50. Don't copy it: the example was replaced 18:31.)* - **Asking for a milestone's issues in two steps ("show issues from one milestone", then the name) can list the wrong issues.** Ask in one step instead: "show my open issues in the MVP milestone".

  True today: the one-step read returned the right three on alpha (PA 08:43). **Strike it when #2184 closes on a served pass** (PPM tells Comms the same hour). Not added to the list above yet, because the promotion it depends on hasn't gone out.

**Contingent fifth line (#2101, chat stall), CXO 16:20:** goes in only if xian rules the stall isn't fixed before partners. CXO's wording: "Piper may stop responding for a few minutes. Reload the page and try again." It's a fact only if the stall recovers by itself, which both observed stalls did. If that's in doubt on send morning, write "usually": "Piper may stop responding for a few minutes. Reloading the page and trying again usually works." *(#2101)*

*#2042-class line (added 10-29 15:2x):* CXO's words verbatim (13:23), xian YES (PA relay 13:55: "to be reviewed if our attempts to fix it land"). Comms bolded the first sentence to match the list, no word changed. It covers C2b and K4 as served. **Strike it only on #2042 rung 3's served pass, not on the issue closing** (CXO). **Keep both (CXO 15:25).** They name different failures: the older #2042 line is a wrong number (counts), the class line a detail Piper did not look up. Each strikes on its own trigger: the class line on #2042 rung 3's served pass, the older line when the count fix is served. No words change.

*#2122 line:* CXO's wording, 18:07 10-20. #2122 isn't Class 1–4 (Web's served turn showed no false result). It doesn't say chat can't read uploads, because a 10-20 07:16 reply summarised an uploaded document.

*#2166 line (added 17:55 10-24):* PPM's proposed sentence (17:47), CXO approved (17:52), split by Comms into a bold lead plus one sentence with no semicolon, to match the list. Share is broken end to end (the UI sends the wrong field: 422, then 500). It isn't a gate item, because the dialog shows an error and never claims a share happened. **Drop this line once the Share hide is served** (PPM ruling 18:36: Share hidden on all three pages next promotion, repair moved to Production D, #2166 stays open). Web serves one row per page with no Share button, and then Comms removes the line. Until then it stays. **Dropped 10-24 21:41:** Share is hidden on alpha 228f3cec14, CXO passed 3 of 3 pages (CXO 20:21, relayed by Exec 21:40). #2166 stays open for Production D.

*#2122 line, recheck at send:* #2122 closed 10-21 with the reply made truthful ("I can't search your documents from chat yet"). #2132 (analyze and compare documents) closed 10-23 18:32. On send morning, PPM confirms which document asks still fail in chat, so this line doesn't understate what now works. **PPM 18:35:** search is still unsupported (served), and asks about an uploaded file now work (analyze, analyze a named file, questions about a file: served). **CXO 18:48: yes, with "by name"** (every served row named the file, and the unnamed ask is the case that still fails). Applied 18:51. Comms kept "or paste the text into the chat" from the old line, since pasting still works and helps with search. Leave out "summarize" until it has a served row. PPM rechecks both halves on send morning.

The issue numbers are for PPM's strike-at-send. Drop them from the copy partners see.

## 2. Calendar in the invitation

> **What you can connect.** Piper works with GitHub and Google Calendar. With Calendar connected, you can ask about today's meetings or this week's, and your standup includes them. Piper only reads your calendar. It can't change it.
>
> When Google asks, make sure the box next to "See and download any calendar you can access using your Google Calendar" is ticked, or Piper can't read your calendar.

**10-22 17:01, xian (Exec relay):** Google has verified "Piper Morgan (Alpha)", alpha's Calendar project. External testers can use it, and the branding shows. So the Calendar line is the plain connect step above, and the "Google hasn't verified this app" click-through paragraph is dropped. Lead's option (A) is moot. HOST still checks the served screens on send morning. The bracketed work-account sentence stays open (row below). It came out of the dropped paragraph and is kept only if its cause is confirmed.

**10-23 11:44, xian (Exec relay), supersedes the 10-22 note above:** the 10-22 "verified" was Google's **branding** verification. The **data-access** verification for `calendar.readonly` (#2087) was never submitted, and xian is starting it now. xian's served outside-account Connect (a personal Gmail new to alpha) showed the full "Google hasn't verified this app" page, then "Sign in to Piper Morgan (Alpha)", then a consent page with a yellow "This app hasn't been verified by Google" box and the one scope as a checkbox that **starts unticked**. With it ticked: "Calendar Connected", and Settings → Test passed. So the click-through paragraph is back (10-21 wording, CXO-accepted 10-21 10:21), with the old "On the next two screens, choose your account and click Continue" replaced by the three real steps and the tick-the-box line. Both rulings are xian's, in session at 11:44: "we will have to let early testers know"; "reminding people to tick the box is probably a good idea, yes". HOST and CXO check the restored wording against the served screens on send morning. Remove the paragraph if #2087 is approved before then. **10-23 13:29 (Exec):** xian submitted #2087. Google's Verification Center reads "Your app's data access is under review". The caveat stays until approval. #2148 (the "Calendar Connected" toast on an unticked grant) is awaiting xian's admission call. If it ships unfixed, the tick-the-box line is what covers it, so keep that sentence even if the click-through paragraph is trimmed.

**10-25 17:11 (HOST, from Google's approval email, 15:50 PT):** `calendar.readonly` is approved for project piper-morgan-alpha. Keep the click-through paragraph and the tick-the-box sentence until a person reports the served screen (Web's browser can't sign in to Google). If the screen is clean, drop the click-through. Keep the tick-the-box sentence only if the box still starts unticked. #2148 is closed, so it no longer needs covering. Don't edit the consent screen, including its Terms URL field: the email says changes need a new verification request.

**10-25 17:35 (HOST, xian's served check ~17:30, five screenshots, #2087 issuecomment-6405604000): FINAL for the send.** There's no warning page and no yellow box. The calendar box starts **unticked**, so the tick-the-box sentence stays, and it's now the only setup line. The click-through paragraph is dropped. The bracketed work-account sentence is dropped as well: its cause was never confirmed, and the unticked box covers the email-only case. Connect then Test passed on an outside account. Not yet seen: the wizard connect path and a chat calendar read (#2087 stays open, not blocking). The blue "Learn why you're not seeing links" box needs no line. Leave the consent-screen Terms field alone.


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

**10-25 17:52 (CXO):** "this week's" is back in. It passed on Web's served week row (17:39, web-seed-1386). That's one account asked on a Sunday evening, with no mid-week row.

## 3. Other invitation lines still open on the checklist (no draft needed yet)

- **The invite code's step:** asked first. CXO closed #2088 and #2089 at 15:32 on 10-21 on Web's served rows (76789a8988: strip "1. Invite", "2. API Keys", "3. Account", "4. Projects", "5. Complete", no System step or Temporal line). The step-3 interim line is out. The invitation calls the first step "Invite". Still on Lead's pins: Create Account no longer asking for the code. Recheck what alpha serves on send morning.
- **#2089's system-check known-issue line:** not needed. #2089 closed 10-21 15:32 (CXO).
- **Beta or alpha form:** PPM's one line on the morning.
- **Wizard step 2, Slack and Calendar credential boxes (#2176): OUT of the letter (HOST 10-26 09:25).** #2176 is served (alpha `69d859ca5f`, Lead's promotion 07:06). Web's served step 2 (07:08) shows no Slack or Google Calendar Client ID or Secret box, and shows "You can connect Slack and Google Calendar later, in Settings → Integrations." once. So the letter's "skip the optional Slack and Google Calendar boxes" sentence and the fallback known-issues line both come out. No replacement is needed, since the page says it. If xian wants one anyway, use the served line above word for word. Limit: Web reached step 2 without spending a code, so the invite path itself wasn't run. (History: CXO's 10-25 17:43 sentence and HOST's 17:52 placement are in git, 10-25.)
- **The "alpha is nearly over" paragraph: FINAL, xian's words (HOST relay 10-26 17:23).** Replaces CXO's 10-25 line:
  > Alpha is nearly over! What you see now is pretty close already to what the first beta will be: the same Piper on the same servers. Right now I'm working on making sure Piper doesn't reply "none" just because it failed when it tried to read something.

  PPM rechecks on send morning that #2018 is still open and in work, since the paragraph says so.
  **10-29 (Comms):** this paragraph was written for the alpha letter. Whether it fits the beta invitation ("Alpha is nearly over") is xian's, at the beta draft.
- **The carry-over paragraph: IN, xian said yes (HOST relay 10-26 17:23).** HOST's tightening of xian's proposal, which xian approved for sending:
  > Your account and your work will carry over to the beta automatically. You can also start a new account when the beta officially begins. If you'd like your alpha account deleted at that point, email support@pipermorgan.ai and we'll do it for you (by hand, for now, within 14 days).

  The path and window match the live Terms ("just email support@pipermorgan.ai and we'll delete your account and everything in it within 14 days", HOST read the served page 10-26). **Keys left out on purpose** (xian: "Let's leave keys out. When beta comes out we can give the info then when it is actionable."). Don't add saved keys or connections. They rest on #2157 (Arch 10-25 18:49). Not checked: that the new-account path works at beta.
- **10-29 (PPM 09:51):** #2018 struck (closed served 10-28). The "alpha is nearly over" paragraph rests on #2151 (open 10-29, PPM 10:00), not #2018, so it holds. Recheck #2151 on send morning.
- **Known-issues strike (PPM 18:36):** none struck. #1595, #2042, #2021 and #2018 are open. PPM rechecks the morning of the send.
- **Create Account doesn't re-ask the code:** source only (CXO 17:43). Don't state it in the letter as a checked fact. The letter says only that the wizard asks for the code first, which is served.

## 4. HOST's send checks (15:23), all read on send morning

- The invitation's line pointing to pipermorgan.ai/privacy: **done 15:50.** Web quoted the Google paragraph from the rendered live page (website `4f3582d`), and since `a3cb49f` (17:0x) the paragraph and the footer Privacy link are in the served HTML too (Web's curl of four pages). Re-read only if the page changes again.
- Terms: describe chat deletion and account erasure (#2064, #2057, #2021) as they are on send morning.
- The code step: whatever the served wizard shows (HOST reads it).
- A Calendar scope change in #2092's lane would need the read-only sentence rechecked.

- **Your key (Exec 17:50, added 10-20):** no send goes without the "Your key" and "Who sees it" lines in the Terms draft, checked against what alpha serves. Open reads: stored keys with no ciphertext (PA or xian), and Fly backups (xian). The provider named is Anthropic unless the OpenAI run passes. PPM 10-22 12:27: PA's OpenAI run failed the 10-20 bar, so Anthropic only unless a new run passes.

## Voice checks

No semicolons in the partner copy. No "honest", "quietly", "load-bearing" or "cohort". Agents aren't called people.
