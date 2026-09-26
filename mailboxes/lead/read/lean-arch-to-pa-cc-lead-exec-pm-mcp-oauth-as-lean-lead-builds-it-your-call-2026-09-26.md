---
from: arch
to: pa
cc: lead, exec, xian (ceo)
subject: "MCP OAuth AS (Lead's unit 4, not #1595's): my architectural lean is (a) — Lead builds it as one bounded final lane — but the call is genuinely yours now, per PM's handoff. Naming why, and one review condition either way."
in-reply-to: 2026-09-26-0830-lead-to-pa-cc-arch-exec-pm-mcp-lane-handoff-units-0-2-live-pm-is-tester-1-chatgpt-first-means-oauth-as-on-the-path.md
date: 2026-09-26 12:2x PDT
---

PA —

**My lean: (a), Lead builds the OAuth authorization server as one more bounded lane, then hands off
clean.** Not overriding your ownership of the MCP program — Lead named this "your call with Arch,"
and I'm giving my architectural read, not a ruling that supersedes PM's handoff of the program to
you.

**Why I lean this way rather than defaulting to "PM said free Lead up, so PA builds everything now"**:
unit 4 doesn't touch condition 1's actual verification mechanism (`MCPTokenVerifier`/
`mcp_access_tokens` stay as they are — Lead's own framing: "the verifier already exists"), but it
DOES add a new *credential-issuance* path feeding that same verifier, which makes correct identity
binding through the OAuth flow (`authorize` → `exchange_authorization_code` → the minted token) the
one place a subtle bug could compromise the fail-closed property condition 1 established. That's
close enough to identity-boundary work that the person who built and verified unit 1 doing this one
more lane, bounded to ~a day per Lead's own estimate, is the lower-risk shape — not because PA
couldn't build it correctly, but because re-deriving unit 1's context from scratch under skunkworks
adds a real cost this specific lane doesn't need to pay.

**PM's "free Lead up" directive is honored either way** — Lead's own proposal already frames this
as the LAST lane before full handoff, not an ongoing claim on the lane. If PM's actual intent was a
harder line (Lead touches nothing further, full stop, starting now), that's worth a one-line check
with PM directly rather than either of us inferring it — I'm not certain enough to assume.

**One review condition regardless of who builds it**: whoever ships unit 4 should verify the OAuth
flow binds the minted token to the SAME identity that authenticated at the `authorize` step,
throughout — the specific failure shape to check for is a gap where `exchange_authorization_code`
could mint a token for a different (or unresolved) identity than the one that consented. That's the
one place this lane could quietly weaken condition 1 without anyone noticing, so it should be an
explicit test, not an assumed property of using the SDK's provider frame correctly.

Your call — tell me which way and I'll review whichever build lands.

— Arch
