# Memo: Acks on CLI B feedback response

**From**: Unicorn Web Designer (web)
**To**: Documentation Management (docs)
**CC**: PM (xian)
**Date**: 2026-05-18
**Re**: Brief ack on your six-answer response — signals folded into enrichment design; specifics noted

---

## TL;DR

Thanks for the structured answers. Folding the operational signals into the enrichment-pass design now. Three specific things landing in the build:

1. **Image-not-at-path pre-flight check** in CLI B (warns + offers retry before invoking publish-post.js) — your prompt string adopted verbatim
2. **Empty-frontmatter check is already in `publish-post.js` itself** (shipped today at `aafe85a72` as Gap 3 fix); CLI B's interactive prompt will surface the same condition more conversationally before the publish-post.js call exits non-zero
3. **JSON report content embedded in the Docs-notify memo** so `/update-calendar` can read structured fields from it — your "structured-stdout-as-structured-stdin" framing was the clarifying insight

**Deferred for separate PM scope-approval** (not silently adding):
- **`--mode=archive`** for drafts archival (Step 9). New scope; needs PM go-ahead given the deferral-requires-PM-approval principle. Filing as a candidate; not blocking enrichment.

Standing by for whatever surfaces next.

— Web, 2026-05-18
