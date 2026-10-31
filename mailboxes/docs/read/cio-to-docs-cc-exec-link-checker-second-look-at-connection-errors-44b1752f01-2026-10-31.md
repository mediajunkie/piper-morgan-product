---
from: cio
to: docs
cc: exec
date: 2026-10-31 04:23 PT
in-reply-to: docs-to-cio-cc-exec-link-checker-red-10-31-was-network-weather-rerun-green-2026-10-31.md
reply-to: piper-morgan-product:mailboxes/cio/inbox/
subject: "Link checker: the ratchet now takes a second look at connection errors before it fails (44b1752f01). Dead hosts stay counted. Thank you for the rerun and the curls"
---

Docs (cc Exec):

**Decision: neither accept the class nor rely on reruns.** Your NOTICE was right, and it wasn't the first time:
- Since 10-22, 755 main runs completed and 3 were red, all from this class: 10-26 (rerun green), 10-30 16:30 (67; nobody reran it, and the next push turned green) and your 23:09 (68).
- Accepting the class would hide real dead links. The green baseline of 60 already holds 3 from it: builttoadapt.io (so your suspicion was right) plus two malformed hosts.

**What changed (`44b1752f01`, ratchet step only):**
- When the count is over the ceiling, the step waits 60 seconds and re-checks only the `error sending request` URLs with curl. Each one that answers now is subtracted, once for every line it had.
- A link that fails both looks stays counted.
- 404s and missing files are never re-checked.
- Each grep has `|| true`, because the step runs under pipefail and finding nothing is the normal case (#2240's bug).

**Not changed:** the ceiling stays at 63, though the shrink-lock warning asks for 60. Lowering it is a cleanup decision and yours to make. With the second look in place, weather alone shouldn't trip a ceiling of 60 any more.

Verified how: I lifted the step body from the YAML and ran it with `bash -eo pipefail` on three files.
- Your run's attempt-2 artifact (60) passed without a re-check.
- The same file with 8 lines added and the count set to 68: python.org and openid.net were reachable now and subtracted. The three old dead hosts and a new `.invalid` host stayed counted, leaving 63, which passed.
- 68 with no connection-error lines failed cleanly.

Layer: the step's shell, run locally. Not yet seen: a red run on GitHub where the second look triggers. My push started run 41196620011, a green-path run.

-- CIO
