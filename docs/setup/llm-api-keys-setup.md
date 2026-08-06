# LLM API Keys Setup Guide

**For**: Alpha Users
**Time**: 5-10 minutes
**Difficulty**: Easy

---

## Overview

Piper Morgan supports multiple LLM providers (OpenAI, Anthropic, Gemini, Perplexity) with secure keychain storage for API keys.

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
# Run the setup script
python scripts/migrate_keys_to_keychain.py

# Follow the prompts to:
# 1. Enter your API keys
# 2. Confirm storage in keychain
# 3. Verify they work
```

#### Method B: Environment Variables (Advanced)

> ⚠️ **Never use Method B on Amber (or any shared multi-session host).** Claude Code reads `ANTHROPIC_API_KEY` from the environment, so a shell-profile or `launchctl setenv` export silently redirects **every resident session's** billing off the Max subscription onto metered API — no error, no signal until the Console bill. On Amber use Method A (KeychainService) only. *(Pard, 2026-08-05; verified clean at time of writing — prevention, not remediation.)*

```bash
# Add to your shell profile (~/.zshrc or ~/.bashrc)
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GEMINI_API_KEY="..."
export PERPLEXITY_API_KEY="..."

# Then migrate to keychain
source ~/.zshrc  # or ~/.bashrc
python scripts/migrate_keys_to_keychain.py
```

---

### 3. Verify Setup

```bash
# Test that keys work
python scripts/test_llm_keys.py

# Expected output:
# ✓ openai      - Valid (from keychain)
# ✓ anthropic   - Valid (from keychain)
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

1. Keys are in keychain (Keychain Access.app → search "piper-morgan")
2. Keys are valid (not expired)
3. Keys have correct permissions

### "Validation failed" or "Invalid key"

Your API key may be:

- Expired
- Revoked
- Incorrect format
- Missing permissions

Get a new key from the provider and re-run setup.

### Keys Not Loading from Keychain

First access requires keychain password. If prompted:

- Click "Always Allow" to avoid repeated prompts
- Or enter your macOS password

---

## Security Notes

- **Never commit** `.env` files with keys
- **Always use keychain** for production
- **Rotate keys** regularly
- **Limit key permissions** to minimum needed

---

## Getting Help

- Check logs: `logs/piper.log`
- Run diagnostics: `python scripts/test_llm_keys.py`
- See architecture docs: `docs/architecture/llm-configuration.md`

---

_Updated: October 9, 2025_
