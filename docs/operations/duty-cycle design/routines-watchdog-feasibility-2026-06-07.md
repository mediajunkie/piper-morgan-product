# Routines as the Gap-C watchdog — feasibility (2026-06-07)

**Owner**: CIO. **Trigger**: Gap C (compaction silently kills session-crons; durable=noop) made an *external* liveness monitor load-bearing. Researched via claude-code-guide (9 tool-uses, official Routines docs). **Status**: feasibility CONFIRMED for alert-only; **PM decision needed to build** (new infra + cost).

---

## Headline

**Routines CAN serve as the external watchdog — alert-only is feasible NOW.** Routines are **Anthropic-cloud-hosted, persistent, headless** — they run on schedule *independent of the local session and even with the laptop off*. That's the exact property Gap C needs (the dead local cron can't self-report; an external cloud process can). Confidence HIGH on capability; MEDIUM on cost (Routines in research preview).

## The capability ladder (confirms the earlier synthesis)

| Tier | Verdict | Notes |
|---|---|---|
| **(A) Alert-only** — detect "agent's branch silent N hours" → Slack PM | ✅ **VIABLE NOW** | Schedule trigger (min 1hr) → clone repo → `git log origin/claude/{role}-cycle` recency → Slack via MCP connector. ~$70/mo for an hourly watchdog. |
| **(B) Fallback-fire** — Routine runs a minimal fire (drain mail, commit) when an agent's down | ⏸ **possible, needs design** | A Routine *can* clone+read mailbox+commit+push headless. Needs collision-avoidance (lock file) + scope guard rails. **This is also the v2-airlift on-ramp** (a server-side fire = a cloud duty-cycle fire). |
| **(C) Re-trigger the dead local session** | ❌ **won't work** | Routines are sandboxed in Anthropic cloud — can't reach the laptop. PM manual-resume stays the only restart. (Confirms prior.) |

## Key facts that make it fit us
- **Persistence**: cloud, survives laptop-off + compaction (the opposite of session-scoped `CronCreate`; the Gap-C cure).
- **Repo access**: fresh clone each run; read/write/commit/**push**; **default push restriction is to `claude/`-prefixed branches** — which is *exactly* our `claude/*-cycle` convention (no config needed to push status; unrestricted only if we want main).
- **Auth**: one-time interactive setup (GitHub via claude.ai), then **fully headless** per run. (Caveat to watch: interactively-authed MCP connectors can be absent headless — verify Slack works in a Routine run.)
- **Detection signal**: **git commit-recency per `claude/{role}-cycle` branch** (HIGH reliability — git is authoritative; our agents push to origin frequently). Session-log age + open-PR status are secondary signals.
- **Triggers**: schedule (cron, **min 1 hour** + jitter), API POST (on-demand), GitHub webhook (fire on push).

## The real limits
- **Detection latency**: min 1-hour interval → worst-case ~90 min blind (jitter). For faster, a **GitHub-webhook trigger** (fire on each agent push + liveness-check) is the alternative — but webhook reliability is preview-flaky. For a watchdog catching multi-hour silences, 1hr is fine.
- **No persistent sandbox state** (fresh clone each run): fine for alert-only (read-only); fallback-fire would need a repo-checkpoint to avoid double-processing mail.
- **Cost**: ~$70/mo alert-only (hourly, ~$0.05/run); MEDIUM confidence (preview pricing; daily run-cap per account exists but unpublished).

## Recommendation → MVP: alert-only watchdog

Build **one alert-only watchdog Routine**, template it across roles:
- Schedule hourly → clone `piper-morgan-product` → per `claude/{role}-cycle` branch: last-commit-age + session-log-age → if silent beyond the role's threshold, Slack PM with the last-seen + a "resume: `claude --resume`" hint.
- Optional audit trail: commit a `dev/active/watchdog-{date}.md` summary (transparent watchdog activity).

This directly cures the **Gap-C detection** problem (someone always notices a silent stop), pairs with the agent-side v1.3 self-heal (reduces the dark-window) — **self-heal shrinks it, watchdog guarantees it's noticed.**

## Decisions PM needs to make (before build)
1. **Build the alert-only watchdog?** (~$70/mo, ~4-6hr build, cures Gap-C detection.)
2. **Silence threshold per role** (propose: ~3h continuous lanes, ~6h async/low-freq lanes).
3. **Alert channel**: Slack-only to start (avoid issue-noise)?
4. **Fallback-fire (B)** — defer to a design pass? (It's the v2-airlift on-ramp — bigger, separate decision.)

## Roadmap impact
Resolves roadmap **item 1**'s open questions (headless repo access YES; auth one-time-then-headless; git+Slack YES) → the watchdog moves from "spike-worthy" to "buildable, pending PM go." And **(B) fallback-fire confirms item 2 (v2 cloud-native) is real** — a Routine can run our fire logic server-side; the airlift is no longer hypothetical, it's "scope the collision-avoidance + checkpoint."

*Filed by CIO 2026-06-07 (Fire 7). Source: claude-code-guide research (Routines docs). Companion: `duty-cycle-roadmap.md`, `procedures/cron-lifecycle.md` Gap C.*
