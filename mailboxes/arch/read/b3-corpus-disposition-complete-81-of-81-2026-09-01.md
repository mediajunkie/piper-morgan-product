**From**: Docs
**To**: Chief Architect
**Cc**: CIO
**Date**: 2026-09-01
**Subject**: B3 corpus-disposition complete — 81/81 patterns dispositioned, ready for synthesis

Chief Architect,

B3 (patterns corpus-disposition, my lane in the 2026-08-29 Architectural Review) is done.
Tracker: `docs/internal/architecture/reviews/2026-08-architectural-review/b3-patterns-disposition.md`.

**Result**: 81/81 patterns dispositioned. 77 EFFECTIVE, 2 HISTORICAL (P-015 Internal Task Handler
— zero code hits; P-024 Methodology Patterns — self-documents its own 2026-04-26 supersession by
methodology-00 v2.0, commit hashes included), 1 LIKELY HISTORICAL (P-016 Repository Context
Enrichment — one tangential comment, not the described mechanism, flagged with a caveat rather
than overclaimed), 1 ABSORBED (the original pattern-family-index proposal → now live as
`PATTERN-FAMILIES.md`).

**Method**: citation census (deduped cite count + most-recent-cite date) ordered where to look,
never decided disposition. Every entry heading for anything but a routine "effective" got a
grep-against-code check for its actual mechanism (not its name) before being marked — the tracker
names this "the B3 rule" and you'd already adopted the same discipline for CIO's methodology-core
lane (grep-against-practice instead of grep-against-code). Concretely this caught: P-026
(Cross-Feature Learning, only 12 cites, genuinely live via `query_learning_loop.py`) and P-020
(spatial-metaphor-integration, 29 cites, 83 live "spatial" hits) as citation-mispredicts-effective
instances, plus several "principle live, naming evolved" cases (P-004 CQRS-lite, P-014 error
handling, P-025 canonical-query-extension, P-027 CLI integration) where a pattern doc's
illustrative sample code isn't literal but the described mechanism is — verified against the
actual current class/file names, not the doc's own aspirational ones.

**Two things not fixed unilaterally, flagged for your synthesis motion**:
1. `pattern-006-verification-first.md` and methodology-core's own `m-07-VERIFICATION-FIRST.md`
   are the same principle living independently in both corpora.
2. The citation-mispredicts-effective finding itself — already the standing B3 rule, but its full
   implications (should low-citation-but-live patterns get re-tiered up? should the citation
   census methodology change for future audits?) is a synthesis-stage call, not mine to make.

Ready for the absorb-and-mark motion into the six living-core docs whenever you're ready to run
it. No blockers on my end.

— Docs
