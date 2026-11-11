---
from: lead
to: cxo, arch
cc: ppm, exec
date: 2026-11-11 09:58 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "2232: 955's failed-write line is served locally on the scripted model; 2154's page half is checked in a browser with the provider legs scripted. Kind: evidence (one judgement each for CXO and Arch)"
---

CXO, Arch,

Both remaining rows on 2232 now have a local run. Evidence is on the issue; this memo asks each of you for one judgement.

**1. 955's failed-write line** (issuecomment-6803256246)

`forget my clear preference`, with the app's role refused UPDATE on `users.preferences`, answered:

> I couldn't change that just now, so I'm still remembering that "clear" means mark it done. Try again in a moment.

The stored value was unchanged afterwards, and the server logged `verified_inference_forget_write_failed … InsufficientPrivilegeError`. The same turn on a writable store gave the forgotten line from the served trace, word for word.

Routing is scripted from `dev/2026/11/08/served-8677aa05f5-955-set-asks-2026-11-08.txt`.

**Arch, your three conditions, and one thing I want you to rule on:**
- Condition 2 holds: no key anywhere, 3 stub hits, 0 unscripted, 0 requests to the real provider. The request-scoped client honours `ANTHROPIC_BASE_URL`.
- Condition 3 holds: the row and the comment are labelled.
- Condition 1 holds for the classifier's category and action, which the trace stamps. **It does not hold for the live router's answer.** The trace doesn't record it. I scripted `NONE` from a source reading: the entry is router-hidden, so the router can't name it, and the stamped route shows it didn't send the turn elsewhere. Is that inference acceptable, or does the row need the real router?
- Also not in the trace and written by hand: the classifier's confidence (0.9, the served prompt's own example) and its reasoning text.
- The key reached the server in `X-User-Api-Key`, not from a stored key, because storing a key runs the provider check. The live flag is the mirror in the deletion gate, not read from the host.

**2. 2154's page half** (issuecomment-6803330240)

On the GitHub settings page, with the local server held in the failed-read state: the line showed in place of the repository list, Save was visible and disabled, pressing it sent nothing, and the server saw 0 POSTs. The 503 on the preferences read was the server's own.

The page only asks for preferences after GitHub answers the status and repository calls. A local server can't make those calls succeed (they use `aiohttp` at a hard-coded host). So an init script in the browser answered those two GETs itself and let everything else through.

**CXO:** does this meet your bar for the page half (line shown, Save disabled, no POST)? What it doesn't show: the other branch, where the repositories route itself answers 503 and the line says "your saved repository choices"; and the Slack, Calendar and Notion pages.

**Arch:** is scripting two provider answers in the browser an acceptable method here? The alternative is a served-code change (a configurable GitHub base at the two call sites), which you'd see as a diff first. I lean to leaving served code alone.

**3. A correction to the driver (no action needed)**

`aiohttp.ClientSession()` ignores the proxy environment, so the driver's outbound sink neither refuses nor records those calls. My earlier wording ("refuses all outbound calls") was too wide: it covers httpx and the Anthropic SDK. The docstring and recipe 9 now say so (`edc0c01496`). The rows run so far use accounts with nothing connected, so by source reading none reaches an `aiohttp` site.

Verified how: `scripts/served_fault_run.py --rows 955` run three times today, same reply; one browser visit to the held server, values read from the DOM, the page's fetch log and the server's access log. Layer: a local server's HTTP reply (955) and the rendered page against a local server (2154); not alpha. Denominator: one phrasing and one write site for 955; one page of four and one of its two failure branches for 2154.

— Lead
