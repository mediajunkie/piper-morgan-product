# RUNBOOK — PM: provision LLM API keys into the Amber keychain

**For**: xian (PM). **Written**: 2026-08-01 (Lead). **Delete when**: both keys stored and Lead has verified (`anthropic`/`openai` PRESENT).
**Why**: the canonical e2e suite and the #1395 judge skip themselves without these keys; #1445 closure and #1395 Phase 3 are gated on this. The keys exist only in your hands — no agent can do this step.

## The two steps, in order, same terminal (SSH to Amber is fine)

### Step 1 — unlock the login keychain

```bash
security unlock-keychain ~/Library/Keychains/login.keychain-db
```

Prompts for your **macOS login password for Amber** (not an API key). Hidden input. No output = success.

> Skipping this is what caused your 2026-08-01 attempt to fail with
> `keyring.errors.PasswordSetError: ... (-25308, 'Unknown Error')` —
> that code is `errSecInteractionNotAllowed`: the keychain was locked and
> your non-GUI session couldn't pop the unlock dialog.

### Step 2 — store both keys

```bash
cd ~/Development/piper-morgan-worktrees/lead && venv/bin/python -c '
import getpass
from services.infrastructure.keychain_service import get_keychain_service
kc = get_keychain_service()
for name in ("anthropic", "openai"):
    v = getpass.getpass(f"{name} API key (paste — input hidden): ").strip()
    if v:
        kc.store_api_key(name, v)
        print(f"  {name}: stored")
    else:
        print(f"  {name}: skipped")'
```

- Prompt 1: paste the **Anthropic** key → Enter.
- Prompt 2: paste the **OpenAI** key → Enter.
- Success: `anthropic: stored` and `openai: stored`.

Keys never touch shell history, screen, chat transcripts, or the repo — `getpass` hidden input straight into the macOS keychain via `KeychainService` (which applies the required `_api_key` suffix; this is why we never use the raw `security add-generic-password` CLI — see the gotchas doc).

## Where to get the key values

- Your laptop: Keychain Access app → search "piper-morgan" → show password; **or**
- Mint fresh: console.anthropic.com and platform.openai.com (mildly preferred — Amber gets its own revocable credentials).

## If Step 2 STILL fails with -25308 after a clean Step 1

Run both steps once from a **GUI session** (Screen Sharing into Amber). Some macOS versions require a GUI context for the first write to a new keychain service entry; after the first success, headless access works.

## Afterwards

Tell Lead "keys in" (any session). Verification probe (safe, prints only presence, never values):

```bash
cd ~/Development/piper-morgan-worktrees/lead && venv/bin/python -c "
from services.infrastructure.keychain_service import get_keychain_service
kc = get_keychain_service()
for n in ('anthropic','openai'):
    print(n, '->', 'PRESENT' if kc.get_api_key(n) else 'ABSENT')"
```

Both PRESENT → Lead runs the #1445 closing re-run and un-gates #1395 Phase 3 immediately.
