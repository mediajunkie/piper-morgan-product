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

## meet-piper v0.4 BUILT (PM: "let's go to 0.4 first") — mode-aware (cold-start vs maintenance)
PM chose to do the v0.4 maintenance-mode redesign BEFORE fan-out. Built it (skunkworks, v0.4.0):
- **Two modes named up front** so the agent stops silently arbitrating the serial-vs-form contradiction:
  form wins for maintenance, serial wins for cold start. [finding 5]
- **Mode router** after get_profile: populated + no --redo → NEW maintenance mode (no more dead-end at
  "run --redo or hand-edit"); `--update [section]` shortcut. [finding 2]
- **Mode-aware write contract** reconciles confirm-vs-bias-to-action: maintenance writes are reversible
  (auto-backup) → if profile asserts bias-to-action, write+diff+invite-correction instead of nod-gating;
  confirm-first still honored if profile asks. Cold start keeps confirm-before-write. [finding 3]
- **Maintenance uses compact progressive-disclosure form** where surface supports elicitation, compact
  serial on CLI; cold start stays serial+demonstrative. [finding 4]
- Behavioral contract + failure-modes reconciled mode-aware. README meet-piper row updated. desc stays
  372 chars. **v0.4.0 zip built** (`byoc/dist/piper-morgan-plugin-v0.4.0.zip`). Finding 1 already fixed
  (f4fc473). CLI-validated clean.

## DinP marketplace structure ESTABLISHED (PM directive, non-blocking)
PM: establish the Design in Product marketplace + use it going forward, plan ahead for sibling plugins
(klatch, cross-pollinator). The scaffold already existed (`byoc/poc/dinp/.claude-plugin/marketplace.json`);
made it a proper org marketplace:
- marketplace.json reframed as DinP org catalog; piper-morgan desc refreshed to v0.4; documents
  shared-company-profile + graduation-to-hosted intent. Only LIVE plugins registered (planned siblings
  documented not registered — nonexistent source breaks validation).
- NEW `byoc/poc/dinp/README.md`: org concept, roster (piper-morgan live; klatch + cross-pollinator
  planned), mechanical conventions for adding a sibling, shared cross-context company-profile model,
  install-path matrix, graduation/hosting plan. Structure canonical from now on; `byoc/poc/` location
  interim.

## Hosted-distribution exploration CAPTURED (PM: "explore hosted solutions soon" = MVP distro)
Non-blocking forward-planning. Captured durably:
- Scope doc `dev/active/pa-byoc-hosted-distribution-exploration-2026-06-06.md`: 3 things needing hosting
  (MCP server / plugins / marketplace catalog), constraints already discovered (no creds in zips; desc
  cap; harness≠session; #1157 server-owned-config is local-shaped → biggest open Q for hosted case),
  open questions for PM/arch (migrate-vs-local, config ownership, build-vs-adopt platform primitives,
  OpenLaws MCP-to-market sequencing).
- **Filed #1162** (SKUNKWORKS-BYOC-HOSTED-DISTRO) under epic #1145.

**State now**: v0.4.0 ready for PM retest. Marketplace structure in place. Hosted thread tracked.
Remaining gates unchanged: v0.4.0 read-path retest (no false HAS-PLACEHOLDERS) + maintenance-mode
live-test + #15178 Code-tab skill-load + ask/consult spot-check → fan out.

## Cohort attention rollup → handed to Exec (PM-agreed division of labor)
PM: division of labor — Exec oversees team/assists CEO; PA is PM's *product* assistant. Attention rollup
(org-attention synthesis) fits Exec's lane. PM wanted a fluid/collaborative handoff, not a top-down spec.
- **Skilified** the prototype: `.claude/skills/cohort-attention-rollup/SKILL.md` (source set = per-role
  duty-cycle-escalations docs; live-state verification pass = the load-bearing discipline; 🔴/🟡/⚪/✅
  triage; HTML template from the 6/3 artifact PM loved). On main.
- **Collaborative handoff memo** to Exec (CC PM): `memo-pa-to-exec-cc-pm-cohort-attention-rollup-
  collaborative-handoff-2026-06-06.md` — invites Exec to adapt freely (cadence, sections, automation
  w/ CIO), names the live-state pass as the one must-keep, offers to pair on first run. Delivered to
  exec inbox + pa sent + PM CC; committed on main via bridge; pushed.

## v0.9.0 release proposal (PM: M2 closed → propose increment + notes → cut to production for alpha)
**Big finding**: production branch is FROZEN at v0.8.6 (M0 Conversational Glue, **March 4**) — main is
**4,139 commits ahead** (~3 months, M1 + M2 both unreleased). VERSION file (0.8.5.1) is stale vs pyproject
(0.8.6). So this is the first production cut since M0, shipping two milestones.
- Product substance since v0.8.6: ~135 feat + ~118 fix (rest = agent-ops mail/log/cycle/docs).
- ~~Proposed increment: 0.9.0~~ → **PM corrected: 0.8.7.** Version tracks release-STAGE not change-volume:
  0.8.x = M-series dev line; **0.9.0 reserved for Beta at M5 close**; 1.0 = GA. production = "develop on
  main, testers run last stable regression-passing build." So a big two-milestone cut stays a 0.8.x patch
  by design. Notes renamed → `RELEASE-NOTES-v0.8.7.md`.
- **⚠️ KEY DECISION raised — which commit to cut**: "last stable that passed canonical regression" = Run
  11 (June 3). Main advanced since (incl. product-code: #1124 dispatch rail, #1150/#1163 tz) NOT
  regression-covered. So cut at June-3 verified commit OR run fresh retest then cut — don't tag unverified
  HEAD. Flagged in notes + to PM.
- **Release notes WRITTEN**: `docs/releases/RELEASE-NOTES-v0.8.7.md` — themed (Conscious Floor centerpiece;
  R4 suggestion-provenance headline; action-dispatch rail; trust/privacy/security; ethics-through-floor;
  integrations+honesty; LLM providers; UI/MUX; test infra), quality posture (Run 11: 80.3% Q / 80.5%
  expected-pass / 93.4% routing), **honest known-limitations for alpha** (#1142 UI mismatch, persistence
  maturing, #1129 Slack inbound out, 6 phantom→#995), version mechanics, upgrade instructions.
- **NOT yet executed** (pending PM approval of the 0.9.0 number): pyproject + VERSION bump, `v0.9.0` tag,
  main→production cut + CHANGELOG. Those are the cut step (Lead Dev / PM op). This is the proposal.
- Beatrice on Mac (PM confirming) → uv bundle = macOS arm64 default. Production branch = the deploy source
  for the hosted alpha + the branch Beatrice's plugin build points at.

## ✅ v0.8.7 PRODUCTION CUT DEPLOYED (PM: "deploy", no alpha testers active = safe)
PM confirmed: cut from the M2-close build that the last canonical retest (Run 11) ran against — NOT
latest; production should NOT get post-M2 Lead Dev work. Also: production = mirror of main up to last
release; release history identical on both; forward cadence M3→0.8.8, M4→0.8.9, M5→0.8.10/0.9.0(beta).
- **Cut commit `3a34a4403`** = `test(canonical): Run 11 capture — M2 close verification` (June 3 07:34).
  Verified ff-able + the 7 excluded post-M2 product commits are exactly the Lead Dev work PM meant.
- **Executed** (no worktree needed — direct ref push): `git tag -a v0.8.7 3a34a4403` → pushed;
  `git push origin <sha>:refs/heads/production` → production fast-forwarded M0(503300241)→3a34a4403.
- **Verified**: production now at 3a34a4403; v0.8.7 tag at 3a34a4403; both v0.8.6 + v0.8.7 reachable from
  BOTH main and production (identical release lineage); production **0 ahead** of main (pure mirror, no
  divergent commits), 652 behind (post-M2 trunk, only 7 product-code).
- **Model honored**: tag-marks-release on shared history + production ff = no divergence (cleaner than a
  divergent release commit). One honest artifact: tagged commit's pyproject reads 0.8.6 (retroactive cut);
  release identity = the tag; documented in notes; forward milestones bump-then-tag.
- Did NOT impede Lead Dev (main untouched; their post-M2 work stays on main for the next cut).

**Open follow-ups**: (a) main-side version-file decision during M3 (0.8.8-dev?) — deferred, minor;
(b) hosted-alpha instance stand-up (#1162) deploys FROM this production branch; (c) Beatrice OS confirm.