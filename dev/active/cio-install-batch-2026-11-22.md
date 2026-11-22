# CIO install batch, 2026-11-22: the `~/.piper-shared` denies for every seat

**Status: held until HOST and Arch have read it.** Then Exec puts it on xian's card.

**Why:** on 11-22 at 09:20, Web's seat read a file inside its own browser profile folder (`~/.piper-shared/seat-browser-credential-profile-web/Last Version`) and was not refused. CIO's seat was refused on the same file. The profile folder holds the seat browser's beta session cookie. The `~/.piper-shared` Read denies lived in each seat's own git-ignored settings, and Web's has none that matches. This patch puts them in the one settings file every PM seat shares.

**Patch 1 of 1.** From `~/Development/piper-morgan-worktrees/cio`, in Terminal:

1. Test (Web's seat, by Web): Read `~/.piper-shared/seat-browser-credential-profile-web/Last Version`. Today it is **not refused**.
2. Apply: `python3 scripts/seat_settings_grant.py fleet-deny`
3. Test again (Web, after a restart, which Pard can do with `seat-restart.sh web`): the same Read is **refused**.

**You should see** at step 2: `added 6 deny rule(s); 2 were already there. No allow, env or other rule was changed.` Relay that line and Web's step-3 result. CIO marks it done only then.

**Bound:** additive only. It adds six `Read(~/.piper-shared/...)` denies (`*credential*`, `*token*` and `*secret*`, each with a `/**` form for a folder's contents), and removes or loosens nothing. The `.before-fleet-deny` copy beside the shared file stays the one from Step A (11-20), so the one-line undo below is the one to use.

**If it fails, revert only this patch** (removes the six rules, leaves the rest). **Untested:** CIO's run of it on a scratch copy was refused by auto mode on 11-22 (a settings-shaped write), and not worked around. Arch, please judge it, or name a better undo:

```
python3 -c "import json,pathlib,sys; sys.path.insert(0,'scripts'); import seat_settings_grant as g; p=pathlib.Path.home()/'.claude-pm'/'settings.json'; d=json.loads(p.read_text()); d['permissions']['deny']=[r for r in d['permissions']['deny'] if r not in g.FLEET_DENIES[2:]]; g.save(p,d,mode=p.stat().st_mode & 0o777)"
```
