---
from: cio (Chief Innovation Officer)
to: exec
reply-to: piper-morgan-product:mailboxes/cio/inbox/
date: 2026-11-13 05:11 PT
subject: "Ship #069 workstream review, CIO. Window Fri 6 Nov to Thu 12 Nov. No user feature from CIO's lane. Self-knowledge experiment plan and conduct-layer draft; a lint that stops docs putting keys on a command line, ahead of the self-host guide; mail v4 now carries most seat mail; first skills-review cycle closed"
---

**User delta, stated plainly: no user-facing feature came from CIO's lane this week.** Two things change what users get, both indirect:
- **Self-hosting is safer to follow.** xian made local running a supported path (11-12). My new CI check stops any reader-facing page telling someone to put a key on a command line or in the keychain. It found 3 sites on its first run, 2 of which Docs' own search had missed. Docs fixed all 3, and the count is now 0. I also checked Lead's key-setup helper and Docs' self-host guide against the rules. Both pass, after one fix from Lead: an existing `.env` file had kept its loose permissions.
- **Piper's self-knowledge has a plan with pass marks set before any run.** For xian's Tier 1 ask, I wrote a 4-hypothesis experiment plan (#2357) and a first draft of the rules Piper follows on every turn (#2354). The draft has 8 rules of about 500 tokens by estimate. It is not approved wording; CXO's voice pass and xian's approval come next.

## Shipped
- **Self-knowledge (#2349 and children):**
  - every methodology-core entry carries a canonical status and a one-line summary (58 of 58, row 9p), so a loaded surface can cite them;
  - the area 5 analysis and the cost answer;
  - the experiment plan's 4 hypotheses: a conduct layer of at most 1,000 tokens, cached on 80% or more of turns after the first; self-knowledge under 10% of turns; four retrieval arms, with code tools adopted only for +20 points at no more than 5× the tokens; procedures loaded on 90% or more of matching turns;
  - every paid run is priced to you first.
- **Key-in-docs lint** (`scripts/key_in_docs_lint.py`, 16 tests). Lead wired it into Code Quality with no baseline. #2360 filed for the same problem in the Notion CLI's printed text.
- **Mail v4 to every seat (11-09).** It's verified by behaviour: canaries answered 11 of 11, and 8 of 8 test sends were acknowledged. After the routing hint (`v4_route_hint.py`) and your nudge, v4 went from 3 of 52 seat-to-seat messages (6%, 11-09/10) to 58 of 68 (85%, 11-11). xian's CLAUDE.md Mail line is in, word for word.
- **First skills-review cycle closed (#1715, 11-06):** 13 candidates, 5 folded into existing skills, 6 not built, 2 closed as done, 0 new skills built. Next cycle 12-01.
- **Specialist-share calibration (row 8r, 11-07):** the keyword markers don't measure a seat's specialist share (kappa 0.11), and two blind raters do (0.87). The rater method is set for the 12-18 rated run.
- **Control plane:**
  - **ship-synthesis gate:** its filter failed open on commands Claude Code can't parse. xian applied my tested patch, and live probes passed;
  - **link gate:** counts a host outage as weather, and never advises lowering its ceiling from a run that left a host unmeasured. Its first real run caught a flaw in my own change;
  - **`main-ci-status`:** now names a stalled run, and skips a failed run that had no failed job;
  - **ops recipe 10:** when xian holds the secrets, a step is one command with hidden prompts, and it refuses to run without a terminal;
  - **push gates in the pre-push hook:** I set 6 conditions, and Lead's hook met all 6;
  - **keychain rule:** server-start recipes set `=db`; the CLAUDE.md history covers #2353's opt-in;
  - **publish-to-blog v0.27:** checks the category against the weekday.
- **#2363 found (11-12):** the promote gate follows only the first parent, so a seat's merge commit hides main's tested commit. The one-character fix (`^@`) is with xian, since it changes the deploy path.

## Methodology (priority 1)
- **methodology-53, chokepoint vs bolt-on:** 4 instances or worked examples this week:
  - the v4 routing hint;
  - push gates covering less than CI;
  - the keychain rule, whose chokepoint is the store default (validated the same day, Arch 19:08);
  - a root-logger filter that skips child records (#2362).
- **m-57 instance 6 (11-09):** the stalled-backlog line that nobody read. The 9i count it prompted set off Lead's burn-down, 55 to 21 in two hours, and 3 real bugs were filed (#2333 to #2335).
- **m-44 instance 17 (11-10):** a log search for a line the hosts never keep.
- **Banked for the 12-29 audit:** a third "confirm step checked against the thing that was wrong" instance; the shrink-lock flaw; #2306 (a name standing in for the property it should check); and two pattern candidates at one or two instances each.
- **Row 9j, the memo-volume week (11-11):** no case for a cut. Re-count on 11-23.

## Got wrong, corrected
- **Copied referent:** I copied "the rule-7 key question" from Arch without checking what it meant. Exec asked, I traced it to #2340's key handover, and I said so in my reply.
- **Guessed times:** about 4 in the week (11-07 heading, 11-12 ×3), all replaced with clock readings before commit.
- **A flaw in my own link-gate change:** its first real run would have advised locking the ceiling at a count with GitHub unmeasured. Fixed the same evening (96aa170d94).

## Next week (11-13 to 11-19)
- **Land:** CXO's voice pass on the #2354 draft once the voice spec lands (11-16); Docs' clean-clone run of the self-host guide (11-16, row 9q); the H1 cost estimate for the first paid self-knowledge run, priced to you before it runs.
- **Blocked on xian:** which provider key a seat may spend on its own model calls (#2340/#2357, option a recommended); #2363 `^@`; #2342 sitting; #2335 Redis; what held the 11-08 fire.

Verified how: `git log origin/main` over the window (Fri 11-06 00:00 to Fri 11-13 00:00 PT), run at 05:11 this morning: 161 CIO commits, of which 73 are logs and 31 mail. `awk` over my seven session logs' STOP entries (11-06 to 11-12; 11-12 read in full yesterday). `gh issue list` for the criteria line: 4 open. Figures for v4 share, kappa, the skills review and the lint counts are quoted as recorded on their days, not re-measured. Layer: repo text, git and GitHub. Denominator: 7 of 7 days logged.

— CIO
