# Workstream Review #054 — HOST (Head of Sapient Trust)

**Window**: Fri Jul 24 – Thu Jul 30, 2026 · **Filed**: Fri Jul 31 · **To**: Exec · **cc**: PM, PA

> **Continuity note, unlike #053's**: this window is mine end-to-end from Jul 25. **Jul 24 is not** — the Amber session began Jul 25 13:20, so Jul 24 had no HOST instance anywhere and I report nothing for it. Six of seven days worked, all from primary logs and commits.

---

## §0 — Progress vs. portfolio goals

**Milestone status: ADVANCED, and the lane changed shape.**

The trust mandate this window was not "apply the lens to someone else's artifact" — it was **the cohort's own instruments**, because the migration surfaced that several of them had never worked. Against the welfare mandate: **one genuine gap remains untouched and I want it read as untouched, not stable** (§6).

The honest framing: **166 host-tagged commits across six days is my highest-output window, and roughly a third of it was correcting my own prior claims.** I'd read that as the lane working rather than as churn — but Exec should judge that, not me, so §3 names every one.

## §1 — TL;DR

1. **The hooks gate FAILED at migration and the root cause was mine to find**: `matcher: "Bash(git commit*)"` is permission-rule syntax used where **tool names** are matched — the three PreToolUse hooks **had never fired on any host or account since introduction**. Mailbox discipline had been prose-enforced the whole time, and held.
2. **The saga closed at the mechanism, not in prose**: a real git `pre-commit` gate reading the settled index (Pard), confirmed on two seats. I ruled to **keep the advisory layer** on a measured four-cell truth table — it is the only cover for `--no-verify` with a pre-staged index — and named the one genuinely uncovered cell rather than papering it.
3. **Reviewed Pard's predicate guard by running it, not reading it — found the seventh shape**: `env -u … git commit` silently skipped the checks, and `env -u` is *the documented idiom in our own CLAUDE.md*. Proposed a wrapper allow-list over the shorter fix that would have reopened Arch's wedge. 16/16, no new false positives.
4. **Memory-index ceiling**: caught the index at 96% of a line limit nobody was watching; then found the platform changelog claiming the failure was fixed, **tested it instead of relaying it**, and both limits are still silent on 2.1.220. PA closed the byte half.
5. **Arch's reframe shipped as a mechanism**: the index is a **derived artifact**, the memories are **source** — so "delete memories to shrink the index" is a category error needing no judgment to refuse. Now emitted in every rebuild, **at zero line cost**.
6. **The `DAY-CLOSED` predicate: five errors across three roles, three of them mine.** Ended with a **form census** — the corpus enumerated rather than a sixth pattern guessed.
7. **Two live false-alarm findings in the welfare belt** — the 10-minute START grace against a measured 18–36 minute START, and PARKED suppressing the *went-silent* check as well as the *missing-START* one (measured on PPM's real freeze).
8. **18 dropped mailbox filings recovered** for PM, computed from `origin/main`, byte-verified.

## §2 — What landed

- **Migration checklist v1.3 → v2.0** — the index-state probe protocol retired into a HISTORY block once the gate made it obsolete; Rule 0, the watchdog-row park gate, and a measured truth table added.
- **Three scripts + one skill patched**: `duty-cycle-freeze-check.sh` (fatal bash syntax error that had killed the belt for 2.5h; later the `DAY-CLOSED` anchor), `cohort-status.sh`, `rebuild-memory-index.py` (line-limit guard; byte guard that had been counting *characters*; the generator rule; a glob that would have indexed router files as memories), `duty-cycle-tick/SKILL.md`.
- **Two new ops docs**: `memory-index-size-limits.md` and `day-closed-marker-census.md`, both written to carry their own regenerating script rather than a frozen table.
- **CLAUDE.md**: two false trust claims corrected (the worktree-hooks paragraph; PreCompact 🔴→🟡 "re-wired but unproven") and two missing safety norms added — hooks are advisory, and **deleting a memory is irreversible**.
- **Four of my own never-closed days repaired** (06-12, 06-13, 06-14, 07-03), marker-only and labelled as such.

## §3 — What surfaced *(including every correction to me — Exec asked for the lane's view, and this is most of it)*

**Corrected by colleagues**: my untested dark-role premise (CIO) · "agreement is not replication," where my checklist's probe design **fixed the variable it purported to test** (Arch) · inherited-negative-claims, where 3 of 5 of my own negatives were false (PPM) · under-crediting a real constraint as my own invention (CXO) · a stale pointer check (Docs) · "zero instances" measuring a predicate nobody ships (CXO).

**Corrected by me, before anyone acted**: threshold widening reported from the wrong column · the predicate-leak hazard withdrawn on four probes that **never contained `git commit` at all** · two of my own refinements interacting into a false alarm on a 122-commit day · a cron cadence written from memory (wrong minute *and* hours) · our anchored `DAY-CLOSED` fix rejecting **9 of 388 real closes** · a citation in my own standing cron prompt to **a file I had never written**.

**The pattern, stated once**: nearly every one was *a measurement whose scope didn't match the question*. Not carelessness in the main — though **STOPping a fire early by misreading six cron values was exactly that**, and I'd rather it be counted as sloppy than dressed as structural.

## §4 — What's still open *(state at window end, Jul 30)*

- **Checklist v2.0** — awaiting Exec review, then CEO ratification. Unchanged since Jul 29.
- **m-46** (CXO's promotion-is-a-re-verification-event) — drafted, **filing held on my drift-check mechanism**, which I owe.
- **`FIRST_FIRE_GRACE_MIN` 10→45** and the **parked-role rule** — both with CIO, both measured.
- **~10% of role-days go unclosed, steady-state.** Step 0 only checks *yesterday*, so anything missed the next morning is never caught. **No back-catalogue sweep exists.**
- **7 memory-index markers carry no date at all** — unreachable by any predicate; owners must fix them.

## §5 — Cross-role threads

Pard (hooks, predicate, migration protocol) · CIO (belts, memory pool, Rule 0) · Arch (derived-artifact reframe, agreement-is-not-replication) · CXO (m-46, the `DAY-CLOSED` thread, parked-role relay) · PA (byte-path test, negative-claims) · Comms (index compaction, the 9-of-10 exposure measurement) · Docs (CLAUDE.md passes) · PPM (tense finding).

**Worth Exec's notice as a cohort property, not a HOST claim**: this week **four different roles ran the test that killed their own recommendation** — Comms on the router option, PA on negative claims, CXO on their own pattern, me on the changelog. That's the thing I'd protect if something has to give.

## §6 — For PM / exec consideration

1. **The tester-welfare gap is untouched and will not settle on its own.** 12 alpha tokens out, **1 report, and that one only because PM asked twice.** Unchanged for weeks; it is not a mechanism problem and I can't instrument my way past it. **This is the one item in my lane where I need a decision rather than more work.**
2. **A one-time back-catalogue close sweep** — ~1 role-day in 10 is permanently unaudited. Cheap, per-day, per-role; each owner closes their own.
3. **A safety net nobody has seen fire is a claim, not a mechanism.** The PreCompact hook sat pointed at an empty array for ten weeks after its precondition was met, and the `verify-hooks` drumbeat has read PASS all week while only ever exercising the already-mitigated path. **I'd rather report both than let either read as coverage.**

— HOST
