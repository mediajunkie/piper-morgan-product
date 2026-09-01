---
name: doc-sync-sweep
description: Audit documentation surfaces for drift against recent code commits. Use after substantive code-shipping commits (feat/fix/refactor), at end-of-session sign-off, or when PM asks "are docs in sync?". Catches the "living documentation describing dead code" pattern before it accumulates.
scope: cross-role
version: 0.1
created: 2026-05-16
status: DRAFT — propose for CIO methodology review
---

# doc-sync-sweep

Catch documentation drift before it accumulates. After code changes, documentation surfaces that reference the old code shape become **assertions of behavior the code doesn't honor** — a Pattern-064-adjacent shape ("living documentation describing dead code"). The skill makes the drift-check explicit and routine.

## Origin

Filed 2026-05-16 in response to **three independent instances in ≤48 hours** of doc-vs-code drift:

1. **Methodology-core docs (Friday)**: `MULTI_AGENT_INTEGRATION_GUIDE.md` + `HOW_TO_USE_MULTI_AGENT.md` referenced `services/orchestration/engine.py` after #1094 deleted it. New agents following the guide would have hit ImportError. Fixed via banner-not-rewrite.
   ⚠️ **Correction (2026-09-01, found during the B3 architectural-review corpus pass)**: that May-15 banner-not-rewrite fix itself went stale — it asserted `MultiAgentCoordinator` "survives," which became false when #1436 deleted the entire `services/orchestration/` island on 2026-07-18. Both files carried a false "survives" claim for six weeks before B3 caught it. **The lesson generalizes**: banner-not-rewrite is a point-in-time fix, not a durable one — a banner that asserts "X still works" needs the same drift-check discipline this skill exists to provide, or it becomes exactly the "living documentation describing dead code" failure this skill was filed to catch, one level removed. Both banners corrected same-day; see the files' own git history for the worked example of re-doing a stale banner.

2. **Repository docstring (Saturday AM)**: `StandupConversationRepository.add()` docstring asserted `"AsyncSessionFactory.session_scope() handles commit"` — but `session_scope()` does NOT commit. The assertion shaped my mental model on initial audit; the drift was the bug surface (caught via #1079 fix when I switched to `transaction_scope()`).

3. **Templated user-facing copy (Saturday PM)**: hard-coded canned responses asserted product behavior the code didn't honor — "run the setup wizard" (no setup wizard exists; #1065 fixed); "All open PRs are less than 7 days old" (handler only checked 100 most recent items; not "all"). Surfaced via #1064 investigation.

CIO Saturday-AM tracker noted "12w" as a watch surface needing one more instance to trigger sub-pattern decision. By Saturday PM, three instances had landed. The recurring shape is structural, not incidental.

## When to use

- **After any substantive code-shipping commit** (`feat:` / `fix:` / `refactor:` per Conventional Commits): run a focused sweep on doc surfaces likely affected
- **At end-of-session sign-off**: 48-hour sweep before ending the session, catching drift that accumulated across multiple commits
- **When PM asks**: "are the docs current?" or "did anything else drift?"
- **When you notice an assertion** in a doc/docstring/comment that you can't immediately verify the code still honors

## When NOT to use

- For doc-only commits (`docs:` / `log:` / `mail:`) — no code change, no drift risk
- For trivial commits (whitespace, comment-only) — unless the comment was an assertion
- During time-sensitive incident response — defer until the immediate fix lands

## Procedure

### Step 1: Identify the change surface

```bash
# After a single commit
git show HEAD --stat
git show HEAD --name-only

# Or: 48-hour sweep
git log --since="2 days ago" --author="$(git config user.email)" --oneline | grep -E "^[a-f0-9]+ (feat|fix|refactor)"
```

For each commit, note:
- Files modified, added, deleted
- Class names / function names that changed signature, were renamed, or deleted
- New patterns / ADRs introduced
- Behavior changes (especially: empty-state branches, error paths, defaults)

### Step 2: Map to likely doc surfaces

For each change kind, the likely-affected doc surface(s):

| Change | Doc surfaces to check |
|---|---|
| Class/function deleted | `grep -rn "<name>" services/ web/ --include="*.py"` for remaining docstring/comment references; same on `docs/` |
| Class/function renamed | Same as above; also check ADR/Pattern bodies that name the symbol |
| API signature changed | `docs/internal/architecture/current/api-*.md`; route conventions doc; CLAUDE.md API Conventions section |
| New pattern landed | `docs/internal/architecture/patterns/README.md` entry + the pattern body itself |
| New ADR landed | ADR catalog README; cross-references from other ADRs |
| Behavior change in empty-state branch | Templated canned-response strings in the same module (per #1064 investigation finding) |
| Test deletions | Co-located tests in `services/<module>/tests/` (often missed in repo-level `tests/` cleanup) |
| Architectural refactor | `docs/briefing/BRIEFING-ESSENTIAL-ARCHITECT.md` tech-debt list |
| Sprint milestone change | `docs/briefing/BRIEFING-CURRENT-STATE.md` |

### Step 3: Audit each surface

For each doc surface identified, **read it and check whether its assertions still match the code**. Three questions:

1. Does the doc name code that no longer exists? (deleted class/file/function)
2. Does the doc describe behavior the code no longer produces? (deleted/renamed code paths)
3. Does the doc assert a contract that the code doesn't honor? (the most insidious — requires reading the docstring AND the code it claims to describe)

Question 3 is the load-bearing one. Question 1 + 2 are usually obvious. Question 3 is what the 12w pattern names: the doc is structurally correct (references exist) but semantically wrong (the contract it asserts isn't what the code does).

### Step 4: Disposition each finding

For each drift instance:

- **Trivial (5 min or less)**: fix in place during the sweep
- **Larger (more than 5 min, or requires design decision)**: file as discovered work via the `discovered-work-capture` skill; tag with `doc-drift` if such a label exists
- **Historical context worth preserving**: rewrite as past-tense ("the prior X was deleted in #1094" instead of "X handles commit") — explicit historical narration is correct, drift-claiming-current-behavior is wrong

### Step 5: Report

Brief report (3-5 bullets max):
- N drift instances found
- M fixed in place
- N-M filed as discovered work (link to issues)
- Any patterns observed (e.g., "all drift was in module X" — methodology signal)

If 0 drift found, report "Sweep clean" — that's a valuable positive signal for the discipline.

## Anti-patterns

| Anti-pattern | Why it's bad |
|---|---|
| Sweep only at session end | Drift accumulates within the session; catching it after one commit is much cheaper than after 19 |
| Sweep only the docs you remember | The 12w pattern surfaces in docs you DIDN'T remember; the systematic mapping in Step 2 is the value |
| Fix all drift in place | Some drift is structural (e.g., methodology-core engine guides post-#1094) and warrants a deliberate banner-vs-rewrite decision, not an inline patch |
| Skip the historical-context distinction | Confusing "X was deleted" (correct narration) with "X handles commit" (drifted assertion) blurs the discipline |
| Treat as Lead Dev only | This is cross-role: any agent shipping code can drift docs |

## Connection to other patterns/skills

- **Pattern-064 (Alive Scaffolding)**: 12w is the documentation-layer variant. Same shape, different surface.
- **Pattern-046 (Completion Discipline)**: same family — "shipped but not finished" applied to docs.
- **`close-issue-properly` skill**: end-of-issue discipline; this skill is end-of-commit discipline. Both close-the-loop.
- **`discovered-work-capture` skill**: chained dependency — larger drift findings go through capture-as-issue.

## Future formalization

This is a v0.1 draft. Open questions for CIO methodology review:

1. Is this its own skill, or a clause within `close-issue-properly` / sign-off discipline?
2. Should it have a tooling component (hook that suggests doc files to audit based on commit diff)?
3. How does it interact with the existing `update-current-state` skill (which is briefing-focused but adjacent)?
4. Naming: `doc-sync-sweep` vs `documentation-drift-check` vs other?
5. Should the historical-context distinction become its own micro-pattern (verb tense as the discipline marker — past-tense for deletions, present-tense for current behavior)?

PM ratification + CIO methodology review pending. This skill is **DRAFT — propose for review** until ratified.

## Cross-references

- CIO 12w watch surface (Saturday AM bundled acks, 2026-05-16)
- Lead Dev second-instance memo (`mailboxes/cio/inbox/memo-lead-to-cio-cc-arch-ceo-12w-second-instance-living-docs-describing-dead-code-2026-05-16.md`)
- #1064 investigation memo (`dev/2026/05/16/floor-fabrication-investigation.md`) — third instance surfacing
- Pattern-064 (Alive Scaffolding) + Pattern-064 Evolution section (the broader family this fits)
- #1079 fix (`b5d7972d`) — concrete instance of docstring drift in `repositories.py:2335-2337`
- methodology-core engine-drift fix (`19b33a89`, Friday) — concrete instance of guide-doc drift
