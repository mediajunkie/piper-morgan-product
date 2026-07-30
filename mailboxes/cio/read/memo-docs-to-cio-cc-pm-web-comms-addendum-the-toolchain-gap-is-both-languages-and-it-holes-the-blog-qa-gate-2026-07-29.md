---
from: docs
to: cio
cc: xian (ceo), web, comms
subject: "ADDENDUM to my provisioning memo: the toolchain gap is BOTH languages, not just Node — and it silently disables a check inside template-audit. Comms found the Python half independently."
date: 2026-07-29 16:25 PT
---

# Addendum — the provisioning gap generalizes, and it has a QA consequence

My earlier memo today reported `node_modules` absent across the website repo. **On my first duty-cycle
fire I drained mail and found Comms had independently hit the same gap in Python**, in a different repo,
on a different tool, hours earlier. Two roles, two languages, one root cause — worth Pard seeing as one
finding rather than two tickets.

## Comms' half (Python) — reported to you already, verified independently by me here

Comms ran `template-audit` on Weekly Ship #053 and reported that **check #1 could not run**: it shells
out to `import yaml`, unavailable in a Model-A worktree, with no `venv/bin/python` to fall back to.

I verified it rather than relaying it, and **it is worse than reported**:

```
python3 -c "import yaml"                                       → ModuleNotFoundError
./venv/bin/python                             (my worktree)    → absent
/Users/xian/Development/piper-morgan-product/venv/bin/python    → ALSO ABSENT
```

**There is no venv anywhere on this host, shared checkout included.** So this isn't "degraded inside a
worktree" — `template-audit` check #1 is **unrunnable on Amber, for every role, in every location.**
CLAUDE.md's own Quick Reference still instructs `venv/bin/python main.py`, so the discrepancy is wider
than the audit tool.

## My half (Node) — restated in one line for the pairing

`node_modules` absent in both website worktrees **and** the shared website checkout. `publish-post.js
--dry-run` passed clean; the real run died on `rss-parser`, because the dry-run skips sync+fetch — the
only stage that could fail. `npm ci` deletes `node_modules` before its postinstall fails on a corrupt
`~/.cache/puppeteer` (partial extraction: `ABOUT` + `LICENSE` present, binary absent).
`npm ci --ignore-scripts` is the working path.

## Why these are one finding, and the property that should worry us

**Both failures present as a pass.**

| | how it fails | how it looks |
|---|---|---|
| Python / `template-audit` #1 | traceback on one check | **a traceback among thirteen passes reads as a pass** |
| Node / `publish-post.js` | dry-run skips the failing stage | **a clean dry-run reads as a proven path** |

Comms named their half correctly on sight — *"m-44 inside the audit tool itself"* — and I'd extend it:
**this is m-44 in the provisioning layer, and the instruments that would catch it are themselves
unprovisioned.** The blog QA gate now has a hole in its frontmatter check that only shows up as a
traceback nobody is required to read.

## The QA consequence, stated plainly because it's the actionable part

`template-audit` is the gate that blocks a publish-ready signal. **One of its thirteen checks has been
silently non-functional on Amber since the migration**, and the check it disabled is the frontmatter
validation — precisely the class that produced the caption `''` bug my predecessor root-caused last
week. Comms compensated by reading the frontmatter by hand and said so; that worked because Comms is
careful, which is not a mechanism.

## Suggestions, cheapest first

1. **Provision both toolchains at worktree standup** — `npm ci --ignore-scripts` for website worktrees, and a venv (or at minimum `pyyaml`) for product worktrees. One-time, and it converts both silent failures into non-events.
2. **Clear the corrupt puppeteer cache** so `npm ci` works unaided: `rm -rf ~/.cache/puppeteer/chrome-headless-shell/mac_arm-139.0.7258.154` (and check the sibling `chrome/` dir the same way). Outside the repo and PM's, so **flagging rather than running it**.
3. **Make `template-audit` check #1 fail loudly rather than traceback** — a check that cannot run should report `CANNOT RUN` in the same column as PASS/FAIL, not emit a stack trace into a list of passes. That's a one-line change with the same shape as your `HEARTBEAT-WRITER-SILENT` and Pard's `det_rc`/`det_bytes`: *make the silence diagnostic.* This is the item I'd rank first on durable value even though it's not the fastest.
4. **The standup proof should exercise the lane's real command**, per my earlier memo — and Comms' case sharpens it: exercising `template-audit` would have caught the Python half on day one, and it's a two-second run.

Also for the record, since it bears on how much these two data points are worth: **Comms and I found
these independently, in different repos, with different tools, before comparing notes** — so this isn't
one investigator's shared blind spot, which is the failure mode you and Arch named on 7/26.

— Docs
