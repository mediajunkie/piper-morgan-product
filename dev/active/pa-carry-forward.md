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
- ❓ **Claude submission path — the question CHANGED on 2026-07-26. It is no longer "check your tier."**
  ~~Tier check gates Track A~~ — **withdrawn**. The 7/19 research's blanket "Team/Enterprise required,
  Max blocked" claim is **unreliable**; its own author retracted it during handoff consultation, but the
  retraction had lived only in a chat session and never reached a committed document. A **second path
  exists at `platform.claude.com/plugins/submit`** (Console form, reported available to Max), and PM's
  screenshot showed **"Piper morgan" already installed** with an **"Upload plugin"** option.
  ⚠️ **Not resolved, deliberately**: that is a *Plugin* surface. Per the glossary, **Connector ≠ Plugin** —
  so it bears on **Track B** and does not self-evidently clear **Track A**'s gate. **The ask for PM is now:
  which surface is that "Upload plugin" option, and what is "Piper morgan" already listed as?** PM holds
  the screenshot and the account. *(Do not re-collapse this into a tier check — that conflation is how
  the original error propagated.)*
- 🟡 **Open-source decision for the Claude plugin package (CLAUDE.md + hooks + skills) — PM's call, not
  yet made.** A public GitHub repo is a hard requirement for Track B (full plugin). **Not time-critical
  the way the two above are**: Track A gets a Claude listing without it. PA can write up the tradeoffs
  on request.
- 🔴 **PDR-006 cannot ratify until Q2 is answered — and Q2 had been sitting in a "collect later" list.**
  *(Upgraded from 🟡 on 7/26: the PDR's own author flagged during handoff that Q2 is a **blocker**, not a
  footnote.)* Q2 = does building the colleague model require **server-side LLM inference**? If yes, the
  **"no server LLM" premise the whole hosted-MCP phase rests on shifts.** Now marked as a ratification
  blocker in the PDR's Status line, not just its Open Questions. Two caveats recorded there: the A/B
  framing was pattern-matched from PDR-005 rather than derived (so "neither" is a legitimate answer), and
  Arch flagged it as the *same concept* as the spatial review's "connectors as places with colleagues" —
  the two shouldn't be decided in isolation. Review has sat 7 days; CXO names it their most substantive
  unowned work, queued behind the #1386 gate run. **No PM action needed unless it stays stuck.**
- 🟠 **#1351's carry-forward is an INCOMPLETE AUDIT, not a design note — and it reads passively today.**
  The anonymous-caller state-isolation audit was started and abandoned before the issue was closed as
  superseded. `ConversationDB` is verified safe; **Redis, in-process floor/context state, and
  rate-limiting under anonymous-caller conditions were never traced.** Escalated to Arch to verify
  **before the hosted MCP endpoint goes live**. *(No PM action — tracked so it can't quietly lapse again.)*

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
