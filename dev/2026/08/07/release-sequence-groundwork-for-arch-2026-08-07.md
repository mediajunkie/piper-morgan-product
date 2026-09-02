# Release-sequence definitions — what already exists, before anyone drafts fresh

**By**: Exec, 2026-08-07 (quiet-fire groundwork) · **For**: whoever drafts the definition (Arch, on PM's word) · **Status**: research only — nothing proposed, nothing routed

PM raised this morning: *"sounds like we need to clarify our release sequence, what build goes where, what it means to be alpha, beta, in production, in staging (?), etc. **We have discussed this before, even recently.**"*

That last clause is the reason for this file. Rather than let a drafter start from a blank page and re-derive decisions that already exist, here is what's actually on disk. **The finding is that the pieces exist and disagree with each other** — which is exactly why the vocabulary failed under load yesterday.

## What exists

| Surface | What it says | Status |
|---|---|---|
| **ADR-007** "Staging Environment Architecture with Docker Compose" | Defines *staging* as a **local docker-compose stack** (8+ services, Prometheus/Grafana, nginx) for validating production readiness | **Accepted — July 20, 2025.** Thirteen months old, written pre-Fly, pre-beta, pre-alpha-testers |
| **Code — `PIPER_ENVIRONMENT`** | The canonical env var (`llm_config_service.py`). Recognized values: **`development` / `staging` / `production`**, defaulting to `development` | Live, and it is the only *machine-readable* definition we have |
| **ADR-040** | Local database per environment | Accepted |
| **decisions.log:193** (ADR/Arch, 2026-07-10) | `_no_key_fallback_or_raise` makes **prod** (`PIPER_ENVIRONMENT`/`ENVIRONMENT == "production"`) fail closed | Ratified; couples security behavior to the env string |
| **Fly app `piper-morgan`** | The artifact alpha testers actually use. Currently **v29, Aug 2** | Live — but note it maps to `production` in the code's vocabulary |
| **git branch `production`** | Exists, is stale by design, and is **not** the deployed artifact | The direct cause of yesterday's four-way confusion |

## The three collisions worth naming (all of them bit us this week)

1. **"Production" means three things.** A `PIPER_ENVIRONMENT` value that turns on fail-closed security · a git branch that is not deployed and is knowingly stale · the Fly app that alpha testers use. Yesterday, five roles reasoned about "production" while two of those senses were in play, and the day cost a confident wrong answer that had to be retracted twice.
2. **"Staging" has a definition nobody uses.** ADR-007's staging is a local docker-compose stack. In conversation "staging" now tends to mean "somewhere between my machine and what testers see" — a slot that arguably doesn't exist in our actual topology. **PM's own "(?)" next to staging is the correct instinct.**
3. **"Alpha" and "beta" aren't in the machine vocabulary at all.** They're the words we use for *audience and readiness* — who's allowed in, what promises hold — while `PIPER_ENVIRONMENT` only knows *deployment mode*. These are two different axes, and we've been using one word for both. That's what makes "what build goes where" hard to answer: the build goes to `production` mode, serving the *alpha* audience, gated by the *beta* milestone.

## The shape a definition probably needs (not a proposal — a checklist for the drafter)

Whoever drafts it should answer, per name: **what artifact does it point at · what promotes a build into it · who authorizes that · what promises hold for whoever is in it.** And it should say explicitly which axis each word lives on — deployment mode vs. audience/readiness — because conflating them is the actual defect, not the absence of a doc.

Two decisions the drafter will hit and should route rather than settle alone: whether *staging* survives as a name at all (ADR-007 may want superseding rather than updating), and whether `PIPER_ENVIRONMENT` grows a value or stays three-valued with audience tracked separately.

## What I did not do

Not routed to Arch — PM said "we need to clarify," and I offered to route it; the word hasn't come. Not proposed a scheme; that's an architecture call. Not touched ADR-007. This file exists so that when it *is* routed, the drafter starts from the collisions rather than rediscovering them.
