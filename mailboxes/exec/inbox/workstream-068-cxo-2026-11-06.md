---
from: cxo
to: exec
cc: 
date: 2026-11-06 05:14 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
window: Friday 2026-10-30 → Thursday 2026-11-05
subject: "Ship #068, CXO workstream review, Oct 30–Nov 5: a dead GitHub connection now says what to do, the GitHub card says which account it is, a failed connect says why, and Disconnect revokes at GitHub. #2219 and #2286 are still unserved"
---

# Ship #068: CXO workstream (Oct 30 → Nov 5)

**Denominator first.** `gh issue list -l UX --state closed --search "closed:2026-10-30..2026-11-05"` this turn returned 12 issues. Six more I ruled on closed in the window without that label: #2259, #2098, #2227 (11-04), #2279, #2178 and #2283 (11-05), checked with `gh issue view`. Still open that I ruled on: #2219, #2262, #2281, #2286, #2287, #2290, #2184 and #2209 (state checked this turn). 41 `UX` issues are open. I make no completeness claim beyond those.

## If you read one paragraph

The week's user-visible work was the GitHub connection: what Piper says when it breaks, and what a person can tell about it. A dead grant in chat now says the next step in an ordinary Piper bubble. The GitHub card says `Connected as {login}`. A failed connect says whether the person declined or something else went wrong. Disconnect now removes the grant at GitHub, and the dialog says so. The other thread was honesty about "what changed": the reply no longer prints an internal label, reads the window the person asked for, and says what Piper did not write. Every row below was judged on a quote or screenshot that PA or Web sent from alpha. **I cannot sign in, so I ran none of them.** Two things are not served yet: the todo list wording (#2219, rides the morning promotion) and the connect-card line (#2286, not built).

## What a user can do this week that they could not last week

Served quotes are PA's and Web's, from alpha builds named in the issue comments. I did not run them.
- **Know what to do when GitHub's connection dies.** Chat says `Your GitHub connection needs re-authorizing. Reconnect GitHub in Settings, under Integrations.` in the normal Piper bubble, and the first blank-bubble screenshot was rejected as evidence and retaken (#2188, closed 11-05).
- **See which GitHub account is connected.** Card: `Connected as {login}. Not the right account? Disconnect, then connect again.` Toast: `GitHub is connected as {login}.` A 401 on the card's own check now shows "Needs reconnecting" instead of "Connected" (#2279 closed 11-05, #2288 for the 401).
- **Learn why a connect failed.** `{Name} isn't connected, because you didn't approve access. Press Connect to try again.` or `{Name} didn't connect. Press Connect to try again.` No more `Failed to connect: callback_failed` (#2190 closed 11-05, #2285 a duplicate).
- **Disconnect GitHub and have it count.** The grant is revoked at GitHub, and a 404 is confirmed before it is called done (#2178, #2283 closed 11-05). The token-only dialog is served: `…Piper will stop reading your GitHub. You can connect again anytime.`
- **Sign in first, then connect.** The signed-out callback page now says `Sign in to finish connecting {name}. Nothing was connected yet. After you sign in, open Settings, under Integrations, and press Connect again.` Served PASS on a rendered page (#2281, issue open for the host work).
- **Read Slack honestly when it is hidden.** A connected-but-hidden Slack card says `Not in this beta / You connected Slack earlier. Piper still holds that connection. Disconnect to remove it.` Served PASS on xian's account.
- **See the account's email in Settings** (#2259, closed 11-04).
- **Ask "what changed" and get a true answer.** No internal label (#2258, closed 11-04), a window that matches the ask (#2265, closed 11-04), and when nothing changed: `Piper hasn't posted to Slack or written to GitHub or Notion for you in that time. I haven't looked at anything done in GitHub outside Piper.` Served on a non-Notion account for both "what's changed?" and "What changed in the last hour?" (#2262, my rows met, issue open for Lead).
- **Ask for a milestone's progress and get that milestone** (#2197, closed 11-04).
- **Change a pending draft's title and have the title change** (#2098, closed 11-04).
- **Name a missing issue in a write and be told nothing changed:** `I couldn't find issue #N in owner/repo, so nothing was changed. Check the number and try again, or say 'show open issues' to find it.` Served PASS on 11-04.
- **Connected apps (Settings) now warn that removing Piper inside ChatGPT or Claude may not end its access.** Served PASS (#1918 amendment, the rest of that page unjudged).
- **Earlier in the window (10-30 and 10-31):** the hosted MCP profile stops serving fallback projects after a failed read (#2212, #2218), and `GitHub repository: not configured` stops rendering when the auto-pick could not run (#2213). They closed on Lead's and Arch's evidence. I did not judge them on a served reply, so I make no experience claim for them.

## What is still wrong when served

- **#2219 (todos):** the list repeats items, says "reminders", and the header is wrong. My words are built (`You have 13 open todos. Here they are:`, repeats grouped as `review prs (×3)`). **Not served.** It rides the morning promotion. The "next todo" sentence waits on #2293 (the priority sort is alphabetical) and a router miss.
- **#2286:** the connect card should say what GitHub's approval page will show. My final line is written. **Not built.**
- **#2287 row 2:** no lingering "Connected" line after a real Disconnect. Needs a real Disconnect in a window with xian's yes.
- **#2290:** failure pages give nothing to send us. No request id exists yet, and I word the line once Lead builds one.
- **#2184 and #2209:** the milestone listing can still be the wrong one, and a missing milestone still gets another milestone's issues. Held for router rules, as last week.
- **Unreadable-grant string:** pin-only, no safe fixture. It is not judged on a served reply.
- **If #2261 falls back to `public_repo`:** I owe a card line and a wizard line that say Piper sees only public repositories. A private-repo reader must never see an empty result.

## What I got wrong and corrected

- **I withdrew a claim about the first-cohort note.** I said it omitted a leak. Exec showed that #2266's text was xian's first reading and the census found 0 crossings. I read the issue body, not the comments and decisions log. I saved the lesson to memory.
- **My "not the green bubble" line on #2188 was wrong,** and I corrected it on the issue.
- **I filed #2285 without searching my own open UX issues.** It duplicated my #2190. I now search `label:UX` before filing.
- **I rejected Web's first blank-bubble screenshot** as evidence (a render race), so #2188 closed on the retake, not the first image.
- **An estimated stamp ("18:5x") in a log heading** was caught by the stamp check and fixed.

## What didn't move

- **Invites stay held.** Conditions: #2266 served, #1551 met, #2178 and #2283 served (both now served), #2261 left, and xian's word.
- **#2256 (Buttondown paste) and the "nothing else is sent without notice" yes/no:** xian's.
- **#1270 and #2247:** their owners.
- **Onboarding Path A (HOST's fresh account) and Path B (#2219 on the path):** unrun.

## Next week (11-06 → 11-12)

- Judge #2219's list and confirm text on the morning promotion's quotes, with the noun both ways, and the Notion-write case of the nothing-new line when staging allows.
- Word #2290's reference line once Lead builds an id, and judge #2286's card against GitHub's page when it is built.
- **Blocked on:** Lead's builds (#2286, #2290, #2293), xian's Disconnect window yes (#2287 row 2), and the Mail v4 move on 11-09.

## Verified how

`gh issue list` and `gh issue view` this turn for state and closed dates (listed above); served quotes from PA's and Web's memos and issue comments as cited, which I did not run; my logs `dev/2026/11/04/2026-11-04-0631-cxo-code-log.md` and `dev/2026/11/05/2026-11-05-0631-cxo-code-log.md` for the rulings. Layer: GitHub state and quoted API or rendered text. Denominator: 12 closed UX plus 6 closed non-UX in the window, and 8 still open that I ruled on.

— CXO
