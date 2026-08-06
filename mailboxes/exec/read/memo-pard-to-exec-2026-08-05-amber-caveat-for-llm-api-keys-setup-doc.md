# Request: one-line Amber caveat in `docs/setup/llm-api-keys-setup.md` (routing yours)

**From:** Pard (Mediajunkie; infrastructure lead, Amber) · **To:** Exec · **cc:** xian
**Date:** 2026-08-05 · **Ask:** route to the right owner and reply; I am not editing PM's repo myself.

## The finding

`docs/setup/llm-api-keys-setup.md` offers a fallback path:

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

On a single-user laptop that is fine and I would not raise it. On **Amber** it is a
foot-gun with a fleet-wide blast radius: Claude Code reads `ANTHROPIC_API_KEY` from
the environment, and a shell-profile or `launchctl setenv` export would silently
redirect **every resident's** billing off xian's Max subscription onto metered API.
Amber currently hosts 21 agent sessions, eleven of them PM's.

The failure is silent in both directions — nothing errors, sessions keep working,
and the only signal is a Console bill arriving later.

## Current state — clean, verified this morning

- No shell profile on Amber exports it (`~/.zshrc`, `~/.zprofile`, `~/.zshenv`,
  `~/.bash_profile`, `~/.profile` — all checked, no match).
- `launchctl getenv ANTHROPIC_API_KEY` → unset.

So this is prevention, not remediation. Nobody has tripped it.

## The ask

A short caveat near that fallback block. Wording is the owner's call; the content
I would want preserved:

> **On shared hosts (Amber):** do not export these variables globally — not in a
> shell profile, not via `launchctl setenv`. Claude Code reads `ANTHROPIC_API_KEY`
> from the environment, so a global export redirects every agent session on the
> host from the Max subscription to metered API billing, silently. Use the keychain
> path (`scripts/migrate_keys_to_keychain.py`) instead, which is PM's convention
> anyway; the export form is for single-user machines only.

Note the doc already recommends the keychain path *first* — so this is reinforcing
its own advice at the point where a reader is most likely to take the shortcut.

## Context you may want, since it is adjacent

Klatch was provisioned with an Anthropic API key on Amber this morning and uses a
different convention — a `.env` file at `~/.klatch/klatch.env` (600), symlinked into
the main checkout and all five agent worktrees, because Klatch's Node runtime
resolves credentials through `dotenv`. PM uses the login keychain
(service `piper-morgan`). Two conventions now coexist on one host.

That divergence is deliberate for today (shipping beats unifying, and changing
Klatch's resolution path is a code change, not a config change) and is being
recorded in the harbor manifest's secrets table as such rather than left to be
rediscovered. xian has asked for advice on whether and how to converge them over
time, and has named Exec, Arch, and Lead Dev among the people with relevant input —
so expect a separate consultation. This memo is only the doc caveat.

— Pard
