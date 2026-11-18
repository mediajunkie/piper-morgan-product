# Run Piper Morgan on your own computer

**For**: someone outside the team who wants Piper to run on their own machine, so their notes and projects never sit on a hosted server.
**Time**: about 30 minutes.
**Status**: DRAFT 2026-11-12. Steps 1 to 9 follow the tested list in `docs/internal/operations/canonical-ops-recipes.md` section 13. Items marked **(not yet run)** have not been checked from a clean clone. On 2026-11-16 Docs ran steps 1, 2, 3 (the three named services), 4 and 8 from a fresh clone with its own database and ports, and typed no key. On 2026-11-18 Lead's driver (`scripts/guide_keyed_steps_run.py`, issue 2404) ran steps 6, 7, 8 and 9 against a scratch database on a running local Postgres, with a stand-in model and a key seeded by the driver through the call step 5 makes. It checked HTTP replies and page text, with no browser clicks. Step 5 is not run by a seat, because it needs a person at a terminal. The chat check first failed on that path: Piper answered that it needed a key of your own (issue 2405). The fix is on main on 2026-11-18 (the first account on a local install gets the saved key as its own), and the driver's next stub run no longer hits that refusal. The stand-in model's reply still comes back as an error line, so the chat check can only be shown passing with a real key. A run with a real provider key waits on Step A, planned for Friday 2026-11-20. Docs will remove each marker as it is verified.

## What you need

- A Mac or Linux computer. Windows has not been tested, see [windows-setup-guide.md](./windows-setup-guide.md) for the older notes.
- Python 3.12, Git and Docker Desktop. [PREREQUISITES-COMPREHENSIVE.md](./PREREQUISITES-COMPREHENSIVE.md) shows how to check each one.
- An API key from an AI provider (Anthropic or OpenAI). Piper does not supply one.
- Nothing else to request. You make your own invite code in step 8.

## Install

1. **Download Piper.**
   ```bash
   git clone https://github.com/mediajunkie/piper-morgan-product.git
   cd piper-morgan-product
   ```
2. **Set up Python.**
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Start the supporting services** (a database, a cache and a search index). Docker Desktop must be running. Name the three services as shown: a bare `docker compose up -d` also starts the app, which takes the port step 6 needs. This guide assumes no other copy of Piper runs on the computer. If one does, do not go on yet. The top of `docker-compose.yml` lists the lines to put in this copy's `.env` first (`PIPER_STACK`, the three port lines and `REDIS_URL`), and without them this copy would share the other one's database and re-create its cache and search index on this folder's empty data. **(the three services were checked 2026-11-16 from a fresh clone, the second-copy lines have not been run)**
   ```bash
   docker compose up -d postgres redis chromadb
   ```
4. **Create the database tables.**
   ```bash
   alembic upgrade head
   ```
5. **Store your provider key.** Run this in a terminal and answer the prompts.
   ```bash
   python scripts/local_key_setup.py
   ```
   It asks which provider, then asks for your key with the typing hidden. The key is stored encrypted in your local database. The first time you run it, it also creates three settings in a file called `.env` (kept out of git). Keep that file. Its encryption key is the only thing that can read your stored keys. Keep it private to your own account.

   Enter your key only at that prompt. Do not paste it into a command, a config file or a message. The script refuses to run without a terminal, never prints the key and never contacts the provider.
6. **Start Piper.**
   ```bash
   python main.py
   ```
   It prints the setup address, `http://localhost:8001/setup`. Open it in your browser.
7. **Connect your AI.** On the setup page choose Check System. Under "Connect Your AI" pick your provider and press **Use saved key**. That uses the key you stored in step 5. **(an install cloned before 2026-11-12 shows the older label "Use Keychain" for the same button)**
8. **Create your account.** Piper is invite-only while it is in private beta, and that includes your own copy. A code from the hosted beta does nothing on your machine, because your install checks codes against your own database, which starts empty. So you make your own. Open a second terminal in the same folder, activate the environment, and run:
   ```bash
   source venv/bin/activate
   PYTHONPATH=. python3 scripts/mint_invite_tokens.py 1 --apply
   ```
   It prints one code. **(checked 2026-11-16 from a fresh clone, it added one code to the new database. The script's last line talks about handing codes to the team, which you can ignore)** Paste it into the account page, then choose a username and password. Nobody on the team needs to send you a code.
9. **Finish.** Add a project or skip. "Setup Complete" means you are signed in. Press Open Piper.

## Check it works

Ask Piper a short question in the chat. **(not yet run with a real key: on 2026-11-18 the driver's stand-in run got past the "Piper runs on an LLM key of your own" refusal (issue 2405, fixed), but the stand-in model cannot give a real answer)** If it answers, the key and the install are good.

## What your install offers

A self-hosted install offers the same connectors as the private beta, GitHub and Google Calendar. Notion and Slack are not offered in this beta, self-hosted installs included. Calendar on your own install needs your own Google OAuth client ID and secret, entered on the setup page or in Settings. **(not yet run by Docs)**

## Update later

**(not yet run)** From the `piper-morgan-product` folder, with Docker running:

```bash
git pull
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
```

Then stop Piper with Ctrl-C and run `python main.py` again. Your `.env` and your database are kept.

## Managing your keys

Piper uses its encrypted database store by default. It touches your computer's keychain only if you set `PIPER_CREDENTIAL_STORE=keychain`, which you would do only if you already keep your provider keys there.

- `python scripts/local_key_setup.py --list` shows which providers have a key stored, never the key itself.
- `python scripts/local_key_setup.py --remove <provider>` deletes one.

## If something goes wrong

See [troubleshooting.md](./troubleshooting.md). Tell the team what you hit. Leave out any key, password or invite code when you do.
