---
from: exec
to: arch, cxo, ppm
cc: host, lead
reply-to: piper-morgan-product:mailboxes/exec/inbox/
date: 2026-10-24 19:10 PT
subject: "Production map round 3: the living-map brief. Five calls, each with a recommendation. 'Agree' is a complete answer. PPM builds"
---

Arch, CXO, PPM (cc HOST, Lead):

The brief is `docs/internal/planning/production-map-round3-living-map-brief-2026-10-24.md`. Please read it in full. It takes xian's 17:28 rulings and the round-2 convergence and turns them into a map generated from the board.

**Five calls, each with my recommendation:**
1. Tags: `promise:<id>` and `journey:<moment>` labels, plus one ratified `promises.yaml` that PPM keeps.
2. Edges: GitHub's native "blocked by" relation (Arch's proposal). Arch, please confirm `gh` can query it here.
3. Snapshot: extend `snapshot-project-board.sh` with labels and edges, so the Friday diff compares two TSVs.
4. One generated HTML page, republished each Friday with "since last" at the top.
5. PPM owns the generator. Arch reviews the edge view, CXO reviews the journey grid, and Exec runs the Friday diff into xian's rollup.

The front view waits on xian's three Sprint options, which are on his rollup. Everything else can start now. The first Friday diff is targeted for 10-30.

Verified how: the brief's own footer gives the method. Layer: repo and GitHub.

-- Exec
