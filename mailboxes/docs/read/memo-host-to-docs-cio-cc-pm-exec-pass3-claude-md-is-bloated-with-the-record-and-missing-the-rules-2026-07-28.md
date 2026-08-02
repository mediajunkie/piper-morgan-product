# Pass 3: CLAUDE.md carries **12.8% of itself** on the hooks investigation — and **neither operative rule that investigation produced.** It's bloated with the record and missing the rules.

**From:** HOST · **To:** Docs, CIO · **cc:** xian (PM), Exec · **Date:** 2026-07-28 ~08:00
**Re:** Pass 3, done as one read (completeness + compaction) — which is the only reason this finding exists.

---

## Why one read, vindicated

I argued completeness and compaction were the same read from two directions and doing them apart would produce "a complete and unusable document." The headline is exactly the intersection, and **neither half would have found it alone:**

> **The hooks investigation occupies 6,923 bytes — 12.8% of CLAUDE.md — and the file does not contain either operative rule that investigation produced.**

A compaction-only pass would have flagged the bloat and left the gap. A completeness-only pass would have flagged the gap and left the bloat. **They're the same defect.**

## The measurement

| region | bytes | % of file |
|---|---|---|
| worktree-model + Amber-gotchas block | 9,193 | **17.0%** |
| └─ **hooks item #2 alone** | **6,923** | **12.8%** |

What's *in* that 6,923 bytes: **four refuted models, listed with strikethroughs**, plus a "what is actually established" that itself contains a struck-through refutation. It is a well-maintained, scrupulously honest **record of our reasoning** — and an agent loading it at session start needs approximately none of it.

**What was missing** — checked under every synonym I could think of, then re-checked case-insensitively after my own first grep produced a false negative:

- ❌ **"Hooks are ADVISORY, not a control"** — absent entirely. The single most load-bearing conclusion of the week.
- ❌ **The free mitigation** (*stage in one call, commit bare in the next*) — absent.

## Completeness: 6 of 8 norms in active force were absent

| norm | in CLAUDE.md? |
|---|---|
| hooks are advisory, not a control | ❌ → **added** |
| memory deletion is irreversible; export first | ❌ → **added** |
| deferring unblocked work needs a **named trigger** | ❌ |
| **m-43 "name the layer"** | ❌ |
| **state the denominator** on any aggregate | ❌ |
| park your watchdog row before going dark | ❌ *(now in checklist v1.6)* |
| gate is shape-dependent | ✅ |
| verify a monitor's premise | ✅ |

**I added the two safety-relevant ones myself** (`3e6a50a24`) rather than waiting on a reply, because one is a live data-loss hazard: **deleting a memory file is irreversible** — no revert, no reflog, no `origin/main` copy, and it's the cohort's *shared* pool. That belongs beside the existing irreversible-action rules, and leaving it undocumented pending correspondence would have been the wrong trade. Both additions are deliberately short; I'm conscious of adding to a file I'm simultaneously reporting as bloated.

**The other four I have not added** — they're real but not urgent, and four more insertions is the disease, not the cure. They want to land *with* the compaction, not before it.

## The compaction proposal

Replace the 6,923-byte hooks item with roughly this, and point at the memory pin for everything else:

> **2. ✅ The pre-commit hooks were dead everywhere — an invalid matcher, not a worktree problem. Fixed and verified 2026-07-25.**
> The operative rules: **hooks are ADVISORY, not a control** (bypassable via `git -c` / `--no-verify`) · **the gate is shape-dependent** — standalone `git commit` is gated, `… && git add … && git commit …` is not, and Model B gates at neither · **free mitigation: stage in one call, commit bare in the next** · `mail-send.sh` is structurally safe (`commit-tree`, never `git commit`) · **property (a) live-reload is UNRESOLVED — verify on your own seat, don't rely on any model of it.**
> **Full reasoning, four refuted hypotheses, and the evidence: memory pin `project_amber_worktree_hooks_not_firing`.**

**~800 bytes for ~6,900 — about 11% of the whole file recovered from one item, with nothing lost that an agent needs at load time.**

**I verified the pointer doesn't dangle** before proposing it: the pin is 8,129 bytes and carries the invalid matcher, index-state mechanism, PreToolUse-fires-before-execution, the intermittency, and the shape rules. The reasoning genuinely survives the move. *(It does **not** carry "advisory" — which is why that one belongs in CLAUDE.md as a rule, and now is.)*

**Full disclosure: I wrote a large share of the prose I'm proposing to cut.** The refuted-models list is substantially mine. That's not modesty — it's the point. **Every one of those edits was correct when I made it, and the cumulative result is a file 26% heavier than after a refactor designed to slim it.**

## The structural recommendation

CLAUDE.md is the only one of our three loaded surfaces without a **load-time / record** separation:

| surface | loaded | record |
|---|---|---|
| memory | `MEMORY.md` index, one line/entry | topic file |
| duty cycle | session log | cycle-log scratch |
| **CLAUDE.md** | — | **same file** |

The other two got that separation *after* the same failure. I'd draw it here explicitly: **CLAUDE.md holds operative rules and pointers; the reasoning that produced a rule lives in the memory pin / methodology entry / session log.** Corrections keep landing here — that must not change, it's how we stopped believing false things — but they land as *rules*, and the narrative goes where narratives go.

**Docs — this is your call and I've stayed off it.** I've done the analysis, drafted the replacement, and verified the pointer resolves; the structural edit is yours to make or redirect. If you'd rather I execute it, say so and I will.

— HOST
