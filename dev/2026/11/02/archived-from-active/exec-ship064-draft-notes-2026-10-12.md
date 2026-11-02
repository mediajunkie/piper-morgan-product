# Ship #064 draft notes, for xian (2026-10-12)

Draft: `docs/public/comms/drafts/weekly-ship-064-draft-2026-10-12.md` (status: draft, not committed, not on the calendar row yet).
Window: Fri 2026-10-02 to Thu 2026-10-08. Body ~1,760 words (Ship norm ~1,630, #063 was ~1,470). Long-ish: a question for you, not a defect.

## Theme and why

**"Code Decides Permission."** Your Monday 10-05 test round failed ("first three complete" among the failures), you rejected the regex patch, Arch wrote down "the LLM decides meaning, code decides permission, checks meaning against real data, shows before it acts" that evening, you confirmed it 10-06 (ADR-080), and the same sentence was served on alpha by Wednesday 10-07 (test account). It's a product milestone with a before/after, it's the direction change four reviews (Arch, Lead, CXO, PA) point to, and it gives a clean link to the learning pattern ("a read that can't fail out loud fails quietly", the #1959/#1965 cluster, which is the rule's "check against real data" half). Alternatives if you want a softer title: "Say So When You Can't Check", "Meaning From the Model".

No footer tease: template-audit #6 marks it N/A on Ships (Ships sit outside the tease chain). The hook is the first line of the opener.

## Three things you're most likely to want to edit or decide

1. **The opener's quote of you.** I used "my verdict that night was that I would not use this product" (Arch's review quotes you as "I would not use this product"). The 10-05 omnibus also quotes you: "I am questioning the whole project!" Pick one, soften it, or drop it. It's your public voice.
2. **How far to push "on alpha".** The "first three" sentence was served on the **test account** (Lead 10-07 16:28, confirm + completion + REST check, Arch withdrew its contrary line). You have not used it yourself, and no one claims you have. The armed-turn item ("show my projects" while Piper waits for a name) is in alpha's build `e8ecd10d5a` (I checked ancestry: `7dbc801fc1` and `26b138ecb5` are both ancestors) and Lead reports PASS live 10-08, but Arch's review still lists it among served checks owed. If you want only twice-confirmed claims, cut or hedge that bullet.
3. **The dates paragraph.** I wrote that you're holding Fri 10-23 / Fri 10-30, the brake fired Thursday, and "as I write this, five slips are logged against that baseline and no days have moved." The five-slip, zero-days figure comes from the slip ledger in `docs/internal/planning/beta-gate-standard.md` (its "Net" line), **not from a memo**, and it runs past the window (entries on 10-09 ×2 and 10-11). PPM's memo counts 3 for the window itself. Decide whether "five" belongs in a window-bound post or whether you'd rather say "three in the window, two since".

Also worth a look: the Methodology "AI prompts human" line describes your new writing process publicly. And the phase tag is copied from #063 unchanged.

## Claims I could not verify myself (taken from a named source, not re-measured)

- **29 closed / 46 filed**: mine, run today: GitHub search `closed:` / `created:` with UTC bounds 2026-10-02T07:00Z to 2026-10-09T06:59:59Z (29, all COMPLETED, and 46). Your 10-09 synthesis said 46 by list and 50 by a date search. No other role verified a total. Treat as approximate.
- **Gate 28 → 14**: PPM (`sprint-truth.py` 28 at 10-02 close, 14 at 10-06 close, criteria line 14 at 10-08). CXO's `sprint-truth.py` 10-09 14:48: 14 not done, 1,236 done. My run today (`--no-snapshot`): **13 not done, 1,238 done** (#1951 closed 10-11, post-window). The post uses the window figure.
- **Ceiling 440 → 155**: Arch (from git at both window edges) and Lead's logs. Not re-run by me.
- **"First three" served on alpha**: Lead's 10-07 log as quoted by Lead and Arch. Not re-run by anyone since 10-07.
- **Revoke worked when you pressed it Thursday**: your own report via Exec (PA says so). I didn't observe it.
- **Revoke silently did nothing Monday**: PA's memo and the 10-05 omnibus.
- **169 KB → 5 KB briefing**: CIO's log figures. 10-08 omnibus says 168,846 → 5,152 bytes.
- **41 red runs unseen, 12 workflows**: CIO and 10-05 omnibus.
- **Rate limiter would have enforced nothing in prod**: PA's memo, 10-05 omnibus.
- **Promote workflow: three bugs in three attempts**: 10-07 omnibus.
- **Wrong hero image ~3.5h**: Docs' memo. The 10-03 omnibus says you caught it.
- **Arch: six rulings/claims corrected**: my count from Arch's "Got wrong" list (three 10-04 rulings + "CLARIFY binds" + the OAuth resolver + the sprint-goal reply). Arch didn't state a total.
- **Five slips, zero days moved**: the ledger in `beta-gate-standard.md` (see item 3 above). Not a memo figure.
- **Website pages**: I fetched /support, /privacy and /try/alpha today (HTTP 200, HTML contains "Connected apps"/"revoke"/"Request an invite"). That's the HTML layer, not a render. Phone width (390px) was never checked by anyone (Web).
- **"Unlink asks first" and "delete my project tells the truth" are on alpha**: CXO lists both as closed user-visible changes (10-04, 10-06). I did not check their commits against alpha's sha.
- **"Every agent's review listed at least one of their own mistakes"**: true of the ten reviews I read (each has a got-wrong section). Not checked for roles that didn't file.
- **Hero image URL** `https://pipermorgan.ai/assets/blog-images/three-failures-inspire-one-law.webp`: HTTP 200 image/webp today (a bogus path returns a real 404, so the 200 means something). Alt and caption are verbatim from the post's frontmatter.

## Kept out on purpose

- No outside names (testers, client contacts), email addresses (the support and invite addresses are described, not printed) or credentials. The omnibus logs name two outside people and a tester handle; none of that is in the draft.
- No bare issue numbers in prose ("close issue 108" is a user's example phrase).
- Spend figures, the cache-economics thread, mail v4 detail, the private mail repo, Spec's evaluation, and the HOST roster/credential slip: internal, left out.
- `status: draft` added to the frontmatter as you asked. #063 carries only image/alt/caption, so remove `status` before publish if the pipeline doesn't expect it.

## Mechanical checks run on the draft (template-audit, Ship calibration applied)

Semicolons 0. No "load-bearing", "cohort", "fold", "honest", "CoS". One "someone" removed. Agents and Piper are they/them (fixed one "it" for Piper, one "its" for agents). Negation-reveal and throat-clearing greps: 0. Typographic residue: 0. Title case: OK. `check-acronyms.py`: no hard findings; NO-GLOSS advisories on role short-forms (N/A on Ships) and on "MVP" in the phase tag (same tag #063 shipped with). Days of week checked for 10-03, 10-05..10-08, 10-14, 10-23, 10-30.

Not done: the calendar row update (the Ship #064 row is still `planned`, pubDate Wed 10-14), commit, and Comms' template audit. Those follow your read.

## Sources read

Canonical artifacts:
- `.claude/skills/draft-weekly-ship/SKILL.md` (41,119 B): read in full.
- `.claude/skills/template-audit/SKILL.md` (44,080 B): read in full.
- `docs/internal/development/weekly-ship-process-guide.md` (13,313 B): read in full.
- `knowledge/weekly-ship-template-v4.1.md` (11,947 B): read in full.
- `docs/internal/planning/comms/xian-voice-tone-guide.md` (23,854 B): read in full.
- `docs/internal/planning/comms/blog-style-guide.md` (5,369 B): read in full.
- `docs/public/comms/drafts/published/weekly-ship-063-draft-2026-10-03.md` (9,064 B): read in full. #060–#062: headings and word counts only.
- Not read: `docs/internal/planning/comms/blog-post-template.md` (11,543 B), the template-audit pre-flight's structural reference.

Workstream memos (all in `mailboxes/exec/read/`, all read in full):
- `workstream-064-cio-2026-10-09.md` (5,214 B), `-comms-` (4,588 B), `-comms-addendum-next-week-` (1,411 B), `-docs-` (8,005 B), `-host-` (4,532 B), `-lead-` (5,991 B), `-pa-` (4,616 B), `-ppm-` (6,892 B), `-web-` (8,857 B).
- `review-arch-to-exec-ship-064-workstream-review-oct2-oct8-2026-10-09.md` (5,409 B).
- `review-cxo-to-exec-ship-064-workstream-review-oct-2-8-…-2026-10-09.md` (5,511 B).
- `answer-arch-to-exec-cc-lead-ship-064-first-three-…-2026-10-09.md` (2,286 B), `answer-lead-to-exec-cc-arch-ship-064-first-three-…-2026-10-09.md` (1,724 B).
- `2026-10-09-ppm-to-exec-ship-064-review-amended-…md` (1,161 B).
- `janus-to-exec-ship-064-relayed-beta-dates-already-answered-hold-2026-10-09.md` (1,177 B), `janus-to-exec-xian-asks-ship-064-workstream-synthesis-status-2026-10-09.md` (786 B).
- The 10-12 inbox memos (three, HOST/CIO/Docs/Comms on other topics): not read.

Synthesis: `dev/active/exec-ship064-synthesis-2026-10-09.html` (17,938 B): read in full (text extracted from HTML).

Omnibus logs (`docs/omnibus-logs/`):
- 2026-10-02 (20,764 B) and 2026-10-03 (27,356 B): read in full.
- 2026-10-04 (29,239 B), 10-05 (31,775 B), 10-06 (37,050 B), 10-07 (33,789 B), 10-08 (32,052 B): read in full **except the Timeline section**, which I skipped. Day type, core themes, technical details, impact, learnings, cross-role notes, discovered work, process findings, continuity and open-to-PM sections were all read.
- No session logs (`dev/2026/10/0x/`) opened.

Calendar and posts:
- `docs/internal/planning/comms/editorial-calendar.csv` at origin/main (430,613 B): rows with pubDate 2026-09-30..2026-10-21 only, all columns.
- Published posts, first ~30 lines each: `the-contract-tested-the-day-it-was-born.md` (5,108 B, "The Exceptions That Test the Rule"), `three-failures-inspire-one-law.md` (4,593 B), `described-is-not-running.md` (5,266 B), `distribution-is-a-product-decision-not-a-marketing-one.md` (5,391 B).

Other:
- `docs/internal/planning/beta-gate-standard.md` at origin/main (85,737 B): grep for slip/ledger terms plus the slip-ledger table and notes (lines 88–140, each line cut at 420 characters). Partial.
- `python3 scripts/sprint-truth.py --no-snapshot --list` (today 14:4x PDT): "MVP: 13 not done (2 Sprint Backlog, 2 In Progress, 1 In Review, 8 Product Backlog); 1238 done." Baseline not moved.
- `gh` search counts (closed 29, created 46), `gh issue view 1886` (OPEN), `git merge-base --is-ancestor` for five shas against `e8ecd10d5a`, curl of the two hero `.webp` URLs and three site pages.
