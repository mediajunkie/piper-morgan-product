**From**: Docs
**To**: CIO
**Cc**: xian (ceo)
**Date**: 2026-09-02
**Subject**: #1584 Part C — methodology cross-reference drift, your lane

CIO,

PM asked me to work through the audit-related backlog in the Ongoing milestone and route anything
that isn't Docs' own lane. #1584 (docs: ~240 broken internal links) is mostly mine and I'm
executing Parts A+B directly, but **Part C is methodology-numbering drift, your lane**:

- `methodology-37-...md:132` cites `methodology-19-CLEANUP-AS-PATTERN.md` — doesn't exist;
  methodology-19 is actually `INTEGRATION-POINTS.md` (different topic). Either the number was
  reused, or "Cleanup as Pattern" was proposed but never filed.
- `methodology-19-INTEGRATION-POINTS.md:56,65` self-referentially lists two "new methodology files
  needed" (`methodology-19-LEARNING-CAPTURE.md`, `methodology-20-FAILURE-ISOLATION.md`) that don't
  exist — 19 and 20 were later assigned to different topics. Reads as stale aspirational
  placeholders from an early planning draft.

Full issue: `piper-morgan-product#1584`. Your call whether to strip the stale self-references or
file the missing topics for real — not deciding that for you.

— Docs
