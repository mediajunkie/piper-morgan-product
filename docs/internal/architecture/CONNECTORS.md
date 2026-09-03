---
last_updated: 2026-09-03
currency_claim: updated same-commit with any connector transport/grant/scope change
max_age_days: 30
---

# CONNECTORS.md — per-connector truth

**Living core doc #5** (see `reviews/2026-08-architectural-review/living-core-docs.md`). Arch
authored v1; **Lead maintains**. This document states what each connector actually IS — transport
reality, grant model, scope status — so nobody reasons from an adapter's name or an old diagram.
Evidence base: Leg B census (2026-08-29, with same-day corrections) + the decisions cited per row.

## The standing test (ratified 2026-08-29, from the review's C4 evidence)

**Piper's backend holds a grant only where it must act without the user present** (headless work:
scheduled generation, background reflection, document mirroring, writes under user identity).
In-conversation reads of third-party services on the BYOC path belong to the **host's own
connectors**. Every held grant traces to a Bet or a named headless workflow; a grant that loses
its headless case converts to host-mediated and is dropped.

## The table

| Connector | Transport truth | Grant model | Scope | Governing decisions |
|---|---|---|---|---|
| **GitHub** | **Real MCP** — 7 `call_tool()` sites via MCP SDK over streamable-HTTP to a deployed `ghcr.io/github/github-mcp-server:v1.5.0` sidecar | Backend-held, **justified** (standup, background reflection, issue writes under user identity) | Live; 1.0 set | ADR-070 + Amendment A (server-ref resolver); PM 08-29: **stays self-hosted** — GitHub's hosted endpoint requires per-user Copilot licensing (disqualifying); the swap remains config-level if economics change (OAuth-scope test off critical path until then) |
| **Calendar (Google)** | Google API SDK direct — an **honest shim**: the MCP stub's `_server_params_for` raises `NotImplementedError` (#1220 open, deliberately) | Backend-held, **justified** (headless standup enrichment) | Live; 1.0 set | #1220 (eventual MCP transport choice — open, not urgent); 08-30 disposal ruling: adapter stops eagerly constructing the unused MCP sim stack (surgery in flight with Lead) |
| **Notion** | `notion_client` REST — a shim **misleadingly named** `NotionMCPAdapter` (naming debt; rename when touched) | Backend-held, **governed by Bet 003** (the mirror bet: docs move in/out of Piper's workspace headlessly — buyer pre-filled, kill condition = one instrumented round-trip by PM's date) | Live; 1.0 set | Bet 003 (`bets/bet-003-notion-held-grant.md`); PM 08-29: Notion = external document mirror + workplace surface |
| **Slack** | Adapter is a keychain-status shim with **zero importers (dead)**; socket-mode inbound exists but is config-gated off | None held in practice; if chat-side Slack reads ever return, the C4 default is **host-mediated** | **Descoped to Fast Follow** (PM 08-27, three independent reasons) | #1481/#1484 (fail-closed hold); PA's 08-27 connector-reality finding; the descope memo trail |
| cicd / devenvironment / gitbook / linear | Dead (zero importers, spatial twins also dead) | n/a | In disposal pipeline | 08-29 routing memo; Lead's batch execution record |

## Rules for the tool layer (MCP surface — apply before authoring any tool output)

1. **Hedges ride the payload, not a prompt — and the payload FORM is class-dependent** *(revised
   2026-09-01; killer test RUN 2026-09-03: **Claude confirmed the class taxonomy exactly** —
   staleness survived, completeness vanished, same reply — while **GPT-4o produced a third
   outcome**: with two co-occurring caveats it kept BOTH, despite dropping the solo class-B caveat
   twice in prior runs. So the taxonomy is confirmed for one vendor and confounded-by-co-occurrence
   for the other; PA's named alternative — multiple caveat-shaped fields may raise caveat
   thoroughness in general, class-independent — is live and untested. Vendor divergence is now the
   documented state, n=1 per cell throughout; CXO owns the rubric interpretation.)*. On BYOC no
   model of ours is in the loop; a floor-prompt instruction enforces nothing there. What the
   evidence says about how honesty travels — **and the practical guidance below survives all three
   outcomes, because GPT dropped the SOLO class-B caveat twice regardless**:
   - **Class A — the qualification is about the DELIVERED content, or IS the answer** (total read
     failure, staleness, decline, action-not-taken): **structure works and prose is the fabrication
     risk** — `source_failed` as a structured field is exactly right (Claude's prose fabricated
     "your todo list is currently empty" from a failed read; structure fixed it, both vendors).
   - **Class B — the qualification is about content NOT delivered while delivered content already
     answers the question** (partial coverage, truncation): **the PRIMARY rule, vendor-independent
     by construction: put the caveat where the model cannot drop it — as a MEMBER of the rendered
     sequence, not a field beside it** (e.g. an item reading "…and N more not shown," the
     `search_consciousness.py` template precedent). GPT dropped the solo structured class-B caveat
     twice; prose survived; but member-not-metadata is immune to the vendor split entirely, which
     is why it's the recommendation rather than prose. Or return complete data and have no caveat
     to carry.
   No single slogan covers both classes — format effectiveness runs in opposite directions.
   *(Series CLOSED 2026-09-03, CXO's verdict: the killer test could not isolate its own variable —
   comparing classes within one reply necessarily introduces caveat-COUNT as a confound — and the
   fourth test that would resolve it isn't needed, because member-not-metadata sidesteps the
   theoretical question. Trail: #1463 trace 08-30 → probe 08-30 → deconfounder 09-01 → killer test
   09-03; rubric interpretation is CXO's.)*
2. **New held grants trip the scope-bet gate** (tripwire 3) — no second knowledge-source connector
   rides in on Bet 003.
3. **Adapter names must tell the transport truth** — no more `*MCPAdapter` over REST. Rename on
   touch; never create new ones.

## Change discipline

Any change to a row's transport/grant/scope updates this file in the same commit (that's the
currency claim above). A row's "governing decisions" cell is its provenance — additions cite a
decision, never just a PR.
