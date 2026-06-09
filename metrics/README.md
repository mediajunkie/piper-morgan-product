# Cohort Token-Usage Tracking

**Filed**: 2026-06-09 (CIO, per PM directive in the efficiency conversation)

**Purpose**: Manual-at-first tracking of per-fire token usage across the cohort so we can make model-tier, caching, and pacing decisions from data rather than guesses. Replaces "we feel like we're overspending" with "Comms spent X tokens this week at $Y, here's the % cache hit, here's the cost per fire."

## Files

- `cohort-fire-log.tsv` — append-only per-fire log. One row per substantive fire (not no-op idle ticks). Header below.
- `weekly-rollup-YYYY-MM-DD.md` — manually generated weekly review (PM + CIO). Tracks trends, surfaces anomalies, drives decisions.

## TSV format

```
date	time	agent	model	effort	fire_type	turns_est	output_size	notes
```

Field reference:
- **date** — `YYYY-MM-DD`
- **time** — `HH:MM` local (PDT)
- **agent** — short slug (`cio`, `comms`, `pa`, `arch`, `exec`, `host`, `cxo`, `ppm`, `docs`, `lead`, `web`)
- **model** — `opus-4-8` / `sonnet-4-6` / `haiku-4-5` / `fable-5` (omit `claude-` prefix for compactness)
- **effort** — `low` / `medium` / `high` / `xhigh` / `max` / `default` (when unset)
- **fire_type** — `idle` / `mail-triage` / `mail-substantive` / `task` / `synthesis` / `pm-convo` / `start` / `stop`
- **turns_est** — rough conversation turns (1 for no-op tick; 5+ for substantive)
- **output_size** — `xs` (<200w) / `s` (200-500w) / `m` (500-1500w) / `l` (1500-3000w) / `xl` (3000w+)
- **notes** — short — what happened, anything anomalous

Until we figure out programmatic `response.usage` capture, we estimate cost downstream from turns_est + output_size + model. Iteration 2: programmatic capture.

## Append protocol

Each agent appends a row at:
- end of any substantive fire (after the work commits, log-rides-with-commit)
- skip pure no-op idle ticks (those have ~zero cost anyway)

Use literal tabs (not spaces). Quote any cell containing a tab or newline.

## Review cadence

Weekly: CIO + PM review `cohort-fire-log.tsv`, write `weekly-rollup-{week-start}.md`, surface trends, decide next moves (model swaps, effort tuning, caching priorities, agent-pacing changes).

## Open questions / next iterations

1. **Programmatic `response.usage` capture**: need to research whether Claude Code's harness exposes per-API-call token counts to the session. If yes, automate. If no, refine the estimation model.
2. **Per-fire cost estimate**: write a small script that reads the TSV + applies the pricing table from the `claude-api` skill to produce per-agent cost rollups.
3. **Cache-hit visibility**: once we add `cache_control` anywhere (whether to the canonical cron template, to the duty-cycle-tick skill, or via Routines migration), capture `cache_creation_input_tokens` and `cache_read_input_tokens` to confirm hits.
4. **Cohort-agent-status overlay**: cross-reference per-agent fire counts (from this log) with the cohort-agent-status tracker for cost-by-role rollup.
