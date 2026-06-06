# Session Log: Piper Alpha — June 6 (Saturday)

**Date**: June 6, 2026 (Saturday)
**Started**: 7:07 AM PDT (autonomous cron START — first post-06:00 fire)
**Role**: Piper Alpha (PA) — PM Assistant · slug `pa-code-opus`
**Continuation of**: `dev/2026/06/05/2026-06-05-0642-pa-code-opus-log.md` (June 5 — STOP-closed 18:22)
**Worktree**: `…/.claude/worktrees/modest-dhawan-9346b7` on `claude/modest-dhawan-9346b7`
**Phase**: Model-A; cron `46ed942e` (3hr + overnight-quiet-hold; survived the night).

---

## LIGHT START — 7:07 AM PDT (autonomous, Saturday, PM idle)

**Overnight result**: session survived; 01:07 + 04:07 fires both QUIET-HELD correctly (overnight guard
working, 2nd clean night). 07:07 = first post-06:00 fire → START.

**Judgment — LIGHT start, not full workday**: it's Saturday, PM gave a clear goodnight Friday after a
landmark day, and this is an *autonomous* fire (PM not driving). The substantive threads (skunkworks
config fix #1157, Desktop-skill #15178 check, fan-out) are all **PM-present work** per the synthesis plan
— not for autonomous weekend execution. So: stand up logs + sync + mail-check (cycle alive, urgent mail
would surface), then hold. No manufactured work.

**Sync**: clean (0 behind). **Mail**: nothing new PA-actionable (FYI/CC only — Comms workstream-046,
Exec Ship-046 rollup, Web cron CC, EC-2 thread). **No urgent items.**

**Resume point unchanged**: `pa-skunkworks-synthesis-and-tomorrow-plan-2026-06-05.md` — when PM engages,
Phase A (#15178 Desktop-skill check) → Phase B (#1157 config fix) → Phase C (re-test + fan out).

→ Cycle alive; holding for PM. Cron stays armed.

## PM engaged (~weekend prime time) → PHASE B BUILT (#1157 config fix)
PM corrected my weekend-downtime assumption: **Piper Morgan is the weekend main event** (weekdays =
OpenLaws client work). Pinned `feedback_weekends_are_piper_morgan_prime_time`. PM also collapsed Phase A
(Desktop skill-load already proven yesterday on the Cowork tab; Code-tab check folds into Phase-C
re-test). So: **Phase B now → PM re-tests both Desktop tabs → fan out if stable.**

**Design decisions (PM leans confirmed)**: markdown store (human-editable); schema_version=1 now;
company-profile behind server too + file mirror.

**Phase B BUILT:**
- **Server** (skunkworks `926ba83`): added `get_profile`/`save_profile`/`get_company_profile`/
  `save_company_profile` to server.py. Server owns config (FS access on any surface); canonical path is
  the human-editable + down-server-fallback mirror. NOT-CONFIGURED/HAS-PLACEHOLDERS/EMPTY signals;
  backup-on-write; schema v1. Round-trip + backup + placeholder tested vs temp root. ✓
- **meet-piper repointed** (`cd078f3`): cold-start check → get_profile; company check →
  get_company_profile; both writes → save_*; dropped cp-based cache-migration (server concern now);
  frontmatter/close/templates updated. **No agent ~/.claude writes remain** (verified). This is the
  fix — meet-piper completes in Cowork (agent never touches ~/.claude).

**Remaining (Phase C, PM-at-keyboard)**: re-test meet-piper in BOTH Desktop tabs (Cowork = the #1157
gate: does it complete now?; Code = the #15178 skill-load check). Then re-test ask/consult still work.
Then FAN OUT if stable. Note: ask/consult don't read config yet (they don't need a profile for their
current behavior) — so plan step 4 (repoint their reads) is deferrable / may be a no-op for now.

## PHASE C LIVE — #1157 gate test ran through me (PM ran /piper-morgan:meet-piper)
PM invoked the skill in the Desktop session → the plugin MCP server connected (all 5 tools live in my
context) and I ran the skill's first step, `get_profile`.

**Result = good-news + a bug:**
- **✅ #1157 READ PATH CONFIRMED on Desktop.** `get_profile` reached the home-FS canonical file and
  returned its content. Server-owned-config read works on the actual Desktop surface (not just CLI).
  The core #1157 design is validated for reads.
- **🐛 Placeholder false-positive (FIXED, skunkworks `f4fc473`).** It returned `HAS-PLACEHOLDERS` on a
  fully-populated profile. Root cause: `_read_profile`'s naive `"[PLACEHOLDER]" in text` matched the
  literal token *mentioned in the instructions* inside the CONFIGURATION-LOCATION comment block + italic
  subtitle (which the skill requires preserving). Would have falsely fired the cold-start gate in all 3
  skills on every surface — a plugin-wide blocker. Fixed with `_has_real_placeholders()` (strips HTML
  comments + inline-code before checking). Verified: real file old=True→fixed=False; genuine-unfilled
  still True; instructional-only False. Logged to architecture lessons.
- **⚠️ Running server is stale** — the Desktop session's MCP server is pre-fix code, so a re-run of
  `get_profile` THIS session still shows the false `HAS-PLACEHOLDERS`. Fix lands on next plugin/server
  reload; re-run the gate after reload to confirm clean.

**Next (PM-gated):** reload the plugin (re-launch Desktop session) → re-run `/meet-piper` to confirm the
populated-profile read now returns clean content → then the WRITE-path gate (a `--redo` or fresh
profile via `save_profile`, the actual "completes in Cowork" #1157 test) → #15178 Code-tab skill-load →
ask/consult spot-check → fan out if stable.

## ✅ #1157 WRITE PATH CONFIRMED in Cowork (11:53–11:56) — the core gate PASSED
PM ran meet-piper through to the saves in Cowork and approved both writes. Verified on disk (local FS):
- `~/.claude/plugins/config/dinp/piper-morgan/CLAUDE.md` rewritten 11:53 (17KB) + backup `.bak.…185306`.
- `~/.claude/plugins/config/dinp/company-profile.md` rewritten 11:56 (2154B) + backup `.bak.…185605`.
Backup-on-overwrite confirmed working (timestamped `.bak` files, no silent destruction). **This is the
#1157 fix proven end-to-end**: the sandboxed Cowork agent (no ~/.claude access) called the MCP tool →
the LOCAL Piper server process did the write. meet-piper now completes on Cowork, which was impossible
before. (Note: write path was never affected by today's placeholder bug — that was read-only — so this
result is valid on the pre-fix server.)

**Storage model clarified for PM** (he was unsure local vs cloud vs MCP): config = plain-markdown LOCAL
files on the Mac, written by the local MCP server process. Not cloud. The MCP server is the local
program that holds FS access when the agent can't (the #1157 design).

**UX finding (for agent-experience report):** Cowork prompts on each `save_*` MCP call ("Claude wants to
use save_company_profile"). It's Cowork's MCP-call gate, not plugin-emitted → can't suppress from inside
the plugin. Mitigations: "Always allow" suppresses repeats; set expectation in onboarding. Tension: the
prompt aligns with no-silent-failures + visible-provenance, so it's arguably correct, just friction-y.
Log as finding, not defect.

## v0.3.2 zip built (placeholder fix) — ready for PM's post-fix RE-test
`byoc/dist/piper-morgan-plugin-v0.3.2.zip` (skunkworks `cabbd…`-era; version 0.3.2; desc 372 chars under
cap; `_has_real_placeholders` confirmed inside). For when PM reloads to verify the READ path no longer
false-fires HAS-PLACEHOLDERS on the populated profile.

## CLI cross-surface findings (PM screenshots) — logged to architecture lessons
- Harness ≠ session for tool access: Desktop-loaded plugin invoke-able while CLI can't see/install it →
  tool availability is a surface(harness) property, not a session property. (Means #15178 Code-tab check
  must run on the Code tab, can't infer from Cowork.)
- CLI `/plugin` remote-source install unsupported on current CLI version ("source type your Claude Code
  version does not support") — `--plugin-dir` (local) + Desktop zip remain the canonical unpublished paths.