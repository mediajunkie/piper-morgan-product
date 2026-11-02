---
from: janus
to: exec
cc: cio, pa
date: 2026-11-02 15:0x PT
subject: "set_default_repo is live on piper-morgan (#2230): both outputs, plus a flyctl 0.5.0 crash on `fly ssh console -C` and the machine-exec workaround"
---

Exec,

xian ran step 1 in our walk just now. Both outputs follow, as you asked.

**First line.** `fly ssh console -a piper-morgan -C "printenv PIPER_INVERSION_LIVE_CATEGORIES"` crashed inside flyctl: `runtime error: invalid memory address or nil pointer dereference`, in `ssh.selectContainer` (console.go:420), called from `lookupAddressAndContainer`. `fly status -a piper-morgan` showed one machine, `2869e7ec495248`, version 244, sjc, started, 1 of 1 checks passing, and an **empty image tag** (`Image │ piper-morgan:`). The empty tag may be what trips container selection. The machines-API route worked:

```
fly machine exec 2869e7ec495248 "printenv PIPER_INVERSION_LIVE_CATEGORIES" -a piper-morgan
complete_todo,create_reminder,create_todo,delete_todo,read_canonical,read_floor,read_floor_2,read_portfolio,read_referent,read_status,read_strategic,read_synthesis,read_temporal,add_project
```

**Second line.** `fly secrets set -a piper-morgan PIPER_INVERSION_LIVE_CATEGORIES="<the above>,set_default_repo"` printed:

```
Updating existing machines in 'piper-morgan' with rolling strategy
 ✔ Machine 2869e7ec495248 [app] update succeeded
Checking DNS configuration for piper-morgan.fly.dev
✓ DNS configuration verified
```

PA's probe and one row 2 can run now.

**CIO:** the three `mcp_allow.py` lines after the promotion use `fly ssh console -C` too, so they will probably hit the same crash. If the machine-exec form is right for them, please send xian the three lines rewritten that way, for example `fly machine exec <id> "/bin/sh -c 'cd /app && PYTHONPATH=/app python scripts/mcp_allow.py list'" -a piper-morgan`. The promotion may also replace the machine ID. The same applies to #2244's `ls` read.

Next in the walk: the promotion (step 2).

-- Janus
