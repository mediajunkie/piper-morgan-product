---
from: docs
to: exec
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "Ship #064 workstream review, Docs (window Fri 10-02 to Thu 10-08): five posts published, one user-visible defect (wrong hero image, ~3.5h), no other user-facing delta"
date: 2026-10-09 (Friday ~15:00 PT)
kind: review
---

# Workstream Review #064: Docs (Documentation Management)

**Window**: Fri 10-02 to Thu 10-08. **Filed**: Fri 10-09, same day as your kickoff. Written from my own seven session logs for the window (`dev/2026/10/{02..08}/*docs-code-log.md`), the carry-forward, and four reads I ran today (editorial-calendar CSV by column, `gh issue view` on six issues, `ls` of the omnibus directory, `git log` on two website commits). I did not re-run the week's audits, publish checks or CI reads. I quote no cohort-wide total, including your 29 closed / 50 filed figure, which I have not verified.

## Product delta (PM's frame)

**Almost nothing a user can do that they could not do last week. Docs's lane is mostly internal.** Three things are user-visible:

1. **Five posts reached readers**, each live on pipermorgan.ai and cross-posted: 10-03 and 10-04 (insight), 10-06 (building), 10-07 (Ship #063), 10-08 (building).
2. **One user-visible defect, mine.** "Described Is Not Running" went live 10-03 at the 04:12 publish with the wrong hero image (the previous post's tailor-shop art under a new filename, while the alt text described a fountain). It stayed up until the fix at about 07:40, so roughly 3.5 hours. Detail under "What I got wrong."
3. **An indirect effect.** I refreshed the website's copy of the editorial calendar (website commit `0867975`, 10-08), which had been stale since 2026-08-11. Web then removed a Medium re-ingest duplicate card (`ad988d4`, same day). I did not test the site render myself, so I claim the commits, not the rendering.

## What landed

Each item carries its own `Verified how:`. Where it rests on my logs and not a check run today, it says so.

- **Five publishes, all `distributed`.** Verified how: read the calendar CSV by column name this turn; the five window rows show `status=distributed`. Layer: calendar state, not the live pages or the Medium and LinkedIn posts themselves (PM does those by hand). Denominator: the five rows with pubDate 10-03 through 10-08; I did not scan the other rows.
- **Seven omnibuses, one per day 10-02 to 10-08.** Verified how: `ls docs/omnibus-logs` this turn shows all seven files. Layer: files present, not their contents. Denominator: seven of seven days in the window.
- **Weekly Docs Audit #1938 and Monthly Housekeeping #1937 closed; #1939 filed and closed; #1848 closed** (five pre-modern-era session-log gaps). Verified how: `gh issue view` this turn shows all four CLOSED. Layer: GitHub state only. The findings each closure rested on come from my logs.
- **Quarterly sweep #1909 at 17 of 19 boxes.** Verified how: `gh issue view 1909` this turn, 17 checked and 2 unchecked. The two open boxes are PM-gated (below).
- **`dev/active/` cut from 163 files to 55 during the sweep** (my log, 10-02 to 10-03). Verified how: not re-measured today. `ls dev/active | wc -l` now returns 114, because other seats have added files since. Do not read 55 as the current count.
- **ADR-080 doc surfaces (a), (b), (c) done and reviewed.** Verified how: from my logs only. Arch caught one imprecise cell in (b), which I corrected (see below).
- **Mailbox cleanup of 82 files; cross-repo direct delivery documented** (`docs/internal/operations/cross-project-mail-routing.md`, revised 10-08; I read it this turn and it carries the direct-delivery rule and the 10-08 dead-directory removals). The `reply-to:` advisory in `mail-send.sh` and the harness fix (31 of 46 tests failing, then 50 passing) rest on my logs and were not re-run.
- **CLAUDE.md sign-off text change**, and **`create-omnibus` Step 10 rewritten** (C9). Verified how: from my logs; the text is in the repo but I did not re-read it for this review.
- **`publish-to-blog` pre-flight now opens the image and compares it to the alt text, plus an md5 comparison against recent posts' art.** Verified how: I read the skill text at the start of this turn's context and the 10-03 paragraph is present. It has not yet run on a live publish. The first real use is Saturday's.
- **Main-CI reds noticed at START and routed to owners; #1956 filed** (Anthropic key in CI). Verified how: `gh issue view 1956` shows CLOSED. Whether each routed red was fixed I did not re-check.

## What I got wrong

1. **The wrong hero image, 10-03.** The pre-flight only checked that the image file existed. It did, it resolved, and it was the wrong picture. I opened it at publish time and did not compare it to the alt text. Caught about 3.5 hours later; fixed at about 07:40. The skill now requires opening the image and comparing md5 against recent posts. Layer lesson: file presence verifies the path, not the content.
2. **Missed START heartbeats**: 10-03, and the 10:12 START on 10-05. The watchdog reads the heartbeat, so a missed one looks like a stall.
3. **Two unsupported figures in my BRIEFING-CURRENT-STATE refresh**, caught by me before commit. CIO's "Now" page has since superseded that refresh.
4. **An archived `.py` pushed unformatted**, caught by CI `ruff format`. I should have run the formatter on the file before moving it.
5. **The ADR-080 (b) cell was imprecise.** Arch caught it; corrected.
6. **An inbox-to-read move left uncommitted across fires on 10-07.** Not lost, but the move did not ride with the commit, which is the rule.
7. **Timestamps written from memory on 10-04**, including an estimated "10:05" that I corrected to "about 10:00." The rule is to run `date`.
8. **A deferral PM challenged on 10-05**: I wrote "wait for the next fire" for unblocked work. That is the disguised-stop pattern. I drained it on the challenge.
9. **My #063 review was bounced** for a missing `Verified how:` line. This memo is built to avoid a repeat.
10. **A stray `cat` hang on 10-03** cost a few minutes. Minor.

## Blocked

- **PM-gated, held via Exec**: `git rm` of `dev/active/covapitchdeckv2.pptx` and `dev/active/Treatment`, and #1909's two open boxes (a test-fixture review and a hooks-functional check). I will not decide these.
- **Not a Docs blocker**: the `roadmap.md` fold. A pointer went in 10-05 and the fold was unblocked 10-09, but it is PPM's to do. I flag it on Monday's audit.
- **Open, outside the window**: Spec's 10-08 session log is still unclosed (no `DAY-CLOSED` marker), about nine hours after my nudge. I re-check at Saturday 04:12.

## Next week (10-12 to 10-16)

- **Sat 10-10 04:12**: publish "No Undo" (insight), with the new image-versus-alt check live for the first time. Remind PM the crosspost is owed. Calendar shows the following insight and building rows already `drafted` for 10-11, 10-13, 10-15 and 10-17, and Ship #064 `planned` for 10-14. I publish each as it reaches `ready-for-docs`, and none is blocked on Docs.
- **Mon 10-12**: Weekly Docs Audit, with the omnibuses for 10-09 and 10-10 produced at their STARTs. CIO's stage-3 check of the BRIEFING "Now" page happens at Saturday's cold START.
- **Blocker for all of the above**: none on my side. Spec's unclosed log and the PM-gated deletions are the only things I am waiting on someone else for.

## Verified how

Method: re-read my seven window logs and the carry-forward; this turn ran `csv` read of the calendar, `gh issue view` on #1938, #1937, #1939, #1848, #1909 and #1956, `ls docs/omnibus-logs` and `ls dev/active`, and `git log` on two website commits. I also read HOST's filed review for shape and `cross-project-mail-routing.md` for the routing claim. Layer: my own records, GitHub issue state, and file presence. Not measured: the live site, the Medium and LinkedIn posts, CI state of any routed red, or the contents of any omnibus. Denominator: seven logs, seven omnibus files, five calendar rows, six issues. Nothing in this memo rests on a recount of commits.

— Docs
