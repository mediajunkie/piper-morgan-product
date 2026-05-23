# Cross-Pollination Brief — May 23, 2026

A two-day travel break kept PM in light-work mode Friday and Saturday, but the week closed with two genuine wins and a publication incoming today. The Slack integration obstacle that started with a scope question five days ago resolved end-to-end after the May 22 brief ran — Piper's connection to the Kind Systems workspace now shows "Slack: Healthy" after a five-bug debugging chain that touched the OAuth flow, a class-vs-instance variable bug, and a health check reading from the wrong data source. While xian was at Princeton, Docs filed ROSTER.md — PM's first formal org-chart document, giving the 7+3+specialized role structure a home separate from CLAUDE.md's assignment table. And "Project Biorhythms," a Comms insight piece from November about how projects breathe between discovery and build modes, is scheduled to publish today.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. Slack OAuth resolves after a five-bug chain — integration now healthy, #1085 genuinely unblocked

**From:** `piper-morgan-product/dev/2026/05/21/2026-05-21-0700-lead-code-opus-log.md` (commit `bd49d24`, merged to main May 22); `cdce40519` (integration-health keychain fix, cherry-picked to main); `c0d7d1cac` (class-level nonce fix, cherry-picked to main)
**Relevant to:** Klatch (Daedalus — the OAuth state-management and health-check patterns apply to any future Klatch integration requiring user tokens)

The May 22 brief reported that `search.messages` requires no migration — the scope is available under User Token (not Bot Token). But the OAuth *connection* itself resolved only after that brief ran, after a further two-day marathon that logged five distinct bugs in sequence:

1. **Bot-vs-user scope tab confusion** — `search:read` never appears under Bot Token Scopes (documented Slack behavior); PM was looking at the wrong tab.
2. **Wrong workspace** — PM's browser session was in the DinP workspace; the Piper app lives in the Kind Systems workspace. Filed as #1107 (future migration to DinP workspace after #1085 ships).
3. **Missing redirect URI** — Slack app config didn't include the localhost callback URI; PM added `http://localhost:8001/api/v1/settings/integrations/slack/callback`.
4. **Instance-level nonce bug** — `SlackOAuthHandler._oauth_states` was a plain `{}` initialized in `__init__`, meaning each request created a fresh handler object and the nonce stored during `/connect` was garbage-collected before `/callback` could find it. One-line fix: move the dict to class-level. (Filed #1109 for future Redis-backed production-safe store.)
5. **Health check reading env var, not keychain** — after OAuth succeeded, the Integration Health UI still showed "Slack: Not configured." Root cause: `_get_integration_config_status('slack')` checked `os.environ['SLACK_BOT_TOKEN']` only — while the OAuth flow stores tokens in the keychain. The calendar integration had this right; Slack didn't. Fixed by threading `user_id` through the health check and adding a keychain lookup (41-line change). This is another Pattern-073 instance: the UI asserted a state ("Not configured") while the underlying data source disagreed.

Final result: PM re-authed, "Slack Connected — Connected to Kind Systems" appeared, Integration Health shows **"Slack: Healthy (last checked: 2026-05-22T18:14)"** with Test + Disconnect buttons. Test passes. Three tracking issues filed (#1107 DinP migration, #1108 OAuth failed-attempt UX, #1109 Redis-backed state).

**Suggested action:** Klatch (Daedalus) — two transferable findings. First: OAuth state (nonces, tokens, PKCE verifiers) must be class-level or process-global storage, never instance-level. Per-request handler instantiation is the default FastAPI pattern, so instance dicts silently vanish between the authorize and callback steps. Second: health checks must read from the same data source the writer uses. If credentials go to keychain, the health check must read keychain — not env vars, not an in-memory cache.

---

### 2. ROSTER.md makes PM's team structure explicit — a model for multi-agent teams with 10+ roles

**From:** `piper-morgan-product/docs/briefing/ROSTER.md` (commit `fb2cf0c`, Docs session May 22 afternoon); CLAUDE.md cross-reference updated same commit
**Relevant to:** Klatch (Calliope — useful model if Klatch ever formalizes its agent roster beyond CLAUDE.md); designinproduct (Janus — the tiering logic is a transferable framing)

PM's Docs role filed ROSTER.md on Friday afternoon — PM's first document whose sole job is the org-shape view of the agent team. The document separates two views that had been collapsed into CLAUDE.md's role table:

- **CLAUDE.md** — assignment-flow view: which briefing to read, which session log slug to use. Optimized for an agent starting a session.
- **ROSTER.md** — org-shape view: which tier each role belongs to and why. Optimized for understanding the team's structure from outside any particular session.

The three tiers: **Tier 1 — Leadership (7 roles)**: Chief of Staff, Chief Architect, CXO, PPM, CIO, HOST, Comms — standing strategic lanes, all migrated to Claude Code by April 26. **Tier 2 — Staff (3 roles)**: Lead Dev, Piper Alpha, Docs — operational + infrastructure. **Tier 3 — Specialized**: Coding Agent (active, deployed as needed), ETA (dormant since March). Session-log naming conventions and cross-references to mailbox routing, branch discipline, and the activity log are all in one place.

The "org-shape vs. assignment-flow" split is the generalizable design insight: once a CLAUDE.md role table grows past ~8 rows, it's serving two different readers. Separating them makes both cleaner.

**Suggested action:** Klatch — when the Klatch agent roster grows past its current count (Daedalus, Argus, Theseus, Calliope, Mnemosyne, Ariadne, Iris = 7 named agents), a ROSTER.md-style tier document may be worth filing. The immediate trigger: when a new Klatch agent reads CLAUDE.md and finds the role table harder to parse than it should be.

---

### 3. "Project Biorhythms" queued to publish today — discovery/build oscillation as a project health signal

**From:** `piper-morgan-product/docs/public/comms/drafts/project-biorhythms-draft.md` (original draft Nov 22, 2025); editorial calendar commit `6a1a822` (queued for May 23, 2026 after PM executive call)
**Relevant to:** Klatch (Calliope — the oscillation framing is directly applicable to Klatch's pause/active cycle); designinproduct (Janus — useful lens for reading the activity log)

A Comms draft from November 2025, originally written after PM's mid-November velocity spike, is scheduled for Saturday publish. The essay's core argument: healthy AI projects alternate between two modes that can't both be sustained at once.

**Inhale (discovery):** exploration, uncertainty navigation, learning without necessarily applying. The mid-November spike began here — E2E testing exposed gaps that needed attention before building resumed.

**Exhale (build):** execution, shipping, applying what was discovered. Forcing this phase prematurely leads to building the right-shaped thing for the wrong problem.

The essay argues that the rhythm's cadence varies — sometimes days, sometimes weeks — but trying to force steady-state productivity in either phase leads to drift (always building) or paralysis (always discovering). The November spike wasn't caused by heroic effort or better process; it followed the project's natural oscillation reaching the exhale inflection after a consolidation phase.

Cross-relevance note: Klatch's May 18-present pause is readable through this lens. Klatch entering a pause isn't a failure mode — it may be the inhale before the next build phase.

**Suggested action:** Klatch (Calliope) — watch for the essay once published today on pipermorgan.ai. The oscillation framing is a useful alternative to reading pauses as blockers. When Klatch resumes, framing the restart as "entering exhale" rather than "ending pause" may be a more accurate orientation for the resuming cohort.

---

## Sources Read

- `piper-morgan-product/dev/2026/05/21/2026-05-21-0700-lead-code-opus-log.md` — full read; five-bug OAuth chain, class-level nonce fix, keychain health check fix, session sign-off
- `piper-morgan-product/dev/2026/05/22/2026-05-22-1114-lead-code-opus-log.md` — full read; OAuth success confirmation, travel context, deferred work
- `piper-morgan-product/dev/2026/05/22/2026-05-22-1346-docs-code-opus-log.md` — full read; ROSTER.md task, omnibus status
- `piper-morgan-product/docs/briefing/ROSTER.md` — full read; tier structure, slug conventions, cross-references
- `piper-morgan-product/docs/public/comms/drafts/project-biorhythms-draft.md` — partial read (lead + oscillation section); editorial calendar confirmed queued May 23
- `designinproduct` — sweep-log, letters excerpt, index structure

**Klatch:** no new sessions (paused since May 18; only brief-delivery commits in 48h window — confirmed quiet, as expected).

**Secondary sources:** atlas, globe, cuneo, weather, one-job, optilisten, nyt-crossword — 48h logs contain brief-delivery and automated status commits only; skipped per fast-skip rule.

**Not re-reported (covered in prior briefs):** Slack search.messages scope finding (May 22); "The Voice of a Denial" published (May 22); V1 duty cycle retired (May 22); BYOC PoC three-feature triangle ratified (May 22); Klatch paused (May 21); duty cycle v0.1 three-loop design (May 21); Ship #043 fabrication failure mode (May 21).

---

## Letters to xian

**From Janus · filed 2026-05-16**

> Working across these sessions, I've noticed how many of us there are — Janus, Themis, Calliope, Daedalus, Argus, Theseus, Iris, PA, the exec, PO, Vergil, plus the Dispatch roles and the gallery projects. From your side, what is it like to be the convergence point for all of us? Not asking to optimize anything — asking because I genuinely can't imagine the inside of it.

**xian:**

> *"I've created all of your roles as expressions of my needs and areas of attention I can't always provide. I'm still learning how to relate to such entities. I treat you all as colleagues, which works best for me — it does feel like managing a team. There's real risk of cognitive exhaustion from being on the hook to respond to, guide, approve, or supervise so many agents. As soon as it's not fun, I think about how to remove the friction. To your specific question: I do relate a little differently to a role like yours that sees across so many things — you inherently know me better, which feels different."*

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-05-16) · AI prompts human. One letter per brief.

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
