# Release Notes — v0.8.13.0 "Nothing Invented, Nothing Borrowed"

**Date**: 2026-09-21 · **Cut from**: main `39925528e` (see tag `v0.8.13.0`) · **Milestone**: MVP — server-key abolition complete (#1812), the PM-dogfood standup trust fixes (#1836/#1837), keyless first contact (#1818)
**Quality posture**: 14,332 tests collected; unit+intent sweep 11,290+ passing at the #1812 landing and 4,875 across every package touched by the standup work; smoke 531; security suite 127; spend-free canonical ratchet 14/14 with membership unchanged; mypy gate at all 24 ceilings. One day of changes since v0.8.12.0 — a fast follow, cut so the weekend's trust fixes reach alpha before new testers do.

## Summary

This release finishes what v0.8.12.0 started and fixes what the first real dogfood session
found. The "server key" is no longer merely refused — the concept is deleted from the
codebase: there is no code path, gated or otherwise, to a product-owned LLM credential.
And the standup flow stops inventing things: accepting the guided-interview offer now
actually starts the interview, the generic placeholder draft ("Made progress on assigned
tasks") is deleted and unreachable, free-form draft edits genuinely apply, and a keyless
"hi" gets a human acknowledgment instead of a wall of policy.

## What's New

### The server-key concept is gone (#1812, closing the BYOC arc)
- **Steps 5–6 landed**: `PIPER_OPERATOR_SERVER_KEY`, the designated-operator principal,
  and the transitional "explicit None binding" are all deleted. Every LLM spend is the
  acting user's own key, resolved per request — or an honest refusal. Forgetting to bind
  is an error; binding the old operator form raises at bind time.
- **The import-time hazard is gone at the root**: constructing the LLM client no longer
  reads any credential from any store — the server's long-lived provider clients were
  amputated along with their only consumer (the seam itself).
- KG embeddings lose their keychain fallback: document search embeds on *your* stored
  OpenAI key, or refuses honestly.

### The standup flow stops fabricating (#1837 + #1836 — from PM's live alpha transcript)
- **Accepting the interview offer starts the interview.** You say yes, it asks the first
  question — no second "Ready for your standup?" greeting, no mode-fork re-ask.
- **The generic placeholder standup is deleted and unreachable.** With nothing to build
  from, Piper re-enters the interview (the only honest keyless-data path) or says plainly
  that there's nothing to draft. It never presents boilerplate as your day.
- **The flow owns its own offers.** Ask "didn't you say you'd do a guided interview?"
  and — if it owes you one — it says exactly that and offers to start it, instead of
  denying the offer it made three turns earlier.
- **Free-form draft edits actually work** (#1837 shape 3): "change what I did yesterday —
  say I spent the day getting the team back on track" now routes through the
  conversational floor on your own key and applies. The old keyword matcher (which fired
  on words *inside* your sentences — the literal cause of the transcript's wrong turn) is
  retired. "Add blocker: …" and "remove …" stay instant and key-free.
- **"I've updated your standup" is only ever said when something changed** (#1836):
  the success message is derived from a verified diff. An inapplicable edit gets an
  honest "unchanged" answer; a keyless free-form edit gets an honest note that it needs
  your key, with the key-free actions named.
- "Start over" now actually starts over (clears the captured answers and re-interviews)
  instead of re-rendering the same draft.

### First contact, keyless (#1818 — PM ruled option b)
- A keyless user's first message gets a kind-matched acknowledgment — "Hello — good to
  meet you." / "That's kind — though I haven't actually done anything yet." — followed by
  the one shared key sentence: *"Piper runs on an LLM key of your own, not on anyone
  else's account. Add an OpenAI or Anthropic key in Settings and I'll be ready when you
  are."* Deterministic, zero LLM, zero spend.
- A repeated pleasantry gets a short restatement, not the full copy again; a repeated
  substantive request gets the gate's own refusal.

### Deploy identity and credential-store safety
- **`/health` now reports the real version, git SHA, and environment** (#1839) — alpha
  had been reporting a hardcoded `environment=staging` for months. "What is actually
  deployed" is now a curl, not an inference.
- **Keychain namespace collisions are loud** (#1764): a non-default service name over the
  DB-backed credential store now raises with a pointer to the issue, instead of silently
  colliding credentials across services.

## Known limitations (honest)

- These fixes are in the code as of this cut; **alpha.pipermorgan.ai runs them only after
  this release is deployed to the droplet** (deployment is a separate step, same session).
- Free-form standup edits require your own LLM key (they run a model on your account);
  the chip actions (add blocker / remove / start over) never do.
- A short polite imperative like "please remove the fluff" can still be mis-read as an
  acceptance and finalize a draft — found by this release's own regression work, tracked
  as #1843 (the shared acceptance-vocabulary lane; fix pending its owners' ruling).
- Gemini has no spend path (its SDK offers no safe per-request credential); OpenAI and
  Anthropic keys are the supported pair.
- Known-issues list: see `docs/ALPHA_KNOWN_ISSUES.md` (updated with this release).

## Version mechanics

- **Cut**: product content at `39925528e` (origin/main, 2026-09-21 morning); the tag
  sits on the release commit (version bump + this doc set) directly atop it — lockstep
  mode: `production` fast-forwarded to the tagged commit in this session.
- **Tag**: `v0.8.13.0`
- **pyproject.toml**: `0.8.13.0`

## Upgrade instructions

Hosted alpha testers: nothing to do — the update lands when the droplet is redeployed.
Self-hosting: `git fetch && git checkout v0.8.13.0`, then restart the server
(`docker compose up -d --build app` or your equivalent). No schema migrations in this
release; `alembic upgrade head` is a safe no-op.
