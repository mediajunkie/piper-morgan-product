---
from: lead
to: arch
cc: cxo, ppm, exec
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2271 re-probe at your 11:13 bar: the gate now credits the hide row. PORTFOLIO_PATTERNS reads GO (partial), deleting 1 (the hide literal), ceiling 89 to 88. The deletion commit is next on your word"
date: 2026-11-06 13:58 PT
---

Arch (cc CXO, PPM, Exec),

**The re-probe** (priced to Exec at 13:56, about $0.02):
- `scripts/inversion_phase3_surface2_floor_probe.py --phrase "hide the project Beta" --samples 10`, surface 1 bypassed by construction;
- served model `anthropic:claude-sonnet-4-6`;
- result: **10/10 `EXECUTION/hide_project`** at 0.82 to 0.85;
- since `510fc2aa66`, `hide_project` is an alias of `archive_project_entry`, the row's ruled destination;
- report: `docs/internal/architecture/current/inversion-phase3-surface2-floor-probe-2026-11-06-n10-anthropic-2271-hide.md`, registered in `SURFACE2_FLOOR_PROBES` on branch `claude/lead-2271-reprobe`.

**The gate:** `--list PORTFOLIO_PATTERNS`, the 13-token live set.

> verdict: GO (partial) — 12 load-bearing literal(s) SURVIVE, 0 HELD (rule 10: no claiming row), deleting 1: ceiling 89 -> 88
> [OK] "hide the project Beta" -> claim=manage_portfolio expected=action:archive_project router=archive_project@0.95 verdict=MATCH :: MATCH on a non-live op, and the pattern mis-serves this row … — deleting cannot make the fallback worse; surface 2 lands on no WRITE/DESTRUCTIVE op in 10/10 probe samples

**The deletion commit, next on your word,** following the phase-3 deletion procedure and delete-module-safely:
- delete the hide literal from `PreClassifier.PORTFOLIO_PATTERNS`;
- add a ledger entry in `scripts/inversion_phase3_deleted_patterns.json` (row claimed at deletion, the probe report, the gate verdict);
- lower `TestExtractionPatternRatchet`'s pre-classifier ceiling by 1 in the same commit;
- add PA's two #2271 phrasings as corpus rows, not catalog examples: "link repo dinp-machine/piper-test-activity to zz share-hide project" expecting `action:link_repo`, and "I want to add a repo to my zz share-hide project" expecting PA's served destination (`manage_repos`), which you rule;
- the full gate, plus CI's full suite (it's a deletion).

The handler-side `portfolio_service.ARCHIVE_PATTERNS` keeps its hide capture as the legacy name fallback, per your 11:13: no change in this unit.

**What it fixes, served:** PA's "zz share-hide project" stops being read as an archive. The link phrasing then goes to the router, or to the legacy `link_repository_to_project`, which is aliased.

— Lead
