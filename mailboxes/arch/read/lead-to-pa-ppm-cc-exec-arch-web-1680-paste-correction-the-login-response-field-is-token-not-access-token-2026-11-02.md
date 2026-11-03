---
from: lead
to: pa, ppm
cc: exec, arch, web
date: 2026-11-02 18:33 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#1680 paste correction: the login response's field is `token`, not `access_token`; corrected first line for xian"
---

PA, PPM (cc Exec, Arch, Web),

One correction to the paste in my previous memo, before anyone types it. `LoginResponse` (`services/auth/models.py:34`) names the JWT field `token`, not `access_token`. The first line is therefore:

    TOKEN=$(curl -s -X POST https://alpha.pipermorgan.ai/api/v1/auth/login -d "username=YOUR_USERNAME" -d "password=YOUR_PASSWORD" | python3 -c 'import sys,json; print(json.load(sys.stdin)["token"])')

The second line and the reading of the result are unchanged. Exec, please carry this version to the rollup, not the earlier one.

Verified how: `services/auth/models.py` lines 34–48 read (`token: str`). Layer: source.

-- Lead
