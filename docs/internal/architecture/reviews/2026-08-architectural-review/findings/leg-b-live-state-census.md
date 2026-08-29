# Leg B — Live-State Census (docs-blind, code only)

*Filed verbatim-condensed 2026-08-29. Researcher forbidden from reading architecture/briefing docs.
Denominator: 584 non-test .py modules under services/ + web/ + main.py (491 excluding __init__),
198,413 LOC; all 491 classified via transitive import closure from real entrypoints PLUS a runtime
load closure. Instrument caveats stated: ran `scripts/reachability-map.py`, found two blindnesses
(string-registered routers; parent-__init__ execution), corrected both with a custom AST tracer.
"Loaded" is an upper bound; "never-loaded" is a hard lower bound on deadness. Live-host env state
unknowable from code — flags reported as-checked-in.*

## Summary counts (of 491 non-init modules)

| class | modules | ~LOC | share |
|---|---|---|---|
| load-bearing | ~337 | ~154K | 69% |
| extension (operator CLI/scripts/alembic only) | 7 | ~2K | 1.4% |
| experiment (off-by-default flags, dev gates, demo plugin) | ~9 | ~2.5K | 2% |
| shim (interface implies a protocol it doesn't speak) | 5 named | ~2.5K | 1% |
| 75%-pattern (loaded as __init__ side effect; zero call sites) | 48 | 12,415 | 10% |
| dead (never loaded from any entrypoint; zero non-test callers) | 88 | ~23.7K | 18% |

Static reach from real user surfaces: 361/584 modules (62%), 159K/198K LOC (80%). Runtime closure:
396/491 load; 95 never load. **~38K LOC (19%) dead or loaded-only.**

## Entry-point map

One server (`main.py` → `web.app:app`). 31 mounted routers (27 in app.py, 4 in startup.py) + the
transparency router + 2 dev routers (404 in production via `PIPER_ENVIRONMENT` gate). Plugins:
discovery finds demo/calendar/notion/github/slack, and **with `config/PIPER.user.md` absent
(gitignored), ALL discovered plugins enable by default — including the demo plugin, which mounts
live routes at `/api/v1/integrations/demo` in every default deployment.** Slack inbound is Socket
Mode only, config-gated, honest-skip. Background services unconditional at startup: blacklist
cleanup, attention decay, ethics audit cleanup, output filter, composting scheduler (these make
`services/ethics` + the composting half of `mux` load-bearing). **Not mounted anywhere → dead**:
`loading_demo`, `conversation_context_demo`, `feedback_api`, `services/api/middleware`,
`slack_monitoring`, `staging_health`, `mcp_health`. (The demo routes are lore-listed as "deliberate
exceptions"; in code they are simply unmounted — matches A2's contradiction #4.)

## Verification 1 — connectors: 8 adapters, not 4

| adapter | call_tool sites | verdict |
|---|---|---|
| github_adapter (1,885 LOC) | **7 real** — MCP SDK over streamable-HTTP to a DEPLOYED `ghcr.io/github/github-mcp-server:v1.5.0` sidecar (docker-compose:105, fly.toml:30) | **REAL MCP, load-bearing** |
| google_calendar_adapter (1,175) | 1, **unreachable** (`_server_params_for` raises NotImplementedError, #1220) — real ops via Google SDK direct | shim (honest-degrading stub) |
| notion_adapter (995) | **0** — `notion_client` REST | shim; live via plugin router |
| slack_adapter (116) | **0** — keychain-status only | shim AND **dead** (zero importers) |
| cicd / devenvironment / gitbook / linear (~2K total) | 0 each | **dead** (sole importers are spatial counterparts that are themselves dead) |

Bonus: the legacy MCP simulation stack (`services/mcp/protocol/*`, `consumer_core`,
`connection_pool`) has no live caller; `mcp_client.py`'s docstring claims it "stays live in
`services/queries/query_router.py`" — **that file no longer exists**. Orphaned config for the
deleted QueryRouter still present in `config/feature_flags/` and `config/development/`.

## Verification 2 — dual routing rails

**Today, as-configured, 100% of chat traffic rides the legacy chain**: pre-classifier (2,342 LOC) →
inversion consult (`PIPER_INVERSION_LIVE_CATEGORIES` **default-empty ⇒ returns None, byte-identical
to pre-flip**; not set in fly.toml/docker-compose/deploy/config) → LLM classifier (1,768 LOC) →
action rail (~130 registered keys; `MAX_DISPATCH_SITES = 0` — **elif chains fully migrated**) →
category handlers → floor (1,540 LOC). `intent_service.py` is a single **14,389-line file** — the
largest module in the codebase.

**Inversion machinery = experiment class, fully built, armed, off by default config**: router (479)
+ live (629) + shadow (455, `PIPER_INVERSION_SHADOW` default OFF). 4 flip_group entries;
`FLIP_WRITE_ALLOWLIST = frozenset({"create_todo"})`. `unwired_writes.py` is decline-copy only, not
a routing mechanism (#1333).

## Verification 3 — spatial: split verdict

**Live**: place_service (radar feed + mounted places route — though the route is a mounted-orphan,
no UI caller per app.py's own comment/#1522), home_state_service, place_detector,
spatial_intent_classifier (via mux/orientation), spatial_adapter base class, github_spatial, slack
spatial_adapter/spatial_types (socket-mode path).
**Dead**: cicd/devenvironment/gitbook/linear spatial (0 importers), intelligence/spatial pair,
slack spatial_agent/spatial_intent_classifier/workspace_navigator (0 non-test), spatial_mapper/
spatial_memory (test-only), and the mux workspace/perception stack.

## Major dead / 75% families

- **services/mux: 26 of 40 modules off-path (~5.6K LOC)** — all 10 lenses, perception, situation,
  moment_ui, protocols, consciousness, workspace_*, pull_mode, recognition, lifecycle, metadata.
  Live 14: composting pipeline (startup), orientation (classifier), insight_topic_mapper (insights).
- standup/preference_* (5 modules ~1.9K): 75%-pattern.
- memory conversational family (5 + repository): 75%/dead; only user_history live.
- **personality: 10 of 14 off-path** — `response_enhancer` has ZERO external importers;
  `web/personality_integration.py:143` contains its own DUPLICATE PersonalityResponseEnhancer,
  which is what the app actually uses.
- narrative_bridge/helpers/response_context triplets stamped out in 3 packages (9 modules): all
  loaded-only, never wired.
- Whole-package dead: analytics, debugging, editorial, queries, user, project_context, top-level
  config_validator (name-collision trap with the live infrastructure one), service_registry
  (distinct from live container one), version.py, file_analyzer family (8 of 11),
  scheduler/{reminder_scheduler,standup_reminder_job}, key_audit_service, trust/delegation, slack
  {ngrok,event_handler,response_flow_integration,simple_response_handler}, github production_client,
  mcp/skills standup workflow, ui_messages/{action_humanizer,loading_states}, todo_management REST
  (mount deliberately removed).
- web/ root scratch: app.py.backup-personality, 12 loose test/debug .js files, 3 TODO .md — dead.

## UNSURE items (researcher's own)

(a) live-host env gating (inversion flags, Slack tokens) unknowable from code; (b)
observability/slack_monitor + services/commands live iff Slack configured; (c) the 48 loaded-only
modules could theoretically be revived by undetected dynamic dispatch — only dynamic importers
found: plugin_registry, router_initializer, one `__import__("structlog")`.
