# `origin/main-old` stranded-commit review — 2026-09-24

**Model observed running as (dispatch-logging convention): Claude Sonnet 5 (claude-sonnet-5).**
Dispatched by Exec (Chief of Staff) at PM's direct instruction. Read-only analysis task; this file is the one permitted write.

**Question being answered**: is anything critical stranded on `origin/main-old` that isn't on `origin/main` — "a missing cog the current build depends on without anyone knowing it's missing" — or is it all obsolete/superseded?

**Bottom line: NO. Nothing critical is stranded. High confidence, no uncertain items remain.**

Of the 503 commits unique to `main-old`, 494 are content-identical (by patch-id) to a commit already
in `main`'s own 28,197-commit history — i.e. not stranded at all, just reached `main` by a different
commit path. The only 2 commits with no content-equivalent anywhere on `main` are pure documentation/
shell-script additions for a manual "create a sprint" workflow (Oct 8 2025) that has been fully
superseded by `main`'s current GitHub-Projects-v2-based Sprint field and its dedicated tooling
(`scripts/sprint-truth.py`, `scripts/restore-sprint-field-from-snapshot.py`, the `assign-sprint-safely`
skill — all canonical per this repo's own CLAUDE.md). The 7 merge commits in the 503 add no content
beyond what's already accounted for by their constituent non-merge commits.

---

## Verified counts

| Metric | Command | Result | Note |
|---|---|---|---|
| Commits on `main-old`, not on `main` | `git rev-list --count origin/main..origin/main-old` | **503** | Exact match to the number given in the task brief. |
| Commits on `main`, not on `main-old` | `git rev-list --count origin/main-old..origin/main` | **28,197** | Brief estimated ~27,685; grew ~512 in the interim — consistent with normal ongoing commit volume on `main` between when that estimate was taken and now (2026-09-24), not a discrepancy worth chasing. |
| Non-merge commits in the 503 | `git log --oneline --no-merges origin/main..origin/main-old \| wc -l` | **496** | |
| Merge commits in the 503 | `git log --oneline --merges origin/main..origin/main-old \| wc -l` | **7** | 496 + 7 = 503. ✅ |
| Patch-id equivalent to something in `main`'s history (`-`) | `git cherry origin/main origin/main-old` | **494** | Content already lives in `main`'s lineage under a different commit. |
| NOT patch-id equivalent to anything in `main`'s history (`+`) | same | **2** | The only commits whose diff content is absent from `main`'s entire history. Both are the same PR (#219, "sprint creation system"). |

`git cherry` only evaluates non-merge commits (494 + 2 = 496, matches exactly). The 7 merges were
inspected individually (below) since `git cherry` doesn't score them.

---

## Classification table

| Class | N | Definition |
|---|---:|---|
| **Superseded by content-equivalence** | 494 | Patch-id-identical to a commit already in `main`'s 28,197-commit history. Mechanically verified for all 494 via `git cherry`; separately spot-checked 19 of the highest-risk-looking ones by name (security/auth/migration/Docker — see Spot-check section) by hand-matching full SHA against the cherry output. |
| **Superseded by successor mechanism** | 2 (+ 1 merge that only merges them) | Content genuinely absent verbatim from `main`, but the *function* it served has a current, more mature replacement on `main`. See below. |
| **Genuinely absent, no successor found** | **0** | None. |
| **Merge commits — net-new content beyond constituent commits** | 0 of 7 | All 7 merges' diffs are fully explained by non-merge commits already classified above; none introduces content the underlying commits don't already carry. |

Total: 503 = 496 non-merge (494 equivalent + 2 successor-superseded) + 7 merges (0 additional unique content).

### The 2 patch-id-absent commits (the entire "genuinely absent" set)

Both are from copilot-swe-agent PR #219, merged as `main-old`'s tip commit (`5275936ee7`, 2025-10-26):

- `fa857f27082162c32697e68c66f928a59e0d40d0` — "Complete sprint creation system: methodology,
  automation scripts, and documentation" — adds `docs/HOW-TO-CREATE-A-NEW-SPRINT.md`,
  `docs/SPRINT-CREATION-SUMMARY.md`, `docs/internal/development/methodology-core/methodology-21-SPRINT-CREATION.md`,
  `scripts/create_sprint.sh`, `scripts/new-sprint`, plus three `dev/2025/10/08/` planning docs. 1,641 lines, all new files.
- `29e87a52e3f4a51695507798717c176eac4026b6` — small 6-line follow-up fix to the same files.

**What it is**: a local, file/script-based "spin up a new sprint" methodology and its automation
(`create_sprint.sh`, `new-sprint`).

**Verified absent, not just renamed**: checked every path these commits touch (`docs/HOW-TO-CREATE-A-NEW-SPRINT.md`,
`docs/SPRINT-CREATION-SUMMARY.md`, `scripts/create_sprint.sh`, `scripts/new-sprint`, `dev/2025/10/08/AGENTS.md`)
against `origin/main` with `git cat-file -e origin/main:<path>` — all report "does not exist." Grepped
`main`'s full tree for `methodology-21` and `SPRINT-CREATION` — no match anywhere under any path.

**Does the current build depend on it?** No — it has a successor mechanism, and a much more mature one.
Current `main`'s CLAUDE.md documents Sprint membership as a **GitHub Projects v2 board single-select
field**, not a local script/methodology-doc workflow, with a dedicated skill
(`assign-sprint-safely`) and purpose-built scripts already present on `main`
(`scripts/sprint-truth.py`, `scripts/restore-sprint-field-from-snapshot.py`) — plus hard-won
incident history (the 2026-07-05 full-option-list-replace wipe of 1,175 issues' sprint assignments)
that the old file-based methodology never had to reckon with. This is a full architectural
generation ahead of the Oct-2025 script, not a gap.

**Confidence: high.** Nothing currently loads, sources, or references `create_sprint.sh`,
`new-sprint`, or the two docs anywhere on `main` (checked by path and by grep for the
distinctive `methodology-21`/`SPRINT-CREATION` strings — zero hits).

### The 7 merge commits — individually inspected

| SHA | Date | What it merges | Verdict |
|---|---|---|---|
| `5275936ee7` | 2025-10-26 | PR #219 (the sprint-creation commits above) | Fully accounted for by the 2 commits above. |
| `26dda2ce44` | 2025-08-15 | PR #111, "Enhanced Autonomy Multi-Agent Coordination System" — adds an early `CLAUDE.md` (139 lines), `pattern-catalog.md`, blog images, `gitbook-integration-plan.md` | Every constituent non-merge commit already scored `-` (content-equivalent) by `git cherry`. The 139-line proto-`CLAUDE.md` is a distant ancestor of today's file (which we have in full in this session — it is now enormously more developed); no unique surviving instruction was found only there. |
| `3e70b1eee3` | 2025-08-08 | Old static site scaffold changes (`site/`, `docs/*.svg`, README) | `site/` and the old exported `docs/` static-site tree are entirely gone from `main` — this predates the site's move to the separate `piper-morgan-website` repo (confirmed live in this cohort's tooling, e.g. the `publish-to-blog` skill, which explicitly bridges piper-morgan → piper-morgan-website). Not a gap; a repo split. |
| `e8aa9a0151` | 2025-08-08 | Same static-site history, explicitly flagged conflict on `piper-morgan-website/README.md` | Checked directly: `piper-morgan-website/` does not exist at `main-old`'s own tip *or* on `main` — confirmed with `git cat-file -e` on both refs (both report "does not exist") and a full-tree grep (0 hits both sides). The conflict was resolved by removing the directory entirely, on both branches, long before either diverged further — nothing survives to be missing. |
| `1badbaae46` | 2025-08-03 | Old GitHub Pages deploy workflow + early site README | Same static-site generation, same disposition as above. |
| `3112ea9a37` | 2025-08-01 | 1-line `docs/CNAME` add | Trivial; part of the same retired static-site tree. |
| `1bf3f3fadf` | 2025-06-29 | 0-line `docs/.nojekyll` | Trivial; empty file, same retired tree. |

No merge introduces content beyond what its own constituent commits already carry, and none of the
merges' payloads (proto-CLAUDE.md, old static site scaffold) has any content living only there — the
proto-CLAUDE.md's lineage is visible in the current file; the static site moved to its own repo and
was cleanly removed from this one on both branches.

---

## Spot-check: the "sounds critical" subset (security/auth/migration/config/Docker)

Searched all 503 commit subjects for `migrat|security|secret|vulnerab|cve|alembic|\.env|docker|
requirements\.txt|schema|api[_ -]?key|password|token|auth` — 19 distinct commits matched (JWT/API-key
systems, OpenAI client migration, encrypted keychain storage, Slack/Notion/Calendar integration-router
migrations, FileRepository ADR-010 migration, WorkflowRepository migration, Docker build-context fix,
GITHUB_TOKEN inheritance fix, etc.). Cross-referenced every one of these 19 full SHAs against the
`git cherry` output by hand: **all 19 are `-` (patch-id equivalent to something already in `main`'s
history)**. None is in the 2-item genuinely-absent set. This is the highest-risk-looking subset of
the 503 and it fully resolves to "already on main."

## Broader sanity check: whole subsystems that look "missing" from a file-presence diff

A raw file-presence diff (`comm -23` of tree listings) shows ~13,400 paths that exist on `main-old`
but not on current `main`, including large chunks of `services/orchestration/`,
`services/llm/adapters/`, `services/integrations/spatial/`, `services/intelligence/spatial/`,
`services/mcp/consumer/{cicd,devenvironment,gitbook,linear}_adapter.py`, and
`services/intent_service/llm_classifier.py`. **This metric is not the same question as "stranded
commits"** — most of these paths were deleted by `main`'s own subsequent history (normal refactors
over a year), not withheld from it. Checked because the names sound consequential (spatial
intelligence is flagged in this cohort's memory as protected architecture):

- **Spatial intelligence**: alive and extensively developed on `main` — 149 hits across ADRs
  (adr-013, adr-017, adr-038), `docs/internal/architecture/current/spatial-*`, and active dev logs
  through 2026-07. The old `services/integrations/spatial/*` and `services/intelligence/spatial/*`
  files are early-generation; the concept was carried forward and heavily built out, not lost.
- **Orchestration**: old `multi_agent_coordinator.py`/`workflow_factory.py`/`chain_of_draft.py` gone;
  replaced by `services/intent_service/` (`workflow_entries.py`, `WorkflowEntry`, the pre-classifier →
  classifier → action-rail → floor stack this repo's CLAUDE.md calls out as the canonical
  intent-routing architecture) plus `alembic/versions/b942_orchestration_tables.py` and
  `services/domain/standup_orchestration_service.py`.
- **LLM adapters**: old `services/llm/adapters/{claude,openai,gemini,perplexity}_adapter.py` +
  `provider_selector.py` gone; replaced by `services/llm/{clients.py,config.py,provider_selection.py,
  request_key.py}` + `services/config/llm_config_service.py` (Keychain-first credential resolution,
  the exact mechanism this repo's CLAUDE.md documents in detail).
- **MCP consumer adapters**: old set (cicd/devenvironment/gitbook/linear) replaced by a different,
  currently-relevant set (github/google_calendar/notion/slack adapters + OAuth handler) — a swap of
  which integrations matter, not a loss of the MCP layer itself (which is present and larger on
  `main`: `services/mcp/{client.py,exceptions.py}`, `services/mcp/protocol/*`, `services/mcp/
  consumer/*`).
- **Intent classification**: old single `llm_classifier.py`/`llm_classifier_factory.py`/
  `services/queries/query_router.py` replaced by a much larger current stack (`services/intent_service/
  classifier.py`, `pre_classifier.py`, `spatial_intent_classifier.py`, plus dozens of gate/handler
  modules) — this is the exact 4-surface routing chain this repo's own CLAUDE.md calls "MANDATORY
  before touching classification, dispatch, or chat-response behavior."

None of these represents a silent gap — each has a visibly larger, actively-maintained successor on
`main` today.

---

## Answer to xian's question

**Is anything critical stranded on `main-old` — a missing cog the current build depends on without
anyone knowing? No.**

- 494 of 496 non-merge commits are provably content-equivalent (patch-id match) to something already
  in `main`'s own history — by definition not stranded, just reached `main` via a different commit.
- The remaining 2 commits (plus the merge that lands them) are the *only* content anywhere in the 503
  that is verifiably absent from `main` in any form — and they are a local sprint-creation script/doc
  set with a confirmed, more mature successor already live on `main` (GH Projects v2 Sprint field +
  `assign-sprint-safely` + `sprint-truth.py`).
- The 7 merge commits add no content beyond their own already-classified constituents.
- The highest-risk-sounding subset (security/auth/migration/Docker, 19 commits) was individually
  hand-verified and is 100% already on `main`.
- **No uncertain items remain to name.** Confidence is high, not merely "probably fine."

---

## Verified how

**Method** (exact commands, in order run):
```
git fetch origin main main-old
git rev-list --count origin/main..origin/main-old        # 503
git rev-list --count origin/main-old..origin/main        # 28,197
git log --oneline origin/main..origin/main-old            # the 503 list, spot-checked head/tail
git log --format='%H %s' origin/main..origin/main-old      # full-SHA version for cross-referencing
git log --oneline --merges origin/main..origin/main-old    # 7
git log --oneline --no-merges origin/main..origin/main-old # 496
git cherry origin/main origin/main-old                     # patch-id equivalence: 494 '-', 2 '+'
git show --stat <sha>                                       # inspected both '+' commits in full
git cat-file -e origin/main:<path>                          # existence checks for every '+'-commit path
git ls-tree -r --name-only origin/main-old > A ; git ls-tree -r --name-only origin/main > B ; comm -23 <(sort A) <(sort B)
                                                              # file-presence diff, filtered to services/web/scripts/config/alembic/main.py
git show --cc --stat <merge-sha>                             # all 7 merge commits, individually
grep -iE '<keyword-list>' 503-list.txt                       # 19-commit security/migration/config spot-check
                                                              # then hand-matched each full SHA against the cherry output
```

**Layer each measured**:
- `git rev-list --count` / `git log --oneline` = **commit-presence** layer only (which this task's
  brief explicitly warned is not sufficient — "a commit can be unmerged while its content landed via
  another route").
- `git cherry` (patch-id) = **content-equivalence** layer — the load-bearing check. It hashes each
  commit's normalized diff and checks for a match anywhere in the compared range's own diffs. This
  proves the change *is part of `main`'s lineage somewhere*; it does not prove today's `main` still
  contains that code unmodified (later `main` commits may have further evolved or removed it — but at
  that point it's ordinary `main`-side history, visible to everyone working on `main`, not something
  stranded off to the side).
- `git cat-file -e` / `git ls-tree` + `grep` = **live-tree / live-symbol** layer — used to confirm the
  2 patch-id-absent commits' specific paths are genuinely gone from `main` (not renamed), and to check
  whether "missing" subsystems from the raw file-presence diff have successor code on `main` today
  (spatial, orchestration, LLM adapters, MCP consumers, intent classification).
- `git show --cc --stat` on the 7 merges = manual inspection for merge-introduced content not
  attributable to any single already-classified commit (conflict-resolution content). Confirmed none.

**Denominator**:
- **496/496 non-merge commits** classified mechanically via `git cherry` (100% coverage of that set —
  not a sample).
- **7/7 merge commits** individually inspected by hand (100% coverage — small enough to do all of
  them, not a subset).
- **2/2 patch-id-absent commits** — the entire genuinely-absent set — fully spot-checked: full diff
  read, every touched path checked against `main`, full-tree grep for distinctive strings, successor
  mechanism identified and confirmed present on `main`.
- **19/503 commits** (the security/auth/migration/config/Docker-sounding subset) additionally
  hand-verified by full-SHA cross-reference against the cherry output, as the task's requested
  "5-10 most consequential-looking" spot-check (came out larger, 19, because that's how many matched
  the keyword grep — all were checked, none left unexamined).
- The **~13,400-file raw presence-diff** was **not** classified item-by-item (that would be a
  different, much larger question than "stranded commits," and most of it is `main`'s own normal
  file churn over a year) — it was used only as a sanity net, filtered to code-relevant directories,
  and the specific subsystems it surfaced (spatial, orchestration, LLM adapters, MCP, classification)
  were checked for successors on `main`, all confirmed present. Nothing in that filtered list was left
  as an open question — everything checked resolved to "has a successor on main."
