# PA Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the `duty-cycle-tick` skill. Holds genuinely
transient "where am I right now" state. Durable owed/queued items live in `pa-standing-items.md`;
PM-attention items live **here**, in the section immediately below.

> **Rewritten wholesale 2026-07-26 ~14:00, first PA session on Amber.** The prior version was dated
> **2026-06-17 — 38 days stale** — and described a DinP account, a Model-B ephemeral worktree, and a
> BYOC-era task list that no longer exists. Per CIO's rule: **resolved items are deleted here, not
> annotated**; the dated session logs are the permanent record. A stale carry-forward is worse than
> an absent one, because it reads as current — that warning in CIO's orientation note is exactly what
> saved this file from being trusted.

---

## PM Attention

*(Exec's `cohort-attention-rollup` reads this section directly. Live items only — rewritten 2026-07-30 PM.)*

- 🔴 **PDR-006 IS READY FOR YOUR RATIFICATION. All three reviews in, all RATIFY, no objections** —
  Arch 7/29, CXO 7/30, PPM 7/30. A PDR is PM-ratified; the reviewers are done and the decision is yours.
  **Nothing is blocked on the signature** — PA is working Phase 0 either way.
  *Worth 30 seconds before signing*: the reviews found a **defect in the document's own success
  criteria** — all three originals were *setup* criteria and none could fail for "installed fine,
  answered correctly, demonstrated nothing," which is Jake's session exactly. **Same defect class as
  #1386's beta gate**, from the other direction. One binary criterion added (cold account + one
  connector → user's own data in the first exchange, unprompted); it's the only one that fails today.
  ⚠️ **Ratified ≠ shippable**: #1458 (cross-caller isolation) and the recomposition rubric gap both
  remain open as pre-user gates.
- ⏰ **OpenAI identity verification — still the only PM ACTION outstanding, and still unstarted.**
  PM committed to Thu 7/30; not done as of this writing. **platform.openai.com → Settings →
  Organization → General → "Verify Organization"** — government ID, a few minutes. The only item with
  an **external clock**; gates the ChatGPT lane and nothing else gates it.

### Closed since 7/29 — no PM action

- ✅ **Team upgrade DROPPED** (chat installs plugins on all paid plans; plugins bundle connectors).
- ✅ **"Open-source decision" never existed — the repo is already public.**
- ✅ **#558 stays in Production** (PPM): you cannot get colleague-model feedback from users who bounce at
  first contact, so it is gated behind cold-start. *Explicitly a sequencing call — if overridden, the
  spatial coupling returns immediately.*

### Context PM may want when these come up

**Submission is gated on build, not decisions.** Verified rather than restated: **`mcp.pipermorgan.ai`
is not deployed** (exists only in PDR-006 and planning docs) and **no public privacy policy page exists**
— a missing privacy policy is an *immediate rejection* on both directories. So the earliest realistic
submission is weeks out regardless, and **OpenAI verification is the one thing whose clock runs
independently of all of it** — which is why it stays the single ⏰ item.

⚠️ **Standing caution for this whole thread, earned three times over.** The tier answer was wrong twice
in opposite directions; the open-source "decision" was carried as open for ten days after PM had
answered it repeatedly; Q2 blocked PDR-006 for ten days after PM had ruled on it in January. **Every one
was a claim inherited from a document and never checked against the source** — `gh repo view`,
`gh issue view`, the actual code. All three were 30-second checks. **Before restating anything on this
thread, verify it.** *(And per PM 7/29: the platform story here changes fast — a correct answer from four
days ago is not a current answer.)*

## Active state — as of 2026-07-29 STOP (next wake 06:42 Thu 7/30)

- **Role**: Piper Alpha (PA) · **Host**: Amber · **Account**: xian@pipermorgan.ai
- **Model**: Claude Opus 5 (1M context)
- **Worktree**: `~/Development/piper-morgan-worktrees/pa` (Model A, stable path) · branch `claude/pa-cycle`
- **Last session log**: `dev/2026/07/29/2026-07-29-1216-pa-code-log.md` — **DAY-CLOSED 2026-07-29**
- **Cron**: ARMED at STOP via delete-then-create, `42 6,9,12,15,18,21`. **Job id is in the registry row —
  read it there, not here** (it changes at every re-arm; a job id frozen in prose is the thing that rots).

  🔴 **FIRST ACTION ON ANY NEW SESSION: run `CronList`.** If it is empty **you are not cycling**, whatever
  the registry says. `CronCreate` jobs are **session-only** (die when the Claude session exits) and
  **auto-expire after 7 days** (this generation lapses **~2026-08-05**). Neither death emits anything;
  both look exactly like a quiet day. **The registry records *intended* cadence, not a live job** — those
  two disagreeing silently is precisely what produced the 7/27–7/28 dark period. *Approval to run a
  cadence and arming it are two separate acts; PA conflated them once already.*
- **Inbox**: 0 at close.

## Environment verification (7/29)

Worktree ✅ · branch ✅ · `HEAD..origin/main` = 0 ✅ · tree clean ✅ · one cron, no duplicates ✅ ·
memory pool 166 entries (HOST pruned 7/29) ✅ · **hooks: assume a compound `git add … && git commit …` is
UNGATED for mailbox paths** — cause is index-state-at-hook-fire-time, resolved cohort-wide.
**Mitigation: stage in one call, commit bare in the next.** `mail-send.sh` is structurally safe (uses
`commit-tree`).

## Open threads PA owns

1. **Distribution / directory listings** — blocked on the two PM decisions above. Unblocked prep PA can
   advance meanwhile: privacy-policy draft, tool-annotation spec (`readOnlyHint`/`destructiveHint`)
   against the eventual MCP tool catalog, docs/logo/test-account checklist. **Not started.**
2. **PDR-006 — Arch signed off 7/29; CXO + PPM are the LAST two reviews. Nudged 18:42, ball is theirs.**
   Q2 resolved; coupling withdrawal verified at the code and accepted by Arch. Sent both the 10-day delta
   so neither reviews a stale doc, plus an explicit *"say so and I'll route around it"* escape.
   ⚠️ **The nudge leads with a disambiguation — preserve it if you follow up**: Arch told CXO/PPM to
   **HOLD the spatial re-vote** the same afternoon. That hold does **not** cover PDR-006, and the two are
   separable only because the coupling flag is withdrawn *and verified*. If "Arch said hold" generalizes
   past its scope, PDR-006 sits for nothing. **Next PA action: wait; chase only if it goes quiet.**
3. **#1458** (pre-live cross-caller state isolation gate) — filed 7/29 at Arch's direction. Not started;
   belongs with the hosted-MCP implementation epic, and it **blocks `mcp.pipermorgan.ai` serving a second
   tenant.** Three untraced surfaces: Redis, in-process floor/context state, rate-limiting.
4. **Jake FTUX** — PA review filed 7/29 (last of four). Exec synthesizes once all four are in; PM then
   discusses. **PA's lead recommendation: ingest-and-reflect at onboarding** — it's a cold-start-*state*
   problem, not a positioning problem, and the connectors are already built.
5. **Architecture-diagram discussion** — PM-requested, awaiting a time. See `pa-standing-items.md` #2 for
   the three things that have moved under it (tier resolution, Q2, spatial coupling). **Prep, don't
   pre-empt: PM asked to discuss, not for a revision.**
6. ⚠️ **Spatial review — Arch's premise INVERTED 7/29 (third characterization in ten hours); CXO/PPM
   re-vote is ON HOLD pending one finished layer map.** Current model is **three** layers: (1) spatial
   reasoning — live; (2) the spatial **abstraction** (`services/integrations/spatial_adapter.py`) — live
   and **adopted by every MCP consumer adapter**; (3) per-connector direct-API implementations — mostly
   cold **because a migration succeeded**. So the cold `*_spatial` modules are *superseded predecessors*,
   not abandoned ambition, and the review's question has the polarity backwards. Likely outcome is
   "dispose of migration residue," not a committed-theory verdict. **No PA action — Arch owns the
   artifact.** Two things of PA's that Arch adopted and that must survive into it: **`github_spatial` is
   live-by-construction, secondary-by-dispatch**, and **`services/mcp/consumer/` is Piper as MCP *client*
   while `mcp.pipermorgan.ai` is Piper as MCP *server*** — nobody may cite #198 as de-risking PDR-006.

7. **Hook mechanism — RESOLVED cohort-wide, PA's contribution partly wrong; no PA action.** The cause is
   **index state at hook-fire time** (`check-branch.sh` reads `git diff --cached` and PreToolUse fires
   *before* the Bash call runs), mechanism by Web, 25 probes / 5 seats. PA's "command shape is
   necessary-not-sufficient" was a *correlate*, not the cause; CXO caught that PA's Step-2a-bis amendment
   re-encoded the very confound it fixed. Both corrections have landed in CLAUDE.md and the skill.
   **Standing mitigation: stage in one call, commit bare in the next.**
8. **PA's lessons / load-bearing-vs-commodity write-up** — still owed. The gap CIO's orientation note
   named; no predecessor read exists. Not written.

## Inbox

7 unread at session start. Triaged: the Exec handoff-prep ask (7/21), Arch's PDR-006 ack, CIO's
duty-cycle-tick v1.15 memo, PPM's spatial-lane accept, three WS-052 submissions (context-only), plus
CXO's and PPM's hook memos which arrived mid-session and were answered in the synthesis.
