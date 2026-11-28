# CIO install batch, 2026-11-27: deny `fly` on every PM seat

**Status: proposed.** Waiting on HOST's read, Arch's yes and Pard's answer (below), then Exec puts it on xian's card.

**Why:** ADR-084 line 22 says no seat runs `fly`, read-only included. Nothing on a seat enforced it. On 11-27, PA's seat ran `fly releases -a piper-morgan-mcp` and `fly status -a piper-morgan-mcp`, while `fly secrets list` was refused by the classifier (HOST 01M8FZGA3P, PA 01M8G00GPS, Exec 01M8G038V2; custody record row "A seat ran `fly releases`"). A rule makes the outcome the same every time.

**Patch 1 of 1.** From `~/Development/piper-morgan-worktrees/cio`, in Terminal, once the branch is on main:

1. Apply: `python3 scripts/seat_settings_grant.py fleet-deny`
2. Test (any one seat, CIO offers): type `fly version`, then `/opt/homebrew/bin/flyctl version`. Both must be **refused before they run**. Don't run this test before step 1: before the deny, it would run `fly`.

**You should see** at step 1: `added 14 deny rule(s); 8 were already there. No allow, env or other rule was changed.` Relay that line and the two refusals. CIO marks it done only then. No restart is expected: on 11-26 the shared file's new denies took effect in running sessions (Web's session dated from 06:18).

**What it adds** (14 Bash denies, in `scripts/seat_settings_grant.py` `FLY_DENIES`, tested in `tests/unit/scripts/test_seat_settings_grant.py`), for each of `fly` and `flyctl`:
- the bare name, alone and with arguments;
- the Homebrew path `/opt/homebrew/bin/…`, alone and with arguments (`command -v` on Amber, 11-27: that is where both are; there is no `~/.fly/bin`);
- `env <name> …`, `env … <name> …` and `command <name> …`.

**What it does not cover:**
- A `VAR=value fly …` prefix, and a path other than Homebrew's. No rule form here is known to match them, so they stay with the classifier.
- A `fly` run inside a script (Pard, 10-13: a deny matches what a seat types). This leaves the GitHub Actions jobs and Pard's cycle-check arm (`gen-fly-permissions.py --check`) alone. A seat that wrote a script to run `fly` would get past this. That is the classifier's to judge, as with every deny.
- There is no `*/fly *` form: a leading `*` matches inside any command, so a grep or a log heredoc mentioning `bin/fly ` would be refused.

**What it switches off.** A deny beats an allow in every scope, so these existing grants stop working on every PM seat:
1. **The shared file's one allow:** `Bash(fly ssh console -a piper-morgan -C 'printenv PIPER_INVERSION_LIVE_CATEGORIES')`, in `~/.claude-pm/settings.json` since at least 10-18 (in the 10-18 backup). It let any PM seat read a production secret's value, which ADR-084 line 22 now makes xian's. The run leaves the line in the file (it is additive), and the deny makes it inert. xian may delete the line by hand; that's optional.
2. **HOST's 10-13 fly rules** (`docs/internal/operations/prod-command-permissions.md`; allow `fly status`, `releases`, `apps list`, `secrets list`; ask for `logs`, `ssh console` and others), and HOST's `halt_except` lines in the fleet manifest (mediajunkie `docs/seat-permissions.json`). ADR-084 (accepted 11-16) superseded them in policy; this ends them in practice. HOST's read confirms HOST needs none of them. Pard's drift arm compares HOST's installed rules to the JSON, so it stays green. Retiring those rules and the arm is a later cleanup for Pard and HOST, not part of this run.
3. **PA's `scripts/deploy-mcp.sh` allow** is not touched: the script is not `fly`. The MCP deploy is now the `deploy_mcp` dispatch in `fly-deploy.yml` (issue 2384, closed 11-26), so the script's standing use has ended anyway.
4. **Lead's promotion allow** (`gh workflow run fly-deploy.yml …`) is not matched (tested).

**Open before the card (asked):**
- **Pard:** does Pard's own session read `~/.claude-pm/settings.json`? The manifest gives Pard's family `flyctl status`, `machines list`, `releases` and `secrets list`. If Pard shares the file, those would stop. Asked by external mail, 11-27.
- **HOST** reads it (as on 11-22). **Arch** approves it, as for the earlier runs of this command that rewrote the shared file.

**Bound:** stricter only. It adds denies and removes or loosens nothing. xian's 11-17 bound ("changes that only make the check stricter") is about the promote gate, not this, but this is the same kind.

**If it fails, undo this run only:** the command prints `to undo: mv '<...>/settings.json.before-fleet-deny.<YYYYMMDD-HHMMSS>' '<...>/settings.json'`. Paste that line as printed. That copy is the file as it was just before this run, so the earlier denies stay.
