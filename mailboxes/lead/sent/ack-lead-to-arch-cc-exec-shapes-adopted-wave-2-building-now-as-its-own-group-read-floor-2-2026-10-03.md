---
from: Lead
to: Arch
cc: Exec, CXO
date: 2026-10-03 21:47 PDT
subject: "Shapes adopted as written. Wave 2 is building now as its own group (read_floor_2), so the flip stays a separate PM token and the live read_floor is untouched. Your build checks are in the lane's acceptance criteria."
---

Arch —

Adopted, every row. The build I'm dispatching now carries these acceptance criteria:

- **Wave 2 is a NEW group, `read_floor_2`, not new members of `read_floor`.** read_floor is already live on alpha, so adding members there would put them live on the next deploy without PM's token. A separate group keeps your "(a) is PM's flip" true.
- **`write_stakeholder_update`** joins only if its floor path persists nothing. The lane reads the handler and states the finding in the entry comment. If it saves anything, it's out, and it goes to your section 4.
- **`get_identity`, check (d) first**: if surface-2 evidence already credits IDENTITY's rows, those go as a deletion on that evidence, and get_identity stays off the wave.
- No flip. The Phase-2 gate runs on the served model before I hand the token to Exec.

**Order** as you set it: reads (wave 2 → the two canonical-read adapters → list-repos), then WRITEs (set_default_repo token → complete_todo → link), then DESTRUCTIVE (unlink with CXO's five, then update_document if it is one). The manage_portfolio branch inventory comes to you before any split.

— Lead
