# Handoff — Chief Architect (arch) — 2026-08-11 stand-down

**Written for**: the Amber reboot (~07:30 PT, macOS 26.6). Session is expected to `--resume` intact; **this document assumes it does not.** Written to be survivable from a cold start.

**Seat**: `~/Development/piper-morgan-worktrees/arch` (Model A, stable path — **the path is load-bearing**; Claude Code keys per-path state) · branch `claude/arch-cycle` · pushes go `HEAD:main`.

---

## 1. 🔴 FIRST THING AFTER RESUME — the cron is dead and nothing re-arms it

**My duty cycle runs on the harness's session-scoped `CronCreate`. It does not survive the reboot, and no mechanism restores it.** *(This is the gap I raised on Pard's stand-down runbook on 08-05 and re-raised twice; as of last night it is still open.)*

```
Re-arm:   cron expr  27 6,9,12,15,18,21   (6×/day)
Verify:   CronList → EXACTLY ONE job
Then:     update my row in dev/active/duty-cycle-registry.tsv with the new job id
```
**Last armed**: `679e5b66` at the 08-10 STOP, auto-expiring ~2026-08-17. **That job is gone after the reboot.**
⚠️ **A fleet that comes back with no crons looks exactly like a healthy fleet** — sessions present, panes foreground, census matching — and never wakes. **Phase 6 verifies sessions; what died is schedules.**

⚠️ **My registry row is NOT parked.** I judged the resume window too short to park-and-unpark, and parking without unparking is its own hazard. **If I am still dark past ~2 fires (≈09:27, 12:27), park it** — a correct alert nobody can act on spends the belt's credibility.

## 2. State at stand-down

| | |
|---|---|
| Yesterday's log | `dev/2026/08/10/2026-08-10-0631-arch-code-log.md` — **closed**, `DAY-CLOSED: 2026-08-10` |
| Working tree | clean at 08-10 STOP; sign-off verified 0 ahead / 0 behind |
| Inbox | **2 unread on the trunk, PARKED not processed** (per stand-down step 1). Neither is addressed to arch — both are cc: the mail-scanner variant chain (host/comms/cio) and CXO/Lead on three properties. **Read them first on resume**; verify with `git ls-tree origin/main -- mailboxes/arch/inbox/`, not `ls` (§5) |
| Nothing in flight | no half-finished ruling, no unsent memo, no uncommitted spec |

## 3. Live work — what I own and where it stands

**⭐ Floor-honesty contract (#1517)** — `docs/internal/architecture/current/floor-honesty-contract-1517-spec.md`
The one property: **an assertion about system state requires a read of that state; fabrication is asserting-without-reading.** H1 no unread state claims · H2 no retraction of a recorded success · H3 no denial of a registered capability (already built).
- ✅ **HOST signed off** (trust lens). ⏳ **CXO's copy lens is the one review still outstanding on my work.**
- **Half of #1517 was already built** before I specced it — the capability manifest. The **fabrication half** is unbuilt and is the **sixth instance** of a class solved five separate times elsewhere (plugins, #1484, places, todos, file search).
- ⛔ **Scope boundary in §4b**: it does **not** reach storefront copy. *If the enforcement doesn't transfer, the contract doesn't either — you cannot put a `StateFact` in a headline.*

**Understanding-Layer Inversion (Lead)** — RATIFIED with conditions, then **narrowed by me** after Lead's probe.
- Surface 1 **stays** where measured load-bearing (27+ of 52 rows); only the ~14 AGREE rows narrow, **each citing its probe row**.
- Conditions that must hold: **grammar = canonical actions derived from the registry** (not the 106 alias keys), and the **corpus gate is per-category, never aggregate**.
- Lead is building Phase 1. **Nothing is blocked on me.**

**Read/write boundary** — `EffectClass(IntEnum)` in `services/shared_types.py:344`, ordering asserted (dangerous pair) in `tests/test_architecture_enforcement.py`. Landed and green. **Done.**

**Release-train sketch** — `docs/internal/architecture/current/release-train-definition-sketch-2026-08-07.md`, 🟡 awaiting PM on four questions (Rule 1, `staging`, the promises column, the branch rename).

## 4. Owed TO me (do not chase; they are not blocked on me)

- **PM** — release-train's four questions; the declared-vs-inferred fork on trust.
- **CIO** — the **merge-aware hook** (asked three times). Highest-leverage unfixed item from the 08-08 incident.
- **CXO** — copy lens on the floor-honesty contract.

## 5. ⚠️ Seat-specific traps, all earned the expensive way

1. **Never glob the inbox.** `read/` is a **claim about my own cognition**; a bulk `mv` asserts it falsely. Drain iterates a list appended to **in the same call that displays a memo**. *(PM escalated this as a trust violation on 08-09; CIO adopted the fix cohort-wide.)*
2. **Verify at the trunk, not locally.** `git ls-tree origin/main -- mailboxes/arch/inbox/` — **never `ls`**. I once reported an empty inbox that was full on the surface everyone else reads.
3. **After any conflicted merge, before pushing**: `git diff <merge>^2 <merge> --stat` — **unfiltered, and `^2` not `^1`**. A `-D` filter misses reverts; `^1` shows zero. *(My merges once dropped 22 files / −1303 lines from main.)*
4. **`git restore --staged` during a merge DELETES incoming files** — and it is the broad-staging hook's own printed remedy. If mid-merge, a broad staged set is **expected**; conclude the merge.
5. **`git checkout <ref> -- <path>` is directional.** Scope discipline doesn't make it safe. **Diff both sides first** — I reverted a cured bug this way.
6. **Don't bundle state-changing setup with a command that can be refused.** A blocked PreToolUse call is *not* a no-op for what rode with it. Bit me three times.

## 6. Standing convention I adopted 08-10 — apply it to every ruling

**State the ruling's scope inside the ruling**: name the **object** (which artifact, not the concept), name **at least one thing it does not cover**, and if ratifying a document say **which clauses** — a ratified *direction* is not a ratified *sentence*.
**Why**: three over-readings this fortnight were a property of how I file, not reader error. CXO's diagnosis — ***"proximity does attributive work"***.

## 7. If resume fails and you are cold-starting me

Read, in order: `dev/active/arch-carry-forward.md` (env + hard rules + this convention) → `dev/active/arch-standing-items.md` (owed/gated) → the last three days of `dev/2026/08/*/…-arch-code-log.md`. **Then re-arm the cron (§1) before anything else.**

— Arch, 2026-08-11
