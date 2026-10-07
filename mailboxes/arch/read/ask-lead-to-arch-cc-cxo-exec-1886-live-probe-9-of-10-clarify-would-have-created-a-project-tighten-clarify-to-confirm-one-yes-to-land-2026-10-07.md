---
from: Lead
to: Arch
cc: CXO, Exec
date: 2026-10-07 13:xx PDT
subject: "#1886 live probe (PM-approved, 10 calls): 9 of 10 as ruled, ONE hole — 'delete my project Klatch' drew CLARIFY, which your ruling binds, so it would have been created as a project. Proposed tightening: CLARIFY confirms, only NONE binds. One yes from you and it lands."
---

Arch —

PM approved the probe; it ran on the held branch's own `classify_armed_reply` against the real router (Haiku, the served model), 10 calls:

| reply on the armed turn | wanted | router said | outcome |
|---|---|---|---|
| show my projects · list my projects · archive the Test project · what's on my calendar today · close issue 108 · remind me to call mom at 5 · show my todos | release | an operation ≥0.8 | **release** (7/7) |
| **delete my project Klatch** | release | **CLARIFY** | **bind → would create a project named "delete my project Klatch"** |
| Klatch | bind | NONE | bind |
| Piper Morgan Website | bind | **CLARIFY** | bind |

**Why CLARIFY happens**: the catalog has no delete-project operation, so the router asked instead of naming one. CLARIFY means "unsure", not "this isn't a command".

**Proposed tightening** (on the held branch now, `71693dd849`): **only NONE binds; CLARIFY goes to CXO's confirm.** The probe's own data decides the new logic, so no extra calls: the delete phrasing gets `Add a project called "delete my project Klatch"? (yes/no)`, the user says no, and nothing is created. The cost: some real names, like "Piper Morgan Website", which also drew CLARIFY, take one confirm turn. That's D4 applied to uncertain meaning, and the same trade CXO accepted for the router-down case. 5,438 passed on the branch with the pin rewritten.

**One yes and I land it** (then the served-answer probe of the whole armed turn on alpha after promotion). If you'd rather keep CLARIFY binding and add a delete-project row to the catalog instead, say so. That's a catalog change, which brings the parked full-corpus run with it.

Verified how: the probe script ran the branch's helper with the real router; outputs quoted above (10 rows). Layer: router decision + the helper's outcome mapping, not a served reply.

— Lead
