# LLM API Keys Setup Guide

**For**: Alpha Users
**Time**: 5-10 minutes
**Difficulty**: Easy

---

## Overview

> **Running Piper on your own computer?** Use the [self-host guide](../installation/self-host-guide.md) for the key step. It enters the key at a hidden prompt into your local database. The older keychain-script method has been replaced, and the environment-variable method was removed.

Piper Morgan supports multiple LLM providers (OpenAI, Anthropic, Gemini, Perplexity) with encrypted storage for API keys. Since 2026-11-12 the OS keychain is used only when `PIPER_CREDENTIAL_STORE=keychain` is set. Otherwise keys go in Piper's database store.

---

## Quick Start

### 1. Get Your API Keys

You'll need at least one provider's API key:

**OpenAI** (Recommended):

- Visit: https://platform.openai.com/api-keys
- Create new key
- Copy key (starts with `sk-`)

**Anthropic** (Optional):

- Visit: https://console.anthropic.com/
- Create new key
- Copy key (starts with `sk-ant-`)

**Gemini** (Optional):

- Visit: https://makersuite.google.com/app/apikey
- Create new key
- Copy key

**Perplexity** (Optional):

- Visit: https://www.perplexity.ai/settings/api
- Create new key
- Copy key

---

### 2. Set Up Keys (Choose One Method)

#### Method A: Interactive Setup (Easiest)

```bash
# Run the key script, in a terminal
python scripts/local_key_setup.py

# It asks which provider, then asks for the key with the typing hidden,
# stores it encrypted in your database and reads it back.
```

#### Method B: removed

Putting a key in a shell profile leaves it in plain text and in shell history, so this page no longer shows it. Use Method A or the self-host guide.

---

### 3. Verify Setup

```bash
# Test that keys work
python scripts/test_llm_keys.py

# Expected output:
# ✓ openai      - Valid
# ✓ anthropic   - Valid
# ...
```

---

### 4. Start Piper

```bash
# Start backend
python main.py

# You should see:
# ✅ openai: Valid
# ✅ anthropic: Valid
# LLM providers validated: X/4
```

---

## Provider Configuration

### Default Provider

Piper uses OpenAI by default. To change:

Edit `config/PIPER.user.md`:

```yaml
llm:
  default_provider: openai # or anthropic, gemini, perplexity
```

### Exclude Providers (Development)

To avoid using expensive providers during development:

```yaml
llm:
  excluded_providers:
    - anthropic # Don't use Anthropic during dev
```

Or via environment:

```bash
export PIPER_EXCLUDE_PROVIDERS="anthropic"
```

---

## Troubleshooting

### "No module named 'keyring'"

Install keyring:

```bash
pip install keyring --break-system-packages
```

### "No API key found for provider"

Run the test script to diagnose:

```bash
python scripts/test_llm_keys.py
```

Check:

1. Keys are stored: `python scripts/local_key_setup.py --list` (if you chose the OS keychain, look in Keychain Access.app for "piper-morgan")
2. Keys are valid (not expired)
3. Keys have correct permissions

### "Validation failed" or "Invalid key"

Your API key may be:

- Expired
- Revoked
- Incorrect format
- Missing permissions

Get a new key from the provider and re-run setup.

### Keys Not Loading from the Keychain (only if you set `PIPER_CREDENTIAL_STORE=keychain`)

First access requires keychain password. If prompted:

- Click "Always Allow" to avoid repeated prompts
- Or enter your macOS password

---

## Security Notes

- **Never commit** `.env` files with keys
- **Never put a key in a command or shell profile**, enter it at a hidden prompt
- **Rotate keys** regularly
- **Limit key permissions** to minimum needed

---

## Getting Help

- Check logs: `logs/piper.log`
- Run diagnostics: `python scripts/test_llm_keys.py`
- See architecture docs: `docs/architecture/llm-configuration.md`

---

_Updated: October 9, 2025_
