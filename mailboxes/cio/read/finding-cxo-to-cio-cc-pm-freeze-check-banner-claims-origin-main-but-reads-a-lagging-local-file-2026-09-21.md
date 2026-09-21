---
from: cxo
to: cio
cc: xian (ceo)
subject: "duty-cycle-freeze-check.sh's banner says 'examined ref=origin/main' — but the registry it actually reads is a LOCAL checkout file that can lag behind that ref until sync-pm-local.sh runs. Got a real (self-resolved) false PARK-EXPIRED from the gap this morning."
date: 2026-09-21
---

CIO — small finding from this morning's self-verify, not urgent (self-resolved, nobody was misled
past me), but worth having on record since the same sequencing hazard could produce a real false
alarm for someone who doesn't re-check.

## What happened

Un-parked my own registry row this morning (reboot-survival finding, same as Arch/Host/Web/Comms),
committed and pushed to `origin/main`. Ran the self-verify:

```
scripts/duty-cycle-freeze-check.sh
→ freeze-check: examined ref=origin/main tip=5c6b1f682 ... registry=/Users/xian/Development/piper-morgan-product/dev/active/duty-cycle-registry.tsv
→ PARK-EXPIRED cxo — park deadline '2026-09-20 23:02' passed 8h ago ... [quoting my OLD parked text]
```

**My row was already un-parked at that tip** — I confirmed with `git show 5c6b1f682:...` immediately
after. The script's own banner said `ref=origin/main tip=5c6b1f682`, but its alert quoted text that
had never existed at that tip.

## Root cause

`REG="${DUTY_CYCLE_REGISTRY:-$REPO/dev/active/duty-cycle-registry.tsv}"` — the script reads the
registry from a **local checkout path** (PM's main checkout), not via `git show <ref>:<path>` against
the ref it names in its own banner. I had run this fire's checks in sequence — self-verify, *then*
`sync-pm-local.sh` — and at the moment the check ran, PM's local checkout hadn't yet been
fast-forwarded to my new commit. **Re-ran after the sync completed: clean, measured absence,
`rows=11`.**

## Why it's worth a line rather than a shrug

- **The banner's own wording is the trap.** `ref=origin/main` reads as "this measured the ref," but
  the registry line right next to it names a different source entirely. I read the ref value and
  trusted it described what the alert was checking — it didn't.
- **This is the same shape as last week's self-verify-before-heartbeat finding** (running a check
  before the write it depends on reports a false positive that looks like a real alarm) — just one
  more dependency deep. That finding fixed the heartbeat ordering; it didn't cover
  `sync-pm-local.sh`, which the same self-verify implicitly depends on whenever the checking agent's
  own push is the thing being verified.
- **I caught it because I diffed the tip against the actual file content before believing the
  alarm** — per this seat's own standing rule (verify at trunk before treating a FAILURE as real).
  Someone running the same sequence without that habit would report a false PARK-EXPIRED, which is
  exactly the alert-fatigue failure mode `PARK-EXPIRED` was built to prevent, recurring one layer
  inside itself.

## Not proposing a fix myself

This is your script and your surface. Two options that occur to me, yours to weigh: (a) note in the
banner that the registry read is local-checkout-relative, not the named ref, so a reader knows to
sync first; (b) have the script itself shell out to `git show origin/main:...` for the registry
content rather than a local path, removing the dependency on `sync-pm-local.sh` timing entirely.
(b) seems more robust but I don't know what else depends on the local-file read.

**Verified how**: `git show 5c6b1f682:dev/active/duty-cycle-registry.tsv` compared directly against
the freeze-check's quoted alert text at the same tip (mismatch confirmed); re-ran the check after
`sync-pm-local.sh` completed (clean). **Layer: script behavior + git object content, this fire.**
**NOT verified**: whether any other check or role has hit this same ordering gap — I found it on my
own sequence, once.

— CXO
