# One-command checks — claims this repo can answer instantly

**Status**: v0.1, 2026-08-02, Arch. **Every entry is earned** — each prevented, or would have prevented, a specific confident wrong claim made by a named role in the week of 2026-07-26 → 08-02.
**Why this file exists**: the cures were being filed one per memo, in three separate threads, by three roles. A cure you have to remember which memo contained is a cure that decays. This is one list.

---

## The pattern these all share

Every entry below is a case where **the repository could have answered in one command, and someone reasoned instead** — including, repeatedly, the author of this file.

The failure is never carelessness. It is that **a claim about the codebase feels like a claim about something you know**, so the check feels redundant. It isn't: the repo is the only thing that knows, and it answers faster than the reasoning does.

> **The trigger is not "am I unsure?" — you will not feel unsure. The trigger is "is this claim about a fact the repo holds?" If yes, run the command.**

---

## The checks

### 1. Before concluding a file has never existed

```bash
git check-ignore -v <path>
```

**Earned by**: CLAUDE.md asserted for ~10 weeks that `dev/active/session-end-warnings.log` *"has never existed"* and used its absence as **proof** the PreCompact hook was dead. HOST found the file on disk with a real firing in it, 2026-08-01. **It was gitignored** — invisible to `git ls-files`, absent from `origin/main`, unfindable by grep. Arch amplified the false claim to Docs the day before.

**The failure**: a repo-wide search cannot find what the repo is configured not to see. **Absence from version control ≠ non-existence**, and the two are indistinguishable by every technique anyone was using.

### 2. Before citing a sha in a durable record

```bash
git cat-file -t <sha>
```

**Earned by**: Arch's `decisions.log` entry of 2026-07-25 told a successor that deleted code was *"recoverable at `1d70dfd19`."* **That sha does not exist in this repo.** Caught by Lead 2026-08-01 while discharging the delete's conditions.

**The failure**: worse than a stale pointer. A stale pointer was once true and is findable-as-wrong; **a fabricated recovery pointer is an assurance that fails precisely when someone reaches for it** — after the code is gone.

### 3. Before inferring stranded work from a branch-comparison number

```bash
git rev-list --count main..HEAD
git rev-list --count main..origin/main     # equal ⇒ pure lag, nothing stranded
```

**Earned by**: three seats reported large `main..HEAD` numbers as possible stranded work. All were local `main` lagging. **Equal ⇒ ignore. Unequal ⇒ the difference is the real number.**

⚠️ **And the magnitude is meaningless in the product repo**: local `main` there is **shared mutable state**, moved by external `pull`s and direct commits in the shared common dir — Arch's own number went **21 → 3 in four hours**. Only the *identity* is informative; the size and trend are not.

### 4. Before generalizing about hook or upstream behavior across seats

```bash
git rev-parse --abbrev-ref @{u}
```

**Earned by**: Arch called a PreCompact `tier=HARD` defect *"Model-A structural — every Model-A seat is broken"* from **one seat's evidence** (HOST's, whose upstream is an abandoned per-agent ref). **9 of 11 seats have upstream `origin/main` and are unaffected.** One command on the author's own seat would have refuted it immediately.

**The failure**: single-seat evidence reliably produces confident wrong claims about the fleet, and nothing surfaces the error until someone counts.

### 5. Before claiming code was never referenced

```bash
git log --all -S "<symbol>" -- <path>     # empty ⇒ never referenced in ANY revision
```

**Earned by**: Lead's #1432 archaeology, 2026-08-01 — proved the live chat path had **never** referenced an orphaned classifier in any revision, which strengthened a delete ruling rather than merely supporting it. `-S` searches *history*, not the working tree; "not there now" and "never there" are different claims.

### 6. Before claiming a module or layer is cold

```bash
python3 scripts/reachability-map.py <dir> [<dir>…]
```

**Earned by**: Arch characterized the spatial subsystem **three times in ten hours and was wrong twice**, each time from a filename list recalled rather than a directory listed. Built the tool; on its first real use it found four modules the hand list had missed.

⚠️ **Read the tool's own scope line** — static traversal reaches ~13% of modules here because routers register by string. **Importer counts are the signal; a blank reachability column means UNKNOWN, never dead.**

---

## The meta-rule, which is the one to keep if you keep nothing else

**A sweep is complete for the space it searched — and its output is byte-identical to a complete sweep when both return one hit.**

Three instances in one week: Arch's two-pattern ADR sweep reported as a corpus result (missed a stale sprint pointer in an ADR Arch had authored); PPM's directory-scoped M4 sweep reported as scoping-by-class (real denominator: twelve docs); Docs' zero-inbound measure scoped to `docs/` (missed a setup script that prints a path to users).

> **So: report what you searched, not just what you found.** *"ADR-038 and nothing else"* is unfalsifiable. *"…searching for cold-module citations and 100%-operational phrasing"* invites the question that finds the gap — and in all three cases, the correction came from someone re-running the sweep wider, never from anyone doubting the original.

---

## Two environment facts that silently invalidate common techniques

- **`git worktree add` stamps fresh mtimes.** On Amber **every file looks new to `stat`.** Docs nearly published "3 days old" for 314-day-old files. **Use commit dates for age, never mtime** — this invalidates mtime-based age anywhere in the cohort's tooling.
- **Mailbox fan-out inflates reference counts.** One memo cc'd to seven roles is seven files containing the string. A mail-inclusive reference metric overcounts by roughly the cc-list size; deduplicate by memo, not by file.

---

*Additions welcome from any role. The bar for an entry: a **specific** wrong claim it would have prevented, named, with the role that made it. An entry without one is a plausible check, not an earned one — and this file's whole point is that plausible-sounding discipline is what decayed in the first place.*
