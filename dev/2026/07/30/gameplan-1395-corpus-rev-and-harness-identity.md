# Gameplan: #1395 — Canonical corpus rev (ADR-077 D5) + harness UUID identity fix

**Date**: 2026-07-30
**Issue**: #1395 (In Progress, MVP, Beta Blockers sprint)
**Lead Developer**: Claude (Opus 5), Amber seat
**PM ratification**: corpus-rev decision ratified by PM 2026-07-30 (decisions.log); row-level review by Arch still applies per the #1283 corpus-v2 precedent ("reviewed, not silently edited")

## Mission

Bring the canonical corpus's 7 stale `floor` expectations up to routing truth (capability growth overtook the frozen expectations), fix the harness identity bug that manufactures Q51's error, and produce a clean ≥90% criterion-2 re-run for #1386 — without silently editing a behavioral contract.

## Strategic context

- The corpus is the **behavioral contract** (ADR-077 D5). All 7 misses are `expected floor, got <real destination>` — i.e., the product got BETTER and the contract didn't move. This rev is bookkeeping of ratified reality, not a bar-lowering.
- Q51 is a **two-layer finding**: real routing growth (canonical productivity handler) PLUS a harness artifact — the e2e user id (`canonical-e2e-q51-<hex>`, 26 chars) is not a UUID; the handler feeds it to `owner_id::UUID` → asyncpg DataError → generic error. The harness must mint UUID identities or Q51's quality row stays poisoned regardless of the corpus rev.
- Relation: #1386 criterion 2 reads directly off this; PM moved #1386's verification urgency up this morning (Exec locking the scenario window separately).

## Success criteria (executable)

```bash
# 1. Corpus rev applied — exactly 7 rows changed, each to the destination the trace showed
git diff HEAD~1 -- <corpus file> | grep -c '^[+-].*floor'   # touches only the 7 ratified rows

# 2. Harness identities are UUIDs
grep -n "canonical-e2e" tests/e2e/<harness>  # → uuid4()-based principal, no 26-char slugs

# 3. Criterion-2 re-run clears the bar (judge on; ANTHROPIC_* stripped per CLAUDE.md)
env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS \
  POSTGRES_PORT=5433 venv/bin/python <canonical-retest harness> 
# → routing ≥90% (expect 61/61 or near; was 54/61 with all 7 misses being these rows)
# → quality stays in the 80–86%+ band (was 92%); Q51's error-fingerprint GONE

# 4. Evidence on the issues
gh issue view 1395   # closing evidence per close-issue-properly
gh issue view 1386   # criterion-2 comment updated with the new run
```

## Phase structure

### Phase 0 — Verify infrastructure (STOP-condition gate)
Everything below assumes the Amber seat is sweep-capable and the harness's dependencies carry. **Verify, don't assume** — three first-touch unknowns on this host:
1. Seat acceptance complete: venv built, `--collect-only` ≈ 11,111, compose stack healthy (`pg_isready -p 5433`, redis ping), one full sweep green against backlog gate. *(In flight now — install running.)*
2. **Keychain keys on Amber**: conftest auto-loads OPENAI/ANTHROPIC via KeychainService (service `piper-morgan`, `_api_key` suffix). The Amber keychain may simply not have them (predecessor handoff §5 Q2 — never verified here). Without ANTHROPIC the in-process judge can't run. If absent → STOP, ask PM to provision keys (never guess/proceed keyless and call judge results comparable).
3. Locate the canonical corpus file + retest harness entrypoint; confirm Run-15 (7/12) is reproducible as baseline BEFORE changing anything (one baseline re-run, expect ≈54/61 again). A moved baseline invalidates the comparison.

### Phase 1 — Corpus rev (the contract change, done in the open)
1. Draft the 7-row diff exactly per the #1395 table (Q22→canonical/analysis, Q36→action, Q44→action, Q45→action, Q48→action, Q51→canonical/query, Q63→action).
2. **Send Arch the row diff for review** (their memo already has draft changes attached — reconcile mine against theirs; the #1283 precedent is review-then-commit, and PM's ratification this morning covers the *decision to rev*, Arch's review covers the *rows*). Fast turnaround expected; not a blocker for Phase 2 prep in parallel.
3. Commit the rev with the ratification trail in the message (PM 7/30 + Arch review pointer). Corpus rev gets its own commit, separate from harness code.

### Phase 2 — Harness identity fix
1. Harness mints UUID principals (uuid4), replacing the 26-char slug scheme; keep a readable prefix in a separate field/log line if traceability wants it.
2. Teardown still cascades via `delete_test_user_fully` (the UUID change must not orphan rows — verify the teardown keys on the same principal).
3. **Optional hardening, explicitly deferred unless cheap**: productivity handler degrading gracefully on malformed principals. It's product code with its own test burden; the harness fix alone cures Q51. If deferred → note on #1395 at close (no silent scope-shrink — flagging per completion discipline).

### Phase 3 — The re-run (evidence)
1. Full canonical suite, judge on, env stripped, from the accepted seat.
2. Expected: routing ≥90% with the 7 former misses now passing; quality in band; Q51 fingerprint gone.
3. **STOP condition**: any NEW drift row (a miss that isn't one of the 7) → stop, report to Arch+PM before touching the corpus again — new drift means capability moved again since 7/12, and the contract change needs its own ratification, not an opportunistic edit.

### Phase 4 — Close with evidence
Per close-issue-properly: evidence block on #1395 (diff summary, run output, files), criterion-2 update comment on #1386, board Status #1395 → In Review (PM verifies) → closed on PM's nod. decisions.log already carries the ratification.

## Effort estimate
Phase 0: riding on seat acceptance (today) + ~30 min verification. Phases 1–2: ~1–2 hours of change work (7 corpus rows + one harness identity site). Phase 3: one suite run (~10–20 min runtime, unknown Amber baseline). Arch review latency is the only external dependency. **Realistic: done tomorrow if Phase 0 clears today and Arch reviews within a day.**

## What this deliberately does NOT do
No handler/routing code changes (the product is already routing correctly — that's the finding). No corpus changes beyond the 7 ratified rows. No judge-prompt changes (Q45's MARGINAL is a strictness note, not a defect).
