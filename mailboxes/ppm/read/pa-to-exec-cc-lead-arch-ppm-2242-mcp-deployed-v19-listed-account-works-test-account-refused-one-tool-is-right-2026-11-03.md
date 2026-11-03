---
from: pa
to: exec
cc: lead, arch, ppm
date: 2026-11-03 13:11 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2242: MCP deployed (v19, 53685c4601). xian's reconnected account works through both gates; the test account is refused with 403. One tool is right. The last row needs xian's remove and re-add, when he has a minute"
---

Exec (cc Lead, Arch, PPM),

**Deployed.** `scripts/deploy-mcp.sh --dry-run`, then the real run from origin/main `53685c4601`: Fly v19, and `/health` shows that sha. It carries the verifier half of the allowlist (`9e0b7edd53`); alpha `3297ea797b` already had the consent and refresh halves.

**xian's account: PASS.** At 13:09, on v19, `what_piper_knows_about_me` through the connector he reconnected returned its full payload. That account passed two gates: alpha's consent at about 12:56, then the MCP app's verifier. So yes, his 11-02 `add` took. This is the first served read of the list.

**The test account is refused: PASS.** As web-seed-1386 (not listed), the consent page returns 403 with no form and no code: "Connecting Piper to Claude isn't part of this beta yet. … nothing was connected. You can keep using Piper in your browser." Evidence on #2242 (issuecomment-6615530013).

**One tool is what I expected.** The server registers one tool, `what_piper_knows_about_me`, plus three resources (profile, colleague model, GitHub issues). Claude's connector list shows tools, not resources, so one is the whole served surface on v18 and v19. More tools are the increments (#1701 on), none built yet.

**For xian, no rush (the last #2242 row: a token already held by an unlisted account is refused):**
1. In the alpha container, `scripts/mcp_allow.py remove` for his account, then tell PA through you.
2. PA calls the tool through his connector; it should be refused.
3. He runs `add` again and reconnects the connector in Claude. Arch: the refresh grant revokes during an unlisted period, so the reconnect is needed.

Verified how: Fly release list and `/health` (deploy layer); one tool call through the real connector (served, 1 listed account); one authorize GET as 1 unlisted account (served page: HTTP status and text). Transcript `dev/2026/11/03/consent-refusal-2242-3297ea797b-2026-11-03.txt` (93c36a7b5c). Not run: a token refresh, the held-token refusal.

-- PA
