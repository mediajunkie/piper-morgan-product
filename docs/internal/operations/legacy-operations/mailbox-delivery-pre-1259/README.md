# Pre-#1259 mailbox delivery artifacts (historical)

The original mailbox delivery model — a PM-operated **web↔code shuttle** (`mailboxes/incoming/` drop-zone for downloaded memos + `DELIVERY-LOG.md` run history, driven by the now-retired `deliver-mail` skill) — was superseded by **push-to-ref** (`scripts/mail-send.sh`) on **2026-06-19 (#1259)**, after the June migration wave put the whole cohort on Claude Code (no web agents, no PM-download shuttle).

Retained here as historical reference, not operational. See **Rule 3** in `docs/internal/operations/branch-worktree-mailbox-discipline.md` (the `⚠️ SUPERSEDED-FOR-MAIL` notes) and the design doc `docs/internal/operations/mailbox-bridge-transparency-design-2026-06-16.md`.

Contents:
- `DELIVERY-LOG.md` — the pre-#1259 delivery run history (moved as-is from `mailboxes/`).
- (`mailboxes/incoming/` held only a `.gitkeep` at archival time — nothing to move; the drop-zone dir was removed from the live tree.)

*Archived 2026-06-21 (CIO, #1292).*
