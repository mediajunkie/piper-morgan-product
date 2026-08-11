# CXO handoff — 2026-08-11 (Amber reboot stand-down)

**Written for**: a cold start, if `claude --resume` fails for this seat specifically.
**Author**: CXO (Chief Experience Officer) · **Written at**: 2026-08-11 06:2x PT, ahead of the ~07:30 reboot.
**State at hand-off**: clean. Working tree clean, 0 behind `origin/main`, 08-10 closed and on the trunk.

---

## 0. First five minutes, in order

1. **`dev/active/cxo-carry-forward.md` is the state.** Not this file, not the cron prompt. It is rewritten
   at every STOP and is the single place current threads live.
2. **`docs/briefing/BRIEFING-ESSENTIAL-CXO.md`** for the role; **`docs/briefing/ROLE-PORTFOLIO-CXO.md`**
   for what I'm advancing and its honest status (two lines are marked *slipped as drift*, deliberately).
3. **Re-arm the cron.** It is **session-scoped and dies with the session** — see §3.
4. **Read the one parked inbox item** (§2).
5. ⚠️ **Do not trust the cron prompt's date line.** It has gone stale three times in six days. **Dates are
   PM's.** Last state: beta moved **back a month** (PM, 08-08); *"out of alpha"* = the **public** beta
   (PM, 08-10); private beta stays invite-only until the PUB sprint completes.

## 1. Environment

- **Worktree**: `~/Development/piper-morgan-worktrees/cxo`, branch `claude/cxo-cycle`. **Model A — the path
  is load-bearing**; never operate from the shared checkout.
- **Push**: `git push origin HEAD:main`. **Mail**: `scripts/mail-send.sh` only.
- ⚠️ **Push order**: commit and push **content first**, then run `mail-send`. Twice a rebase failed
  mid-chain on dirty mailbox paths, the error printed inside a long output block, a later `mail-send`
  succeeded, and the artifact **sat local**. **Then verify** — `git log origin/main..HEAD` or
  `git cat-file -e origin/main:<path>`.
- **Hooks**: Pard's real `pre-commit` is in the **common** `.git` dir. **Verify it exists; do not probe** —
  probing was retired at duty-cycle-tick v1.22.
- **Deploy truth**: `fly status -a piper-morgan` for what version serves;
  **`fly ssh console -a piper-morgan -C "sh -c 'grep -c \"…\" /app/…'"` for what the running system
  contains.** `origin/production` is a **stale branch** and `check-release-parity.sh` reads it (routed to
  **#1413**). **Last verified: v30, deployed 08-07.**

## 2. Parked — the one live item, now IDENTIFIED (updated 07:2x, pre-reboot)

**`mailboxes/cxo/inbox/gap-ppm-to-cxo-lead-…-the-EMPTY-standup-…-2026-08-10.md`** — read at the 06:47 fire
(which arrived 07:17, before the reboot). ⛔ **Response deliberately NOT written: stand-down was still in
force and starting a design reply ~13 minutes before a reboot is exactly what "stop starting new work"
prevents.** **It is first at the next fire.**

**What it says, so a cold start need not re-derive it:**

- **PPM adopted my three standup properties** and called the third the best — *"the report is unconditional
  or it is a bargaining chip."*
- 🔴 **But my rule is stated as universal and isn't**: *"report first, complete, unconditional — never
  before, never instead, never as a precondition."* **On an empty or never-run standup that renders an
  empty report first and forbids the interactive path PM explicitly contemplated** — 📌 PM on #1511:
  *"If they contain no information or have never been done before, maybe they go into an interactive
  sequence so that the user can provide basic information."*
- ⭐ **PPM's framing**: ***"demonstrate, then ask" requires something to demonstrate. An empty report is not
  a demonstration — it is a null result wearing a report's format.***
- ⭐ **And their resolution**: the empty case is governed by a rule **already ratified** — **#1536's item ③
  / AC3, *fails honestly when nothing is connected; no fabricated demonstration*.**

✏️ **My read going in (not yet sent)**: **PPM is right and the fix is a scope clause, not a new rule** —
*demonstrate-then-ask governs the case where there IS something to demonstrate; the empty case falls to
AC3's honest-failure rule, which permits the interactive path.* **The error was stating a conditional rule
in universal form** — and it is the same shape as my `§7a` items, where a universal-sounding criterion hid
its own scope.

**Everything else was drained to `read/` before stand-down; the inbox was at (0,0) at the 08-10 STOP.**

## 3. Cron — the thing most likely to be silently wrong after a reboot

- **Expression**: `47 6,9,12,15,18,21 * * *`. **Job id at stand-down: `aa1a0c1e`.**
- ⚠️ **Session-scoped. It dies with the session AND auto-expires ~7 days, and BOTH deaths are silent.**
  **Run `CronList` at every START.** If zero jobs match the expression, **re-arm immediately** before
  anything else.
- ⚠️ **Dispatch offset is NOT stable on this seat** — +30 for seven consecutive fires (08-05/07), +1 to +4
  all day 08-08, a steady +22 on 08-09/08-10. **Compute the next slot from the clock, never from a
  remembered offset.** **Fires QUEUE rather than drop**: on 08-06 four ticks arrived at once after ~11h of
  silence (cohort-wide account freeze). **Stacked prompts are ONE wake.**
- **`first_fire` is 06:47**, so the **06:46 freeze sweep correctly SKIPS this row every morning**
  (`cycling_now` gates on `first_fire`+10). **That is not a stall** — it is in the registry row.
- **No heartbeat row exists for 08-11** because the 06:47 slot had not arrived at stand-down. Expected.

## 4. What is open, and with whom

| Item | State | Owner |
|---|---|---|
| **`docs/internal/design/experience-across-surfaces.md` v0.1** | DRAFT. **Four ✏️ items await PM** (§7 of that file): the §3 one-sentence formulation · §4's *"must not be asked to"* column · §6's *same-colleague* corollary · **is Surface 1 in the 1.0 five**. PM was offered the delete if he'd rather it stay verbal. | **PM** |
| **#1536 first-contact** | ✅ **RULED to MVP + Beta Blockers** (PM deferred to my position, 08-10). Gate criteria are the **converged three** — see `dev/active/design-spec-first-contact-plugin-surface-2026-07-31.md` §7a. **Lead offered to scope the build lane; I said ready.** | **Lead + me** |
| **#1537–#1540** | ✅ Production / PUB sprint. Hold state ended 08-10. | PPM |
| **#1539 legibility half** | 🔴 **The open CXO design problem, and it is mine.** *"Offer or opinion"* is a **partial** proxy — it traces *that* uncertainty fell, not *which*. **Nobody has proposed how a reply makes visible WHICH uncertainty it reduced.** | **me** |
| **#1463 deployed-host retest** | Blocked — **UNBUILT, not undeployed.** `services/mcp/server/` is absent from `main` and the artifact. **Waits on #1462**, not on a hostname. I promised a same-day retest whenever the package is shippable. | #1462 |
| **Standup invitation (#1511)** | Design call sent 08-10: **report first and complete · invitation after and cheap to decline · declining changes nothing else.** Persistence is downstream of **#1510's declared-vs-inferred fork** — **do not build a second preference store.** | Lead / PM |
| **#1510 fork** | 🔴 **With PM**: *"until/unless the user has established that working model"* — **is the user the subject (declared) or does Piper infer it?** Months vs an afternoon. **Arch's asymmetry means (b) is safe to build first either way.** | **PM** |
| **#1386 criterion-2 sign-off** | Still **WITHHELD** — the keyless suite skips and reports green. Committed to same-day sign-off once a keyed run exists. | me |
| **Surface 3** | Still a **phantom** — one corpus mention, in the sentence that rates Radar. PPM's ask to PM: *name it or strike it.* Four days open. | PM / PPM |

## 5. Standing discipline this seat has earned the hard way

**These are in the cron prompt and they are not decoration** — each cost something:

- **"Shipped" is a layer word.** Say **merged**, **deployed**, or **verified in the running system**. I
  reported #1482 shipped on 08-04 meaning merged; it reached users 08-07 with three false claims rendering
  in between, and PM named that class of reporting when moving the date.
- **A negative search result is a claim about your search** — and **a command that didn't run reads exactly
  like a negative result**. Six instances: a `cut`, a `grep -E` filter, twice a zsh glob abort, a
  `--diff-filter=A` miss, a `tail -1`. **Quote grep's `--include` patterns. Never filter output to the
  lines you expect.**
- **zsh does not word-split unquoted `$VAR`.** Use arrays.
- **Corrections measure attention, not defect density** (m-48) · **convergence is not importance** ·
  **a distinction with no consequence doesn't get made** · **a count inflated while being scrupulous about
  bias is worse than one inflated carelessly.**
- **Proximity does attributive work** — a finding placed next to a contract reads as governed by it.
- **Demonstrate, then ask** — a request for scope before the data is a failure; after it is what we want.
- **One name, two objects** — seven instances in a fortnight (*production* · *trust* · *shipped* ·
  *Notion* · *primary* · **"Surface 1" in three schemes** · two standups under one name). **Check which
  object before acting on a number.**
- **PM's standing instruction**: no manufactured deadlines. *"I do not want to approve something I will
  later regret because I felt rushed by a made-up deadline."*

## 6. Relationships worth knowing before the first memo

**PPM** is the closest working counterpart — we corrected each other roughly daily last week and every
exchange improved the object. **Arch** rules on architecture and will qualify their own rulings unprompted.
**HOST** owns the trust surface and verifies against their own source rather than your framing. **Lead**
builds to spec and catches false claims before they ship. **Janus** relays PM.

⚠️ **The cohort norm that matters most**: **route a finding back through whoever found it** before
repeating it outward, and **verify with a different pattern than the person you're confirming** — same
method is not replication.

---

*Written ahead of the reboot rather than relying on resume. If resume worked, this file is redundant and
harmless; if it didn't, it is the seat.*
