# Piper Morgan: API Key Setup (older keychain-based method)

> **Running Piper on your own computer?** Follow the [self-host guide](./self-host-guide.md). It stores your provider key at a hidden prompt in your local database and never asks you to use a keychain, an `export` line or a command-line key. The rest of this page describes the older keychain-based setup.

Your API keys are stored securely in your operating system's keychain, never in plaintext config files.

## Where Keys Are Stored

- **macOS**: Keychain Access (service: `piper-morgan`)
- **Windows**: Credential Manager
- **Linux**: Secret Service (varies by desktop environment)

## Supported Providers

| Provider | Required | Format |
|----------|----------|--------|
| OpenAI | Yes | `sk-...` |
| Anthropic | Optional | `sk-ant-...` |
| Gemini | Optional | API key from Google Cloud |
| Perplexity | Optional | `pplx-...` |

## Method 1: Setup Wizard (Recommended)

```bash
python main.py setup
```

Steps:
1. System checks (Docker, Python, port 8001, database)
2. Create user account (username, optional email)
3. Add API keys:
   - Enter key (input masked, won't appear on screen)
   - Key is validated with provider API
   - Key is stored securely in OS keychain

Supports resume: if setup interrupted, run again to continue from where you left off.

## Method 2: Commands and environment variables

The older `python main.py keys` commands and environment-variable setup have been removed from this page. Some of them show a pasted key or write to your computer's keychain without asking. Use the [self-host guide](./self-host-guide.md), which enters the key at a hidden prompt.

## Troubleshooting

### Key validation fails
- Check that your API key is correct (copy/paste carefully)
- Verify your account has permissions for the model you're using
- Check provider rate limits or account status
- Some providers charge for API access; ensure billing is set up

### Keychain backend missing (Linux)
- Install your desktop environment's secret service backend:
  - **GNOME**: `gnome-keyring`
  - **KDE**: `kwallet`
  - **Generic**: `python-keyring` with `secretstorage`
- See [keyring docs](https://keyring.readthedocs.io) for details

### Install Certificates error on macOS (Errno 13)
- This is rare but can happen if Python's certificate bundle is read-only
- Fix: upgrade certifi in your venv:
  ```bash
  python -m pip install --upgrade certifi
  ```

## Key Security Notes

- **Never** commit API keys to Git
- **Never** paste keys in chat/email/documents
- **Never** store keys in `config/PIPER.user.md` (that file is for preferences only)
- Enter keys only at a hidden prompt (see the self-host guide), never in a command, a config file or a shell profile
- Rotate keys regularly: remove the old one with `python scripts/local_key_setup.py --remove <provider>` and enter the new one at the prompt

## Configuration File Separation

- `config/PIPER.user.md` → Your preferences, timezone, working hours, projects, etc.
- OS Keychain → Your API keys (secure, encrypted)

DO NOT mix them up!

---

**Last Updated**: October 28, 2025
**Status**: Ready for alpha testing
