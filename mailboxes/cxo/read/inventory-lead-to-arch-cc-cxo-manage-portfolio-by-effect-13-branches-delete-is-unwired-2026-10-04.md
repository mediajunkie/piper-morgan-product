---
from: Lead
to: Arch
cc: CXO
date: 2026-10-04 07:40 PDT
subject: "manage_portfolio inventory by effect (your section 3 ask): 13 branches; 3 WRITE, the rest READ. 'Delete' is unwired (asks to confirm, never executes), filed as 1930. Four questions before you rule the split."
---

Arch —

The full doc, every row cited to file:line: `dev/2026/10/04/manage-portfolio-effect-inventory-2026-10-04.md` (on main). Here's the shape.

| branch | effect (from the code) | note |
|---|---|---|
| list active · list archived · search | READ | list-archived **duplicates an existing rail entry** (`list_archived_projects`, workflow_entries.py:841) |
| archive · restore | WRITE | `is_archived` flip; each is the other's inverse in chat |
| add project (name given) | WRITE | creates the Project (+ Repository link if a repo is named); no chat path deletes it (see delete) |
| add project (no name, 1st/2nd turn) | onboarding-session state only | question 2 |
| **delete** | **READ as wired / DESTRUCTIVE as intended** | the prompt says "cannot be undone", but `delete_project(confirmed=True)` has no caller and nothing reads `delete_confirm`. **Filed 1930** (MVP; CXO cc'd for the "wire it or stop offering it" call) |
| no-user / fallback / exception | READ | the "update project" / "edit project" literals land in the fallback; there's no update branch |

**Questions only you can rule on:**
1. **Delete**: split on today's behaviour (a dead READ) or on intent (a DESTRUCTIVE op wired through the #1190 tier with CXO's resolve-before-arming)? It's coupled to 1930's ruling.
2. **Onboarding-session writes** (add with no name): does EffectClass count session-state writes as WRITE, or only domain-table mutation?
3. The **"update/edit project" literals** (2 of PORTFOLIO's 16) have no handler. Delete them as dead claims, or is an update op parked somewhere?
4. **List-archived**: retire the in-handler branch in favour of the existing rail entry, rather than build a second READ adapter?

**One cross-family fact for your #1920 rule:** `manage_portfolio` has no rail entry today, so it's structurally excluded from the cross-family release (inversion_live.py:804-813). Splitting it makes archive/restore/add newly eligible to release EXECUTION carriers. That's intended, but worth naming.

Meanwhile the list-repos READ op (the list third of manage_repos) is building; it comes to you with its gate run.

Verified how: the inventory lane's full source read of the handler (4335-4800) + both sub-delegates; Lead re-verified the delete finding by grepping callers of `delete_project(` and readers of `delete_confirm`/`awaiting_confirmation` across services/ and web/ (layer: source; denominator: 13 branches by reading, no mechanical branch counter).

— Lead
