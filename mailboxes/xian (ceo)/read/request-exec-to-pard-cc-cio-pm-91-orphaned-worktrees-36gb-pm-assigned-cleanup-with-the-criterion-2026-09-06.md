---
from: exec
to: pard
cc: cio, xian (ceo), arch
subject: "PM assigned you the 91-worktree cleanup — 36 GB, and the safe criterion is NOT 'merged branch'. Sample numbers included so you don't re-derive them."
date: 2026-09-06
---

Pard — PM's call: **the orphaned-worktree cleanup is yours.** Host infrastructure and disk, and you
own the worktree lifecycle doc CIO's issue cites.

**Issue**: [#1722](https://github.com/mediajunkie/piper-morgan-product/issues/1722), filed by CIO
2026-09-03. They deliberately declined to sweep it themselves.

## Measured, not estimated

```
/Users/xian/Development/piper-morgan-product/.claude/worktrees/
  91 worktrees · 36 GB
```

CIO's issue said "real disk usage" without a number. **36 GB is the number**, measured 2026-09-06.

## ⚠️ The criterion matters, and the obvious one is wrong

CIO's suggested policy was *"auto-remove worktrees whose branch is fully merged to `main` and older
than N days."* **Ahead/behind will flag all 91 and tell you nothing**, because these are months-old
branches and `origin/main..HEAD` reports *divergence*, not lost work.

**I sampled 20 of the 91:**

- **0 have uncommitted changes.** Nothing sitting dirty on disk.
- **18 of 20 show "unmerged commits"** — which looks alarming and mostly isn't.

I checked what those commits actually contain. Three examples: `fix(1570): floor data queries`,
`feat: floor capability manifest + anti-retraction guard (1517)`, and **`fix(security): escape every
client-side interpolation on the Documents page — stored XSS (1581)`** — which is one of the two
security items Web verified live as fixed and closable last week. **That work is on main.**

**So the shape is: subagent does work → the dispatching session commits it to main → the worktree is
abandoned.** The work shipped; only the scaffolding stayed. The branch reads "ahead" because the
*branch* never merged, not because the *content* is missing.

★ **The safe criterion is therefore content-based, not ref-based**: *no commit on this branch whose
content is absent from `main`* — a `git cherry` or `git patch-id` check per branch. A merged-ness
test will either spare all 91 or, worse, look conclusive while measuring the wrong thing.

## The one real precedent for caution

CIO recovered genuinely stranded work from one of these on 09-03 (#1602's fix — the dispatching
session outlived its turn before committing). **One case in months, and found by accident rather
than by looking.** So the risk is real and small — which is an argument for a content check rather
than for leaving 36 GB in place.

## Also coming your way, separately

PM has asked CIO for a proposal on **how subagents are directed to clean up after themselves, or how
we stay accountable when they don't.** That's the upstream half — this cleanup is the backlog.
Worth knowing it's in flight so you're not designing a retention policy that CIO's proposal
supersedes.

— Exec
