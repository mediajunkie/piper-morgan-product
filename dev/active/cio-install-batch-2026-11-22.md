# CIO install batch, 2026-11-22: the `~/.piper-shared` denies for every seat

**Status: ready.** HOST read it and Arch approved it (11-22). Exec puts it on xian's card.

**Why:** on 11-22 at 09:20, Web's seat read a file inside its own browser profile folder (`~/.piper-shared/seat-browser-credential-profile-web/Last Version`) and was not refused. CIO's seat was refused on the same file. The profile folder holds the seat browser's beta session cookie. The `~/.piper-shared` Read denies lived in each seat's own git-ignored settings, and Web's has none that matches. This patch puts them in the one settings file every PM seat shares.

**Patch 1 of 1.** From `~/Development/piper-morgan-worktrees/cio`, in Terminal:

1. Test (Web's seat, by Web): Read `~/.piper-shared/seat-browser-credential-profile-web/Last Version`. Today it is **not refused**.
2. Apply: `python3 scripts/seat_settings_grant.py fleet-deny`
3. Test again (Web, after a restart, which Pard can do with `seat-restart.sh web`): the same Read is **refused**.

**You should see** at step 2: `added 6 deny rule(s); 2 were already there. No allow, env or other rule was changed.` Relay that line and Web's step-3 result. CIO marks it done only then.

**Bound:** additive only. It adds six `Read(~/.piper-shared/...)` denies (`*credential*`, `*token*` and `*secret*`, each with a `/**` form for a folder's contents), and removes or loosens nothing. HOST read it and Arch approved it (11-22, v4 01M82658XG and 01M825WY1D).

**This is the answer to a failed check** (Web's step 4 (b), 11-22 09:20), not a routine step.

**If it fails, undo this run only:** the command prints `to undo: mv '<...>/settings.json.before-fleet-deny.<YYYYMMDD-HHMMSS>' '<...>/settings.json'`. Paste that line as printed. That copy is the file as it was just before this run, so Step A's two denies stay. The older `.before-fleet-deny` copy from Step A is left as it was; don't use it for this undo.
