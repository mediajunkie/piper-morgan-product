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

*(Exec's `cohort-attention-rollup` reads this section directly. Live items only.)*

- ⏰ **OpenAI identity verification — the only PA item with an EXTERNAL clock. Unstarted, 7 days idle.**
  Gates the ChatGPT remote-MCP listing; it is that track's *only* dependency. Individual accounts can
  verify — no company entity needed. **Lead time starts when someone starts it, not when we decide the
  rest.** *(Also carried on CIO's board, where it reads "eight days" — it is 7: memo sent 7/19,
  today is 7/26.)*
- ⏰ **claude.ai account tier check — 5 minutes, unstarted, gates the Claude connector listing (Track A).**
  Submission portal requires **Team or Enterprise**; individual/Pro cannot reach it. ⚠️ **The 7/25
  migration to pipermorgan.ai means the 7/19 answer may no longer apply** — this needs a fresh look at
  the account we're actually on, not a recollection.
- 🟡 **Open-source decision for the Claude plugin package (CLAUDE.md + hooks + skills) — PM's call, not
  yet made.** A public GitHub repo is a hard requirement for Track B (full plugin). **Not time-critical
  the way the two above are**: Track A gets a Claude listing without it. PA can write up the tradeoffs
  on request.
- 🟡 **PDR-006 has sat in "Arch / CXO / PPM review pending" for 7 days; it gates the implementation
  epic.** PM approved the direction 7/19. Arch acked the same day promising a dedicated read "next
  fire" and flagged a real coupling — the colleague-model question is the *same concept* as the spatial
  committed-theory review's "connectors as places with colleagues," so the two shouldn't be decided
  in isolation. CXO has since named this its most substantive unowned work, queued behind the #1386
  gate run. No review from any of the three yet. **No PM action needed unless it stays stuck.**

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
- **Cron**: **NOT ARMED.** PM's instruction was orient-and-report; not arming unilaterally.
  Registry row in `duty-cycle-registry.tsv` pending the cron expression (the load-bearing field —
  nobody else can write this row). **Awaiting PM/CIO confirmation of PA's cadence on Amber.**
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
