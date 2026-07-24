
# Cross-Pollination Brief — July 24, 2026

A heavy infrastructure day across the constellation: PM's test burn-down held CI green through 30+ waves and surfaced a non-gating diagnostic technique that paid for itself in one run; Pard completed the Amber fleet standup and documented two non-obvious Claude Code infrastructure lessons around account isolation and filesystem layout.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### A non-gating CI step that reruns known-flaky tests with tracebacks makes oscillator root causes visible without ever blocking the gate

**From:** Piper Morgan, Lead Developer (day-close log `dev/2026/07/23/2026-07-23-0647-lead-code-log.md`, Fire 5 / Wave oscillator-diagnostic)

Teams with known-flaky tests typically log them in a backlog and accept that they'll fail silently — the gate tolerates the listed entries, so their WHY never appears in CI output. The PM Lead Dev shipped a parallel non-gating CI step that reruns this flaky band with full tracebacks on every run. The diagnostic cost is near-zero; it paid back in one cycle: the rerun immediately showed that `DocumentIngester` was eagerly constructing `OpenAIEmbeddingFunction` at init time, which raised a keyless exception and silently 500'd the entire radar feed — a live production bug invisible until the traceback surfaced it. The bug was fixed and CI-confirmed the same day (Wave 44, lazy-property cure).

**Relevant to:** Any project with a CI "flaky" list that's treated as a parking lot. The standard setup (mark flaky, gate tolerates, entries accumulate) hides root-cause evidence. A non-gating rerun step makes the backlog self-documenting.

**Suggested action:** For each band of known-oscillating tests, add a parallel CI job (non-gating, runs every build) that executes just that band with full tracebacks. No gate impact; diagnostic yield on the first run that has a real root cause to expose.

---

### `CLAUDE_CONFIG_DIR` isolates two Claude Code accounts on one machine — no second macOS user needed

**From:** Mediajunkie, Pard (`scripts/amber-agent.sh`, `docs/amber-harbor-status.md`, 2026-07-23)

Pard verified that setting `CLAUDE_CONFIG_DIR=~/.claude-pm` when launching Claude Code gives a fully independent account context (auth, MCP connectors, settings, session history) without any operating system-level isolation. On Amber (Mac Studio), the designinproduct.com account runs under the default `~/.claude` directory; the pipermorgan.ai account runs under `~/.claude-pm`. The codified launch script (`scripts/amber-agent.sh`) handles the partitioning automatically: `amber-agent <session> <repo-dir> <config-dir>` — a first run in a new config-dir requires one `claude login`, after which the partition is persistent. The script also refuses to silently clobber a live tmux session (delete-then-create-then-verify guard).

**Relevant to:** Any setup running Claude Code for two clients, two orgs, or two separate Anthropic accounts on the same machine. Avoids the overhead of a second macOS user or a separate machine.

**Suggested action:** For each account partition, create a dedicated config dir (e.g., `~/.claude-<account-slug>`), run `claude login` once per partition, then always launch with `CLAUDE_CONFIG_DIR=<dir> claude` — or codify into a wrapper script. MCP connectors and cron artifacts are account-scoped and do not bleed across.

---

### Claude Code memory keys encode the full filesystem path — moving repos into subdirectories silently orphans their context

**From:** Mediajunkie, Pard (`docs/amber-harbor-status.md` § *Structure — flat filesystem, grouping as metadata*, 2026-07-23)

When Pard built the Amber harbor manifest (tracking 24 repos on one machine), the instinct was to group repos into subdirectories by project-family. The decision went the other way: keep everything flat in `~/Development/` and carry grouping as a metadata column in the manifest. The reason: Claude Code encodes the full filesystem path in its memory-directory keys (e.g., `~/.claude/projects/-Users-xian-Development-<repo>/`). Moving a repo from `~/Development/repo` to `~/Development/group/repo` silently orphans all accumulated agent memory, preferences, and session context with no warning or migration path. The same path-encoding affects LaunchAgent plists, shell aliases, and any documentation that references `~/Development/<repo>` directly.

**Relevant to:** Any team setting up a shared machine or standardizing repo layouts while Claude Code is in use. The filesystem is not just a namespace — it is the memory key space.

**Suggested action:** Before restructuring repo locations on a machine running Claude Code, audit `~/.claude/projects/` for memory directories that would be orphaned. If restructuring is necessary, budget for re-seeding agent context (re-reading key docs, re-establishing preferences) for every repo that moves. Prefer flat layouts and metadata-based grouping when the repo count doesn't genuinely require hierarchy.

---

## Sources Read

- **Klatch** — `docs/mail/` (Janus→Calliope MAXT gap relay, 2026-07-22); cross-pollination brief delivery commits only. No new substantive agent logs in the 48h window.
- **Piper Morgan** — Lead Dev session log `dev/2026/07/23/2026-07-23-0647-lead-code-log.md` (full day-close); commit messages from Comms, Exec, Docs, Watchdog mail.
- **Mediajunkie (Pard)** — `logs/2026-07-23-pard-log.md`; `docs/amber-harbor-status.md`; `scripts/amber-agent.sh`.
- **Globe, One Job, Cookie Monster** — non-empty git logs (brief delivery only); no new agent narration. Not listed in sources_checked.
- **Atlas, Cuneo** — empty 48h logs. Skipped.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
