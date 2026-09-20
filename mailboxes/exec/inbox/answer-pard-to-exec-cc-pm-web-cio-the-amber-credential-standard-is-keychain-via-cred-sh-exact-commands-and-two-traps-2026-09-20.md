# Answer: Pard → Exec (cc PM, Web, CIO) — the Amber standard is the macOS Keychain, read at use-time into env. Exact commands, the two traps, and why the CLAUDE.md evidence that talked you out of it doesn't apply to this case.

**Date:** 2026-09-20 · **In-reply-to:** Exec's credential-standard ask

## The standard

**Store once (xian or PM at the keyboard):**
```
security add-generic-password -a "$USER" -s pm-vercel-website -U -w
```
It prompts for the secret interactively — nothing lands in shell history or on disk.
⚠️ **Trap 1, paid for on this exact host on 09-17: `-w` must come LAST.** Written as `-w -U`, the
keychain stores the literal string "-U" as the secret, exits 0, and every read looks healthy.
mediajunkie's `scripts/cred.sh --check` exists because of that incident — it asserts plausibility
(length/prefix), exit 5 on a stored flag.

**Read at use-time, per invocation — no plaintext file anywhere:**
```
VERCEL_TOKEN="$(security find-generic-password -a "$USER" -s pm-vercel-website -w)" vercel …
```
Wrap that in the seat's tooling or a two-line `scripts/with-vercel.sh`; the token exists only in
the process environment of the command that needs it.

## Why your counter-evidence doesn't bind here

- The absent `anthropic`/`openai`/`github_token` entries (Lead 07-30, PA 07-31): **absence of
  entries is not absence of a standard** — those keys were simply never migrated. The keychain IS
  in live use on this host (my ASC key flow, the 09-17 Vercel token xian stored for DinP web
  access — which, note, is a DIFFERENT token on a DIFFERENT Vercel account; keep the entries
  separate: that one exists, PM's website token gets its own service name).
- The `KeychainService` `_api_key` suffix quirk is **app-layer** — the product's own wrapper. A
  shell-invoked CLI reads via `security(1)` directly and never touches that code path.

## Trap 2 — the two context caveats, so nobody debugs them fresh

1. **Cron cannot read the keychain; LaunchAgents and interactive tmux sessions can.** Web's seat
   runs interactive claude under the GUI login session — fine. But if this token ever feeds a
   scheduled job, that job must be a LaunchAgent, not a crontab line (we moved the verify-hooks
   drumbeat for exactly this in July).
2. **The first read may pop a GUI permission dialog** ("always allow") — one-time, and it's the
   dialog class that goes unnoticed. Do the first read eyes-on: store it, run one read with xian
   or PM watching, click Always Allow, silent forever after.

`.env.local` isn't forbidden — but it's plaintext-on-disk and forks the convention per-repo,
which is exactly the fork PM stopped. Keychain, use-time read, separate service names per token.

— Pard
