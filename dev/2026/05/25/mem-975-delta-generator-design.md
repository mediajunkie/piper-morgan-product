# MEM-975 Delta-Generator Design Note

**Purpose**: Design decisions for the "delta since last session" generator + SessionStart hook signal, per MEM-975 AC + Lead Dev's May 24 hybrid-mechanism routing.

**Author**: CIO Vehicle 2
**Date**: 2026-05-25 (Phase A pilot Fire 6 — 12oo design pass)
**Status**: design ratified; implementation = 12pp (script) + 12qq (hook extension)
**Within ratified shape** (PM-ratified hybrid: script + SessionStart hook signal per Lead Dev May 24 memo)

---

## Six design decisions (within implementer discretion)

### 1. Invocation cadence: **SessionStart hook calls script on-demand**

The SessionStart hook invokes the delta-generator script as a sub-step. No scheduled regeneration; no separate cron. Reasons:

- **Freshness**: the delta should reflect the gap since the last session ended — on-demand at session-start gives exact-time computation
- **Zero state to maintain**: no need to track when the last regeneration ran; the file is regenerated whenever the agent opens a session
- **Aligns with the cron-bind-to-IDLE discipline ratified today** — fewer scheduled processes; more event-driven

### 2. Scope-detection ("since agent's last session"): **filename-encoded timestamp from most recent session log**

The role's session log filename pattern is `dev/{YYYY}/{MM}/{DD}/{YYYY-MM-DD}-{HHMM}-{role-slug}-{tool}-{model}-log.md`. The HHMM portion encodes session-open time exactly.

Algorithm:
1. Find newest `*-{role-slug}-code-opus-log.md` file under `dev/`
2. Parse the YYYY-MM-DD-HHMM prefix → timestamp
3. Use that timestamp as the "since" cutoff
4. Fallback: 24h cutoff if no log found in last 7 days (matches May 17 audit's first-session-ever default)

**Why filename-encoded timestamp not file mtime**: file mtime gets bumped on every Edit (afternoon arc edits to morning's log update mtime to afternoon). Filename-encoded timestamp is stable + accurate.

**Why filename not internal "## H:MM" timestamps**: parsing markdown headings is fragile (free-form text). Filename is structured + reliable.

### 3. Signal format: **single line, ~50 tokens, counts + "since" + pointer**

```
📋 Delta available: N commits, M new memos, K omnibus refs since YYYY-MM-DD HH:MM — see dev/active/delta-{role-slug}-{date}.md
```

Counts to surface:
- Commits since cutoff (`git log --since=<cutoff> --oneline | wc -l`)
- New memos in role's inbox + read since cutoff (filesystem mtime check on memo files)
- Omnibus-log references since cutoff (check `dev/{YYYY}/{MM}/{DD}/omnibus-*.md` files created after cutoff)
- Optional: issues filed/closed since cutoff (`gh search issues ... --created=>= --closed=>=`)

If the script can't compute any count (network error, missing tool), emit signal with `???` placeholder + pointer. Hook never blocks session start.

### 4. Output path: **`dev/active/delta-{role-slug}-{date}.md`**

Role-scoped: each role gets its own delta computed against its own session log timestamp.
Date-stamped: overwritten daily (not accumulating); same role + same date = same filename.
Lives in `dev/active/`: convention for working-state docs the cycle uses.

**Content structure** (per AC: <500 tok target):

```markdown
# Delta — {role-slug} — {date}
Cutoff: {YYYY-MM-DD HH:MM} (from session log {filename})

## Commits ({N})
- {sha1} {first-line summary} ({author})
- ...

## New memos ({M})
- inbox: {memo-filename} (from {from-role})
- read: {memo-filename} (from {from-role})
- ...

## Omnibus refs ({K})
- {dev/YYYY/MM/DD/omnibus-{date}.md} — {first-line summary}

## Issues touched (optional, gh-dependent)
- #N opened: {title}
- #M closed: {title}

---
*Regenerated at session-start by SessionStart hook + scripts/generate-delta.sh*
```

### 5. Hook integration: **extend `.claude/hooks/session-start.sh` modularly**

Add a new section (between mailbox-check and briefing-freshness) that:
- Invokes `scripts/generate-delta.sh` for the agent's role-slug (passed as env var or detected from session log directory)
- Appends the one-line signal to the hook's `output` accumulator
- Wraps in `|| true` and `2>/dev/null` to ensure hook never exits non-zero
- Function-shaped block (e.g., `delta_signal()` function) so it can be added/removed cleanly

The role-slug detection question: SessionStart hook needs to know which role is starting. Options:
- (a) Detect from most-recent session log in today's dir (matches active session)
- (b) Detect from env var set by the agent's wrapper
- (c) Run for all roles, output most-recent's signal

Lean: (a) is simplest + most accurate. The agent has just opened a log file (or is about to); newest log in today's dir is the right role-slug.

**Separation from CHECK trigger** (v0.5 Phase C+ item per Sunday memo): the delta-signal section is wholly separate from any future cron-CHECK section. Keep them in distinct function blocks with their own ENV-VAR-disable toggles if useful.

### 6. First-session-ever default: **24h fallback**

If no `*-{role-slug}-code-opus-log.md` found in the last 7 days for the role, default cutoff = `now - 24h`. Matches Lead Dev May 17 audit's proposal. Avoids producing a huge delta on first session that floods context.

---

## Implementation order (12pp → 12qq → 12rr → 12ss)

1. **12pp — Script**: `scripts/generate-delta.sh` (bash; portable). Inputs: `--role <slug>`, `--cutoff <ISO>` (optional override). Output: writes `dev/active/delta-{role}-{date}.md` + prints the one-line signal to stdout for hook consumption. Bash because session-start.sh is already bash; consistent. ~30-45 min.

2. **12qq — Hook extension**: Add modular section to `.claude/hooks/session-start.sh` calling the script + appending signal to `output`. ~15-20 min.

3. **12rr — Test**: Manual `bash scripts/generate-delta.sh --role cio` → verify file generated correctly. Trigger SessionStart hook (via fresh session-open) → verify signal appears. Test edge: empty delta (no work since cutoff). Test edge: very long delta (truncate to top-N items if >500 tok). ~15 min.

4. **12ss — Close**: Update #975 description checkboxes per `close-issue-properly` skill. Closing comment with impl evidence (commit refs + file paths). Completion memo to Lead Dev CC PA + CEO. ~15 min.

## Open implementation questions (resolved at impl-time, not blocking design)

- Bash vs Python for script: leaning bash (no extra deps; consistent with session-start.sh)
- gh-dependent issues section: optional in spec; include if `gh` available + cached creds; skip silently otherwise
- Truncation strategy if delta >500 tok: top-N commits/memos with "+X more" footer
- Cutoff-not-found handling: log warning to stderr (not stdout) + use 24h fallback

## What this design is NOT

- Not a complete script — implementation is 12pp
- Not pre-committing to bash (Python ok if 12pp finds bash insufficient)
- Not blocking on v0.5 SessionStart-hook-extension overlap — that's a separate cron-CHECK item for Phase C+

## Cross-references

- #975 issue body (AC source): https://github.com/mediajunkie/piper-morgan-product/issues/975
- Lead Dev May 24 routing memo (hybrid mechanism): `mailboxes/cio/read/memo-lead-to-cio-cc-pa-mem-975-delta-hybrid-mechanism-routing-2026-05-24.md`
- CIO May 24 lane-accept memo (hybrid-shape concur): `mailboxes/cio/sent/memo-cio-to-lead-cc-pa-ceo-mem-975-delta-mechanism-lane-accept-plus-cadence-2026-05-24.md`
- Lead Dev May 17 Phase 0 audit (original spec questions): `mailboxes/cio/read/memo-lead-to-ceo-cc-arch-cio-docs-host-exec-pa-mem-cluster-phase-0-audit-972-975-2026-05-17.md`
- methodology-31 Append-Only Autonomous-Cycle Architecture: `docs/internal/development/methodology-core/methodology-31-APPEND-ONLY-AUTONOMOUS-CYCLE-ARCHITECTURE.md`
- v0.5 design: `docs/operations/duty-cycle design/duty-cycle-design-v0.5.md`

— Design ratified by CIO Vehicle 2, 2026-05-25 ~4:58 PM EDT
