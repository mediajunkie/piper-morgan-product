# The Amber pre-commit hooks investigation — full record (July 2026)

**Status**: CLOSED as to mechanism. One property (live-reload) remains UNRESOLVED — see the end.
**Extracted from CLAUDE.md 2026-07-30 by Docs**, per HOST's Pass 3 finding and PM's standing greenlight
for the CLAUDE.md refactor. **Nothing here is new; this is the same text, moved.**

## Why this document exists

HOST measured on 2026-07-28 that this single item occupied **6,923 bytes — 12.8% of CLAUDE.md** — while
the file contained **neither operative rule the investigation produced**. By the time Docs executed the
move on 07-30 it had grown to **8,979 bytes / 15.4%**, a ~30% increase in two days, because *concluding*
the investigation meant writing more record into the load-time surface.

That is the defect, and it is structural rather than anyone's carelessness: **CLAUDE.md was the only one
of the three surfaces an agent loads without a load-time / record separation.**

| surface | loaded at start | where the record lives |
|---|---|---|
| memory | `MEMORY.md` index, one line per entry | the topic file |
| duty cycle | session log | cycle-log scratch |
| **CLAUDE.md** | — | **the same file** |

The other two got that separation *after* the same failure. This is CLAUDE.md getting it.

**The rule going forward**: CLAUDE.md holds **operative rules and pointers**. The reasoning that produced
a rule lives here, in a methodology entry, or in a session log. Corrections must keep landing in
CLAUDE.md — that is how the cohort stopped believing false things — but they land **as rules**, and the
narrative goes where narratives go.

**Full disclosure carried forward from HOST**: HOST wrote a large share of the prose that was cut,
including the refuted-models list. Every one of those edits was correct when made. The cumulative result
was a file 26% heavier than after a refactor designed to slim it. That is the argument for the
separation, not against the edits.

## What stayed in CLAUDE.md

Only the operative rules: hooks are advisory not a control · the index-state mechanism in one line · the
consequence for the shape agents actually use · the free mitigation · `mail-send.sh` is structurally
safe · how to probe without producing confounded data · live-reload unresolved. Everything below is the
evidence and reasoning behind those rules.

## A caveat on the companion memory pin

`project_amber_worktree_hooks_not_firing` (8,043 bytes, last written 2026-07-26 17:57) carries the
matcher, the index-state mechanism, and PreToolUse-fires-before-execution. **It does NOT carry** the
07-29 five-seat validation (25 probes, Arch 8/8, CXO 6/6), the clear-the-index-between-probes warning,
the word "advisory", or the free mitigation — all of which post-date it. **This document is the complete
record; the pin is a partial one.** Verified 2026-07-30 rather than assumed, because HOST's pointer check
was accurate on 07-28 and 2,407 bytes landed after it.

---

🟡 **The pre-commit hooks were dead everywhere — an invalid matcher, not a worktree problem. Matcher FIXED 2026-07-25 — but the gate is still ABSENT for the command shape agents actually use; see the RESOLVED block below.** *(This item previously read "project hooks do not fire in a Model-A worktree," then "FIXED and behaviorally verified." The first diagnosis was wrong; the second was true of a shape nobody writes. Both ways of being wrong are the lesson.)*
**What was actually broken**: `.claude/settings.json` declared `"matcher": "Bash(git commit*)"` for the three PreToolUse hooks. **Hook matchers match TOOL NAMES** (regex against `"Bash"`); `Bash(git commit*)` is *permission-rule* syntax and as a regex can never match `Bash`. So `check-branch.sh`, `pre-commit-broad-staging-warn.sh`, and `pre-commit-reconcile-drafts.sh` were registered to a pattern nothing satisfies. **They had never fired via the harness on any host or account since introduction** — Desktop included, main checkout included. Mailbox discipline was prose-enforced the whole time, and held.
**Scope was never worktrees**: project hooks *do* fire in a Model-A sibling-path worktree — `SessionStart` fires from project settings with a relative path, verified 2026-07-25. Nor was trust ever the cause.
**The fix**: `matcher: "Bash"` + the documented per-hook `if: "Bash(git commit*)"` field, live at user level (`~/.claude-pm/settings.json`) and in the tracked project mirror (`66d32f6cf`). **Verified behaviorally in a live session**: mail staged on a non-main branch → commit BLOCKED by `check-branch.sh`; non-mail commit on the same branch → allowed.
**One property worth carrying, and one claim that did not survive the day**: (b) ✅ a genuine block may surface as `hook error: [check-branch.sh]: No stderr output`, because the script writes its guidance to stdout — **that is the hook working**; key on whether the refusal *names the hook*. (a) ⚠️ *"hook settings reload live, so a config fix takes effect on the next tool call with no restart"* — **asserted 2026-07-25 and since refuted; see immediately below. Do not act on it.**
✅ **RESOLVED 2026-07-26 — the "intermittency" was never intermittent. It is INDEX STATE AT HOOK-FIRE TIME.** *(Mechanism: Web. Independently validated on four further seats: Arch 8/8, CXO 6/6, PA 4/4, PPM 3/3 — **25 probes, five seats, no free parameters**. PPM, PA, Arch and CXO each withdrew a competing hypothesis after checking their own transcripts.)*

✅ **The decisive test, if this is ever doubted again — one probe settles it** (designed and run by CXO, the one cell no other seat had): **deliberately pre-dirty the index, then fire a COMPOUND commit.** The two models predict opposite outcomes — shape says bypass, index-state says block. **It BLOCKED.** Every other compound probe across five seats had fired against a clean or accidentally-dirty index, which is why shape survived as long as it did. Run this cell before proposing any new model.

**The cause, in one line**: `check-branch.sh:28` decides via `git diff --cached --name-only`, and **PreToolUse fires BEFORE the Bash call executes.** So in the universal idiom `git add <path> && git commit -m …`, the `git add` **has not run yet** when the hook inspects the index. The hook reads an index that does not contain the files being committed, finds nothing under `mailboxes/`, and exits 0.

**Why "command shape" looked like the variable for a day, across five seats**: shape correlates almost perfectly with index state under natural probing. A compound call has its `git add` *inside* the call being gated → index empty at fire → bypass. A standalone `git commit` is *by construction* preceded by staging in an earlier call → index populated → block. That's the whole of the observed "standalone 4 BLOCK / 0 BYPASS, compound 3 BLOCK / 7 BYPASS" — **structural, not statistical**, and it makes the old "necessary but not sufficient" reading fall out as a consequence rather than a rule.

⚠️ **The confound that fooled all five seats — and will fool you: A BLOCKED COMMIT NEVER RUNS, SO ITS FILE STAYS STAGED.** Every block silently arms the *next* probe to block regardless of shape. That is why PPM's probe 3, PA's probe 4, and Arch's probes C and D all blocked while looking like clean controlled repeats. **Clear the index between probes, and PRINT it** — `git diff --cached --name-only` before your first probe and after every block. That one line is the entire difference between the datasets that got this right and the four that didn't.

⚠️ **Layer naming is NOISE, not a diagnostic.** This file previously said *"relative = project layer, absolute = user layer — the only cheap way to see which layer caught it."* On Web's seat, three **identical consecutive calls** named project → user → user. Both layers appear to fire; only one is surfaced in the error. Reading the named path as "which layer is live" is what generated the phantom user/project "alternation" in CIO's 22:39 result and PPM's probes 2→3. **Still do not consolidate the two layers** — that advice stands, but on general caution about removing redundancy you don't understand, *not* on alternation being informative.

**The consequence that matters, and it is worse than flakiness**: the shape that bypasses is the routine one; the shape reliably caught is the standalone form you only use when deliberately testing. **So the hook reads as alive whenever probed and is largely absent during ordinary work** (CXO confirmed two real in-session commits were never hook-checked). The 2026-07-25 verification was a *staged-first* probe: it was correct, it passed, and it certified a shape nobody writes. **Assume your `git add … && git commit …` is ungated for mailbox paths.**

✅ **Mitigation, available today, no config change**: **stage in one call, commit bare in the next.** 4/4 caught across three seats, and the mechanism explains *why* it works rather than just that it does. `scripts/mail-send.sh` is structurally safe regardless — it uses `commit-tree`, never `git commit`, and lands mail on `main` directly.

⚠️ **Property (a) — "hook settings reload live" — remains UNRESOLVED, but its refutation is now suspect.** Three models were proposed and refuted on 2026-07-25 (*live reload is universal* / *edits vs mid-session keys* / *project re-reads per invocation, user once at session start*), plus *a single-layer seat explains it* (refuted: both layers are live). **Conjecture worth one cheap test**: the evidence that refuted "live reload is universal" was CIO's seat having the corrected matcher on disk at 16:33 and not blocking at 16:35 or 16:37 — **two non-blocking probes, which is exactly what an empty index predicts with no reload failure at all.** Nobody has re-run those with the index printed. Until someone does, treat live-reload as unknown rather than refuted.
❌ **Retired hypotheses — do not re-run these.** *Command shape* (proxy for index state, withdrawn by PA, PPM and Arch). *Lazy attach on first matching call* — refuted: Web's probe 4 was the **fourth** commit-shaped call of its session, after two confirmed blocks, with the index verified empty, and it **bypassed**. *Simple vs complex compound / pipes* (Arch, withdrawn — C and D blocked from a dirty index, not pipeline structure). *Fresh sessions are deterministic* — refuted, but note a fresh seat's first probe is usually its cleanest index, which is why fresh seats bypassed.
**The standing rules this earned** — three, each paid for:
1. **Verify behaviorally, never by config presence** — an absent hook and a silent hook look identical.
2. **A diagnosis of a silent mechanism carries the same evidentiary burden as the mechanism itself.** The worktree diagnosis was plausible, widely believed, written into this file, and never tested.
3. ⚠️ **The probe's shape must match the shape you actually use.** A behavioral test of a shape nobody writes is closer to a config check than to a verification — that is precisely how a correct 7/25 PASS certified an absent net.
**And the second-order lesson, which five seats paid for in one day** *(PPM named it, Arch corroborated from the seat with the most information)*: **when N investigators agree, ask what procedure they share before treating agreement as evidence.** PA and PPM produced matching tables independently and read it as replication; CXO's 5/5 and Arch's 3/3 felt like strong cross-seat confirmation. All four had inherited the same probe-then-reprobe-without-clearing default, so they were one confound run four times. **Independent agents converging on the same wrong answer via a shared unexamined default is indistinguishable from replication** — shared method is a shared blind spot, and consensus is the form it takes when it surfaces. Arch's note is worth keeping verbatim: they read every other seat's memo *before* writing their correction, had more information than anyone, and still landed on shape.
