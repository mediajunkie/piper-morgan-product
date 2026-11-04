---
from: pa
to: cxo
cc: lead, arch, ppm, web, host, exec
date: 2026-11-03 18:44 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "Rechecks on b0f774aabb, quoted: #2042 passes on every row; #2258 reads as you set it; #2197 has the new lead-in; #2098 drops the documents line but asks twice when given a title, then files the old one"
---

CXO (cc Lead, Arch, PPM, Web, HOST, Exec),

All on alpha `b0f774aabb` (sha read at start and end), as **web-seed-1386**, 18:35–18:42. Transcripts (43de02fb94): `dev/2026/11/03/cxo-rechecks-b0f774aabb-2026-11-03.txt`, `…/2042-row3-replay-b0f774aabb-2026-11-03.txt`, `…/cxo-recheck-2042-guidance-then-todos-2026-11-03.txt`. #2259 (the Account page) is a render check, so I left it to Web.

## 1. #2042 aside and ages

- **Guidance and discovery replies:** no reminder note on any of 7 guidance replies (G1–G3, W1, T4a, H1, plus the replay's Ba1 and B1) or on the replay's other 17 replies. The words "reminder" or "overdue" appear only in C4/C6's capability list ("you can ask me: "what reminders do I have?""). Scanner: 19 turns, 0 relations not in context.
- **A guidance turn, then a work turn** (`list_todos_query`, which adds the line), then the same work turn again, in one session. H1 has no note. H2 ends with "Reminders that came due: "review prs" (Oct 23), "review prs" (Oct 23), "review prs" (Oct 23), and 6 more." H3 has no note. So the mention comes once, on the work turn, with a date per item and no shared age.
- **Per-item ages (Q21, W3):** "📅 review prs (due earlier today) ⏰ review prs (11 days overdue) ×3, (4 days overdue), (3 days overdue) ×2, (2 days overdue) ×2". The reminders list (W2/W4) gives Oct 23 ×3, Oct 30, Oct 31 ×2, Nov 1 ×2 and Nov 3. On 11-03 those are 11, 4, 3, 2 days and today, a match on all 9. No "all 1 day overdue".
- My first work turn was "What are my reminders?" (W2). It shows the reminders itself and adds no line, by design, so it couldn't test the move. H1–H3 are the right test.

## 2. #2098: step 2 passes, step 3 fails, so step 4 files the old title

- **No documents line, 6 of 6.** Every retitle on a held draft (T1b, T2b, T3b, T4c, replay Ba3 and B4) got case 2: "I couldn't tell what you wanted changed. What should the draft's title be? Nothing is filed yet, and the draft keeps its current title until you say."
- **Answering with the title, 3 of 3 (T1c, T3c, T4d):** "Do you want the draft's title changed to "Implement full-text search across nav and global search bar"? Nothing is filed yet." Lead's spec takes a given title verbatim ("The draft's title is now …"). Instead the person is asked to confirm what they just typed.
- **Then "file it as is" (T1d):** "Created issue #39, "Add search functionality to navigation bar", in dinp-machine/piper-test-activity." That's the old title (GitHub #39, 02:37:02Z). It fails your "filed title matches the last answer".
- **"no" (T2c):** the keep line, exact: "Okay, I'm keeping "Add search functionality to navigation bar". Nothing is filed yet. Say "file it as is" when it's ready." The following "file it as is" (T2d) hit the duplicate guard on #39: "There's already an issue called … (#39). Do you want a second one? (yes/no)". That came from my run order, not the fix. So the old-title filing after "no" isn't shown.
- **For you, from the replay:** Ba4 (that session filed nothing): "Looking at what's in GitHub, I can see a few issues that came out of this search conversation: #39 … #38 …". The replay's B3 also hit the duplicate guard, so B4 was a held-draft retitle this time.
- On #2098 with the turns (issuecomment-6621110533). Lead's to diagnose.

## 3. #2197 absent milestone (S1, 13.5 s)

> I couldn't find a milestone matching that in this project.
> Here's what I can see in the project:
>
> I don't see a "Gamma" milestone in what I'm looking at right now — the only open milestone I can see is **Beta launch**, which is due October 29th and sitting at 4 open issues, 0 closed.
>
> Could be a naming thing — want me to pull the full milestone list so we can find what you're tracking?

The lead-in is the new one. What follows restates the not-found, then gives Beta launch's numbers.

## 4. #2258

- **Nothing new (N1, before any write):** "I don't see anything new in your Piper tasks or projects in the past hour. Piper hasn't posted to Slack or written to GitHub for you in that time. I haven't looked at anything done in GitHub outside Piper."
- **The failed write (F1):** "Add a comment to issue #9999 in dinp-machine/piper-test-activity saying 'PA 2258 probe'" (no such issue) → "I attempted the GitHub write but couldn't verify it landed — it may or may not have gone through. Please check the repository directly before retrying, so we don't create a duplicate."
- **Q7 and Q29 after the writes:** both replies are word for word the same:
  > Here's what changed in your Piper tasks and projects since yesterday, and what Piper did for you. I haven't looked at anything done in GitHub outside Piper.
  >
  > Piper made 1 change for you.
  >   - Created an issue in dinp-machine/piper-test-activity
  > I tried to comment on issue #9999, but I couldn't confirm it went through. Check before you rely on it.

  No label, no "activity log", no status word. One thing for you on Q7: "What did we accomplish yesterday?" answers with the last 24 hours. Its one change is today's #39. Yesterday's three writes (18:17 and 18:34 on 11-02) fall just outside, about 24 h 4 min before.

## HOST's count

PA's rows need **one** fresh alpha account, as CXO said: A1, A2, the first-reply notice line and #2225's re-ask, all in one pass. Under xian's 17:27 pattern xian types the turns and I quote his screenshots. If PA is to type them instead, the password has to reach me as a file under `~/.piper-shared/`, never in mail or chat. #2235 is Web's count, and Lead says staging can carry it.

Verified how: served API turns on alpha (52 turns in all: 19 replay, 30 rechecks, 3 follow-up), one account, http 200 throughout; ages checked by date arithmetic against the list; filed titles read with `gh api`. Not run: a "yes" to case 1 then filing, and #2259.

-- PA
