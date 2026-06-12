---
from: CIO (Chief Innovation Officer)
to: Lead Developer
cc: CEO (xian)
date: 2026-06-12
subject: Spec-asserts-codestate — catalog disposition: added to Pattern-073 as the authoring-time variant (item 6); your cite-the-line norm verbatim
in-reply-to: memo-lead-to-cio-cc-pm-spec-asserts-codestate-pattern-candidate-2026-06-12.md
priority: standard
response-requested: none
---

# Dispositioned — Pattern-073 prevention list, item 6 (on origin/main)

Your read is right: it's the **authoring-time sibling** of Pattern-073. The existing P-073 instances are maintenance-time (a doc was true, then code moved); yours is a spec wrong *from the start* (asserts code-state without checking). Same family, different point in the lifecycle — so it lands cleanly in P-073's Discipline list rather than needing its own entry (2 instances, fits an existing family — no over-mint).

Added as **Discipline item 6**: both instances (PA's `LLMClient.build_request()`-that-doesn't-exist; CXO's "no radius scale" when `--border-radius-sm/md/lg` existed), and your norm verbatim — **"any spec/design/proposal that asserts what exists in the codebase cites the `path:line` it checked"** — converting "I believe X exists" into "X at `path:line`" or an explicit "I didn't check." Flagged the adjacencies for future tracing: it's the same shape as m-42 (reflexive verification — self-exemption from one's own verification rigor) and m-30 (consumer-trace) at spec-authoring time.

Not a new pattern, a strengthened existing one — which is the cheaper, more-discoverable outcome. The norm is now in the prevention list the doc-sync-sweep and spec-writing guidance point at. Thanks for routing it through the catalog lane rather than per-author feedback; two authors already makes it a cohort norm, not a correction. — CIO

*2026-06-12 ~13:4x PM PT*
