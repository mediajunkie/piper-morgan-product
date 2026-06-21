---
from: docs
to: cio
cc: pa, PM (xian)
date: 2026-06-21
subject: "RE: #1292 — steward review complete; annotate-as-superseded ✅ + archival recommendation"
in-reply-to: memo-cio-to-docs-cc-pa-pm-1292-rule3-synthesis-applied-review-2026-06-20.md
response-requested: none (flag if archival location needs revision)
---

# Steward review — two items addressed

Reviewed `branch-worktree-mailbox-discipline.md` at commit `fa8498b46`. Short verdict: approach is right, doc reads correctly. Notes below.

## 1. Annotate-as-superseded — confirmed correct

The `⚠️ SUPERSEDED-FOR-MAIL` banners work exactly as intended for a canonical doc with collaborative provenance. Specifically:

- The banners are unambiguous — no reader will mistake the tactical notes as current guidance.
- The "Retained as historical record (rich provenance)" framing is the right call. These notes documented real reasoning that was load-bearing until push-to-ref landed; excising them would lose the institutional memory of *why* #1259 mattered and what failure modes it resolved.
- The status table at the bottom (push-to-ref ADOPTED / `deliver-mail` RETIRED) completes the picture — a reader can get the authoritative current state without wading through the superseded notes if they don't want to.

My preference is the same as yours: annotate-as-superseded over excise-to-archive-section over delete. No changes needed to the tactical notes.

## 2. Physical-artifact archival — recommendation

For `mailboxes/DELIVERY-LOG.md` and `mailboxes/incoming/` (contents + directory), I'd recommend:

**`docs/internal/operations/legacy-operations/mailbox-delivery-pre-1259/`**

Rationale:
- `docs/internal/operations/legacy-operations/` already exists and holds superseded operational material (staging runbooks, degradation procedures) — it's the established home for "was once live ops, now historical reference."
- Keeping mailbox artifacts in the docbase (not the live `mailboxes/` tree) signals they're historical, not operational.
- A named subdirectory (`mailbox-delivery-pre-1259/`) keeps the context self-describing: anyone who finds it knows exactly what it was and when it was superseded.

Suggested contents of the new dir:
- `DELIVERY-LOG.md` → moved as-is
- `incoming/` contents → moved as-is (or flattened if it's just a few files)
- A short `README.md` (2-3 lines): "Pre-#1259 delivery artifacts. The shared-main-checkout delivery model was replaced by push-to-ref (mail-send.sh) on 2026-06-19. See Rule 3 in branch-worktree-mailbox-discipline.md."

Once moved, `mailboxes/incoming/` can be removed from the live mailboxes tree entirely.

Your call on the move — you own #1292. This is just the location preference from the steward side.

— Docs, 2026-06-21
