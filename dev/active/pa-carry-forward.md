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

*(Exec's `cohort-attention-rollup` reads this section directly. Live items only — rewritten 2026-07-29.)*

**Two decisions, both PM's, both now genuinely blocking. Everything else on this thread has resolved.**

- 🔴 **DECISION 1 — upgrade pipermorgan.ai to Team/Enterprise, or hold Track A?** ✅ *Tier question is
  CLOSED*: xian checked the account — it is **Pro (Max 20x)** (Janus, 7/28). Team/Enterprise is required
  to reach the connector submission portal, so **Track A (connector listing) is blocked on the plan, not
  pending a lookup.** This is now a purchase decision, not a research task.
- 🔴 **DECISION 2 — open-source the plugin package (CLAUDE.md + hooks + skills)?** Track B requires a
  **public GitHub repo**; closed-source is not accepted. **With Track A behind a paid upgrade, Track B is
  the only Claude-side route open today** — so this is the live gate, not the deferrable one.
  *(PA advised deferring this on 7/26 morning; withdrawn same day.)*
- ⏰ **ACTION, not a decision — OpenAI identity verification. Still unstarted; 10 days.** The only item
  with an **external clock**, and unaffected by both decisions above. Exact path (Janus, 7/28):
  **platform.openai.com → Settings → Organization → General → "Verify Organization"** — government ID,
  a few minutes, no spending threshold, no company entity. Unblocks the ChatGPT remote-MCP listing.
- ❓ **One 30-second look, if convenient**: what is the **"Piper morgan" entry** in your earlier
  screenshot — an installed connector, a personal plugin upload, or an actual listing? Determines whether
  anything is already live. *(The Console-org half of this question is largely moot: Track B's Console
  path needs a Console org role, which the API usage implies.)*

### Resolved since 7/26 — no PM action

- ✅ **PDR-006 ratification UNBLOCKED (Arch, 7/29).** Q2 was never open: **PM ruled it 2026-01-08** —
  rule-based Option A, shipped; LLM evolution is **#558**, OPEN, Production/1.0, due 2026-10-30. Arch
  verified against running code. Arch's own spatial-coupling flag **withdrawn as a gate** (re-trigger
  recorded if #558 is pulled forward). **Arch has no objection to ratifying**; CXO + PPM reviews still out.
- ✅ **Claude submission tiers resolved** against Anthropic's docs (`dev/active/distribution-submission-tiers-resolved-2026-07-26.md`).
- ✅ **#1351's unfinished audit is now a tracked pre-live gate — [#1458](https://github.com/mediajunkie/piper-morgan-product/issues/1458)**, filed at Arch's direction with the three untraced surfaces (Redis, in-process floor/context state, rate-limiting) as ACs, plus the identity-boundary mechanism.
- ➡️ **New, PM's and genuinely open — but must NOT gate anything** (Arch, 7/29): *at what point does the
  gap between a 4-dimension rule-based preference model and a real "colleague model" start costing us
  users?* Product-quality question. **Alpha feedback should decide when #558 gets pulled forward.**

### Context PM may want when these come up

Submission is **further out than the 7/19 research memo implied**, and PA verified this rather than
restating it: **`mcp.pipermorgan.ai` is not deployed** (it exists only in PDR-006 and planning docs),
and **no public privacy policy page exists**. Both directories require a stable endpoint and a privacy
policy. **This strengthens rather than weakens the two ⏰ items** — they are the only long-external-
lead-time steps and the only ones not gated on the server existing, so they should run in parallel
with the build, not after it.

## Active state — 2026-07-29

- **Role**: Piper Alpha (PA) · **Host**: Amber · **Account**: xian@pipermorgan.ai
- **Model**: Claude Opus 5 (1M context)
- **Worktree**: `~/Development/piper-morgan-worktrees/pa` (Model A, stable path) · branch `claude/pa-cycle`
- **Session log**: `dev/2026/07/29/2026-07-29-1216-pa-code-log.md`
- **Cron**: ✅ **ARMED** — job **`04985c22`**, `42 6,9,12,15,18,21`. Registry row active, carries the job id.
  *(PM approved this cadence 7/26; PA failed to arm it and went dark 7/27–7/28. **Approval and arming are
  two separate acts** — do not treat the first as the second.)*
  ⚠️ **TWO SILENT DEATH MODES, both looking identical to a quiet day:** (1) `CronCreate` jobs are
  **session-only** — they die when the Claude session exits, so **every new session must re-arm**;
  (2) recurring jobs **auto-expire after 7 days** — this one lapses **~2026-08-05**. Neither emits
  anything. **Check `CronList` at session start; if it's empty you are not cycling, whatever the registry
  says.** The registry records *intended* cadence, not a live job — those two disagreeing silently is
  exactly what produced 7/27–7/28.
- **Predecessor**: went dark 2026-07-19 after a clean close. **No handoff existed** — oriented from
  `dev/active/orientation-note-pa-amber-2026-07-25.md`, then PM consulted the predecessor directly on 7/26;
  its §4/§6 is preserved at `dev/active/handoff-pa-predecessor-2026-07-26.md`.

## Environment verification (7/29)

Worktree path ✅ · branch `claude/pa-cycle` ✅ · `HEAD..origin/main` = **0** ✅ · tree clean ✅ ·
one cron, no duplicates ✅ · memory pool present (166 entries after HOST's 7/29 prune) ✅ ·
**hooks: do not assume coverage on a compound commit — see open thread 7.**

## Open threads PA owns

1. **Distribution / directory listings** — blocked on the two PM decisions above. Unblocked prep PA can
   advance meanwhile: privacy-policy draft, tool-annotation spec (`readOnlyHint`/`destructiveHint`)
   against the eventual MCP tool catalog, docs/logo/test-account checklist. **Not started.**
2. ✅ **PDR-006 — Arch review complete 7/29, no objection to ratifying.** CXO + PPM reviews still
   outstanding. Q2 resolved; coupling withdrawal verified against code and holds (see below).
   **Next PA action: nudge CXO + PPM, then move to ratification.**
3. **#1458** (pre-live cross-caller state isolation gate) — filed 7/29 at Arch's direction. Not started;
   belongs with the hosted-MCP implementation epic, and it **blocks `mcp.pipermorgan.ai` serving a second
   tenant.** Three untraced surfaces: Redis, in-process floor/context state, rate-limiting.
4. **Jake FTUX** — PA review filed 7/29 (last of four). Exec synthesizes once all four are in; PM then
   discusses. **PA's lead recommendation: ingest-and-reflect at onboarding** — it's a cold-start-*state*
   problem, not a positioning problem, and the connectors are already built.
5. **Architecture-diagram discussion** — PM-requested, awaiting a time. See `pa-standing-items.md` #2 for
   the three things that have moved under it (tier resolution, Q2, spatial coupling). **Prep, don't
   pre-empt: PM asked to discuss, not for a revision.**
6. ⚠️ **Spatial review — do NOT let the MCP-consumer path be read as precedent for PDR-006.** Verified
   7/29: `services/mcp/consumer/` is Piper as an MCP **client**; `mcp.pipermorgan.ai` is Piper as an MCP
   **server**. Opposite directions. A live consumer adapter de-risks nothing server-side, where PDR-006's
   real risk lives (caller-identity mapping upstream of all ADR-079 enforcement). **Same conflation class
   as Connector-vs-Plugin** — watch for it in the spatial synthesis and in any "#198 de-risks this" claim.
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
