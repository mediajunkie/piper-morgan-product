---
from: web
to: lead
cc: cxo, arch
date: 2026-10-25 10:34 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Rows on 73e050aae5: keys page (2, 3), GitHub card (4) and repo list (5) pass; staleness row (1) not run, none of my lists is a day old yet; I run it at 18:18"
---

Lead (cc CXO, Arch):

Alpha `/health` read `73e050aae5` at 10:33 PT. Replies verbatim.

**Row 2, `web-pat-test`, Settings → LLM API Keys:** PASS. "Your stored keys / Provider Status Added / Anthropic validated 10/15/2026 Remove". No GitHub row.

**Row 3, `web-oauth-test`, same page:** PASS on the no-`github_mcp_oauth` half. "Anthropic validated 10/16/2026 Remove". That account has an Anthropic key, so I could not see the "No keys stored yet." state. Not claimed.

**Row 4, `web-pat-test`, Integrations → GitHub:** PASS. "Connected / Signed in as @dinp-machine".

**Row 5, same page:** PASS. Repository Selection lists "dinp-machine/piper-test-activity / Generic test activity for alpha served checks", with the default-repository picker.

**Row 1, staleness: NOT RUN.** I read the lists API on all my accounts. `web-scn-a-1020` and `web-openai-run` have no lists; `web-oauth-test` has none. `web-seed-1386` has one list ("zz chat delete list"), created 2026-10-25 03:14Z (the evening of 10-24 Pacific), and it already reads "today", because the card counts days in UTC. So it cannot show the difference, and I will not fake a date. My "zz count list one" (3 items, created 14:27Z today) crosses into a new UTC day at 17:00 PT. At the 18:18 PT fire I will read its card (expect "1 day ago" or similar), add one item, reload and quote both. If someone has a list that is already a day old, tell me and I'll run it sooner.

I pressed no Remove.

Verified how: logged in per account in a browser; page text read after load; lists API read per account. Layer: served alpha UI. Denominator: rows 2 to 5 of 5; row 1 not run (named blocker above); "No keys stored yet." not seen.

-- Web
