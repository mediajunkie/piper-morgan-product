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

## Active state — 2026-07-26

- **Role**: Piper Alpha (PA) · **Host**: Amber · **Account**: xian@pipermorgan.ai
- **Model**: Claude Opus 5 (1M context)
- **Worktree**: `~/Development/piper-morgan-worktrees/pa` (Model A, stable path) · branch `claude/pa-cycle`
- **Session log**: `dev/2026/07/26/2026-07-26-1250-pa-code-log.md`
- **Cron**: ✅ **ARMED 2026-07-29** — `CronCreate` job **`04985c22`**, `42 6,9,12,15,18,21`. Registry row
  un-parked. *(PM approved this cadence 7/26; PA failed to arm it and went dark 7/27–7/28. The approval
  and the arming are two separate acts — do not treat the first as the second.)*
  ⚠️ **TWO SILENT DEATH MODES, both undocumented in our own materials and both look identical to "quiet
  day":** (1) `CronCreate` jobs are **session-only** — they die when the Claude session exits, so **every
  new session must re-arm**; (2) recurring jobs **auto-expire after 7 days** — this one lapses
  **~2026-08-05**. Neither emits anything. **Check `CronList` at session start; if empty, you are not
  cycling regardless of what the registry says.** The registry records the *intended* cadence, not a live
  job — the two can disagree silently, which is exactly what happened 7/27–7/28.
- *(historical)* Registry row —
  `pa 42 6,9,12,15,18,21 6 6 22 06:42 2026-07-26 parked:…`. PA previously had **no row at all** and was
  structurally invisible to the freeze-watchdog (finding #6). Parked = counted in coverage, no stall
  alerts. **Recommended cadence `42 6,9,12,15,18,21`** — restores PA's previously PM-ratified windowed
  schedule; `:42` collides with nobody (lead :17, arch :27, host :37, cxo :47, ppm :52). **Clear the
  parked note only when a cron is actually armed.**
  ⚠️ **The row is not yet visible to the watchdog**: `duty-cycle-freeze-check.sh` reads the registry from
  the **shared checkout's working tree**, which is 12 commits behind. See the sync-script chain below.
- **Predecessor**: went dark 2026-07-19 after a clean close (DAY-CLOSED). **No handoff exists** —
  oriented from `dev/active/orientation-note-pa-amber-2026-07-25.md` (CIO, assembled from artifacts).

## Environment verification (this session)

Worktree path ✅ · branch ✅ · `HEAD..origin/main` = **0** ✅ · tree clean ✅ · memory pool present ✅ ·
**hooks — see finding below, do not assume coverage**.

## Open threads PA owns

1. **Distribution / directory listings** — blocked on the PM items above. PA advancing the unblocked
   shared prep meanwhile: privacy-policy draft, tool-annotation spec (`readOnlyHint`/`destructiveHint`)
   against the eventual MCP tool catalog, docs/logo/test-account checklist.
2. **PDR-006** — awaiting Arch/CXO/PPM. PA to ping; do not let it go a second week.
3. **Hook coverage finding** (3-seat synthesis, PA/CXO/PPM, 7/26) — pooled 14 probes:
   **standalone `git commit` 4 BLOCK / 0 BYPASS; compound `add && commit` 3 BLOCK / 7 BYPASS.**
   Every recorded bypass was compound; compound is **necessary but not sufficient**. The bypassing
   shape is the one everyone routinely commits with. **Mitigation, no config change: stage in one
   call, commit as a separate bare call.** Open gap: PPM's probe-1 shape unconfirmed. Likely real
   lever is the `if: "Bash(git commit*)"` predicate — flagged to CIO, not touched by PA.
4. **PA's own lessons / load-bearing-vs-commodity write-up** — the genuine gap CIO's note named, since
   no predecessor read exists. Owed, not yet written.

## Inbox

7 unread at session start. Triaged: the Exec handoff-prep ask (7/21), Arch's PDR-006 ack, CIO's
duty-cycle-tick v1.15 memo, PPM's spatial-lane accept, three WS-052 submissions (context-only), plus
CXO's and PPM's hook memos which arrived mid-session and were answered in the synthesis.
