# V1 Duty Cycle — Phase 5 Prompt Design

**Author**: CIO (Vehicle 2, Code instance)
**Date**: 2026-05-17 ~6:35 PM PT (Sunday evening)
**Status**: Proposal — pending PM ratification before launch
**Predecessor**: Phase 4 v2 (Postel 3-tier extractor; mechanically validated across ~20 fires; cycle paused 10:49 PT)
**Successor**: Phase 6 — main-write surface (cycle updates escalations file)

---

## Lean (per PM concurrence on V1's recommendation)

Incremental extension of Phase 4 v2. **Do NOT redesign the cycle prompt from scratch.** Add ONE step after the existing detect step: read each newly-detected memo's body and categorize it. Log the category + a 1-sentence rationale alongside the existing `from` / `subject` extraction.

**Observation-only.** Phase 5 does not write to mailboxes, does not move files between inbox/read, does not file responses, does not update the escalations file. It only enriches the cycle-log entry with a categorization decision.

This validates that the cycle can "think about content, not just notice existence." It also surfaces categorization-rule edge cases before we trust the cycle with mutation decisions in Phase 6+.

---

## Categorization enum

Three primary categories (mutually exclusive — exactly one per new memo):

| Category | Meaning | Decision rule |
|---|---|---|
| `to-cio` | CIO in YAML `to:` field; explicit response action implied | YAML `to:` field contains "cio" / "CIO" / "Chief Innovation Officer" |
| `cc-cio-with-ask` | CIO in YAML `cc:` field BUT body contains a CIO-targeted question | YAML `cc:` includes CIO AND body contains "for CIO" / "CIO Q" / "CIO question" / "CIO call" / "CIO methodology" / "CIO disposition" |
| `cc-cio-info` | CIO in YAML `cc:` field; no CIO-specific question in body | Default for CC-only with no CIO-ask trigger string |

Two overlay flags (any combination, including none):

| Flag | Meaning | Decision rule |
|---|---|---|
| `methodology-touch` | Memo references methodology corpus or pattern catalog | Body matches `methodology-\d+` OR `Pattern-\d+` OR "methodology corpus" OR "pattern catalog" |
| `cohort-visible` | Memo CC'd to ≥3 distinct roles beyond `from:` and primary `to:` | Count distinct cc entries (split on `,`); flag if ≥3 |

**Rationale** (one sentence per memo): cite the trigger string OR field-count that drove the decision. Example: *"CC memo with explicit CIO Q4 on Janus field-name coordination"* or *"CC visibility memo; no CIO-targeted ask"*.

### Why this enum

Designed to be portable across roles, not CIO-specific. The categories make sense for HOST, Docs, Exec, Architect, Lead Dev with no change. That matters because:
1. PM directive: V1 hardened on one agent first, but extension demand is visible. The categorization enum should not lock in CIO-specific semantics.
2. Cross-agent reasoning becomes possible: once Phase 5 generates categorization data, the Day-N digest can surface "X memos categorized `to-cio` arrived today; you've acted on N of them."

Categories deliberately exclude action-shape categories (e.g., `respond-this-session`, `await-pm`). Action-shape decisions belong to Phase 7+ (live operation), not Phase 5 (observation).

---

## Phase 5 cycle log entry shape (proposed)

Per-fire entry:

```markdown
- 2026-05-17 HH:MM PDT — Phase 5 cycle fire; unread inbox: N.
  - NEW DETECTED: filename | from: F | subject: S
    - category: cc-cio-with-ask
    - flags: methodology-touch, cohort-visible
    - rationale: "CC memo with explicit CIO Q4 on Janus field-name coordination"
```

If no new arrivals:

```markdown
- 2026-05-17 HH:MM PDT — Phase 5 cycle fire; unread inbox: N.
  - No new arrivals.
```

Multiple new arrivals in one fire each get their own sub-block.

Backwards-compatible with Phase 4 v2 reader: same parent line, same NEW DETECTED format, just additional nested keys.

---

## Phase 5 prompt steps (extension of Phase 4 v2)

Steps unchanged from Phase 4 v2:
1. cd to cycle worktree (`/Users/xian/Development/piper-morgan/piper-morgan-product-cio-cycle/`)
2. Verify branch identity (`claude/cio-duty-cycle-2026-05-17`); ABORT if wrong
3. `git fetch origin -q && git pull --rebase origin main` (brings branch current with main)
4. Enumerate `ls mailboxes/cio/inbox/` (excluding `MANIFEST.md`); count = N
5. For each filename in inbox: grep for filename in `dev/2026/05/17/cycle-log-cio-2026-05-17.md` → if absent, it's a NEW memo
6. For each NEW memo: Postel 3-tier extract `from` + `subject` (YAML → Markdown bold → first H1)

**NEW STEP 6.5 — categorize:**
7. For each NEW memo (looping):
   - Re-read memo's YAML frontmatter for `to:` and `cc:` fields
   - Apply category decision rule: `to-cio` if "cio" in `to:`; else `cc-cio-with-ask` if any ask-trigger string in body; else `cc-cio-info`
   - Apply flag decision rules: scan body for methodology/pattern strings → `methodology-touch`; count cc entries → `cohort-visible` if ≥3
   - Compose 1-sentence rationale citing the trigger string OR field-count

Continuing:
8. Append cycle-log entry with category + flags + rationale per the new shape
9. `git reset HEAD` (clear any foreign-stage)
10. Stage explicit path (`git add dev/2026/05/17/cycle-log-cio-2026-05-17.md`); verify `git diff --cached --name-only` shows exact-1-file; ABORT on mismatch
11. Commit (`log(cio): Phase 5 cycle fire TIMESTAMP`); verify `git show --stat HEAD` shows exact-1-file; ABORT on mismatch
12. Push to branch (`git push origin claude/cio-duty-cycle-2026-05-17`); retry once via `git pull --rebase origin claude/cio-duty-cycle-2026-05-17` on rejection

Steps 1-5 + 8-12 are unchanged from Phase 4 v2. Only step 7 is new (+ categorization output added to step 8's entry shape).

---

## Edge cases to handle in prompt

| Edge case | Handling |
|---|---|
| YAML frontmatter missing (Markdown-header memo) | Use Postel Tier 2/3 for from/subject; for to:/cc: categorization, look for `^\*\*To\*\*:` / `^\*\*Cc\*\*:` lines; if both absent, default to `cc-cio-info` with rationale "no YAML to/cc fields found" |
| Empty body | Default to `cc-cio-info` with rationale "empty body" |
| Multiple ask-trigger strings (e.g., "CIO Q1" AND "CIO Q2") | Single category `cc-cio-with-ask`; rationale cites first match |
| Both `to:` and `cc:` contain CIO | Category = `to-cio` (most-action category wins) |
| Ambiguous trigger ("CIO touch-point" without Q#) | Treat as ask-trigger; rationale cites the phrase |

---

## Dry-run plan

1. **Manual fire validation** — feed Phase 5 prompt to the cycle session (or simulate via direct execution in the cycle worktree). With the inbox currently at 0 unread (all triaged), manual fire will produce "No new arrivals" entry. Confirms scaffolding doesn't break.
2. **Synthetic ping** — PM (or CIO via test-memo placement in cycle worktree only, then revert) creates one new memo in `mailboxes/cio/inbox/` matching each category. Phase 5 manual fire categorizes each. Verify the cycle log entry shape.
3. **Cron live** — `CronCreate` Phase 5 prompt at `*/5 * * * *` (or whatever cadence PM picks; 5min for fast feedback during dry-run is reasonable).
4. **Watch window** — let it run ~30-60 min with idle inbox. Cycle should fire ~6-12 times with "no new arrivals" entries. Validates no regression in Phase 4 v2 mechanics.
5. **Real-arrival validation** — wait for or generate a new memo. Phase 5 should categorize on first arrival, then idempotently skip on subsequent fires.

If dry-run is clean: Phase 5 is mechanically validated; design v0.5 absorbs lessons; standing for Phase 6.

If categorization is wrong on any real-arrival case: iterate the enum or trigger strings before claiming Phase 5 done.

---

## What this design IS NOT

- **NOT writing to mailboxes** — Phase 5 is observation-only. Inbox files are never modified. Categorization is recorded in the cycle log only.
- **NOT updating escalations file** — that's Phase 6 (main-write surface; needs branch-vs-main reconciliation design).
- **NOT acting on categorizations** — disposition memos, inbox triage moves, escalation filings all wait for Phase 7.
- **NOT changing Phase 4 v2 mechanics** — extension preserves what works; only adds the categorize step.

---

## Cross-references

- Design v0.4: `dev/active/cio-v1-duty-cycle-design-v0.4-2026-05-17.md`
- Phase 4 v2 entry shape (cycle log): `dev/2026/05/17/cycle-log-cio-2026-05-17.md` on `claude/cio-duty-cycle-2026-05-17`
- V1 handoff doc: `dev/2026/05/17/cio-handoff-2026-05-17.md`
- Day-1 reflection memo: `mailboxes/cio/sent/memo-cio-to-ceo-cc-arch-lead-host-exec-docs-pa-v1-duty-cycle-day-1-reflection-plus-v1-v2-transition-2026-05-17.md`
- Standing items: 12dd (this design), 12cc (reflection memo, done)

---

*Phase 5 prompt design v0.1. CIO Vehicle 2, 2026-05-17 ~6:35 PM PT.*
