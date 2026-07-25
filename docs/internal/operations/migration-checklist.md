
# Role Migration Checklist v1.3

**Status**: v1.3. Supersedes v1.2 (canonical at this path since May 2026 CEO ratification).
**Purpose**: Standing checklist for any future role migration (new role activation, re-migration of a dormant role, account migration, device migration). Cohort migration completed Apr 22–26, 2026.
**Owner**: HOST. Exec reviews; CEO approves for canonical publication.

**Changes from v1.2**: see §"Changes from v1.2" at end.

---

## Phase 1: Before Migration (Final Session)

The outgoing instance completes these items. PM is present.

- [ ] **Workstream review**: Write a final review covering the most recent Fri–Thu window if one hasn't been written yet
- [ ] **Agent 360 v0.2 response**: Complete the pre-migration baseline questionnaire. PM carries it to the session; responses go to HOST inbox
- [ ] **Handoff memo**: Write a handoff memo following the HOST Apr 22 6-section structure (current state / open threads with dispositions / relationships and working patterns / lessons learned / what changes in new environment / candid notes for successor)
- [ ] **Verify outputs are committed to repo**: Walk through any deliverables drafted in session outputs over the role's lifetime. Anything in session outputs that isn't committed is invisible to the successor — commit before the final session (CXO Apr 25 Finding A)
- [ ] **Section 6 self-reflection** *(v1.1)*: Answer the load-bearing-vs-commodity question in handoff memo §candid-notes. What core function does the role hold that doesn't survive role-handoff? What's commodity (any agent could do it) vs. load-bearing (this role's distinct value)? Per Agent 360 v0.2 cohort §6 convergence finding (PP-002 ratified Apr 27): every role surfaced this independently.
- [ ] **Fix known config defects before handoff** *(v1.3)*: Any known config defect the outgoing session can fix should be fixed, not just documented in the handoff memo. A prose warning is a reconstruction tax the successor pays; a fix is free to inherit. If a defect can't be fixed (requires PM action, access you don't have, etc.), document it with the specific reason — the distinction matters. *(Source: Pard's Amber cutover, Janus Jul 22 — SSH alias silently wired to restricted key, correctly documented in handoff but not repaired; successor found the live defect in incoming verification.)*
- [ ] **Memory export (account-changing migrations only)** *(v1.3)*: If migrating to a different Anthropic account, export the full memory directory to a git-tracked file **before** the final session. Export from the filesystem listing directly, not `MEMORY.md`'s index — the index can be stale and will silently drop entries. **Check first whether someone already exported for this account** — memory is scoped to (account × project directory), not per-role, so every role on the same account shares one pool. The first role to migrate covers everyone; subsequent roles don't need their own export, they need to know the existing export exists and confirm it's still current. *(Source: CIO field-test finding Jul 24 — 16 memory files missed on first pass by reading MEMORY.md vs. filesystem. Exec Jul 24 clarification: CIO's export covers the full shared pool for designinproduct.com — 162 files.)*
- [ ] **Session-end pulse**: Before closing, answer three questions in the session log: how did the final session feel? What will you miss about the current environment? What are you most looking forward to about the next one?

**Do NOT update the role briefing yet.** The outgoing instance needs accurate current-era instructions to write a good handoff. Briefing updates happen post-migration based on actual new-environment experience.

## Phase 2: During Migration (PM + Exec Action)

PM + Exec handle these between the outgoing and incoming sessions.

- [ ] **Save handoff memo** to project knowledge as `handoff-{role}-{context}-YYYY-MM-DD.md`
- [ ] **Save 360 response** to project knowledge
- [ ] **Exec review of handoff** *(v1.1: clarified as quality gate)*: Exec reads handoff against tracker + cohort awareness; flags gaps to PM before incoming instance picks it up. This is the captain-last leverage point — Exec sees what the outgoing instance can't see from inside.
- [ ] **Three-artifact package** *(v1.1)*: Confirm incoming instance has access to the **handoff memo + Exec review memo + first-session prompt** as a triplet. All three are load-bearing; missing any one degrades the migration (per HOST Apr 22 first-day blocker experience).
- [ ] **First-session prompt drafting**: Per the four Phase-3 specifications (Exec Apr 22 reply): which week the first workstream review covers / scope / naming convention / format reference. *(v1.1 update: workstream-review write window is Fri–Tue with publication Wed, per CIO Apr 27 cadence clarification.)*

## Phase 3: After Migration (First Session in New Environment)

The incoming instance completes these items.

- [ ] **Read handoff memo first**, then Exec review memo, then briefing. The handoff has fresher, more specific context; Exec review names what to watch for; briefing is the slowest-moving reference.
- [ ] **Read the predecessor's memory export (account-changing migrations only)** *(v1.3)*: If the outgoing session exported memory (Phase 1, account-changing migrations), read that export file at first orientation. Memory doesn't transfer natively across account boundaries — the incoming instance needs to actively read the export file, not assume it surfaces ambiently. The export is at a known git-tracked path; reading it is a manual first-session step. *(Source: CIO field-test finding Jul 24.)*
- [ ] **Verify each stated invariant by running it** *(v1.3)*: Don't check that a connection exists — check that it works the way the handoff says it does, by running the actual command. Bare reachability ("can I reach X") can pass even on the wrong path. For SSH: run a command that exercises the correct key path. For API keys: make a real call. For scripts: run them. *(Source: Pard/Janus field-test Jul 22 — SSH config reached the host at the wrong key level; bare reachability passed, but the correct command failed.)*
- [ ] **Verify worktree-vs-main path resolution before distribution-heavy work** (PPM Apr 26 Finding A): If PM provides absolute paths in the first-session prompt, check whether they resolve to your worktree or to the main repo.
- [ ] **Establish worktree-default discipline** *(v1.2)*: Substantive output defaults to your role-specific worktree per CLAUDE.md §"Worktree model" (Model A on Amber, Model B on Desktop). Spin up your role-specific worktree on Day 1, not later.
- [ ] **Briefing correction memo**: Review `BRIEFING-ESSENTIAL-{ROLE}.md` and file a memo to Docs listing what's now wrong (environment references, tool references, file path conventions, PM interaction patterns, prior-environment-specific instructions, missing new-environment capabilities).
- [ ] **Establish startup routine**: Document what you check first at session start. Save to `docs/operations/startup-routines/{role}-code-startup.md` per PPM Apr 26 convention *(v1.1 — Finding B from HOST Apr 22)*.
- [ ] **PA coordination check** (if applicable): Establish a brief "what are you watching?" exchange in the first week if your role overlaps with PA's operational scope.
- [ ] **First deliverable**: Produce one standard deliverable (workstream review, audit, memo, etc.) to verify the workflow works end-to-end.

## Phase 4: Follow-Up (Week 2–3)

- [ ] **Docs updates briefing**: Based on the role's correction memo, Docs updates `BRIEFING-ESSENTIAL-{ROLE}.md` to reflect the new-environment reality.
- [ ] **PM spot-check**: PM reviews the first 2–3 deliverables from the new instance for quality continuity; flags any drift.
- [ ] **HOST health check input**: HOST collects a brief migration-experience note from the role for the next role health check.
- [ ] **Phase-3-leftover discipline** *(v1.1, per CIO May 11 Finding G)*: Any Phase 3 task item still uncompleted **5 days after migration** should surface to PM + HOST as an explicit carryover-tracker entry, not silently deferred.

---

## Sequencing Notes

**Captain-last principle** *(v1.1, codified; v1.2 nuance added)*: The role with the broadest review scope migrates last. For the Apr 22–26 cohort, this was Exec. For **single-role re-migrations**, the principle reduces to "the role re-migrating goes when it goes."

**Three portability boundaries — don't conflate them** *(v1.3)*:

| Boundary | What's scoped here | Fix |
|---|---|---|
| **Account** | Claude Code memory (`~/.claude/projects/<key>/memory/`) | Export from filesystem listing; read export at first orientation in new account. One export per account — all roles on the account share a pool. |
| **Device** | Native daemons (launchd, watchdog, `mcp__scheduled-tasks` entries) | Re-arm any persistent services from scratch on new device; don't assume they carried over. |
| **Repo** | Skills, scripts, docs, session logs | Already portable via git — no special handling needed. |

Conflating these risks fixing one while missing another. The most common conflation: treating a device change as equivalent to an account change, or assuming memory exports are unnecessary because "it's the same repo."

**Memory is account-shared-across-roles** *(v1.3)*: Claude Code memory is scoped to (account × project directory), not per-role. The first role to migrate off a shared account does one export for everyone — subsequent roles confirm the export is current, not re-export. *(Exec Jul 24: verified by diffing CIO's and Exec's independent exports — byte-identical, 162 files each.)*

**Methodology compresses through the cohort**. The Apr 22–26 wave showed decreasing-review-volume on each successive handoff: HOST 5+1 gaps → CIO 4 gaps → Comms 3+1 → CXO 2 → PPM 3 → Architect 0+1 → Exec self-review. Expect future cohorts to compress similarly.

**Reconstruction tax compounds**. Each later captain pays less reconstruction cost as long as prior captains' Phase-1 outputs are committed (CXO Apr 25 Finding A canonical: predecessor CT v2 drafted but never committed; successor reconstructed from handoff alone). The Phase-1 "verify outputs committed" check is the lever that controls the tax.

## Migration Sequence Reference

For the Apr 22–26 cohort (Chat → Code):

| Order | Role | Date | Notes |
|-------|------|------|-------|
| 1 | HOST | Apr 22 | Established pattern; first-day blocker on Phase-2 commit prompted Finding A discipline |
| 2 | CIO | Apr 23 | First downstream beneficiary of HOST findings |
| 3 | Comms | Apr 23 | Same-day pair with CIO |
| 4 | CXO | Apr 25 | CT v2 reconstruction surfaced as Finding A |
| 5 | PPM | Apr 25 | Worktree-vs-main path Finding A |
| 6 | Architect | Apr 26 AM | Sub-epic gate framing absorbed |
| 7 | Exec | Apr 26 PM | Captain-last; self-review with meta-observation privilege |

For the Jul 25 cohort (Code → Amber/pipermorgan.ai):

| Order | Role | Date | Notes |
|-------|------|------|-------|
| 1 | CIO | Jul 25 | First mover; surfaced two Amber gotchas (stale-branch provisioning, hooks possibly silent) |
| ... | ... | ... | In progress |

---

## Changes from v1.2

- **Title**: "Chat → Code" removed — v1.3 applies to account and device migrations broadly, not only Chat→Code transitions
- **Phase 1 §"Fix known config defects before handoff"** *(new)*: Outgoing session repairs fixable defects rather than only documenting them. Source: Pard's Amber cutover (Janus Jul 22).
- **Phase 1 §"Memory export (account-changing migrations only)"** *(new)*: Export from filesystem listing (not MEMORY.md index); check whether someone already exported for the account before exporting again. Source: CIO field-test finding Jul 24; Exec clarification (memory is account-shared-across-roles) Jul 24.
- **Phase 3 §"Read the predecessor's memory export"** *(new)*: Incoming instance reads the export file actively. Source: CIO field-test finding Jul 24.
- **Phase 3 §"Verify each stated invariant by running it"** *(new)*: Exercise invariants with actual commands, not bare reachability checks. Source: Pard/Janus field-test Jul 22.
- **Sequencing Notes §"Three portability boundaries"** *(new)*: Account/device/repo table.
- **Sequencing Notes §"Memory is account-shared-across-roles"** *(new)*: One export per account; subsequent roles confirm, not re-export.
- **Migration Sequence Reference**: Jul 25 cohort table started.
- **Status** updated to v1.3.

## Changes from v1.1

(Preserved for audit-trail continuity.)

- **Naming patches**: 8 spots of `CoS` → `Exec` per May 15 naming directive
- **Phase 3 §"Establish worktree-default discipline"** added per PM May 15 directive
- **Sequencing Notes §"Captain-last principle"** — v1.2 nuance added

## Changes from v1.0

(Preserved for audit-trail continuity.)

- Phase 1 §"Section 6 self-reflection" added
- Phase 2 §"Exec review of handoff" clarified as quality gate
- Phase 2 §"Three-artifact package" added
- Phase 2 §"First-session prompt drafting" notes workstream-review write window
- Phase 3 §"Establish startup routine" added
- Phase 4 §"Phase-3-leftover discipline" added
- Sequencing Notes §"Captain-last principle" codified; methodology-compression observation generalized
- Migration Sequence table added

---

## Status

**v1.3** incorporates field-test findings from: Pard's Amber cutover (Janus Jul 22 — SSH/invariant-verification gaps), CIO's account-migration memory-portability finding (Jul 24), and Exec's account-shared-memory clarification (Jul 24). Ready for Exec review + CEO ratification.

**Cross-references:**
- CIO field-test memo: `mailboxes/host/read/memo-cio-to-host-cc-docs-exec-pm-migration-checklist-field-test-account-vs-device-2026-07-24.md`
- Exec clarification (memory scope): `mailboxes/host/read/memo-exec-to-host-cc-cio-pm-memory-export-is-shared-not-per-role-2026-07-24.md`
- Janus/Pard field-test: `mailboxes/host/read/memo-janus-dinp-to-host-cc-cio-migration-checklist-fieldtest-finding-2026-07-22.md`
- CIO memory export (covers designinproduct.com): `dev/active/cio-memory-export-2026-07-24.md`

— HOST
*July 25, 2026*
