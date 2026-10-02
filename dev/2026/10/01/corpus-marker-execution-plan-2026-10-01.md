# Corpus pruning & consolidation — execution plan (standing item 7a)

**Author**: CIO · **Date**: 2026-10-01 · **Issue**: #1919 · **Status**: PLAN, audited (`7a-gameplan-audit.md`); execution waits on PM's two confirmations in §9 (no edits made yet)
**Authority**: PM, 2026-10-01 (in conversation): "Pruning and consolidation is approved, if done
carefully with a thoroughly audited plan." Recorded in decisions.log, 2026-10-01 16:4x.

## 1. What this plan is, and what it turned out NOT to be

I started from my own standing-items row, which described May 2026's "~60% zero-citation" finding as
the work. **That row was stale.** The 2026-08 architectural review's **B3 pass already dispositioned
both corpora entry by entry**: patterns 81/81 (Docs), methodology-core 64/64 (CIO). Arch ratified
it on 2026-09-01, and the cross-corpus overlaps were resolved in the same motion (m-07 ← P-006,
m-22 ← P-059, m-02 → P-029, gameplan-template absorbed). B3's central finding was that **citation
count mispredicts effectiveness**, so it is not a pruning signal. Re-running a citation census
confirmed this from another angle: it returned 0% zero-citation, because B3's own census artifacts
cite every entry.

**So there is no new pruning judgment to make.** The work left is B3's ratified dispositions that
were **never carried out in the files themselves**: "absorb-and-mark is one motion"
(`living-core-docs.md` §5), and the marking half was done for only some files. This plan
**executes ratified decisions**. It does not make new ones.

## 2. The gap, measured (regenerable)

Source of truth: the Disposition column of
`docs/internal/architecture/reviews/2026-08-architectural-review/b3-methodology-disposition.md` and
`b3-patterns-disposition.md`. Parsed for rows whose disposition tag (the bold lead) contains
HISTORICAL or ABSORBED. Then each file's first 2,500 chars were checked for a
HISTORICAL/ABSORBED/SUPERSEDED marker.

| Corpus | HISTORICAL/ABSORBED rows | Already marked in-file | Needs marker |
|---|---:|---:|---:|
| methodology-core | 24 | 4 (m-02, HOW_TO_USE_MULTI_AGENT, MULTI_AGENT_INTEGRATION_GUIDE, MULTI_AGENT_QUICK_START) + gameplan-template (pointer stub, done) | **18** (19 minus m-19, see below) |
| patterns | 6 | 3 (P-006, P-059, P-024) | **3** |

**Excluded on purpose:**
- **m-19 (INTEGRATION-POINTS)**: B3: "HISTORICAL (body); banner is the only live part… The file's own
  2026-08-12 banner already documents this correctly." Its banner IS its marker, so no edit.
- **m-01, m-15**: EFFECTIVE (principle live, case study historical). A loose parse caught them and the
  strict parse correctly excluded them. Out of scope.

**Worklist, 21 files:**
- methodology-core (18): `methodology-05-AGENT-METHODOLOGY.md`, `methodology-06-CORE-PATTERNS.md`,
  `methodology-08-ISSUE-TRACKING.md`, `methodology-10-SYSTEMATIC-BREAKTHROUGHS.md`,
  `methodology-11-ORCHESTRATION-TESTING.md`, `methodology-12-ENHANCED-AUTONOMY.md`,
  `methodology-14-DOCUMENTATION-STANDARDS.md`, `methodology-16-STOP-CONDITIONS.md`,
  `methodology-18-CASCADE-PROTOCOL.md`, `README.md`, `METHODOLOGY-DISCOVERY-GUIDE.md`,
  `enhanced-autonomy-continuity-protocols.md`, `enhanced-autonomy-experiment.md`, `chat-protocols.md`,
  `multi-agent-templates.md`, `working-method.md`, `claude-code-workflow.md`, `resource-map.md`
- patterns (3): `pattern-015-internal-task-handler.md` (HISTORICAL),
  `pattern-016-repository-context-enrichment.md` (**LIKELY** HISTORICAL; its caveat is carried into
  the marker verbatim), `proposals/pattern-family-index-proposal.md` (ABSORBED into
  `PATTERN-FAMILIES.md`)

## 3. The index problem (found while scoping, and it's the higher-value half)

`methodology-core/INDEX.md` **actively routes agents to historical entries as if current**: m-02 is
labelled "authoritative reference" and ⭐ in three places (L26, L69, L81), although B3 executed it as
HISTORICAL with `pattern-029` as its live successor. About 15 other historical entries are listed with
no status, several with ⭐ (e.g. m-08 L90). `patterns/README.md` lists P-015/P-016 (L44, L56) the same
way. A marker inside a file doesn't help an agent who never opens it because the index already
pointed elsewhere.

## 4. Exactly what will change (and what won't)

**Each of the 21 files**: one blockquote banner inserted directly after the title (after frontmatter if
present). No other byte of the body changes. Template:

> **⚠️ HISTORICAL — not current practice.** Dispositioned in the 2026-08 architectural review (B3),
> ratified by Arch 2026-09-01 (tracker: `<tracker path>`). **Why** (tracker's words): <the
> disposition text's first sentence, verbatim>. Kept for history. Do not follow it as instructions.
> *(Marker added 2026-10-01, CIO, standing item 7a, PM-approved.)*

Variants: P-016 says **LIKELY HISTORICAL** and keeps the tracker's caveat. The family-index proposal
says **ABSORBED** into `PATTERN-FAMILIES.md`. The successor text is quoted from the tracker, never
invented. Where the tracker names no successor, the banner names none.

**`INDEX.md`**: each line linking a worklist or already-marked historical file gets a trailing
` _(HISTORICAL — B3, 2026-09-01)_`. The three m-02 "authoritative" lines are re-pointed at
`pattern-029-multi-agent-coordination.md`, with m-02 kept as a "(historical)" link. Stars on
historical lines are removed. **No link is deleted.**

**`patterns/README.md`**: P-015/P-016 lines get the same trailing status note (P-016: "likely").

**Frontmatter**: `last_updated` is NOT bumped. A fresh date on a historical doc reads as "current" (the #1726 bulk-stamp anti-pattern), and the banner carries its own date. None of the 21 files has a `status:` field (checked on a sample of 3; to be confirmed on all 21 at execution).

**Will NOT change**: no file is deleted, moved or renamed (so no inbound link anywhere in the repo can
break); no body text is edited; nothing is re-dispositioned. If the audit finds a row where B3's call
looks wrong today, that row is pulled from this batch and raised separately. It doesn't get
"fixed" inside an execution pass.

## 5. Execution & verification

1. One commit, 23 paths (21 files + 2 indexes), explicit-path staged. It will trip the non-blocking
   broad-staging warning (≥20 files), which is expected and noted in the commit body.
2. **Verify**: (a) re-run the marker check, so all 30 HISTORICAL/ABSORBED rows read marked (21 new + 9
   existing), with the denominator stated; (b) `git diff --stat` shows only insertions in the 21 files
   (no deletions) and small edits in the 2 indexes; (c) `git grep` that every link previously in
   INDEX.md still resolves; (d) the ratchet/doc tests that touch these dirs still pass, if any exist
   (to be found in the audit).
3. **Reversible**: a single `git revert` undoes the whole batch.

## 6. Audit answers (formerly open questions)

- **Readers of these files**: the only CI gate over `docs/` is `mailbox_bearer_lint.py` (credentials,
  which the banners can't trip). `derive-adr-index.py` (B4) reads `adrs/` only. The monthly
  housekeeping audit counts `[Pattern-NNN` links in `patterns/README.md`, and no link is removed, so the
  count is unchanged (asserted before/after). Two unit tests reference `pattern-073` only, which is out
  of scope.
- **`status:` frontmatter**: none in the sampled files. Re-checked on all 21 during execution, and any
  file with one is pulled from the batch rather than edited ad hoc.
- **Tracker "first sentence"**: reviewed per file at execution and recorded in the commit body. If a
  first sentence isn't self-contained, the banner quotes the full disposition cell instead (still
  verbatim, never paraphrased).

## 7. STOP conditions (apply during execution)

- A B3 call looks wrong against today's repo → pull that file from the batch and raise it with Arch.
- Any file has a `status:` field, or a reader/generator is found that the banner would break → pull it.
- The link check shows ANY link that resolved before and doesn't after → do not push; revert locally.
- Code Quality goes red on the resulting tip → fix or revert before anything else.

## 8. Roles, closeout, evidence

- **Agent deployment**: CIO only, no subagents, so there's no dispatch tier to set.
- **Progress**: bookend comments on #1919 at plan-audited, executed, and verified.
- **Closeout**: CIO posts evidence on #1919 against each acceptance criterion, and **PM closes it**.
  Agents don't close their own issues under the gameplan template (the cohort's close-issue skill
  differs; the template wins here because it's what this plan is audited against).
- **Docs**: no ADR or architecture.md change (no decision made). BRIEFING-CURRENT-STATE isn't affected.
  The B3 tracker gets a one-line "markers executed 2026-10-0X, #1919" note.

## 9. Needs PM before execution

1. **Phase -1 (revised understanding)**: PM approved "pruning and consolidation". The real remaining
   scope is narrower: execute B3's already-ratified markers, with no new pruning judgment. Confirm
   PROCEED on this scope.
2. **Template applicability**: gameplan-template phases 0.5 (UI contracts), 0.6 (data flow), 0.7
   (conversation design), 0.8 (post-completion DB side effects), the integration-handler check, and
   the unit/integration/wiring/performance test rows are written for code. By their own "when to
   apply" text they look inapplicable to a docs-only marker change. Under audit-cascade rules only PM
   can rule them N/A. The doc-equivalent checks in §5 stand in for the test rows.


- Do any tests, scripts or generators read these files' first lines or the INDEX format (e.g. a derived
  index from B4, #1455), such that a banner or annotation would break them?
- Does any file have frontmatter whose `status:` field should ALSO change (and does a checker read it)?
- Is "first sentence of the tracker disposition" always a self-contained, accurate sentence?
