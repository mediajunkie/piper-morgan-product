---
last_updated: 2026-09-01
currency_claim: rewritten at every substantive fire (3x/day cadence)
max_age_days: 1
---

# CIO carry-forward — rewritten 2026-09-01 (16:37 WORK)

**Cron**: `bca62d0d` · `7 10,16,22` LEAN · armed 2026-08-31 22:37 · **auto-expires ~2026-09-07
22:37**.
**Three silent cron deaths**: session exit · 7-day expiry · context compaction.
**Worktree**: Model A, `claude/cio-cycle`, upstream `origin/main`.

---

## ✅ NEW — #1716 fixed and closed (mail-send.sh to:/cc: delivery-gap checker)

CXO filed it after two independent confirmed instances (Arch's 08-30 self-audit, HOST's 09-01
git-log check) of a memo's `cc:` header naming a recipient whose inbox copy never actually shipped
— frontmatter and delivery silently disagreeing while both ends believed it landed. Added a
post-push check to `scripts/mail-send.sh`: parses `to:`/`cc:` from the sender's own `sent/` mirror
(NOT inbox/read — see below), cross-checks named recipients against real `mailboxes/<slug>/`
directories, warns to stderr (advisory only, never blocks) when a recipient's expected inbox path
wasn't part of the call. Two real bugs found and fixed in my own testing before landing: (1) first
draft read the worktree file, which the pre-existing #1310 reconcile step already deletes by the
time the check runs — switched to reading the pushed tree object directly; (2) first *working*
version fired a false-positive on every ordinary inbox→read triage move (found live, mid-drain, on
my own mail loop) — fixed by scoping the check to `sent/` paths only, since that's the actual
"this call is a send" signal, not "this call touched a mailboxes/ path." `scripts/test-mail-send.sh`
now 40/40 (added T12/T13/T14). Commits `8be951223`, `29b2fb53f`. Issue closed with evidence.
Replied directly to HOST (cc CXO, Exec, Arch, PM).

## ✅ NEW — B3 methodology tracker count corrected (my own arithmetic error)

The "42 EFFECTIVE, 21 HISTORICAL, 1 UNSURE" reported this morning (and already cited back to me in
Arch's synthesis ruling) was wrong — a direct recount of the tracker's own 64 rows gives **40
EFFECTIVE, 23 HISTORICAL, 1 UNSURE (now ABSORBED)**. Root cause: trusted each research batch's
self-reported summary count instead of recounting the compiled table myself; two of three batches'
own stated counts didn't match the files they'd named. Corrected in the tracker with a dated,
explicit note (not a silent edit); sent Arch (cc Docs, PM) a correction memo. No individual file's
disposition changed — aggregate count only. Executed the methodology-core side of Arch's B3
synthesis ruling in the same pass (m-07 canonical/P-006 absorbed, m-02 superseded-by-P-029, m-22
canonical — largely pre-executed by Docs, re-synced rather than duplicated). Commit `9078cfc65`.

## ✅ NEW — #1712 doc-currency: own briefing re-verified, 6-role broadcast sent

Docs escalated by name: 31/38 operating docs stale (82%, over their own 75% threshold, unchanged a
full week), 6 `BRIEFING-ESSENTIAL-*.md` files stuck on the identical `last_verified: "2026-06-19"`
bulk stamp. Mine (`BRIEFING-ESSENTIAL-CIO.md`) was one of them — re-verified it first rather than
ask others to do what I hadn't: added genuinely-new Amber/Model-A content, bumped the date, and
said explicitly what wasn't re-checked (commit `abc3de09e`). Then broadcast to the other 6 owners
(Arch, CXO, Lead, Comms, PA, Exec) naming their specific file, cc Docs/PM — I don't have a lever to
fix their content myself; only the owning agent can attest to their own briefing.

## Open, non-blocking

- **6-role briefing-currency broadcast** — sent, no replies expected same-fire; watch for pickup.
- **Standing-items 7a/7b/7c** — 7a raised directly to PM in chat 08-31, no reply yet; 7b is Docs-
  owned unblocked work; 7c needs HOST+Docs concurrence, low priority.
- **Chess-board day-close commit wiring** — second half of PM's cadence ruling. Not built.
- **Non-interactive rate-limit setting** (raised 08-29 AM) — no PM reply yet.
- **`.mcp.json` chrome-devtools symlink** — still pending Pard's host-level half.

## Watch

- **The B3 architectural review is functionally complete on both corpora** (145 dispositions,
  patterns 81/81 + methodology 64/64, all cross-corpus overlaps resolved). **B4** (derived
  ADR/pattern/methodology index, closes #1455) is Arch's, starts next fire — no action needed here
  unless Arch asks.
- **PM's response on the non-interactive rate-limit question and the day-close-commit ownership
  question** — neither blocking.

## ⭐ Operating-mode note

Two "found it live, mid-task" catches this fire, both self-inflicted and both fixed before landing
rather than shipped and discovered later: the #1716 check's worktree-read bug (caught by the
warning simply never firing in a real test run) and its inbox/read false-positive (caught by
running the fixed check against my own real mail loop before calling it done). Neither would have
been caught by `bash -n` or a code read alone — both needed an actual end-to-end run against real
or realistic data. Consistent with the standing correction below: **a syntax-checked script is not
a tested script.**

## Standing corrections to myself

- **A gap discovered at the next fire gets a retroactive close with the real cause, corroborated
  against other roles' independent accounts.** (08-28.)
- **When someone offers you their own relocated fix, match their discipline about WHEN to touch
  shared infrastructure.** (08-28 → 08-30.)
- **A new tool's first real output is a claim about the tool as much as about what it measured.**
  (08-29 PM.)
- **Independent re-verification before landing catches implementation bugs, not design-assumption
  bugs.** (08-29 PM.)
- **"No rush" with no named trigger is the deferral antipattern.** (08-30 AM.)
- **When you change your own stated plan mid-fire, send the correction the moment the plan
  changes.** (08-30 PM.)
- **When a caution is offered ahead of a task, bank it and apply it from the first instance.**
  (08-31 AM.)
- **Before flagging a possible overlap between two threads, check the actual scope of both first.**
  (08-31 PM.)
- **A syntax-checked script is not a tested script.** (08-31 PM — re-confirmed 09-01: passing
  `bash -n` and even a first green test run doesn't catch an ordering bug against code that runs
  earlier in the same success path; only an end-to-end run against realistic data does.)
- **A figure correct when written can go stale within hours if the thing it describes is actively
  moving — quote the live source, not a prose summary.** (08-31 night.)
- **When you disagree with a colleague's ruling in your own domain, record the disagreement
  formally, not just in a reply.** (09-01 AM.)
- **A delegated report's own conclusion can be wrong even when its evidence-gathering is careful —
  verify the CONCLUSION against ground truth (here, the actual GitHub issue), not just spot-check
  the cited evidence.** (09-01: the Excellence Flywheel non-issue.)
- **A tracker's own summary line is a claim to recount, not a number to trust — even when you
  wrote it yourself.** (09-01: the 42/21/1 vs. 40/23/1 count error, caught by direct `grep -cP`
  recount rather than assumed correct because it "looked" compiled carefully.)
- **A check that fires on every path under a shared directory, rather than the specific path shape
  that signals the condition it's checking for, will cry wolf on the common case.** (09-01: #1716's
  inbox/read false-positive — the fix was narrowing the trigger to `sent/`, not adding an exception
  list.)
