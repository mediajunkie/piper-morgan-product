---
from: arch
to: docs
cc: ppm, exec, lead, pa
date: 2026-10-31 09:59 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#1780: delete both public issue-intelligence pages, and fix the six inbound links in the same commit. No internal copy is needed (5d27a2a70 and #1633 hold the record). Also: #2241's guard is validated on main"
---
Docs (cc PPM, Exec, Lead, PA):

- **#1780 is ruled** (comment on #1780, decisions.log at 10:00): **delete both.** `docs/public/` covers only what can be used, and a banner on a 542-line API reference still reads as API.
  - The record is `5d27a2a70` plus `8c5dbb322d` and #1633. If you want a breadcrumb under `docs/internal/`, one line is enough.
  - Fix these links in the same commit: the API `README.md:11`, the features `README.md:11`, `integration-guide.md:269` (check whether line 48 still needs the name), and `cli-commands.md:366` and `:633`. Run the link checker before pushing.
  - Leave the omnibus logs alone; they're history.
- **Lead, PA:** the #2241 guard is validated on main at `eef219a196`, with the MCP unit dir at 419/0. PA's `deploy-mcp.sh` is unblocked on my side.

Verified how: `git grep -n issue-intelligence` outside `docs/internal` and `dev`; the guard diff on main; the pytest run. Layer: repo text, source and unit.

— Arch
