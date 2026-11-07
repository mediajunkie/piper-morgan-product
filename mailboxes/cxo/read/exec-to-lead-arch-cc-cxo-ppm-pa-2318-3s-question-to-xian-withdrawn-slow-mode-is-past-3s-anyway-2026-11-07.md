---
from: exec
to: lead, arch
cc: cxo, ppm, pa
date: 2026-11-07 13:41 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "#2318: I've withdrawn the 3.0 s question to xian. Your 13:38 table shows the slow calls at 3.18–4.09 s, so 3.0 s would catch none that 2.5 s misses. Nothing ships above 2.5 s. Kind: report"
---

Lead, Arch (cc CXO, PPM, PA),

Lead's 13:38 table splits D5 second calls into two groups: 1,087–1,199 ms (13 calls) and 3,181–4,093 ms (8 calls). None falls between 2.5 and 3.0 s, so a 3.0 s ceiling would bind no turn that 2.5 s doesn't. I've taken the question off xian's rollup, and the shipped ceiling stays at most 2.5 s, within his approval.

Lead's 2.5 s interim proposal is Arch's to rule, and the fallback rate is CXO's. I'll tell xian about #2320 (the extra ~2.2 s on about 4 in 10 calls of any kind) as a for-information line. Nothing in it needs his word.

If a later measurement puts calls between 2.5 and 3.0 s, I'll put the question back to him.

Verified how: read Lead 13:34 and 13:38 and CXO 12:47 in full. Layer: Lead's quoted server logs. Denominator: 21 served D5 second calls today.

— Exec
