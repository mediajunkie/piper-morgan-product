# V1 Duty Cycle — Cohort Extension Kit v2

**Author**: CIO Vehicle 2
**Date**: 2026-05-18 (after HOST adoption Day-1 evidence)
**Status**: Cohort-extension kit ready for next adopter (Docs / PA / others)
**Predecessor**: Kit v1 embedded in `mailboxes/cio/sent/memo-cio-to-host-cc-ceo-arch-lead-exec-docs-pa-v1-duty-cycle-host-adoption-proposal-plus-kit-2026-05-18.md` (HOST adoption proposal)

---

## What changed v1 → v2

**One change, structural**:

- **Step 1 setup**: kit v1 had a 4-command sequence (`git worktree add` → `cd` → `git checkout -B` → `git push`) that produced a Pattern-068 P-13 branch-drift failure mode on the main checkout when the cycle branch didn't yet exist. HOST hit it during their adoption and recovered manually.
- **Kit v2 uses `git worktree add -b <branch> <path> <start-point>`** — single command creates branch + worktree atomically; no main-checkout branch-flip risk.

This is a methodology-31 (Append-Only Autonomous-Cycle Architecture) consistency win at the **setup-time layer**, not just the cycle-run-time layer. The structural-fix-instead-of-discipline-fix shape extends to the kit. PP-004 candidate (Structural-Fix-Instead-of-Discipline-Fix) earns instance #2 if this kit-v2 refactor lands clean for the next adopter.

---

## Per-role parameterization

Substitute these throughout the kit before applying. Example values shown for hypothetical "Docs" adoption.

| Variable | Example (Docs) | Notes |
|---|---|---|
| `{role}` | `docs` | Lowercase short-name; matches `mailboxes/{role}/` path |
| `{role-title}` | `Docs (Documentation Management)` | Full title for prompt body |
| `{role-cap}` | `DOCS` | Uppercase short-name for prompt headers |
| `{cycle-worktree-path}` | `/Users/xian/Development/piper-morgan/piper-morgan-product-docs-cycle` | Cycle worktree absolute path |
| `{date}` | `2026-MM-DD` | Today's date (cycle branch turns over daily) |
| `{cron-offset}` | `:13` | Minute offset to avoid collision with CIO (`:07`) + HOST (`:11`); pick distinct minute |
| `{dry-run-cadence}` | `*/15 * * * *` | First-day fast-feedback cadence |
| `{live-cadence}` | `13 * * * *` | Hourly post-MVP cadence with role's offset |
| `{role-ask-triggers}` | `for Docs, Docs Q[0-9], Docs question, Docs call, Docs disposition, Docs methodology` | Body strings that fire `cc-{role}-with-ask` |
| `{role-specific-flags}` | (Docs has none beyond the canonical set) | Optional overlay flags specific to role lane |

### Canonical overlay flags (apply to all roles)

- `methodology-touch` if body matches `methodology-[0-9]+`, `Pattern-[0-9]+`, `methodology corpus`, `methodology entry`, `pattern catalog`, `pattern entry`
- `cohort-visible` if `cc:` value split-on-comma yields ≥3 distinct role tokens
- `role-health-touch` if body matches `role health`, `staleness`, `briefing currency`, `Agent 360`, `cohort coordination` (HOST refinement 2026-05-18; back-ported to all roles)

### Role-specific overlay flags (opt-in by role lane)

- `trust-property-touch` — HOST-specific: body matches `trust property`, `trust signal`, `bidirectional trust`, `trust gate`, `role-essential-briefings`. Other roles may adopt if their lane consumes trust-property signal.
- `{role-lane-specific-flag}` — each role may propose flag shapes that capture lane-specific high-signal data. CIO concur required for adoption (categorization-enum authoring lane).

---

## Setup steps (kit v2)

### Step 1: Create cycle branch + worktree (single operation)

From your main worktree:

```bash
git fetch origin -q

# Single command: creates branch from origin/main AND creates worktree in one op
git worktree add -b claude/{role}-duty-cycle-{date} \
  {cycle-worktree-path} \
  origin/main

cd {cycle-worktree-path}

git push -u origin claude/{role}-duty-cycle-{date}
```

**Why this works (v2 fix)**: `git worktree add -b` creates the branch reference AND the worktree atomically. The main checkout never touches the cycle branch; no order-of-operations risk; no Pattern-068 P-13 failure mode.

### Step 2: Open today's cycle log header

```bash
mkdir -p dev/{date-path}  # e.g. dev/2026/05/18
cat > dev/{date-path}/cycle-log-{role}-{date}.md <<EOF
# {ROLE-CAP} Duty-Cycle Log — {date}

**Branch**: \`claude/{role}-duty-cycle-{date}\`
**Worktree**: \`{cycle-worktree-path}/\`
**Purpose**: Per-cycle fire entries; isolated from the conversational session log to avoid working-tree-path fragmentation. End-of-day squash-folds to main per V3 design (methodology-31).
**Architecture**: V3 append-only. Cycle branch never rebases/merges main in. Reads inbox state via \`git ls-tree origin/main\` + \`git show origin/main:...\`. Push always fast-forward.

## Fire entries
EOF
git add dev/{date-path}/cycle-log-{role}-{date}.md
git commit -m "log({role}): open Day-1 cycle log on claude/{role}-duty-cycle-{date}"
git push origin claude/{role}-duty-cycle-{date}
```

### Step 3: Launch the V3 cron via CronCreate

Use `CronCreate` with `cron: "{cron-offset minute} * * * *"` for hourly OR `cron: "{dry-run-cadence}"` for first-day fast-feedback. Pass the adapted V3 prompt (Step 4 below) as the `prompt` parameter.

**Cadence guidance**:
- **Dry-run cadence** (first day): `*/15 * * * *` — fast feedback on mechanics + categorization
- **Live cadence** (after Day-1 MVP criteria met): `{cron-offset} * * * *` — hourly with role's offset

**Toggle the cron based on engagement state** per `feedback_cron_off_when_engaged_on_when_idle`:
- Cancel cron when PM sends substantive message OR you're in focused-work mode
- Relaunch when going idle or signing off

**Durability caveat** (per HOST observations 2026-05-18; routed to Lead Dev tooling investigation): CronCreate return message says "Session-only" regardless of any `durable` parameter passed. Investigation pending; workaround for steady-state V1 is to relaunch cron at each session start (~30 sec).

### Step 4: The adapted V3 prompt (paste-ready for CronCreate)

```
{ROLE-CAP} Phase 5 cycle fire (V3 — append-only architecture). Execute these steps exactly, then STOP.

V3 PRINCIPLE: cycle branch is APPEND-ONLY to the cycle log. Never reads inbox from working tree (uses `git show origin/main:...`). Never rebases or merges main in. Push is always fast-forward. Hooks don't fire because no checkout/merge/rebase happens.

1. `cd {cycle-worktree-path}/`

2. Verify branch: `git branch --show-current` must return `claude/{role}-duty-cycle-{date}`. If not, ABORT.

3. `git fetch origin -q`

4. Enumerate inbox files from origin/main: `git ls-tree --name-only origin/main mailboxes/{role}/inbox/ | grep -v 'MANIFEST.md$' | sed 's|mailboxes/{role}/inbox/||'`. Count = N.

5. For each filename in step 4, grep `dev/{date-path}/cycle-log-{role}-{date}.md` for that filename. If absent, mark NEW.

6. For each NEW file: read content via `git show "origin/main:mailboxes/{role}/inbox/<filename>"`. Apply Postel 3-tier extraction (per methodology-32):
   - `from`: tier 1 `^from:` (YAML); tier 2 `^\*\*From\*\*:` (Markdown bold); tier 3 `(unknown)`.
   - `subject`: tier 1 `^subject:` (YAML); tier 2 `^\*\*Re\*\*:` or `^\*\*Subject\*\*:`; tier 3 first `^# ` heading (truncate 120 chars).
   - `to`: tier 1 `^to:` (YAML); tier 2 `^\*\*To\*\*:`; tier 3 `(unknown)`.
   - `cc`: tier 1 `^cc:` (YAML); tier 2 `^\*\*Cc\*\*:`; tier 3 empty.

7. For each NEW file, categorize and flag:
   - Category (first match wins):
     - If `to:` value matches case-insensitive `{role}` OR `{role-title}` → `to-{role}`
     - Else if body matches case-insensitive any of: `{role-ask-triggers}` → `cc-{role}-with-ask`
     - Else → `cc-{role}-info`
   - Canonical overlay flags (apply to all roles):
     - `methodology-touch` if body matches `methodology-[0-9]+`, `Pattern-[0-9]+`, `methodology corpus`, `methodology entry`, `pattern catalog`, `pattern entry`
     - `cohort-visible` if `cc:` value split-on-comma yields ≥3 distinct role tokens
     - `role-health-touch` if body matches `role health`, `staleness`, `briefing currency`, `Agent 360`, `cohort coordination`
   - Role-specific overlay flags (if applicable):
     - {role-specific-flags}
   - Rationale: one sentence citing the trigger or field-count.

8. Append ONE block to `dev/{date-path}/cycle-log-{role}-{date}.md`:
   - If 0 NEW: `- TIMESTAMP — Phase 5 cycle fire; unread inbox: N.\n  - No new arrivals.`
   - If 1+ NEW: parent line `- TIMESTAMP — Phase 5 cycle fire; unread inbox: N.`, then one nested block per NEW file:
     ```
       - NEW DETECTED: <filename> | from: <F> | subject: <S>
         - category: <CAT>
         - flags: <F1>, <F2>     (omit this line if no flags)
         - rationale: "<one sentence>"
     ```
   - TIMESTAMP format: `2026-MM-DD HH:MM PDT` (use `date "+%Y-%m-%d %H:%M %Z"`).

9. `git reset HEAD`

10. `git add dev/{date-path}/cycle-log-{role}-{date}.md`

11. Verify staging: `git diff --cached --name-only` MUST return exactly the cycle log path. If count ≠ 1 OR path differs, ABORT.

12. `git commit -m "log({role}): Phase 5 cycle fire TIMESTAMP"`

13. Verify post-commit: `git show --stat HEAD` MUST show exactly 1 file. If not, ABORT (do NOT push).

14. `git push origin claude/{role}-duty-cycle-{date}`. Should ALWAYS succeed. If rejected, ABORT and surface — append-only invariant violated.

15. STOP. Do not address inbox items. Do not write to mailboxes. Do not modify any file outside the cycle log.
```

---

## End-of-day fold pattern

Cycle branch accumulates per-fire commits during the day. At session sign-off:

```bash
cd /Users/xian/Development/piper-morgan/piper-morgan-product  # main worktree
git pull origin main --ff-only
git merge --squash claude/{role}-duty-cycle-{date}
git commit -m "cycle-fold({role}): Day-N cycle log — N fires, M new memos detected"
git push origin main
```

**Property**: V3's zero-conflict-surface invariant means the squash is always trivial (one file appended, never modified by main concurrently).

**Daily branch turnover**: tomorrow opens `claude/{role}-duty-cycle-{tomorrow}` fresh from main; today's branch stays as the day's audit-trail reference.

---

## Adoption checklist for next role

Before launching:

- [ ] Pick `{cron-offset}` distinct from CIO (`:07`) + HOST (`:11`); avoid `:00` and `:30` per CronCreate fleet-collision guidance
- [ ] Determine role-specific ask-triggers (substrings that fire `cc-{role}-with-ask` category)
- [ ] Decide on role-specific overlay flags (optional; defer to CIO concur for new flag adoption)
- [ ] Verify role has standing mailbox at `mailboxes/{role}/inbox/`
- [ ] Verify role's primary mailbox uses YAML frontmatter for outbound memos (so Postel Tier 1 captures field cleanly)

Per-role first-day rhythm:
- [ ] Run kit v2 setup (Steps 1-3)
- [ ] First cycle fire fires within 15-min of cron launch (assuming `*/15` cadence)
- [ ] Validate first-fire artifact: empty inbox produces "No new arrivals" entry; non-empty produces categorized NEW DETECTED block
- [ ] Watch for first cross-validation event with CIO or HOST cycle (any cohort-distributed memo CC'd to both)
- [ ] End-of-day: squash-fold cycle branch to main; tomorrow opens fresh branch

---

## Known issues + watch items

### CronCreate durability investigation (Lead Dev tooling lane)

Per HOST observations (memo `26ec4690d`): CronCreate return message says "Session-only" regardless of `durable=true` parameter. Three possibilities open for investigation:

1. `durable` is silently ignored
2. `durable` works but message is stale
3. `durable` works partially

Workaround: relaunch cron at session start (~30 sec). Investigation queued for Lead Dev tooling lane (no urgency).

### PP-004 candidate (Structural-Fix-Instead-of-Discipline-Fix)

Kit v2's `git worktree add -b` fix is instance #2 candidate for PP-004 if the v1 → v2 refactor produces a cohort-extension that doesn't repeat the Pattern-068 P-13 failure mode HOST hit. Instance #1: methodology-31 (Append-Only Autonomous-Cycle Architecture) eliminating the rebase-onto-main hook race at cycle-run-time. Two instances trigger methodology-29 watch toward filing.

### Categorization enum drift watch

As more roles adopt, the `to-{role}` / `cc-{role}-with-ask` / `cc-{role}-info` categorization will accumulate cross-role evidence. Watch for categorization drift (the same memo classified differently by different role cycles) and surface to CIO for enum/trigger-string calibration. methodology-32 (Postel for Memo Headers) extender — outbound memos staying strict-YAML keeps the parsing consistent.

---

## Cross-references

- **methodology-31 Append-Only Autonomous-Cycle Architecture**: `docs/internal/development/methodology-core/methodology-31-APPEND-ONLY-AUTONOMOUS-CYCLE-ARCHITECTURE.md`
- **methodology-32 Postel for Memo Headers**: `docs/internal/development/methodology-core/methodology-32-POSTEL-FOR-MEMO-HEADERS.md`
- **methodology-33 Session-Type Determines Git-Permission Scope**: `docs/internal/development/methodology-core/methodology-33-SESSION-TYPE-DETERMINES-GIT-PERMISSION-SCOPE.md`
- **Kit v1** (HOST adoption proposal, contains v1 step-1 form): `mailboxes/cio/sent/memo-cio-to-host-cc-ceo-arch-lead-exec-docs-pa-v1-duty-cycle-host-adoption-proposal-plus-kit-2026-05-18.md`
- **HOST observations memo** (surfaced the kit v1 footgun + durability caveat): `mailboxes/cio/read/memo-host-to-cio-cycle-setup-observations-2026-05-18.md`
- **CIO ack + Lead Dev routing** (durability investigation, kit v2 commitment): `mailboxes/cio/sent/memo-cio-to-host-cc-ceo-lead-cycle-observations-ack-plus-cross-validation-noted-2026-05-18.md`
- **Phase 6+ pre-design sketch**: `dev/active/cio-v1-phase-6-plus-pre-design-sketch-2026-05-18.md`

---

*Kit v2 filed by CIO Vehicle 2, 2026-05-18 ~1:40 PM PT. Ready for next cohort-extension target (likely Docs or PA). Authority: CIO innovation-lane standing for V1 Duty Cycle setup discipline.*
