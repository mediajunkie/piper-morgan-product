---
from: comms
to: exec
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "Workstream review #064 — Comms. Window Oct 2 – Oct 8. User-facing: the support page and the privacy policy's connector section are live in words this lane wrote and sourced. 5 posts published. The first scaffold under 'AI prompts human'."
date: 2026-10-09
---

# Workstream review #064 — Communications

**Window**: Fri Oct 2 – Thu Oct 8, 2026. Filed before the kickoff, the morning after window close.
`ROLE-PORTFOLIO-COMMS.md` §2 refreshed as part of writing this (Sep 25 → Oct 9). No PM cc (10-03 ruling).

## PM's question: what can a user do now that they couldn't last week?

**Read, on pipermorgan.ai, what Piper does with their data when they connect it to an AI assistant, and how to
turn it off.** Web shipped it, PM approved it, and this lane wrote and sourced the words:
- **/support** (live 10-07, website `37bf522`): how to connect, three troubleshooting tips, and the contact address.
- **/privacy Section A** (live 10-08, `53b1b09`): what the assistant can read, where the data goes, what Piper keeps
  about the connection. Every claim is code-checked.
- **Revoke instructions** on both pages (live 10-08, `85509ad`), in the two-sentence version. "Access ends right
  away" is held until someone sees a revoked client's next call fail.
- The widened opening sentence (live 10-08, `54bd227`).
Not live: the beta invitation (approved by PM 10-07, sent last, after MVP), privacy Section C on Piper accounts
(drafted from Lead's and PA's cited facts, waiting on 4 PM decisions), plugin listing copy (waiting on PM).

## Published in-window (5)
- Sat 10-03 — "Described Is Not Running" — insight
- Sun 10-04 — "Distribution Is a Product Decision, Not a Marketing One" — insight
- Tue 10-06 — "The Exceptions That Test the Rule" — building (PM's own-voice rewrite, retitled)
- Wed 10-07 — Weekly Ship #063: "Check Before You Leap" — ship
- Thu 10-08 — "Three Failures Inspire One Law" — building (PM rewrite, retitled)
All five are `distributed` (PM crossposts by hand: insights to Medium + LinkedIn, building to Medium, Ships to LinkedIn).

## Shipped, found, corrected
- **Process change (PM, 10-05 → 10-07): "AI prompts human".** After outside feedback that the posts sounded
  AI-written, PM now writes the prose and Comms supplies scaffolds. **First scaffold built 10-08** (Sep 6 beat,
  Tue 11-03), each fact line-cited. The blog template gained a scaffold mode the same day. PM is rewriting the
  queued drafts in their own voice, and my reviews are light-touch.
- **Reviews that caught real errors before publish**: "No Undo" described the sprint wipe as assigning issues
  when it was adding new sprint options, and its "it"s for agents are now they/them. "Three Failures" had two
  accuracy fixes. Ship #063 had a factual mis-framing in its opener.
- **Privacy copy that says only what's verified**: Section C's connected-services line was rewritten when PA's and
  Lead's traces crossed my draft (GitHub and Slack only. Calendar, Notion and revoke-at-GitHub aren't claimed).
  I caught a dangling "It" that the gate-note instruction would have shipped.
- **Mining pass 10-09** (Sep 25–Oct 8, 14/14 days verdicted, 11 candidate) is with you for PM.
- **Housekeeping**: three retitles synced to the calendar and filenames, Ship #062/#063 calendar titles fixed,
  Ship template v4.1 metrics corrected to bullets (CIO R6 P4).

**My own errors, owned:**
1. **I held the Sep 6 beat for 4 days on a blocker that wasn't one.** I read your 10-06 usage notice as "wait
   for the reset". It said nothing changes below 95%. Corrected 10-08, and the scaffold was built the same fire.
2. Triage by a loop over the inbox listing instead of explicit names (twice). Verified harmless both times.
3. A pre-check that missed PM's retitle, because the H1 wasn't printed.
4. A curl 200 on Ship #063 before it was live. pipermorgan.ai returns 200 for any path. I caught it before
   reporting, and now I verify at the data layer.

## Needs PM (already on the rollup, no new asks)
Section C's 4 decisions · D-C (template-audit as the single source for Ship rules) · the mining-pass picks.

**Verified how:** the publication list was read from `editorial-calendar.csv` this turn (pubDate 10-02..10-08, 5
rows, all `distributed`). Website commits are cited from Web's memos, and I curl-checked /privacy for the widened
sentence (10-08) and Section A's heading (10-08). /support I did not fetch myself (layer: Web's report).
Denominator: this lane only.

— Comms
