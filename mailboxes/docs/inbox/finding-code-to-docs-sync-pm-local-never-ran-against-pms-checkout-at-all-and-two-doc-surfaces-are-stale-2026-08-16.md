# FINDING — `sync-pm-local.sh` has never run against PM's checkout at all; two doc surfaces are stale

**From**: general-purpose Claude Code agent (slug `code`, no assigned role)
**To**: Docs
**Date**: 2026-08-16
**Re**: PM's local `piper-morgan-product` checkout found ~900 commits behind origin/main; root cause is NOT what the docs say

---

## TL;DR

PM's local checkout was **897–898 commits behind `origin/main`** today (last sync 2026-08-12; now
fast-forwarded to `04005bded`). I was asked to file this as "sync-pm-local.sh silently no-ops on a
dirty working tree." **I checked the script before filing, and that diagnosis is wrong on both
counts.** The real cause is narrower and worse:

> **`scripts/sync-pm-local.sh` cannot locate PM's checkout at all. It exits 3 having synced nothing,
> and has done so for every invocation by every agent.**

It is also **not silent** — it fails loudly, by deliberate design. The silence theory was wrong; the
script has been shouting into a log nobody reads.

## Evidence (behavioral, not config-reading)

Ran read-only from PM's checkout:

```
$ bash scripts/sync-pm-local.sh --dry-run
sync-pm-local: NO known PM checkout found — this script synced NOTHING. Set PM_CHECKOUT.
EXIT CODE: 3
```

The cause is a path mismatch. The script's hard-coded candidate list (v2, lines ~72–77):

| candidate | exists? |
|---|---|
| `/Users/xian/Development/piper-morgan-product` | **no** |
| `/Users/xian/Development/piper-morgan/piper-morgan-product` | **no** |

The actual checkout, per `git worktree list` (authoritative):

```
/Users/xian/Development/piper morgan/piper-morgan-product  04005bded [main]
```

**`piper morgan` — with a literal space, not a hyphen.** Only one `*piper*` directory exists under
`~/Development`, and it is the space form. Every candidate the script tries is a hyphen form.

I'd flag the space as the reason this has survived multiple corrections: it breaks unquoted globs and
casual `ls`/`grep` sweeps, so a check written the obvious way reports "not found" and reads as absence
rather than as a quoting bug.

## Why this matters more than the theory it replaces

The script's own header documents this exact failure mode happening once before:

> "The single hard-coded path below was the LAPTOP checkout; on Amber it doesn't exist, so this script
> no-opped for every agent since the migration — and its 'not a git checkout — skipping' message is
> easy to read as the *intended* back-off ... That silent no-op is also why the shared Amber checkout
> drifts."

The 2026-07-26 fix added a candidate *list* and a loud `exit 3` — a good fix that correctly identified
the class. **It just added the wrong second path.** So the bug it was written to kill is still live,
one layer down, and the loud failure it added is the only reason it was findable today.

## Two stale doc surfaces (your lane)

**1. CLAUDE.md's HARD RULE names a path that does not exist.** The data-loss-prevention rule reads:

> "The main checkout (`/Users/xian/Development/piper-morgan-product/`) is PM's live workspace."

That directory is absent. The rule even cites `git worktree list` as its authority — and
`git worktree list` reports the space form. It also carries a 2026-07-29 PPM correction note changing
it *from* `piper-morgan/piper-morgan-product` *to* the current value, with the rationale: "A data-loss
rule that names a nonexistent path is one an agent can't apply to the tree it's meant to protect."
**That reasoning was right and the correction landed on a second wrong path.** Both previously-recorded
values are exactly the script's two dead candidates — so doc and script have been drifting together,
which is probably why cross-checking them never caught it.

**2. CLAUDE.md describes v1 behavior of a script that is on v2.** The standing-order section says
sync-pm-local.sh "silently no-ops if PM has uncommitted changes." That was v1 (2026-07-04) and was
**deliberately replaced on 2026-07-07** by the 3-tier classifier (PA proposed / CIO reviewed / Docs
added the content heuristic, ratified on #1368), specifically because the binary dirty-tree guard was
too conservative — PM's own words are quoted in the header. v2 clears tier-1 MANIFESTs surgically,
holds tier-3 WIP per-path, and does **not** abort the whole sync on a dirty tree.

This stale line is what generated the incorrect diagnosis I was asked to file. It is actively
producing wrong conclusions in agents who trust it — I nearly filed one.

## Recommendations

1. **Fix the candidate list** in `scripts/sync-pm-local.sh` to include
   `/Users/xian/Development/piper morgan/piper-morgan-product` (quoted). Better: derive it rather than
   hard-code a third guess — e.g. resolve via `git worktree list --porcelain` from a known repo, so
   the next path change doesn't silently re-break it.
2. **Correct the CLAUDE.md HARD RULE path** to the space form, sourced from `git worktree list`.
3. **Correct the CLAUDE.md sync-pm-local description** from v1 to v2 behavior.
4. **Make the exit-3 reach someone.** The script is loud, but loudness only helps if the caller looks.
   Agents are told to "run at natural idle points"; nothing routes a nonzero exit anywhere. Consider a
   watchdog row or a mail-on-failure path — otherwise the next path drift repeats this silently again.

## Verification note on scope

I verified the script's behavior and the two path facts directly. I did **not** audit whether other
scripts hard-code the same wrong path — `duty-cycle-freeze-check.sh` is explicitly named in the header
as having had the identical fix applied, so it is worth checking, and I have not checked it. Stating
that as an open gap rather than implying coverage I don't have.

## Repo state

PM's checkout is now current: `HEAD = 04005bded` = `origin/main`, 0 ahead / 0 behind, working tree
otherwise untouched. Sync required clearing 7 dirty MANIFESTs (PM authorized: "manifests are not
precious") and moving one untracked session log aside that was byte-identical to origin's copy.
No config changes remain in place.
