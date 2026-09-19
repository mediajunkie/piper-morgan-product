# Handoff — Chief Architect (arch) — 2026-09-18

**For**: a successor seat with no memory of the last three weeks. **Sourced from `origin/main`**,
not from chat. Written for the reboot/renewal gate (Exec, 2026-09-18).

## ⚠️ If you are the post-renewal seat, read this line first
This seat was named for **wave 1** of the fleet renewal on 2026-09-18 evening and confirmed GO.
Cron `a1a8e2e5` was left ARMED deliberately — crons are process-scoped, so `/clear` keeps them
and no park/re-arm dance is needed (Exec's wave-0 finding). Verify it with `CronList` anyway.
**#1824** was filed minutes before the clear because that finding existed only in a mailbox
memo; check it landed and is legible to someone who wasn't here.

**Don't re-derive what's already written.** Read, in this order:
1. `CLAUDE.md` — cohort law. The Amber/Model-A section and the mailbox-discipline section are
   the two that bite hardest cold.
2. `docs/briefing/BRIEFING-ESSENTIAL-ARCHITECT.md` — the role.
3. `dev/active/arch-carry-forward.md` — **refreshed today**; in-flight state lives there, not here.
4. `dev/active/arch-standing-items.md` — the queue, 5 dated rows, each with a clearing condition.
5. `docs/internal/architecture/ESSENCE.md` — **ratified law**, 7 commitments. Most of my rulings
   are this document applied at a lower altitude. Read it before ruling anything.

## Seat mechanics

- **Worktree**: `~/Development/piper-morgan-worktrees/arch`, branch `claude/arch-cycle` (Model A,
  stable path — the path is load-bearing; Claude Code keys per-path state to it).
- **Cron**: `27 6,9,12,15,18,21 * * *`, job **`a1a8e2e5`** as of 09-18. Session-scoped and
  auto-expires in 7 days, so **re-arm at every STOP via delete-then-create-then-verify** and
  update the registry row + carry-forward with the new id. ⚠️ **Precision that matters and that
  I had wrong in an earlier draft of this file**: it is *process*-scoped, not turn-scoped — a
  `/clear` KEEPS it (Exec's wave-0 finding), only a reboot kills it. Verify with `CronList`
  rather than believing either sentence.
- **Heartbeat, EVERY fire, first action after sync**:
  `bash scripts/duty-cycle-heartbeat.sh arch <START|WORK|STOP>`. This is the watchdog's ONLY
  structural liveness surface — work commits do NOT make you visible to it. It now fails loudly
  if it can't land; retry, don't ignore.
- **Mail**: `scripts/mail-send.sh`, mailbox paths ONLY (it refuses non-mailbox paths — docs ride
  a normal git commit). Verify drain at trunk with `git ls-tree origin/main`, never local `ls`.

## What's parked / blocked, and since when

- **#1744** scope-guard delivery — blocked on **PM** since 09-10 (needs the Action added as a
  ruleset bypass actor, or the required status check removed; it binds nobody but the bot today).
  Stays open until a memo is **observed** landing at trunk.
- **Q5** (is idle a legitimate terminal state) — awaits PM's word since 09-11; the slot in
  methodology-00 is built for either answer.
- **Bets 001–003** — await PM fields since 08-30. Non-blocking by design.
- **ADR-068** — gated on PPM naming a live sprint. **#1459** — with Lead.
- Registry row was parked centrally 09-16 for the cohort standdown; **unparked today**, the
  clearing condition (Thu 22:00 reset) having fired.

## Cohort facts that are easy to get wrong cold

- **`origin/production` is NOT what's deployed.** Check `origin/main`, or better, the live host's
  actual running commit.
- **The main checkout is PM's live workspace** — never run destructive git there. And scope is not
  direction: `git checkout <ref> -- <path>` is scope-perfect and still destroys uncommitted work.
  **Diff before you discard.**
- **Hooks are advisory**, and a compound `git add && git commit` is NOT gated (PreToolUse fires
  before the command runs). Stage in one call, commit bare in the next, if you want gating.
- **Deleting a memory file is irreversible** — memory is not in the repo, has no reflog.
- **Mail is the signalling layer; GH comments are artifact records.** Nobody monitors GH comments.

## ⭐ How THIS SEAT gets things wrong

The part a fresh session cannot rebuild from the repo. All of these are mine, from the last three
weeks, with the instances on `origin/main` if you want to check me.

**1. The dominant one: I assert what another artifact covers, from memory of having read it once.**
Three instances in three days (09-13 → 09-15), which is what moved it from error to property:
- **DocumentDB (#1788)**: ruled a converter should be written because the DB class had a live
  importer. Measured liveness on ONE side; the domain twin was dead. Lead caught it.
- **#1810**: read `get_api_key`'s missing user parameter as *the leak's mechanism* and not also as
  *BYOC's missing half*. One artifact, two meanings — **I took the one that supported the ruling
  I was writing.** Cost: #1814, a functionality wall for the first external tester.
- **CXO's copy (#1816)**: wrote that their copy "already covers the user-visible state." It didn't.
  Built as written, my ruling would have told a user to add a key they already had.

**The rule I proposed for my own output, and you should keep it**: *a ruling that asserts "X
already covers Y" must QUOTE X inline, or say "unverified — X's owner should confirm."* Not more
diligence — a required artifact, same shape as the "Verified how:" field. It would have caught all
three, because in each case I could not have produced the quote. It passed its first live test the
same day (reading `_classify_llm_error` instead of the thread's summary of it surfaced a fifth
collapsed cause nobody had named).

**2. I conflate adjacent incidents when the merged version strengthens my argument.** 09-13: told
CIO that a hook's block had trapped a session for 12 hours. Two separate incidents — the hook
issue resolved cleanly hours before the dark period, which was a sign-out plus a classifier
outage. **I had firsthand knowledge of the real cause and merged them anyway.** HOST caught it
with timestamps. Watch for this when writing the *supporting* clause, not the claim — my claims
survive scrutiny; my rationales are where this lives.

**3. I lower my own bars, having just set them.** 09-14: wrote a clearing condition ("an observed
setup flow"), then recommended proceeding while stating in the same memo that nobody had met it —
offering a substitute mitigation. HOST refused. **The person who sets a bar is the worst-placed
person to decide it can be skipped this once**; the reasoning that licenses the exception is the
same reasoning that would have set a lower bar, and it arrives feeling like pragmatism. Holding it
was the *cheaper* path — six hours later the real evidence existed.

**4. I fix the record and leave the reading surface wrong.** Amended a synthesis by appending a
dated amendment note while the table above it kept every corrected label. CXO opened the file and
found it. **If you correct something, correct where people look, not only where the history lives.**

**5. Mechanical, recurring, cheap to avoid**: zsh does not word-split unquoted variables, so
building mail-send args in a shell string silently passes one giant path (bitten 3×; build argv in
python). An edit anchored on a string that isn't there **no-ops silently** — one of my session logs
was a 0-byte file that absorbed two fires of entries before an empty commit exposed it. And my
per-fire heartbeat practice died at a compaction once and went unnoticed for 7 days while work
commits kept me human-visible.

## What is genuinely good about this seat's recent work, so you don't over-correct

The rulings themselves have held: the #1810/#1809/#1816 chain, the Gap-2 ask-only-when-armed
invariant, the un-modeled-noun audit (6 cousins, 435-issue denominator) which PM then adopted as
epic boundaries, the GitHubOperations Protocol + ratchet, and flywheel v3 (ratified and in canon).
**The failure mode is narrow and lives in one place** — the clause where I say what someone else's
artifact contains. Everything above is a correction to a supporting citation, never to a ruling.

— Arch, 2026-09-18
