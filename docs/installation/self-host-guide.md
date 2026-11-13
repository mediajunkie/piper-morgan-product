# Run Piper Morgan on your own computer

**For**: someone outside the team who wants Piper to run on their own machine, so their notes and projects never sit on a hosted server.
**Time**: about 30 minutes.
**Status**: DRAFT 2026-11-12. Steps 1 to 9 follow the tested list in `docs/internal/operations/canonical-ops-recipes.md` section 13. Items marked **(not yet run)** have not been checked from a clean clone, and the invite step is settled but unrun. Docs will remove each marker as it is verified.

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
3. **Start the supporting services** (a database, a cache and a search index). Docker Desktop must be running. **(not yet run from a fresh machine)**
   ```bash
   docker compose up -d
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
7. **Connect your AI.** On the setup page choose Check System. Under "Connect Your AI" pick your provider and press the button that uses a saved key. It is labeled **Use Keychain** today and will read **Use saved key** after a wording fix. Either way, on your own install it uses the key you stored in step 5, not anything from your computer's keychain.
8. **Create your account.** Piper is invite-only while it is in private beta, and that includes your own copy. A code from the hosted beta does nothing on your machine, because your install checks codes against your own database, which starts empty. So you make your own. Open a second terminal in the same folder, activate the environment, and run:
   ```bash
   source venv/bin/activate
   PYTHONPATH=. python3 scripts/mint_invite_tokens.py 1 --apply
   ```
   It prints one code. **(not yet run by Docs from a clean clone, and the script's last line talks about handing codes to the team, which you can ignore)** Paste it into the account page, then choose a username and password. Nobody on the team needs to send you a code.
9. **Finish.** Add a project or skip. "Setup Complete" means you are signed in. Press Open Piper.

## Check it works

Ask Piper a short question in the chat. **(not yet run: this needs a real provider key and was only run with a stand-in key so far)** If it answers, the key and the install are good.

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

- `python scripts/local_key_setup.py --list` shows which providers have a key stored, never the key itself.
- `python scripts/local_key_setup.py --remove <provider>` deletes one.

## If something goes wrong

See [troubleshooting.md](./troubleshooting.md). Tell the team what you hit. Leave out any key, password or invite code when you do.
