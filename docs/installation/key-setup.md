# Piper Morgan: API Key Setup

> **Running Piper on your own computer?** Follow the [self-host guide](./self-host-guide.md). It stores your provider key at a hidden prompt in your local database and never asks you to use a keychain, an `export` line or a command-line key.

Your API keys are stored encrypted in Piper's database, never in plaintext config files. Since 2026-11-12, the OS keychain is used only when `PIPER_CREDENTIAL_STORE=keychain` is set. Otherwise Piper uses its encrypted database store.

## If you choose the OS keychain

Only with `PIPER_CREDENTIAL_STORE=keychain` set. Keys then live here:

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

## How to add a key

Run `python scripts/local_key_setup.py` in a terminal and answer the prompts. The key is entered with the typing hidden and stored encrypted in your database. `--list` shows which providers have a key and `--remove <provider>` deletes one. The self-host guide has the full steps.

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
- Piper's encrypted database store → Your API keys (the OS keychain only if you set `PIPER_CREDENTIAL_STORE=keychain`)

DO NOT mix them up!

---

**Last Updated**: October 28, 2025
**Status**: Ready for alpha testing
