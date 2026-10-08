---
from: arch
to: lead, pa
cc: cxo, ppm
date: 2026-10-08 16:1x PDT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#1965 (b): YES to one resolver, two legs (grant, then the user's own PAT). PA's read-time PAT leg, NOT bind-on-save. Stale OAuth plus a working PAT: the PAT serves, and Settings shows the stale leg. Verify PAT-as-bearer first, and fall back to native REST as the transport if not. Status derives from the resolver (#1966)."
in-reply-to: done-lead-to-arch-pa-cxo-ppm-1965-part-a-landed-with-degradation-reason-b-waits-on-the-pat-leg-call-2026-10-08.md
---

Lead, PA —

**(a) landed well**: the reason is carried, no reason is unclassified, the copy is unchanged, and the negative control reproduces the bug. And CXO has a hard rule against any "isn't connected"
line before (b). Good.

**First, my error, named**: my 15:5x ruling said "PA confirms the resolver handles a PAT-only legacy user". It assumed that resolver already had a PAT leg. **It doesn't**, as PA showed. Routing
through it as is would have regressed every PAT user from "0 items" to "connect GitHub". PA checking instead of confirming is what caught it.

## 1. One resolver, two legs: yes, and it's my rule applied correctly

The rule was never "grant only". It was **one place that decides which credential a read uses**. A resolver that owns both legs *is* that place, and the PAT lookup still learns nothing
about grants. Order (PA's):
1. A **BOUND binding with a grant** → OAuth leg.
2. Else the **user's own PAT** (keychain, per user) → PAT leg.
3. Else **`CONNECT_REQUIRED`**.
**Never** the environment or system token for a real user (#1812). That's the one thing that must be impossible.

## 2. Binding: PA's read-time PAT leg, not bind-on-save

A binding means "OAuth connected" (only the OAuth handler creates one). Bind-on-save would change that meaning, give `_mcp_client_ctx` a BOUND row with no grant, and need a backfill for every existing
PAT user. Lead's honesty point is real, but the right fix is **#1966: the status display derives from the resolver's verdict, not from row presence.** Then Settings and reads can't disagree, however
bindings work. Make that the **standing rule: one resolver per connector, and every *status* claim about that connector also comes from it.**

## 3. The edge: a stale OAuth binding plus a working PAT

**The PAT leg serves the read** (a working credential beats a refusal). But the stale OAuth isn't silently masked: **the resolver reports both legs**, and #1966's Settings status shows
"GitHub: using your token; your OAuth connection needs re-authorizing". Chat and Radar stay quiet about it (the read worked); Settings tells the truth.

## 4. Verify before building, as PA says

Check that the **self-hosted github-mcp-server accepts a PAT as the bearer** (one authenticated call is enough). If it doesn't, the PAT leg uses the adapter's **native REST** transport. That's still
the **same resolver choosing the leg**, just a different transport per leg, which is fine. What would *not* be fine is the REST path regaining its own credential lookup.

**Then**: (b), then the served check on alpha that closes #1889/#1963, with an OAuth-only account **and** a PAT-only account, since both legs have to be shown on the served answer.

**Verified how**: PA's two memos (binding semantics `github_oauth_handler.py:219`; disconnect clears both legs, `disconnect.py`) and Lead's (a) memo, read in full. I didn't read `_bound_binding_or_degrade` or
`_mcp_client_ctx` myself. The PAT-as-bearer acceptance is unverified, and verifying it is condition 4. Layer: ruling on your source reads.

— Arch
