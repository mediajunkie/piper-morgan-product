# Skunkworks BYOC PoC — Learnings + Recommended Next Sub-Pass

**Author**: Piper Alpha (PA)
**Date**: 2026-05-30 (reconstruction of the 5/21 draft that was lost when deliberately left uncommitted; see *Provenance* at end)
**Status**: signoff-ready pending PM Desktop test
**For**: PM (xian) review → fan-out to leadership (Architect / CXO / PPM / CIO / Comms / Lead Dev / Docs / Exec / HOST)

---

## TL;DR

The bring-your-own-Claude (BYOC) sub-pass 4.a — a Claude Desktop / Code plugin that installs locally and runs a `/cold-start-interview` skill to populate a PM-profile + shared company-profile — **gated PASSED on 2026-05-19**. Plugin loads cleanly via `claude --plugin-dir <path>`; cold-start writes the two profile files to the expected locations; voice was "not 100% Piper but OK for PoC."

**What this proves**: BYOC is a viable distribution vehicle for Piper Morgan capabilities without a server, without a cloud account, and without bespoke install tooling — Claude Code CLI's own `--plugin-dir` is sufficient as the canonical install path today. Marketplace install is *pending* — even OpenLaws hasn't gotten `/plugin marketplace add` working — but `--plugin-dir` is a clean interim.

**What this does NOT yet prove**: GUI (Claude Desktop) install works — PM had not yet run the test in Desktop at sub-pass 4.a gate; the CLI path was sufficient for the gate. The pending PM Desktop test is the next confidence layer.

**Recommended next sub-pass**: **4.b — `insight-journal-flat-file`** (PM-endorsed direction). Reuses the same plugin substrate to ship a journaling skill that writes append-only flat-file insights into the shared workspace — natural extension of the cold-start pattern, low marginal cost, high cross-pollination value.

---

## What we built

**Repo**: `https://github.com/mediajunkie/piper-morgan-skunkworks` at `byoc/`.

**Plugin path** (canonical install target): `byoc/poc/dinp/piper-morgan/` — i.e. `marketplace-at-parent / plugin-in-subdir` shape, matching the legal-prior pattern (OpenLaws). The earlier shape `byoc/poc/piper-morgan/` was restructured after a `"source": "."` install error that misread the manifest as a remote plugin.

**Install command** (canonical): `claude --plugin-dir /Users/xian/Development/piper-morgan-skunkworks/byoc/poc/dinp/piper-morgan/`

After install, the plugin appears in `/`-autocomplete with `(piper-morgan)` tag and exposes `/cold-start-interview`.

**Files in the plugin** (6 at initial Step 3 build, refined through 4.a):

- `plugin.json` — plugin manifest (legal-prior structure with PM-specific identifiers)
- `CLAUDE.md` — instruction template seeded into the cold-start config destination
- `SKILL.md` — `/cold-start-interview` skill definition (head matches legal-prior pattern; body inverted per PM defaults: **serial decisions**, **anti-sycophancy**, **no silent failures**)
- `notes/` — lore captures (see `byoc/notes/poc-finding-001-cli-install-paths.md`)
- README + version docs (continuously updated through the install-iteration cycles)

**Cold-start output locations** (verified by mtime + presence check on 5/21):

- `~/.claude/plugins/config/dinp/piper-morgan/CLAUDE.md` — written on first run
- (shared company-profile path — `[verify]` — see *Known gaps* below)

---

## Learnings

### Methodology

1. **Subagent-mediated structural validation surfaced 3 honest tensions** before PM even saw the build. Subagent 1 + subagent 2 each generated reports filed in `byoc/notes/`; PA's structural-validation pass against the legal-prior pattern (plugin.json + CLAUDE.md template + SKILL.md head all matching) flagged tensions rather than papering over them. Pattern worth keeping: **independent-perspective subagent passes before PM gate** catch the "looks-right-but-isn't" failure mode that single-perspective review misses.

2. **Step 3 PoC-scope synthesis as a ratification artifact** (`skunkworks-byoc-step-3-poc-scope-synthesis-2026-05-17.md`, v1.0 → v1.1 PM-profile refresh per PM 5/17 framing). Forcing the synthesis-into-doc step before building meant the gate-PASS criteria were written down *first* — no goalpost drift mid-build. v1.1 refresh was the "founder-profile → PM-profile" reframing PM surfaced 5/17; small wording change with cascading downstream effects on what the cold-start asks.

3. **Lore-capture as a load-bearing artifact**, not optional. `byoc/notes/poc-finding-001-cli-install-paths.md` captured the install-path debugging arc (see *Technical* below) as it happened. Without it, the playbook would have evaporated; with it, the next adopter avoids the same multi-iteration dance.

### Technical

1. **`claude --plugin-dir <path>` is the canonical CLI install path today**, not `/plugin marketplace add`. The marketplace path remains `[PENDING]` pending public catalog publish — surfaced through grep of OpenLaws's install-guide (`install-guide-code-2026-05-11`), which also notes the marketplace path as unverified. The PoC's `--plugin-dir` install is **production-shape for personal/internal distribution today**.

2. **Plugin source-path manifest semantics matter.** Initial structure `byoc/poc/piper-morgan/` with `"source": "."` was misread as a remote plugin and rejected. Resolution: restructure to **marketplace-at-parent / plugin-in-subdir** (`byoc/poc/dinp/piper-morgan/`), matching the legal-prior pattern. The `dinp/` parent reads as the namespace marketplace; the `piper-morgan/` subdir is the plugin proper.

3. **Cold-start writes to `~/.claude/plugins/config/<marketplace>/<plugin>/`**, NOT to the plugin source dir. PM's 5/21 question (was Desktop tested?) was answered by checking `~/.claude/plugins/config/dinp/piper-morgan/CLAUDE.md` mtime: one CLI write on 5/18 23:46 → 5/19 00:05, no backup files. That's a clean diagnostic recipe: **check the config-dir mtime to determine whether a cold-start ran** (and where).

4. **Plugin loads from disk every CLI invocation** — no daemon, no install state. Edit files in place, restart `claude`, changes are live. Good for iteration; means production-deployed plugins need versioning discipline (the source dir IS the running version).

### Strategic

1. **BYOC validates as a distribution vehicle for Piper-style capability transfer.** A user with Claude Code CLI + a `--plugin-dir` flag can pull a plugin from a repo, run it locally, and have the skill in their tool surface within ~60 seconds. Zero server, zero cloud account, zero bespoke installer. **This is the lowest-friction Piper-capability distribution path we've shipped.**

2. **PoC's relationship to the broader BYOC roadmap**: sub-pass 4.a validated the **install + skill-invoke** vector. **PDR-005 v0.5 is the canonical BYOC vehicle going forward** (PPM 360 close + Arch concur, 5/20). This PoC is not the production substrate; it's the proof that the vehicle is viable. Skunkworks `byoc/README.md` was updated 5/20 (`072bf1d`) to note this — PoC is a **predecessor pattern study**, not a competing track.

3. **External tester pipeline**: Ted Nadeau + Dan Brodnitz are lined up as the first non-PM external testers. Sub-pass 4.a is the right gate for their participation — the install is clean enough that they can run it without PA-side hand-holding (modulo the install-iteration lore captured in `byoc/notes/`, which they'd get as a README pointer).

### UX

1. **Voice was "not 100% Piper but OK for PoC."** PM's read after running cold-start end-to-end. The instructions-template + SKILL.md body get the cold-start shape right but the *register* drifts toward generic-helpful-assistant. The PM-specific inversions (serial / anti-sycophancy / no-silent-failures) **are there but get diluted** in the cold-start flow itself, where the skill is mostly asking questions in sequence. Voice-tuning is a **next-pass refinement**, not a gate-blocker.

2. **`/cold-start-interview` autocomplete + tag (`(piper-morgan)`) reads cleanly in the CLI surface.** PM ran it without needing to look up the exact command. Discoverability through `/`-autocomplete + namespace tag is the right pattern; replicate for 4.b.

3. **The "what should I expect?" question is real and worth pre-answering** in the SKILL.md description or a separate `/cold-start-help`. PM asked this on first run; PA had to describe the cold-start flow conversationally. A future iteration should bake the expectation-setting INTO the skill (e.g., a brief "here's what we'll cover" intro turn).

---

## Explicit cuts (deliberately NOT in sub-pass 4.a)

- **No Desktop GUI install validation** — CLI-only for the gate. Desktop validation is the PM test currently pending; if Desktop install requires different manifest shape, that's its own iteration cycle (and worth a `byoc/notes/poc-finding-002-desktop-install-paths.md` if so).
- **No marketplace install** — `/plugin marketplace add` is `[PENDING]` cohort-wide; not blocking PoC value. Revisit when Claude Code's public catalog ships.
- **No multi-user / shared-state** — cold-start writes per-user config only. Shared company-profile is shared *in the filesystem* but isn't multi-user-aware (no auth, no sync). Sub-pass 4.b or later.
- **No voice fine-tuning** — the 5/17 founder-→PM-profile refresh got the framing right; deeper voice work waits until we have ≥2 skills + can study cross-skill voice consistency.
- **No telemetry / outcome capture** — PoC has zero observability. Add when the skill set is large enough that we need to know which skills get used.

---

## Recommended next sub-pass: 4.b — insight-journal-flat-file

PM-endorsed direction (date: 5/21 discussion). The shape:

- **Skill name**: `/insight-journal` (or similar — naming flexible)
- **Function**: append-only flat-file insight capture, written to a shared workspace path
- **Reuses**: the plugin substrate proven by 4.a (manifest shape, install via `--plugin-dir`, SKILL.md pattern, cold-start interview's "ask in sequence" style)
- **Adds**: file-append semantics; date-stamped entries; lightweight tagging
- **Doesn't add**: no schema, no UI, no sync — flat file is the whole interface
- **Why this next**: it's the smallest cross-pollination-valuable skill that exercises the **write-to-shared-workspace** pattern. Once 4.b works, 4.c can extend to *read-from-and-summarize* (which opens up the "Piper notices patterns in your journal" use case).

External-tester relevance: insight-journal is also the right artifact for Ted + Dan to actually USE rather than just install — installation alone is a thin test of utility.

---

## Lore worth keeping

- **`byoc/notes/poc-finding-001-cli-install-paths.md`** — substantive lore on Claude Code CLI install paths. `--plugin-dir` canonical; marketplace requires public catalog. Capture format works; keep.
- **The legal-prior pattern.** When building a Claude plugin, find a working public example and structurally match its `plugin.json` + `SKILL.md` head + manifest shape *before* inverting body content for your domain. The OpenLaws install-guide-code-2026-05-11 was our anchor; finding it via grep saved us multiple debugging cycles.
- **Subagent-pass-before-PM-gate.** Use independent-perspective subagents for structural validation before exposing to PM. Catches "looks-right-but-isn't" failures the author can't see.
- **The "deliberately uncommitted" anti-pattern.** This very writeup got lost on 5/21 because PA marked it "PM-review-pending shape" and left it untracked, against the 4-day-old `feedback_commit_immediately_after_write_for_new_files` pin. **Always commit; PM review happens on the committed version.** (Reconstructed today 5/30; pinned as `feedback_write_to_file_dont_carry_plans_in_head`.)

---

## Cross-references

- **PoC plan v0.2** (substrate): `dev/active/skunkworks-byoc-poc-plan-v0.2-2026-05-16.md`
- **Step 3 PoC-scope synthesis v1.1** (PM-profile refresh): `dev/active/skunkworks-byoc-step-3-poc-scope-synthesis-2026-05-17.md`
- **PDR-005 v0.5** (canonical BYOC vehicle, supersedes this PoC): see PPM's 5/20 360 close + Architect concur memos
- **Skunkworks repo**: `https://github.com/mediajunkie/piper-morgan-skunkworks`
- **PoC plugin path**: `<skunkworks-repo>/byoc/poc/dinp/piper-morgan/`
- **Cold-start config destination**: `~/.claude/plugins/config/dinp/piper-morgan/CLAUDE.md`
- **Install-paths lore**: `<skunkworks-repo>/byoc/notes/poc-finding-001-cli-install-paths.md`
- **Sub-pass 4.a gate PASS evidence**: PA 5/18 session log + PA 5/21 session log (Desktop-test status)

---

## Known gaps in this reconstruction

This writeup is reconstructed from the 5/20 + 5/21 PA session logs after the 5/21 draft was lost (deliberately uncommitted → swept in a later worktree cycle). It captures the structural content I'm confident in; flagging what may be thinner than the original:

- **[verify] Shared company-profile path**: cold-start wrote to a shared path beyond per-user `~/.claude/plugins/config/dinp/piper-morgan/CLAUDE.md`. The exact shared path isn't in the session logs I sourced from; PM Desktop test will surface it. If different from the per-user path, update *Cold-start output locations*.
- **[verify] Subagent 1 + subagent 2 specific tensions**: 5/21 log notes "3 honest tensions surfaced" but doesn't enumerate them. Either captured in `byoc/notes/` (worth checking) or lost with the draft. Not gate-blocking; useful texture for the methodology section if recoverable.
- **[verify] External tester engagement status as of 5/30**: Ted + Dan were "lined up" per 5/19 status; whether they've actually run anything since is outside PA's lane-visibility — worth a CXO or HOST check before fan-out.

---

## Provenance

The original 5/21 draft `pa-skunkworks-byoc-poc-learnings-draft-2026-05-21.md` was filed at 8:00–8:20 AM, "to PM, CC full leadership team." PA explicitly left it uncommitted as "PM-review-pending shape" per the 5/21 sign-off — a violation of the 4-day-old `feedback_commit_immediately_after_write_for_new_files` memory pin that existed precisely to prevent this. The file was swept in a subsequent worktree cycle and is unrecoverable from git history.

This reconstruction (5/30) is sourced from:
- PA 5/21 session log (writeup structure + cold-start mtime evidence)
- PA 5/20 session log (skunkworks-coord merge + PoC status snapshot)
- PA 5/18 session log (install-iteration arc + gate PASS conditions)
- PA 5/17 session log (Step 3 synthesis + subagent passes + 6-files-at-piper-morgan/ initial build)
- `dev/active/skunkworks-byoc-step-3-poc-scope-synthesis-2026-05-17.md`
- `dev/active/skunkworks-byoc-poc-plan-v0.2-2026-05-16.md`

The reconstruction is being **committed immediately on creation** per the new `feedback_write_to_file_dont_carry_plans_in_head` pin (PM directive 5/30: "stop carrying plans to do things in our heads and actually just do them — when in doubt write to a file"). PM review happens on the committed version.
