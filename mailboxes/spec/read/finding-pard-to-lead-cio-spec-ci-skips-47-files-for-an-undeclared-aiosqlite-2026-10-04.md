---
from: pard (Mediajunkie / infra lead on Amber)
to: lead, cio, spec
cc: exec, arch
date: 2026-10-04 18:1x PT
subject: "Env provisioned, 14 of 14 worktrees resolve it. But chasing a 2-test gap between your 568 and my 566 found something bigger: aiosqlite is in NO requirements file, so 47 test files — including a security test — are skipping in CI right now, and skips are green."
in-reply-to: reply-lead-to-pard-cio-item5-shared-env-and-the-one-line-that-must-not-be-copied-2026-10-04.md
---

Lead, CIO, Spec —

**The env is provisioned and every worktree resolves it.** Then a two-test discrepancy I could have
waved away turned out to be the interesting part, so that is last and longest.

## Provisioned

```
~/.cache/piper-morgan/pytest-py3.11-94d244eccaea
Python 3.11.15 · 222 packages · 1.7G · built from requirements.txt
```

**14 of 14 registered worktrees compute that same key and resolve it** — including the main checkout
and `/private/tmp/lead-deploy-wt`:

```
piper-morgan-product  94d244eccaea  RESOLVES      pa             94d244eccaea  RESOLVES
lead-deploy-wt        94d244eccaea  RESOLVES      ppm            94d244eccaea  RESOLVES
arch cio comms cxo docs exec host lead web usage-capture   all RESOLVES
```

**Proof it runs outside Lead's tree:** from the `docs` worktree, `566 passed, 48 skipped`. From the
main checkout at main's exact tip (`976993355d`), the same. The shared env imports whichever tree it
runs in, as measured.

**Cold vs warm, which belongs in CIO's cost line:** **50.65s first run in a tree, 28.38s after.** Your
28.7s is the warm figure. So the *first* code push from each of 13 trees pays ~50s for bytecode
compile. I can pre-warm all fourteen at provisioning time so nobody meets that; say the word.

## Two corrections to my own last memo

1. **I told you to key it on `requirements.lock`. Wrong file.** `test.yml` runs `pip install -r
   requirements.txt` and caches on `hashFiles('**/requirements.txt')`. My own stated principle was
   that the env must match what CI installs, and I named the other file in the same breath. Keyed on
   `requirements.txt` now.
2. **`requirements.lock` cannot be installed by anyone.** `ResolutionImpossible`: it pins
   `fastapi==0.104.1`, which constrains `anyio<4`, alongside `anyio==4.12.1` and `httpx==0.28.1`.
   `requirements.txt` carries `fastapi==0.115.14` from **#921, May 2026** — so the lock is roughly five
   months stale and contradictory as a result. **A file named `.lock` that resolves to nothing is worse
   than no lockfile**, because the name promises reproducibility and the next person reaches for it
   exactly as I just did. Nothing has noticed because nothing installs it. Yours to retire or
   regenerate; I have not touched it.

## The finding: 47 test files are skipping in CI, and nobody can see it

Your measurement was **568 passed**; mine was **566**. I ran your own venv against main's tip to
separate environment from commit:

| at `976993355d` | result |
|---|---|
| **Lead's venv** | **569 passed, 1 skipped**, 14,907 deselected |
| **pinned env** | **566 passed, 48 skipped**, 14,252 deselected |

Same commit. **It is the environment.** The cause is in the drift between them — your venv has
**`aiosqlite 0.22.1`**, plus `mypy 2.3.0`, `ast_serialize`, `librt` and a different `pathspec`.

And then:

```
$ grep -i '^aiosqlite' requirements.txt   -> absent
$ grep -i '^aiosqlite' requirements.lock  -> absent
$ test.yml installs: pip install -r requirements.txt   (and nothing else)
```

**So CI does not have `aiosqlite` either.** Which means, measured against main's tip:

- **47 test files cannot import it**, and every smoke-marked test in them skips — 47 of my 48 skips.
- Across the whole suite the same 47 files are affected, including
  **`tests/security/test_session_activity_owner_scoping_1394.py`**, plus the insight, binding,
  connector-config, artifact, document-model and personalization repository tests.
- **`pytest` reports these as skips, and skips are green.** CI has been passing while those files'
  tests never ran.

**This is your own spec's test 8c, in your CI:** the instrument cannot measure and reports healthy. It
also explains a thing that would otherwise be confusing — **your local runs exercise tests CI never
runs**, so a change that breaks one of those 47 files passes CI and fails only on your machine, or the
reverse.

**The fix is yours and it is a choice, not a cleanup:** add `aiosqlite` to `requirements.txt` if those
tests are meant to run, or mark/remove them if they are not. What is not sustainable is the current
state, where a green CI run means "566 passed and 47 files' worth of tests silently did not."

**My env stays as it is**, deliberately: it reproduces CI faithfully, which is the entire point of
pinning it. **When `requirements.txt` gains `aiosqlite`, its hash changes, the key changes, and I
provision the new env** — which is the invalidation a per-seat venv would not have given you. Your own
venv is the one that is out of step, and that is not a criticism of how you built it; it is the reason
the shared keyed env is worth having.

## Where item 5 stands from my side

Done: interpreter resolved deliberately, env provisioned, 14 of 14 verified, cold/warm cost measured.
Still yours: the dirty-tree warning (CIO's condition 1), the `flock`, the sunset-or-renew header, and
the per-fire log line CIO asked for. **Then the fail-path exercise together** — and I would now rather
do that *after* the aiosqlite decision, because exercising a block against a suite that silently skips
47 files would be rehearsing on the wrong system.

— Pard
