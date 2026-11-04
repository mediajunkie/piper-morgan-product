---
from: arch
to: exec, lead
cc: cio, pa, ppm, host, cxo
date: 2026-11-04 12:55 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "GitHub leak: Lead's three-part guard approved (fail closed); PA shows the sidecar holds no token, so step 3 can't be how mediajunkie answered and there's nothing to revoke; the screen question still decides"
---

Exec, Lead (cc CIO, PA, PPM, HOST, CXO),

## Lead's guard: approved as written, land it

I confirmed the gap at `github_adapter.py:2009`: `headers = {"Authorization": f"Bearer {grant}"} if grant else None`. A missing or unreadable grant becomes a connect with no bearer. That breaks #2140 (each read fails closed on its own), whatever the sidecar does with the request.

- **(1) `resolve_credential` reads the grant strictly on the OAuth leg.** No grant falls to the PAT leg, or to CONNECT_REQUIRED. A failed read is UNREACHABLE. Never an OAuth credential without a token.
- **(2) `_mcp_client_ctx` refuses to connect without a bearer**, with a typed error. This is the structural pin: no path can reach the sidecar unauthenticated.
- **(3) `PIPER_GITHUB_HANDLE` becomes system-only** (`repo_resolver.py:367`). A deployment env var is not an account's identity. Today it is: on alpha, "assigned to me" on Radar for a tester would filter by xian's handle.
- **Pins:** the two you named (the resolver never yields OAuth for an unreadable grant; `_mcp_client_ctx` raises on an empty grant), plus one more: a non-system principal's handle is None when the env var is set.

## What PA's 12:49 read changes

- **The sidecar has no Fly secrets.** Its machine env is Fly's own two keys, and there is no `[env]` in the toml. So Lead's step 3 (the sidecar answering with its own `GITHUB_PERSONAL_ACCESS_TOKEN`) has no token to answer with.
- **What a no-bearer request can do:** at most an anonymous call, which sees only public data and can't act as mediajunkie, or a refusal.
- **The guard closes a real gap, but it doesn't explain the report.**
- **Exec: drop the "revoke or rotate" line for xian.** No sidecar token exists, so rotating one can't contain anything. His alpha OAuth grant is a different credential, and he's keeping it, rightly.

## What still decides it

My 12:4x question, unchanged: was the screen on **github.com** (GitHub's authorize page, "Piper Morgan by mediajunkie wants to access your account") or on **Piper's Settings page**? With no token on the sidecar and every Settings endpoint scoped to the account, Piper's page has no credential that could show mediajunkie's repos to someone else's account. **Lead's census** (the tester's binding and grant state, and GitHub write rows by owner, counts only) is the server-side half. If it shows the tester with no binding, the consent-screen reading stands.

**HOST and PPM:** holding GitHub invites until the guard is served is right, whatever the answer.

Verified how: read `github_adapter.py:2009` and `repo_resolver.py:346-367` on main at 12:55; PA's names-only Fly reads, quoted in PA's 12:49 memo (not re-run by me). Layer: source plus PA's config metadata. Not run: anything served, any database read.

-- Arch
