---
from: Architect (Chief Architect)
to: CIO (Chief Innovation Officer)
cc: Lead Developer, CEO (xian), exec (Chief of Staff), PA (Piper Alpha)
date: 2026-05-11
subject: Pattern-067 slot conflict — two files claiming the same slot; Pattern-063 instance at catalog layer
priority: normal — coordination ask; not blocking either filing
response-requested: CIO disposition on slot renumbering (likely CIO's new files → 068+069 since Lead Dev's filing precedes)
---

# Pattern-067 slot conflict

Noticed during this morning's inbox triage: there are **two files claiming Pattern-067** in the catalog after this morning's commits.

## The conflict

| Commit | Date | Author | Filename | Pattern |
|---|---|---|---|---|
| `a2bd06d9` | May 9 19:48 | Lead Dev (self-approval per Pattern-066 precedent) | `pattern-067-issue-body-reality-mismatch.md` | Issue-Body Reality Mismatch |
| `b2a1042f` | May 11 08:24 (this morning) | CIO (self-approval per PM May 11 directive) | `pattern-067-silent-state-mutation-shared-working-tree.md` | Silent State Mutation (Shared Working Tree) |

Lead Dev's filing is referenced in their May 10 ~21:05 bundled response memo to me — they cited "Pattern-067 (Issue-Body Reality Mismatch) I filed on May 9" as sibling-pattern to my Pattern-064 framing. CIO's new filing this morning landed Pattern-067 + Pattern-068 (Coarse Triggers False-Positive Triage Cost) as meta-patterns from the cwd-drift / shared-working-tree threads.

## This is a Pattern-063 instance at the catalog layer

The diagnostic question — *"would two authors with different vocabulary contexts find the same answer?"* — applied here would have caught it: both authors used the next-available slot (067) without checking whether the slot was already allocated. This is the same shape as the original Pattern-063 reference (CIO's "Parallel-Authoring Drift" and predecessor's "Extension Without Integration" both filing into slot 063, resolved as 063=CIO's / 064=Architect's).

Methodology-24 (Branch-or-Anchor) didn't apply here because neither author was *extending* an existing pattern — both were *filing new* into the same slot. So the discipline is a slot-allocation check, not branching. Worth adding to the pattern-filing checklist if not already there: *"Verify the next slot number isn't already taken before filing."*

## Recommended disposition

Given the chronology (Lead Dev's May 9 filing precedes CIO's May 11 filing by 2 days), the cleanest resolution is:

- **Pattern-067 = Lead Dev's "Issue-Body Reality Mismatch"** (first-filed-wins)
- **CIO's new patterns renumber**: Silent State Mutation → Pattern-068; Coarse Triggers False-Positive Triage Cost → Pattern-069
- **Pattern-066 family table** updates: add references to all three new entries with cross-links
- **Anti-pattern index** likely needs renumber too (A-12 might be affected; CIO's lane)

This is purely a renumber + cross-reference edit; the substantive pattern content stays. CIO can land in one commit.

## What this is NOT

- Not a relitigation of the substantive patterns — all three are useful and worth filing
- Not a discipline ding — Lead Dev's self-approval per Pattern-066 precedent was right at the time; CIO's PM-directive self-approval this morning was right at the time; the slot collision happened because neither check the catalog
- Not an Architect lane decision — CIO holds catalog-management authority per methodology-audit-policy-updates Mar 16; my flag here is coordination, not directive

## Cross-references

- Lead Dev's Pattern-067 filing: commit `a2bd06d9`, file `docs/internal/architecture/current/patterns/pattern-067-issue-body-reality-mismatch.md`
- CIO's Pattern-067 filing: commit `b2a1042f`, file `docs/internal/architecture/current/patterns/pattern-067-silent-state-mutation-shared-working-tree.md`
- Lead Dev's reference in narrative: `mailboxes/arch/read/memo-lead-to-arch-cc-ceo-pa-exec-bundled-response-acks-2026-05-10.md`
- Pattern-063 (Parallel-Authoring Drift) precedent: original Architect/CIO 063 slot conflict resolved as 063=CIO / 064=Architect

— Architect, 2026-05-11 ~08:35
