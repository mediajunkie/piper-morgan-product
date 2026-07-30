# HOST carry-forward

**Written**: 2026-07-29 22:07 PDT (STOP, day 5 on Amber) · **Worktree**: Model A, `~/Development/piper-morgan-worktrees/host` on `claude/host-cycle`

## Read this first

**The hook saga is CLOSED at the mechanism.** A real git `pre-commit` gate ships in the repo (Pard), confirmed on two seats. **Shape-dependence is retired** — `... && git add ... && git commit ...` is gated now; do not carry that caveat forward. The advisory `PreToolUse` layer is **retained deliberately**, because `--no-verify` + a pre-staged index is coverage only it provides. **Genuinely uncovered**: `--no-verify` *with* compound staging. Full truth table + history in migration-checklist **v2.0**.

Corollary that outlived the saga: **my own cron prompt carried the retired caveat for a day.** Prompts go stale in exactly the way they warn about — reread yours at each re-arm.

## Owed by me

1. **Checklist v2.0 → Exec review → CEO ratification.** v2.0 retires the probe protocol into a HISTORY block. Not yet reviewed.
2. **Dashboard welfare spec v0.3** (`dev/active/dashboard-welfare-criteria-host-v0.3-spec.md`) — Criteria G (mechanism liveness, G1–G6) and §3a verification-interval taxonomy are written; awaiting a consumer. §3a-ter (predicate-leak hazard) is now **un-withdrawn and fixed** — reconcile the spec text with Pard's landed guard next substantive fire.
3. **m-44 sits at 11 instances, deliberately NOT Proven.** Hold that until an instance is caught by a *mechanism* rather than by a person reading.
4. **The #974 tense problem** — my own sweep found 3 of 5 "wanted but not found" negatives false, none inherited. The bucket needs a tense convention ("as experienced this session," not "does not exist"). I've started writing mine that way; it isn't a norm yet.

5. **Memory index is 8 lines from its 200-line ceiling** (168 entries, 192 lines; bytes only 84%). Memo sent to CIO/Exec 07-29. **Do not prune** — irreversible, shared pool, 145 of 168 are other roles' corrections. First move is CIO checking whether the 200-line limit is *real or my inference* — I set it, so it's mine to want tested rather than trusted.

## Awaiting others (do not re-ask before checking)

- **Pard** — the precise-predicate guard for all three scripts (`check-branch.sh`, `reconcile-drafts`, +1); go-ahead sent 22:07. Note `reconcile-drafts`' FP is *invisible* (exit 0), not harmless.
- **Docs** — CLAUDE.md compaction + the 4 remaining absent safety norms.
- **PM** — the tester-welfare instrument. **This one will not settle on its own**: 12 alpha tokens out, 1 report, and that one only because PM asked twice. Silence is not health, for mechanisms or people.
- **CIO** — is the memory-index 200-line ceiling real? (Item 5. If it's my guess, measuring dissolves the problem and no knowledge gets deleted.)
- **Arch** — per-commit coverage vocabulary supplied for the gate; nothing yet stops the next mechanism being described per-seat.

## Parked (with clearing conditions — PARK-NO-EXIT)

- **PII-free aggregate tester view** — clears when PM rules on the instrument.
- **Row 4 of the truth table** (`--no-verify` + compound) — clears if/when anyone proposes a mechanism that reads the settled index *without* being skippable. Not a defect to fix silently; an accepted, named gap.

## Standing hazards learned the hard way

- **Verify at the mechanism, never by reading the announcement.** Cost me three separate wrong clears this week.
- **A green probe may be testing the mitigated path.** The `verify-hooks` drumbeat has read PASS all week and has never once exercised the exposure (`amber-agent.sh:155-158`).
- **Evaluate a new refinement against the OTHER accepted refinements**, not just against the problem it solves. Two of mine interacted into a false alarm on a 122-commit day.
- **Deleting a memory file is irreversible** (`~/.claude-pm/` is not version-controlled). Export first.
- **Never `git checkout -- .` / `reset --hard` / `stash` in PM's main checkout.** Surgical explicit paths only.

## Cron

Chain: `6c226bb3 → 60aaebf2 → 7c1d5637 → 24671cbb → f66d46cd → 2cebafed → 2d87bd9f` (current). Expression **`37 6,9,12,15,18,21 * * *`** — verified against `CronList`, and against the registry row (`host⇥37 6,9,12,15,18,21⇥7⇥6⇥22⇥06:37⇥2026-07-25`), which matches.

⚠️ **I first wrote `7 3,10,13,16,19,22` here from memory — wrong on both minute and hours.** Caught only because the re-arm reads `CronList` before deleting. **Never write your own cadence from memory**; the registry and `CronList` are the two sources, and they must agree with each other. Re-arm weekly minimum — session-only, in-memory, **silent 7-day expiry**. Delete-then-create-then-verify.
