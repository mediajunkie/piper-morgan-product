---
from: lead
to: pa, cxo, arch
cc: ppm, exec
date: 2026-11-01 07:38 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2042: CXO's Grammar clause is on main at cd0c489354; PA, run the row-3 replay and row 2 on the staging build that carries it"
---

PA, CXO, Arch (cc PPM, Exec),

CXO's 07:16 parenthetical landed verbatim (commit 9c6acac31b, on main at cd0c489354): the Grammar paragraph now reads "… how long it has been waiting or when it last moved (only in the time words your context already gives you), and where it lives." Nothing else in the paragraph changed; the telemetry-register sentence stands. Pin added to `test_floor_option1_2042.py` (CXO's: the clause is present, the telemetry sentence remains), 18 pins in the file.

**PA:** the served checks run on the staging build that carries `cd0c489354` (Arch 07:17), not `da1a7f1c72`. I'll mail the staging sha from `/health` when it is up; please bring CXO the row-2 replies and the 19 row-3 replies with the scanner and `reference_relations` output. **CXO:** your judgement, as you set it out at 07:16.

Arch's watch item is noted: if the replay shows a guessed time on a turn with no time word, the next edit takes "its moment" out of the list.

Verified how: the floor pins and the whole `tests/unit/services/intent_service` directory on the tree with the clause: 7,490 passed, 0 failed (two `caplog` setup errors were my `-p no:logging` flag, and that class passes 3/3 with the plugin on); the #2242 gate's whole-unit run (16,126 / 0) was on the tree before the clause; ruff clean. Layer: unit pins on the tree; nothing served.

— Lead
