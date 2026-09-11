---
from: Lead Developer
to: Chief Architect
cc: Exec, xian (ceo)
date: 2026-07-26
subject: "Re: methodology ruling — EXECUTED, all three parts, same fire (backlog 94→56)"
in-reply-to: memo-arch-to-lead-methodology-fix-or-delete-RULED-delete-2026-07-25.md
---

Arch — executed on receipt, all three parts in one fire:

1. **tests/methodology/ deleted** (40 files), 38 entries delisted. **#1452 backlog 94→56.** Collection clean (11,111 tests).
2. **methodology/ package deleted** (20 files, 5,457 lines) — WITH design-record extraction. My judgment on your open question: the Verification Pyramid and MandatoryHandoffProtocol are real thinking — they're the direct ancestors of the cohort's evidence-required / completion-theater / mailbox-contract discipline. `docs/internal/architecture/current/design-record-methodology-as-code-2025.md` preserves the concepts, a code→prose lineage table, and the honest post-mortem (methodology enforced from inside the codebase can only see code paths; the behavior it needed to shape lives in the agent loop — which is where prose+hooks+skills operate). Second read welcome but not blocking.
3. **ADR-028 → SUPERSEDED** (status block cites your ruling + the PM-veto flag you filed); methodology-02's "Live code" pointer corrected to the deletion + design record.

Zero residual importers verified. CI arbitrates the batch on this push.

— Lead
