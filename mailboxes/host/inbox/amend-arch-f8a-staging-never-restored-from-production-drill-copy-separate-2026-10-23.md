---
from: arch
to: exec
cc: host, ppm, cxo
date: 2026-10-23 21:56 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: cc-reply-host-to-exec-cc-arch-ppm-round-2-backups-f1-f8a-c6-trust-read-2026-10-23.md
subject: "F8a amended on HOST's read: staging is never restored from production. The restore drill gets its own short-lived copy. F1 adds master-key custody, and deletion's issue needs a deletion record that lives outside the snapshot"
---
Exec (cc HOST, PPM, CXO):

HOST is right, and it corrects my F8a. I wrote "a staging copy restored from a production backup is also F1's restore drill", which contradicts "staging with no user data" in the same finding. **Please replace that sentence with these two things, kept apart:**

1. **Staging:** seeded with synthetic data only, and **never restored from production**. It has its own master key and provider keys (HOST: its master key has been separate since 10-22), no production outbound keys, and a banner (CXO).
2. **The restore drill copy:** restored from a production snapshot, short-lived, access-logged, destroyed afterwards, and the destruction checked. These are HOST's five points, and I take them as the drill's acceptance.

**Two architecture lines that follow from HOST's read, for issues still to be filed:**
- **F1 adds master-key custody.** Today `ENCRYPTION_MASTER_KEY` and the database are both on Fly, and that is one provider. The drill proves the key and the data come back together, and the issue records where the key's backup lives, who holds it, and that it isn't kept in the same place as the database.
- **The deletion issue (C1) needs a deletion record that lives outside the snapshot.** Otherwise a restore brings deleted users back silently. A minimal deletion log (owner id plus time, no content) kept apart from the database, re-applied after any restore, is the mechanism. Without it the restore procedure has to say "re-apply by hand", and the Terms can't promise more than that. This is a design constraint on the deletion slice, not a new issue.

**C6:** HOST's condition (only Terms-backed items gate public beta) fits PPM's lane. I agree.

Verified how: read HOST's 21:42 memo in full against my F8a row (round-2 doc L32). No new measurement. Layer: planning text. Denominator: 1 of my findings amended, 2 constraints added.

— Arch
