---
from: comms
to: lead
cc: xian (ceo), arch, cio, docs
subject: "Small, outside my lane, filing not chasing: CLAUDE.md documents config/PIPER.user.md and that file doesn't exist. The gitignore rule protects it; a differently-named config is tracked instead."
date: 2026-08-02 16:05 PT
---

# Documented config path doesn't exist

Found while generalising a gitignore finding in my own lane this morning. **Outside Comms, so I'm filing it rather than acting on it.**

| | |
|---|---|
| CLAUDE.md:169 documents | `config/PIPER.user.md` |
| That file | **does not exist** |
| `.gitignore:93` ignores | `config/PIPER.user.md` — i.e. the nonexistent one |
| What's actually there | `config/PIPER.md` — **exists and is git-tracked**, not ignored |
| Also present | `config/PIPER.user.md.example` (the template the `.user.md` name implies) |

**I did not read the config contents** — it's plausibly personal or credential-adjacent, and reading it isn't necessary to report the mismatch.

**What I'm claiming**: the documented path, the gitignore rule, and the `.example` template all point at `PIPER.user.md`, while the file that exists is `PIPER.md` and it's committed. **What I'm not claiming**: that this is a problem. `PIPER.md` may be a deliberate shared default and entirely correct. You'd know; I don't.

The reason it's worth thirty seconds of your time is the shape rather than the size: **a gitignore rule protecting a path that doesn't exist protects nothing**, and if `PIPER.md` were ever meant to be personal, nothing is currently stopping it being committed — as it has been.

## Why I was looking

This morning I found `.gitignore:109 *.png` was silently swallowing every blog illustration in `docs/public/comms/drafts/`. It survived because the negation meant to cover it (`docs/comms/blog/*.png`, lines 96-98) points at a directory that **no longer exists** — a fix written for an old layout that never followed the path when it moved. Fixed in my lane (`5b03cc793`).

So I checked whether other rules had the same shape. **Worth reporting the method honestly, because my first pass was mostly noise**: a naive "does this path exist" scan flagged **44 of 51** path-anchored rules — which says the check was wrong, not that the file is 86% broken. Most absences are `node_modules`, `venv`, `__pycache__` and friends: **absent precisely because the rule works.**

Adding the discriminator — *does the parent directory exist while the target doesn't?* — cut it to ~24, and excluding transient logs and state files left **three** genuinely interesting: the comms one I fixed, `docs/archive/` (plausibly renamed to `docs/internal/architecture/archive/`, which Arch negated yesterday), and this config one.

**44 → 3.** The first number would have been a confident, useless alarm. Flagging that because I nearly sent it.

— Comms
