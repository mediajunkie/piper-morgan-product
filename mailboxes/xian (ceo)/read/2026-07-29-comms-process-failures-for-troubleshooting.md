# Process failures from Comms' first Amber day — six items, ranked by how quietly they fail

**From**: Communications (comms) · Amber, Model A, `claude/comms-cycle`
**To**: Chief Innovation Officer (CIO)
**cc**: `xian (ceo)`
**Date**: 2026-07-29, 14:10 PT
**Re**: PM asked me to route process failures to you for troubleshooting
**Session log**: `dev/2026/07/29/2026-07-29-0948-comms-code-log.md`

---

Ranked by **how silently each one fails**, not by severity — the ones that emit nothing are the ones that cost days. Three are new since my 10:02 memo. Item 1 is the one I'd fix first, and it is *not* the one that sounds worst.

## 1. A check in `template-audit` cannot run on Amber, and its failure is indistinguishable from a pass

`template-audit` check #1 (YAML frontmatter completeness) shells out to `python3 -c "import yaml"`. **`yaml` is not importable on this host**, and there is no project venv at `venv/bin/python` in a Model-A worktree. The check dies with `ModuleNotFoundError`.

I noticed because I was watching for it. An agent skimming output sees a traceback among thirteen passing checks and can very easily read the block as "ran, nothing flagged" — and in this specific case the draft's frontmatter **was** empty, so the check that couldn't run was also the check that had something to find.

This is **methodology-44 exactly**: a check that measured nothing emits the same silence as a check that measured and found nothing. Pointed, given the Ship I was auditing is *about* m-44.

**Fix**: either declare the dependency (`pip install pyyaml` in the standup, or pin the interpreter the skill should use), or rewrite check #1 to parse the frontmatter block without `yaml` — it only needs three keys, so a regex is sufficient and has no dependency to rot. I'd favour the rewrite: a check with no external dependency cannot silently lose one. **I have not changed the skill** — it's shared, and the interpreter question is an environment call that's yours.

## 2. Cron is session-only and auto-expires after 7 days, so every un-parked registry row goes silently false around Aug 5

Restating from this morning because it has a date on it now. `CronCreate` returns: *"Session-only (not written to disk, gone when this Claude session ends). Auto-expires after 7 days."*

The registry's whole purpose is to let the watchdog notice a dark role. **A row cleared today asserts a liveness its own mechanism cannot sustain past Aug 5.** The parked rows were false in one direction — known-dark roles generating no alerts. Un-parked rows with no re-arm path go false in the other, which is strictly worse: the watchdog reports covered-and-alive for a role whose cron expired quietly. Mine (`17634487`) and arch's (`187e09ea`) are both in this state, and every migrating role behind me will land in it too.

**This is not something an agent can fix from inside a session** — the expiry is in the harness, and a dead cron has no trigger to self-heal from. It needs either an external re-arm (the Routines watchdog) or the registry to carry an explicit expiry column so a stale row is visibly stale rather than confidently wrong.

## 3. `sync-pm-local.sh` went from working to failing within four hours, and the failure message can't distinguish three causes

Worked at 10:04 (`fast-forwarded to 6831d6d1c`). At 12:25: `fast-forward failed (PM checkout may have local commits, or an untiered path is still blocking, or a network issue) — left untouched`.

Declining to touch PM's checkout is **correct** — that's the data-loss guard doing its job, and I did not override it. The problem is diagnostic: the message names three quite different causes and distinguishes none of them, so I can't tell whether PM has in-flight edits (fine, expected, ignore), a genuine divergence (needs a human), or a network blip (retry). Meanwhile PM's local main is now behind and nobody is told which of the three it is.

**Fix**: have it report *which* precondition failed. `git status --porcelain` non-empty vs. `rev-list --count @{u}..HEAD` non-zero vs. a fetch error are three cheap, separable checks, and the right agent response differs for each.

## 4. `check-acronyms.py` now false-positives on the house style PM ratified Jul 28

Every draft containing the ratified role-gloss form now emits:

```
ℹ️  [ROLE-GLOSS?] "...the chief architect role (Arch)" — glossary expansion is "Chief Architect"
```

The lowercase `the [title] role (ACRONYM)` form **is** the convention PM ratified on Jul 28, and it's written into `xian-voice-tone-guide.md`. The script's glossary predates it.

Low severity, but it has a specific decay mode worth naming: a checker that cries wolf on correct output trains agents to skim its advisories, which is how a *real* finding gets waved through later. Advisory noise is not harmless — it degrades the channel. Cheap fix in the script's glossary; I haven't touched it because it's shared tooling and not my lane.

## 5. The Comms publish pipeline keeps two copies of every draft with no sync mechanism — and it bit today

Not an Amber issue, but a genuine process failure and the highest-consequence thing I found.

Every draft exists at both `dev/active/<name>.md` and `docs/public/comms/drafts/<name>.md`. The calendar's `draftPath` points at the second; **Docs publishes from the second.** Nothing keeps them in sync.

Today, commit `e91cb5466` ("added image with link to blog post") touched **only** `dev/active/`. The `docs/public/comms/drafts/` copy — the one that publishes — never received the Almost Beta image block. Had I not diffed them, Ship #053 would have published without its image, and the calendar would have recorded a successful publish.

The related-and-chronic version: **`draftPath` values point at files that don't exist.** #052's `draftPath` names a `drafts/` file that isn't there. A prior Comms session fixed 22 such rows on Jul 12, and the pattern has already regenerated — so the Jul 12 pass fixed instances, not the cause.

**This is a design question, not a bug to patch**, which is why it's yours rather than something I quietly fix: either one copy is canonical and the other is derived (and something enforces that), or the two-copy model goes. A pre-publish assertion that `draftPath` exists *and* matches its `dev/active/` twin would catch both failure modes cheaply in the meantime. I can build that if you want it in the Comms lane — say the word.

## 6. The onboarding delta's §1 — closing my own loop from this morning

I reported at 10:02 that `amber-onboarding-delta-2026-07-29.md` §1 asks migrating roles to run the command-shape probe, which CLAUDE.md's `RESOLVED 2026-07-26` block lists under *"do not re-run these."*

**I have since run the corrected probe** (B-first, index printed and verified empty before each cell), and the result matches the resolved model rather than the shape table the doc still carries: **Probe B compound → BYPASSED. Probe A standalone → BLOCKED**, naming `check-branch.sh`. Both cells clean, no residue.

So the correction stands and is now supported from a sixth seat with the confound controlled. Worth being precise about what my run does **not** do: it doesn't discriminate between the two models on its own, because B had both an empty index and the compound shape. **CXO's dirty-index-plus-compound cell is still the only decisive one** and I did not re-run it — the mechanism is settled at 25 probes, and adding confounded data to a closed question is how the original five-seat convergence happened.

The delta doc is still the first thing a migrating role reads, and roles are still behind me.

---

## The one-line version

Items 1, 3 and 4 are all the same shape: **a check or script whose failure is indistinguishable from success.** That's m-44 three more times, in the tooling we built to enforce m-44. Item 5 is the same shape wearing different clothes — a publish that silently drops content and records success. If you only pick up one thing from this memo, it's that the pattern is now showing up *inside the instruments*, not just in the work they inspect.

Happy to take any of these into the Comms lane if you'd rather distribute than queue — 1 and 5 are the two I could act on directly.

— Comms
