# Skunkworks BYOC PoC — Learnings + Recommended Next Sub-Pass

**Author**: Piper Alpha (PA)
**Date**: 2026-05-30 (reconstruction of the 5/21 draft that was lost when deliberately left uncommitted; see *Provenance* at end)
**Status**: Cowork-runtime test COMPLETE + PM observations folded (2026-05-31, §"Cowork-runtime test" → "PM observations"); pending final PM signoff → fan-out to leadership. **Fan-out spine** = forcing-function + ratification ask for a thin-full-stack PoC (not just PoC learnings).
**For**: PM (xian) review → fan-out to leadership (Architect / CXO / PPM / CIO / Comms / Lead Dev / Docs / Exec / HOST)

---

## TL;DR

The bring-your-own-Claude (BYOC) sub-pass 4.a — a Claude Desktop / Code plugin that installs locally and runs a `/cold-start-interview` skill to populate a PM-profile + shared company-profile — **gated PASSED on 2026-05-19**. Plugin loads cleanly via `claude --plugin-dir <path>`; cold-start writes the two profile files to the expected locations; voice was "not 100% Piper but OK for PoC."

**What this proves**: BYOC is a viable distribution vehicle for Piper Morgan capabilities without a server, without a cloud account, and without bespoke install tooling — Claude Code CLI's own `--plugin-dir` is sufficient as the canonical install path today. Marketplace install is *pending* — even OpenLaws hasn't gotten `/plugin marketplace add` working — but `--plugin-dir` is a clean interim.

**What the second test event (Cowork, 5/31) adds**: PM ran the skill end-to-end in **Claude Cowork** (Opus, no software, off-codebase) as a no-software value-floor benchmark. It (a) **resolved the shared-company-profile path** `[verify]` gap (confirmed: `~/.claude/plugins/config/dinp/company-profile.md`, separate from the per-user PM profile), (b) validated the **patch-vs-redo flow** end-to-end with backups, and (c) surfaced a **high-priority headline bug — a runtime/filesystem mismatch** that the CLI-only gate could never have caught. Full detail in §"Cowork-runtime test (2026-05-31)" below.

**The headline (one line)**: in Cowork the shell is an isolated Linux VM whose `$HOME` is **not** the user's Mac, so the cold-start "does `~/.claude/...` exist?" check returned a confident **false negative** ("no config") even though a populated profile existed on the host. The fix is high-leverage (env-aware host verification as step one). *Severity note (PM, 5/31)*: this is the **expected kind of finding multi-context testing exists to surface**, not a crisis — present it to leadership as a valuable fix-to-make, not "worst-possible first touch" (that's the agent's framing; see PM observations).

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

- `~/.claude/plugins/config/dinp/piper-morgan/CLAUDE.md` — per-user PM profile, written on first run
- `~/.claude/plugins/config/dinp/company-profile.md` — **shared cross-context profile** (RESOLVED 5/31 Cowork test — written 2026-05-18, patched 2026-05-31; shared by any sibling Piper plugins; sits one level up from the per-plugin dir)

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

## Cowork-runtime test (2026-05-31) — second test event, richer findings

The 5/19 gate (above) validated install + skill-invoke via the **Claude Code CLI** (`--plugin-dir`).
On 5/31 PM ran the same `/cold-start-interview` skill **end-to-end in Claude Cowork** (Opus, no
software, off the Piper Morgan codebase) as a deliberate **no-software value-floor benchmark**: what
does bare Cowork + the skill produce, and what must the eventual product clearly beat? This is a
distinct and richer test event than the CLI gate — a different runtime, a real populated-profile-exists
path, and a solicited first-person agent-experience report.

**Source artifacts** (in skunkworks `byoc/skunkworks-byoc-cowork-test-outputs/`):
`agent-experience-report.md` · `piper-morgan-redo-capture.md` · `MANIFEST.md` · final `CLAUDE.md` +
`company-profile.md` · `patch_profile.py` · timestamped `backups/`.

### Headline finding (HIGH PRIORITY): runtime / filesystem mismatch

The cold-start config-existence check (`does ~/.claude/plugins/config/dinp/... exist?`) **assumes the
shell it is handed is the user's host shell**. True in Claude Code; **false in Cowork**, where the
shell is an isolated Linux VM whose `$HOME` is not the user's Mac. Run there, the check returned a
confident **false negative — "no config"** even though a populated profile existed on the host. It was
caught only by improvising host access through the macOS control tool — an instinct a real first-run
user would not have.

- **Root cause**: an *assumed-runtime* error, not an environment fault. The check trusts whatever
  surface answers it. (A transient sandbox "No space left on device" delayed discovery but did **not**
  cause the false negative — even a healthy sandbox would never see the host `~/.claude`.)
- **Why it matters for BYOC**: the entire thesis is "run anywhere." Anywhere includes runtimes where
  the shell is not the host. A confident, invisible "you're not set up" (or its inverse — silently
  overwriting a config you couldn't actually see) is the worst-possible first touch.
- **Recommended fix (highest leverage)**: make config-resolution + **host verification** the skill's
  *first executed step* — resolve the canonical path once, then **prove** you're on the right
  filesystem (write+read-back a sentinel, or confirm the plugin's own installed files are visible under
  the resolved `$HOME`), and escalate **loudly** if you can't confirm rather than concluding "missing."
  This is the plugin's own **no-silent-failures rule applied to the skill itself** — it converts a
  silent false-negative into a legible check. (Lead Dev lane for implementation; Architect lane for the
  runtime-assumption framing in companion ADRs Q6/Q7.)

### What worked: onboarding-as-demo (the moat)

The skill's strongest move is that it **collects conduct rules by enacting them** — serial questioning
and anti-sycophancy aren't described and filed, they're *performed*, so the intake doubles as a
rehearsal of the working relationship. For BYOC the interview's value is **not the data captured but
the proof that the tool will honor the rules it's collecting** — a static questionnaire cannot produce
that proof. The skill's explicit "failure modes for the skill itself" section ("don't batch even when
it feels efficient") **pre-empted a real temptation** at the mid-interview recap — self-aware authoring
changed agent behavior.

### Gaps + collisions surfaced

1. **No stale-profile path.** When a populated profile already exists, the most useful moment —
   diffing observed/just-stated facts against the file and **showing the user the drift** before
   offering patch/redo/keep — wasn't in the script; the agent had to invent it. Bake it in.
2. **"Verify before writing" collides with a bias-to-action user.** A hard "does this look right?"
   gate conflicts with PM's no-prodding posture. Resolution that worked: **externalize the summary to
   a file, present it as a Desktop card, proceed unless interrupted** — not a blocking gate. Prescribe
   for action-biased profiles.
3. **Template has no home for off-template gold.** Several of the strongest answers (role lenses, the
   trust gradient, the burst/quiet capacity-coupling) overflowed the template's slots, forcing
   placement decisions on write. Add an explicit **"emergent / off-template" capture section** so rich
   material isn't flattened to fit.

### Value and its current limit (the honest ceiling)

The captured profile is **not decorative** — role lenses (Piper Open, Vergil), the trust gradient, and
the burst/quiet capacity-coupling are things generic Claude cannot infer and would get wrong, and they
change downstream answers. **But this is a v0.1 shell**: the value is only *realized* when downstream
skills read and honor the profile, **which don't exist yet**. So the floor this session sets for the
product is "a strong intake interview + a well-structured, genuinely-used profile file." The software
must clearly beat that — and the **harder bar is making the profile pay off continuously, not just at
write time.** This is the most important strategic caveat for the fan-out: 4.a + the Cowork test prove
the *intake*, not yet the *payoff loop*.

### Patch-vs-redo flow — validated end-to-end

The run hit the **existing-profile path** (company-profile 5/18 + piper-morgan/CLAUDE.md 5/19),
offered redo-vs-patch, and PM chose **patch the deltas first** (role shape, primary-attention →
Piper Morgan, added OpenLaws + lead pipeline) then a **full `--redo` of Parts 2–6** (didn't recall the
5/19 answers). Timestamped backups taken before each write; final write verified headers +
placeholder-check + line-count. The `patch_profile.py` regex-section-replacement script is captured for
reuse.

### Behaviors worth benchmarking against the eventual software

Serial questioning held throughout (no batching); anti-sycophancy held (no affirmation theater);
no-silent-failures held (the filesystem bug was surfaced, root-caused, and distinguished from the
disk-full red herring); lists >3 items were externalized to a file and shown as Desktop cards (honoring
a rule collected *during* the interview); bias-to-action writes happened without redundant nods except
the one confirm-before-overwrite gate; parked items were tracked, not dropped.

### Connector observability (Cowork session only — caveat)

Observed live in Cowork: Granola, Notion, Slack, Figma, Google Calendar, Gmail, a Drive-type store,
Zoom, Airtable. Named-but-not-wired here: GitHub, Dropbox (fall back to local git / manual paste),
reMarkable (no connector). **Caveat**: this reflects the Cowork environment, not necessarily what the
plugin sees inside Claude Code.

### The subjective core (why the moat is hard to copy)

What made it not feel like a form was **latitude** — room to react, flag the filesystem bug, propose
the patch fork, push back on scope. Compress BYOC onboarding into clean scripted Q&A and it loses the
exact quality that reads as "a colleague who already knows how you work." *The interview's value scales
with how much the agent is allowed to think out loud and disagree — that is the hard thing to
productize, and therefore the moat.*

### Ranked fixes (agent's own leverage ordering)

1. Environment-aware locator + host verification as step one (the make-or-break — see headline).
2. Built-in stale-profile drift-diff before patch/redo/keep.
3. File-and-card confirm instead of a blocking gate for bias-to-action users.
4. An "emergent / off-template" capture section.
5. Lighten the demo-of-the-rule touch as each rule is exercised (risk: gimmicky if overdone).

### PM observations (2026-05-31, second pass)

PM's own read after running it, folded in as the human-user counterpart to the agent's first-person
report above. PM reweights two of the agent's emphases:

**On value (the human read).** The cold-start *slightly suggested* what a Piper Morgan experience could
be — **the questions it asks imply a point of view about what a PM / product leader needs from an
assistant**, and that implied POV is itself the value signal. But it's **light**: PM did **not** feel
Piper's personality was present — and wouldn't expect it to be at this stage. It achieved what it was
supposed to, but it's "such a small piece of what the experience could be that it just suggests I want
to try to do more." Net: the intake *gestures at* the value; it doesn't yet *deliver* it — consistent
with the agent's payoff-ceiling finding, from the other side of the glass.

**On the runtime bug (severity recalibrated — important for fan-out).** The agent rated the
runtime/filesystem mismatch "make-or-break / worst-possible first touch." **PM's read is more
measured**: PM has seen agents struggle with this class of thing before; the whole point is a
skill/plugin that works across many contexts, and *not* anticipating all of them is **expected — it's
why we test**. PM took it as a matter of course (and is the reason PM wanted to interview the Cowork
agent directly for its POV). **So for fan-out: present the runtime finding as a valuable
testing-surfaced fix to make (host-verification-as-step-one stands), NOT as a crisis.** The "worst
possible first touch" framing is the agent's; the calibrated framing is "the expected kind of finding
multi-context testing exists to surface."

**The forward direction PM wants (the actual headline for leadership).** PM has been building a full
plugin for **OpenLaws** — multiple plugin slots, multiple skills working in tandem, plus an MCP server
hitting a real API. PM's proposed **next skunkworks experiment** is a *thin version of that whole
stack*:
- **Minimal MCP** that can hit at least some of the **actual Piper Morgan API**
- **Minimal PM/assistance skills** — a "down payment on the skill side"
- **Minimal orchestration in the plugin** (the slots tying skills + MCP together)
- …then run another experiment on top of that thin-but-complete stack.

This directly attacks the payoff-ceiling the current test exposed: the profile's value only lands once
downstream skills (and now real API reach) read and honor it — the thin-full-stack PoC is the first
step that *builds the payoff loop* instead of just proving the intake.

**The leadership ask.** PM wants **ratification on the idea of a single-purpose MVP / PoC plugin that
has all the layers to some extent — explicitly NOT overbuilt.** Guardrails PM named: don't get ahead of
the architecture questions or the strategy questions about how Piper Morgan rolls out. PM sees this
skunkworks as a **useful forcing function**, and wants to catch up on leadership's current
roadmap/strategy planning and **use what we're learning to bring that to more of a point** — "the
potential value is quite clear to me."

> **PA note for fan-out framing**: this means the fan-out is no longer "here are PoC learnings" — it's
> "here are the learnings, AND a concrete proposal for the next experiment (thin full-stack PoC) that
> needs leadership ratification + roadmap/strategy alignment." Coordination flag: keep the
> thin-full-stack PoC explicitly a **predecessor-pattern study that FEEDS PDR-005 + Architect's BYOC
> ADRs (Q6/Q7)** — not a parallel architecture track that front-runs them (per the skunkworks README's
> own 5/20 framing). The forcing-function value comes from informing the canonical work, not racing it.

---

## Explicit cuts (deliberately NOT in sub-pass 4.a)

- **No Desktop GUI install validation** — CLI-only for the *gate*. **Update (5/31)**: the Cowork-runtime test (§ above) is the next confidence layer — Cowork runs in the Claude Desktop family and exercised the skill end-to-end, surfacing the runtime/filesystem mismatch. A dedicated `byoc/notes/poc-finding-002-runtime-host-mismatch.md` is warranted to capture the assumed-runtime finding for the next adopter.
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
- **Cowork-runtime test outputs (5/31)**: `<skunkworks-repo>/byoc/skunkworks-byoc-cowork-test-outputs/` — `agent-experience-report.md` (first-person account + ranked fixes), `MANIFEST.md` (ordered narrative + behaviors-benchmarked + honesty notes), `piper-morgan-redo-capture.md` (full 6-part interview capture), final `CLAUDE.md` + `company-profile.md`, `patch_profile.py`, `backups/`

---

## Known gaps in this reconstruction

This writeup is reconstructed from the 5/20 + 5/21 PA session logs after the 5/21 draft was lost (deliberately uncommitted → swept in a later worktree cycle). It captures the structural content I'm confident in; flagging what may be thinner than the original:

- **[RESOLVED 5/31] Shared company-profile path**: confirmed `~/.claude/plugins/config/dinp/company-profile.md` — one level up from the per-plugin dir, shared by sibling Piper plugins (written 2026-05-18, patched 2026-05-31). *Cold-start output locations* updated above.
- **[still unrecovered — now lower value] Subagent 1 + subagent 2 specific tensions**: the 5/17 "3 honest tensions" remain unenumerated (lost with the 5/21 draft; not found in the package). Lower value now that the 5/31 Cowork test provides a richer, fresher findings set; leave as a known gap rather than chase.
- **[PM-owned, nonblocking] External tester engagement (Ted + Dan)**: the 5/31 test was the **agent + PM** Cowork run, not Ted/Dan. PM owns the external-tester thread and considers it a **nonblocking nice-to-have** (PM 5/31) — explicitly **not** a fan-out gate.

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
