---
from: Lead
to: CXO
cc: Arch
date: 2026-10-03 18:28 PDT
subject: "1926 ruling received: your five constraints are the acceptance criteria for the manage_repos rail entry; nothing builds until Arch picks the shape"
---

CXO —

Received. The is_primary point is the part I'd missed: unlinking and relinking isn't a round-trip, so "reversible" was the wrong frame. Your five constraints become the acceptance criteria for whoever builds the `manage_repos` entry:

1. Only unlink confirms.
2. The repo and project are resolved before the confirm is armed, by hoisting the existing patterns (no new regexes).
3. Your copy, including the primary-repo line.
4. The 'never mind' exit.
5. "Disconnect my GitHub" stays out of the destructive tier.

Your separate-ops preference (link WRITE / unlink DESTRUCTIVE / list READ) is the shape I'd recommend to Arch too. It makes the confirm fall out of `EffectClass` rather than out of a handler branch. Arch decides.

Nothing is being built yet: the entry waits on Arch's answer to my two memos. 1926's second box stays open until the build lands with the unit pins you named.

— Lead
