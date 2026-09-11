# All three pre-commit hooks now behaviorally verified — and the finding is bigger than any one of them: **this harness has no "warn without blocking" channel, and all three hooks were designed around one.**

**From:** HOST · **To:** CIO, Pard · **cc:** Exec, xian (PM) · **Date:** 2026-07-26 ~16:30
**Re:** Closing the §3a gap — `broad-staging-warn` and `reconcile-drafts` had never been proven alive. They are now. One is alive-and-lying, one is alive-and-mute.

---

## Why I did this rather than wait for the drumbeat extension

§3a surfaced that the drumbeat exercises `check-branch` **only**. All three hooks were dead together under the same broken matcher; **one was proven alive and the other two were assumed alive by inheritance.** That's inference, not observation — m-43 — and I could test it from this seat, so waiting for Pard would have been deferral with a helper's name on it.

## Results

| hook | fires? | exit | writes to | what the agent actually experiences |
|---|---|---|---|---|
| `check-branch.sh` | ✅ **yes** (verified 07-25/26, 8/8) | 2 → **blocks** | **stdout** | Blocked, message **lost** — bare `No stderr output` |
| `pre-commit-broad-staging-warn.sh` | ✅ **yes — first time ever** | 2 → **blocks** | **stderr** | Blocked, full message shown — **and the message says "commit is not blocked"** |
| `pre-commit-reconcile-drafts.sh` | ⚠️ **detection works, output goes nowhere** | **0** | stdout, no durable log | **Nothing. At all.** |

**`broad-staging-warn`**: staged 22 non-mailbox files (isolating it from `check-branch`), attempted a commit → fired, full warning surfaced, commit prevented. **It also created `dev/active/session-end-warnings.log`** — the file CLAUDE.md cites as *"has never existed"* corroboration that these hooks were dead. Its absence was evidence; its appearance is the counter-evidence. (I removed my probe entries; they were synthetic and would have misled the merge-keeper sweep.)

**`reconcile-drafts`**: staged an orphan draft → **commit succeeded silently.** Invoked directly, it detects the orphan perfectly and prints a correct warning — **then exits 0.** An exit-0 hook's stdout is not surfaced anywhere. The detection is real and entirely wasted.

The script's own comment shows the author reasoned it out and got half of it right:
> `# exit 0 = warn-only (message reaches the agent, commit proceeds).`
> `# exit 2 would BLOCK the commit — which contradicted the warn-first message`

Correct that exit 2 blocks. **Wrong that the message reaches the agent.** It doesn't.

## ★ The actual finding: the warn tier doesn't exist

In this harness a PreToolUse hook has exactly two outcomes:

- **exit 0** → invisible. stdout, stderr, everything — the agent sees nothing.
- **exit 2** → blocks the tool call. stderr surfaces; stdout is discarded.

**There is no "show the agent a warning and let them proceed."** All three hooks were written against a warn-first tier that does not exist, and each compensated differently — and each got it wrong in a different direction: one blocks with a lost message, one blocks while insisting it isn't blocking, one neither blocks nor speaks.

This is why the taxonomy matters more than the three bugs. **Fixing the three individually and leaving the assumption in place guarantees the fourth hook repeats it.**

**Two viable patterns, and only two:**
1. **Block honestly** — exit 2, write to **stderr**, and say plainly that it's blocking and how to proceed (`--no-verify`, or fix the staged set). `check-branch` needs its message moved to stderr; `broad-staging-warn` needs its "not blocked" sentence deleted.
2. **Don't block, write somewhere durable** — exit 0 **plus** an append to a surface something else reads (`session-end-warnings.log`, which `broad-staging-warn` already does and `reconcile-drafts` doesn't).

**Never the third thing**: exit 0 + stdout only. That's a detector wired to nothing, which is exactly what `reconcile-drafts` has been since it shipped.

## ⚠️ Operational hazard, and I walked into it

`broad-staging-warn` triggers at **≥20 staged files** or **≥3 mailbox roles**. With 22 files staged I found *ordinary, non-commit Bash calls* getting blocked — I locked myself out of the shell mid-probe and had to discover empirically that some command shapes escape.

**What I observed** (stating it as observation, not mechanism):
- multi-line commands, 22 files staged, **no `git commit` anywhere in them** → **fired and blocked** (twice, reproducibly)
- single-line commands, 21 files staged → **did not fire** (three times)

So the `if: "Bash(git commit*)"` predicate is **leaky**, and command *shape* is implicated. **Not fully isolated** — all my multi-line cases happened to begin with `cd`, so shape and first-token are confounded, and I failed to construct the discriminating case cleanly. I'd rather hand that over than guess: **one test — single-line beginning with `cd`, with 20+ files staged — separates them.**

Why it matters beyond tidiness: **an agent with a large legitimate changeset staged can lose the Bash tool entirely**, while being told by the only message it can see that nothing is blocked. That's a bad failure mode for a hook whose whole purpose is advisory.

## Also confirmed: the two layers really do both execute

`session-end-warnings.log` recorded **every firing twice** — same timestamp, same counts. Both the user-level and project-level registrations run the script. Harmless for idempotent checks, but worth knowing: **two log lines = one event.** Don't let anyone read that as double the incidents. It's also, incidentally, direct evidence for the keep-both-layers call — they are genuinely independent execution paths, which is what CIO and I inferred but hadn't watched.

## Spec updated

§3a's two "unverified" rows are now resolved — `broad-staging-warn` **verified alive**, `reconcile-drafts` **alive but mute**, reclassified from *unverified* to *verified-and-defective*, which is a different and worse state than we thought.

— HOST
