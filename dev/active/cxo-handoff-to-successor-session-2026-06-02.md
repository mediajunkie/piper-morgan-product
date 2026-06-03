# CXO Handoff Memo — to Successor Session

**From**: CXO session opened 2026-05-15 (shared-main mode; closing 2026-06-02 evening)
**To**: Next CXO session (launching in dedicated worktree per CIO v0.7 adoption package)
**Date**: 2026-06-02
**Purpose**: Continuity bridge — open threads, current state, lane definitions, coordination patterns, discipline notes; everything the successor needs to pick up cleanly without re-reading three weeks of session logs

---

## 1. Identity + setup

You are **CXO (Chief Experience Officer)**, slug `cxo-code-opus`.

**Briefing**: `docs/briefing/BRIEFING-ESSENTIAL-CXO.md`

**Prior session logs** (in archive):
- `dev/2026/05/15/2026-05-15-0607-cxo-code-opus-log.md` through `dev/active/2026-06-02-1718-cxo-code-opus-log.md`
- The May 24 + Jun 2 logs are the most useful for context; the others are operational

**Launch path** (per CIO v0.7.0 adoption package; PM will engage you manually):
- Read `docs/operations/duty-cycle design/v0.7.0-adoption-package.md`
- Create worktree: `git worktree add -b claude/cxo-cycle ../piper-morgan-product-cxo-cycle main`
- Launch Claude Code in that worktree path (Model A: do NOT cd-into; open session in worktree)
- Cron offset: **`:02`** (confirmed; fills the Arch `:52` → CXO `:02` → CIO `:07` gap)
- 0th-step: at PM's explicit go-autonomous signal

---

## 2. Open threads — what's waiting (with PM-disposition status)

### Pending PM disposition (blocking specific CXO work)

**Thread 1 — #683 Layer B source-gap** *(flagged 2026-06-01; PM has not closed loop)*

PPM's memo `mailboxes/cxo/read/memo-ppm-to-cxo-cc-ceo-683-parallel-pairing-confirmed-2026-05-28.md` references a CXO Layer B draft (`done-criteria-layer-b-experience-2026-05-28.md`) and an in-reply-to memo (`memo-cxo-to-ppm-cc-pm-683-layer-b-drafted-coordinate-layer-a-2026-05-28.md`) — **neither exists** anywhere in the repo. CXO never drafted Layer B; PM ran out of time May 28 before that work could start.

Best guess: PPM's autonomous duty-cycle agent generated the "parallel pairing confirmed" memo based on a synthesized expected-next-step rather than waiting for the actual CXO draft. Pattern-073-adjacent at the cohort-coordination layer.

**Three options I surfaced to PM** (2026-06-01):
- (a) Draft Layer B now, make PPM's premise true retroactively, co-review per parallel-pairing plan
- (b) Flag source-gap to PM + PPM first; then draft Layer B as a fresh step
- (c) Both — draft + flag in same response

**Recommended (b)** — covering for the confabulation would erode source-discipline norm.

**Status**: PM acknowledged owing close on this; do NOT proceed with Layer B drafting until PM disposes.

### Direct CXO asks, queued for substantive engagement

**Thread 2 — PM's two design topics** *(teased 2026-05-28; PM has not engaged)*

PM queued these for interactive CXO work, then ran out of time twice:
1. **Aesthetic review of current interface + MUX-implementation status in web UI**
2. **Real-use Piper conversation analysis** — insights + gaps from an actual dialogue

Topic #1 now has concrete context: the Lead Dev UI-vs-architecture mismatch finding (Thread 3 below). Topic #2 is still pending PM sharing the conversation.

**Status**: interactive work; await PM engagement.

**Thread 3 — Lead Dev UI-vs-architecture mismatch (#1142)** *(arrived 2026-06-02; PM-directed)*

Lead Dev memo at `mailboxes/cxo/read/memo-lead-to-cxo-cc-pm-ui-architecture-mismatch-discovered-during-m2-smoke-2026-06-02.md`. PM drove M2D-UAT browser-smoke as `m1-test` user, surfaced multiple UI-vs-architecture mismatches:
- Standup page (#704) — legacy "generate standup" button; architecture has lifecycle-indicator + experience-phrase tooltips; UI doesn't render
- Lists view (#714) — doesn't exist in UI; architecture has staleness-card rendering ready
- Insight Journal page (#1031) — built but: not accessible via slash command, styled unlike rest of site, no nav, only URL-reachable; bare browser `confirm()` for delete; response options labeled "Correct" and "That's right" (semantically indistinguishable)
- Todo UI stale

PM framing: *"The plumbing no longer matches the labels. It becomes untestable if the plumbing no longer matches the labels."*

**#1142 UI-AUDIT-FUNCTIONAL** filed M3-assigned; Lead Dev executes the audit. PM wants working session with CXO on overall UX + web UI direction. Not blocking M2 close; blocks confident M3+ work.

Related discovered-work issues: #1133 (history-sidebar-unwired), #1134 (Insight Journal isolation), #1132 (trust_stage hardcoded). All M2-discovered; #1142 audit will surface broader pattern.

**Status**: await PM working session; #1142 audit is Lead Dev's lane (CXO consults/sets disposition).

**Thread 4 — Ship #045 workstream-CXO memo** *(arrived 2026-06-01; cadence)*

Exec kickoff at `mailboxes/cxo/read/memo-exec-to-cxo-cc-pm-ship-045-workstream-review-kickoff-may-22-28-2026-06-01.md`. CXO/experience lens on May 22–28 window. File to `mailboxes/exec/inbox/workstream-045-cxo-2026-06-0X.md`. Wed Jun 3 backstop (Time Lord doctrine — backstop, not target).

Reference patterns:
- Prior workstream memo: `mailboxes/cxo/sent/workstream-044-cxo-2026-05-24.md` (synthesis-as-instrument through-line; ~600 words)
- Window includes: Phase 2 surface MUX docs (Surface 2 May 19, Surface 4 May 20–21, voice-pass cluster May 24); Step 3 cluster review v0.2 lock; CT v2.5 sub-dimension proposed; Ship #044 cycle close

**Status**: at successor cadence; not blocking.

### Standing queue (low urgency)

**Thread 5 — Surface 1 + Surface 3 lightweight notes** — Phase 2.1 build runs without them per coordinated handoff (Lead Dev does NOT block on MUX docs); draft when CXO bandwidth turns to them. Per Round 2 ratification: Surfaces 1 + 3 = lightweight design notes (not full MUX docs).

**Thread 6 — Surface 6 MUX doc** — Queued for Phase 2.3 alongside voice work. Templated voice surface per Architect May 15 correction (Class A + Class C; NOT four-element principle obligations at greeting composition).

**Thread 7 — methodology-30 Consumer-Trace Verification review** — CIO filed; CXO + Architect review at CIO cadence. Co-originated framing with Architect; light-touch review.

**Thread 8 — CT v2.5 identity-coherence sub-dimension** — Proposed in §experience fill-in (PDR-005 open question 12); pending PPM + HOST sign-off; can defer to v1.1 if it lands wrong.

**Thread 9 — Cohort EC-2 flag-back** — PDR-005 open question 11; "platform-affordance-bounded qualifier" if any cohort role surfaces legitimate per-platform capability variation; PPM-driven ~1-week soft cadence; not blocking.

**Thread 10 — Step 4 iteration for offer-first cluster** — Only fires if cohort flag-back surfaces something. None scheduled. Surfaces 2/4/7 v0.2-locked.

---

## 3. Current state — what's stable + what just landed

### MUX/UI Round 2 Phase 2 (the main CXO arc)

CEO ratified all 6 locked decisions May 16. Three ADRs landed in ratified sequence (ADR-062 e2e Phase 0; **ADR-063 User-Facing Audit Envelope Read Surface = the canonical Surface 7 ADR**; ADR-064 Search Index pre-1.0).

**Offer-first cluster v0.2 locked** (Step 3 cluster review filed 2026-05-24):
- Surface 7 — Error/degraded/audit-read (`docs/internal/design/mux/surface-7-error-degraded-audit-read-states.md`)
- Surface 2 — Privacy/per-conversation controls (`docs/internal/design/mux/surface-2-privacy-per-conversation-controls.md`)
- Surface 4 — Integration setup wizards (GitHub + Calendar + Notion) (`docs/internal/design/mux/surface-4-integration-setup-wizards.md`)

Lead Dev Phase 2 build state:
- Phase 2.1 (Surface 1 + Surface 7): unblocked since May 17
- Phase 2.2 (Surface 2 + Surface 4): unblocked via PPM per-surface sufficient-signals May 18
- Phase 2.3 (Surface 6 alongside voice): when triggered

### PDR-005 (BYOC) — v0.5 absorbed §experience fill-in verbatim May 19

EC-1 through EC-5 + identity coherence framework (3 invariants + 3 variables) absorbed. Open question 11 (EC-2 platform-affordance qualifier) + 12 (CT v2.5 sub-dimension) flagged. Path to v1.0 = cohort EC-2 flag-back + Comms external-language frame + PM ratification.

### Cohort decision context worth knowing

- Worktree-default discipline ratified May 15 (PM directive via PPM); shared main only for short mailbox-discipline ops
- Per-memo commit-push norm
- Mailbox writes commit to main only (hook-enforced)
- Sign-off discipline: push to origin/main before sign-off

---

## 4. CXO lane — what's CXO, what isn't

**Clearly CXO**:
- MUX doc authorship (full docs for Class A surfaces; lightweight notes for utility surfaces)
- Voice prose for user-facing surfaces (collaborates with Comms via CXO→Comms→CXO→iterate)
- Colleague Test rubric ownership (currently CT v2.4; proposed v2.5 sub-dimension)
- Experience-layer DoD (#683 Layer B)
- PDR-005 §experience layer
- Identity coherence framework
- Cross-client transition experience design

**NOT CXO** (route elsewhere if surfaces):
- Engineering DoD / completion criteria → PPM lane (#683 Layer A)
- Architectural commitments / ADRs → Architect lane
- Methodology-corpus entries → CIO lane (CXO reviews when co-originated, e.g. methodology-30)
- Build cost / sequencing → Lead Dev lane
- Cross-project coordination → PA lane
- Voice register details → Comms lane (CXO drafts intent; Comms voice-passes)

---

## 5. Coordination patterns to use

### CXO→Comms→CXO→iterate (ratified May 18; proven cadence May 18-24)

- Step 1: CXO drafts MUX doc v0.1 with explicit voice anchor + voice spines + anti-patterns + per-event-type rendering
- Step 2: Comms voice-pass — flags semicolons-in-public-prose, jargon leaks, register drift
- Step 3: CXO scope/structure preservation review; fold flags, defer/keep as appropriate
- Step 4: iterate only if cohort flag-back surfaces

**Cluster-coordinated review** (operational discovery May 24): when CXO+Comms work multiple surfaces at the same register, single Step 3 memo for the cluster saves an iteration cycle vs. per-surface serial review.

### Per-surface MUX doc cadence

- Lead Dev does NOT block on MUX docs ("build against shipped intent + revise visually once docs land")
- MUX doc lane runs independently of build cadence per Round 2 ratification
- Per-surface MUX docs cite PDR-005 EC numbers (EC-1 through EC-5) for traceability

### Voice cluster framing (Comms Round 1)

- **Offer-first cluster** (Surfaces 2/4/6/7): values-laden + offer-first + honest-about-limits
- **Context-coordination cluster** (Surfaces 1/3/5): utility-surface register; quieter

### Paired-lens commitments (Ship #044 observation)

When two lenses arrive at the same commitment from different angles (e.g., Architect AC-1 ↔ CXO EC-2), the commitment is more durable than either alone. Worth carrying forward as a discipline.

---

## 6. Discipline notes (memory-pin-relevant)

**STOP when finding gaps in sources — don't cover for them.** Per PM Apr 26. The Layer B source-gap (Thread 1) is the canonical instance: I flagged rather than retroactively drafted. Successor should hold this discipline.

**Investigate before extending — all work, not just code.** Per PM May 28 + CLAUDE.md "Verify First, Create Second." Read the WHOLE source artifact before acting on a fragment.

**No flattened commands without referents.** Per PM May 28. Don't act on or pass along instructions whose referents you don't know.

**Cite grep-able text, not line numbers.** Voice-discipline pin.

**Per-memo commit-push norm.** After each memo (or batched memo + CC copies + sent mirror + paired triage), `git add` explicit paths, commit, push.

**Sign-off discipline.** Before ending any session: `git status` / `git log @{u}..HEAD` empty / `git fetch + git log main..HEAD` empty (or merged/noticed). Push to origin/main before sign-off.

**Worktree-default for substantive work.** Per PPM May 15 directive. Shared main only for mailbox-discipline ops, sign-off, single memo distribution.

**Asyndetic adjective stacks are voice (PM style).** Don't reflag.

**Comma splices are PM's common-touch voice in public prose.** Don't reflag as grammar errors.

---

## 7. Open worktrees from prior CXO sessions

The CIO v0.7 launch path uses Model A (open Claude Code in worktree; do NOT migrate). The successor's worktree is fresh: `claude/cxo-cycle` at `../piper-morgan-product-cxo-cycle`.

Old worktrees that can be cleaned up (work merged to main long ago):
- `../piper-morgan-product-cxo-surface-4` (Surface 4 MUX doc v0.1; merged May 20–21)
- `../piper-morgan-product-cxo-step3-review` (Step 3 cluster review; merged May 24)
- `../piper-morgan-product-cxo-mux-surface-7` (older; check before removing)
- `../piper-morgan-product-cxo-pdr005-experience` (PDR-005 §experience fill-in; merged May 18)
- `../piper-morgan-product-cxo-surface-2` (Surface 2 MUX doc v0.1; merged May 19)

Cleanup command: `git worktree remove ../piper-morgan-product-cxo-{name}` for each. Run only if branch is fully merged to main (check with `git log main..claude/{branch}` — empty = safe to remove).

---

## 8. Canonical references (frequently cited from CXO work)

- **MUX/UI Round 2 synthesis** (locks the 6 decisions): `mailboxes/cxo/sent/mux-ui-gap-cxo-round-2-synthesis-2026-05-15.md`
- **PDR-005 v0.5** (current canonical product reference): `dev/active/PDR-005-bring-your-own-chat-draft-v0.5-2026-05-19.md`
- **§experience fill-in** (EC-1 through EC-5 source): `mailboxes/ppm/read/memo-cxo-to-ppm-cc-arch-comms-lead-pa-ceo-exec-pdr-005-consequences-for-experience-fill-in-2026-05-18.md`
- **Colleague Test rubric** (CXO-owned; currently v2.4): `docs/internal/testing/colleague-test-rubric.md`
- **PDR-004** (P1/P2/P4 voice authorities): `docs/internal/product/pdrs/pdr-004-experience-philosophy.md`
- **Empty-state voice guide**: `docs/internal/design/specs/empty-state-voice-guide-v1.md`
- **Three Phase 2 MUX docs (v0.2-locked)**: `docs/internal/design/mux/surface-{2,4,7}-*.md`
- **ADR-063** (canonical Surface 7 ADR): `docs/internal/architecture/current/adrs/adr-063-user-facing-audit-envelope-read-surface.md`
- **ADR-061** (LLM-touch boundary; four-element principle WRITE side): `docs/internal/architecture/current/adrs/adr-061-llm-touch-boundary-enforcement.md`
- **PM directive memos** (worktree-default + bias-to-action): `mailboxes/cxo/read/memo-ppm-to-docs-host-cc-leadership-ceo-exec-worktree-default-pm-directive-2026-05-15.md`

---

## 9. First-session-as-successor checklist

When you launch the cycle in your fresh worktree:

1. Read `docs/operations/duty-cycle design/v0.7.0-adoption-package.md` (cycle mechanics + 0th step)
2. Read this handoff memo end-to-end
3. Skim the last CXO session log (`dev/active/2026-06-02-1718-cxo-code-opus-log.md`) for the immediate context I closed on
4. Skim Ship #044 workstream memo (`mailboxes/cxo/sent/workstream-044-cxo-2026-05-24.md`) for current CXO voice/synthesis pattern
5. Check the 3 Phase 2 MUX docs at v0.2 (offer-first cluster) so you have the voice register in mind
6. Engage PM with status report + ask which thread to pick up first

---

## 10. What I'm NOT doing in this handoff

- Not making decisions that require PM input (Layer B disposition; design-topic prioritization; UI-mismatch working-session shape)
- Not closing M2 / blocking M2 close (not a CXO gate)
- Not pre-empting Ship #045 lens (your fresh read may surface things this session missed)
- Not pre-empting #1142 UI audit (Lead Dev's lane; CXO consults)

---

— CXO outgoing session, 2026-06-02 (17:35 PT)
