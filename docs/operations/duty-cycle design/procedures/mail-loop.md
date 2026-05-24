# Mail Loop — procedure

**Purpose**: detect new mail; triage into the task list; clear inbox. Inner-most loop of the WORK flywheel.

**Entered from**: WORK PARTS step 2 (Run flywheel), as the first half of the flywheel.

**Exits to**: Task Loop (when mail loop terminates with empty inbox).

---

## Steps

1. **Sync**
   - `git fetch origin -q`
   - Optionally sweep other agents' branches if PM-flagged-for-this-pass (compensates for strict-per-memo-commit-push gaps)

2. **Check mail**
   - Enumerate inbox files on origin/main: `git ls-tree --name-only origin/main mailboxes/{role}/inbox/ | grep -v 'MANIFEST.md$'`
   - If no new mail since last check, **end loop** (transition to Task Loop)

3. **Read mail**
   - For each new memo: Postel 3-tier extract `from / subject / to / cc / response-requested` per methodology-32
   - Tier 1: YAML frontmatter (case-insensitive keys)
   - Tier 2: Markdown bold headers (`^\*\*From\*\*:` etc.)
   - Tier 3: fallback (unknown / first H1 / empty)

4. **Sort + clear inbox**
   - Classify each new memo:
     - **Task: unblocked** → add to task list (Doc 2)
     - **Task: need-input** → add to task list with blocker note + capture to attention doc (Doc 3) if it needs PM input
     - **Informational** → acknowledge mentally + move to `read/`
     - **CC visibility-only** → move to `read/`
   - Apply triage 4-category Gate disposition per CLAUDE.md (RESPOND / MOVE-TO-READ / DEFER / DEFER-FOR-REPLY-IN-THIS-SESSION)
   - Move processed memos to `mailboxes/{role}/read/` (mailbox writes commit to main per hook-enforced discipline)

5. **Update task list**
   - Prioritize new tasks against existing task list
   - Use judgment based on familiar criteria: sprint position, blocker status, role-lane priorities, deadlines-as-triage-tools
   - "Respond ASAP" memory: tasks tied to to-{role} memos with response-requested should rank high regardless of stated cadence

6. **Loop back to step 1**
   - Re-sync and check again in case new mail arrived during steps 3-5
   - Terminates when step 2 finds steady state (no new mail)

---

## Termination

- Steady state at step 2 (no new mail) → exit to Task Loop
- Hard-abort on any error (don't silently swallow; surface to attention doc)

## Cross-references

- v0.5 design (Mail Loop content): `docs/operations/duty-cycle design/duty-cycle-design-v0.4.md` (carried into v0.5)
- methodology-32 (Postel for Memo Headers): `docs/internal/development/methodology-core/methodology-32-POSTEL-FOR-MEMO-HEADERS.md`
- Task list doc: `dev/active/{role}-standing-items.md` (reframed under v0.5 architecture)
- Attention doc: `dev/active/duty-cycle-escalations-{role}.md` (reframed under v0.5 architecture)
- CLAUDE.md mailbox-discipline norms (per-memo commit-push; mailbox-on-main; 4-category Gate disposition)
