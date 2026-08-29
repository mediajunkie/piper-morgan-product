# Bet 003 — Notion as a backend-held grant

**State**: PROPOSED (retroactive, 2026-08-29)
**Tripwire crossed**: #3 (external integration where we hold the grant) — applied retroactively to
the one connector the review's synthesis flagged as genuinely ambiguous under C4's decision rule
("hold the grant only where you must act without the user present").

## 1. The buyer

**xian — pre-filled from PM's own answer, 2026-08-29** (⟨PM: confirm or amend⟩): Notion is "a wiki,
an all-purpose project doc-making tool... the user's external mirror of documents moved in and out
of Piper's workspace, but also connected to the user's colleagues and workplace."

## 2. The bet

PM's answer implies the **headless case is real**: a document *mirror* means Piper moves content
in/out of Notion outside chat turns (sync, ingestion into the knowledge base, publishing artifacts
where colleagues see them). Under C4's rule, that justifies a backend-held grant — mirroring is
exactly "acting without the user present." The bet, stated falsifiably: **the Notion mirror is (or
within the appetite becomes) a real, used workflow — documents actually flow both directions and
land where colleagues encounter them.**

*Arch's honest current-state note*: Leg B found `notion_adapter.py` live via the plugin router but
a REST shim (zero real MCP calls) — which is fine, the transport isn't the question. What discovery
did NOT establish is whether the mirror workflow *runs* today or is aspiration. The smallest true
version below is designed to answer that with evidence rather than either of us guessing.

## 3. The cost box

⟨**PM TO FILL** — appetite for making the mirror real if it isn't yet. Arch's recommendation:
whatever the answer, the pre-registered scope cut is **no second knowledge-source connector**
(Confluence, Google Docs, etc.) rides in on this bet — each would be its own memo.⟩

## 4. The kill condition

If, by ⟨**PM TO FILL** — date⟩, no real document has round-tripped (Piper→Notion where a colleague
could see it, and Notion→Piper's knowledge base with a cited answer served from it), the held
grant converts to the C4 default: **host-mediated on the BYOC path** (the user's own Notion
connector inside Claude/ChatGPT serves in-conversation reads), and Piper's backend grant is
dropped. Not a punishment — just the rule: no headless use, no held grant.

## 5. The smallest true version

One real round-trip, instrumented: (a) Piper publishes one artifact (e.g., a standup or a PRD
draft) to PM's actual Notion workspace; (b) one Notion doc is ingested and a chat question is
answered from it with a citation. Both verified at the user-visible layer (m-43), not by API
200s. If both already work today, this memo's bet is simply WON and the grant is ratified as
correctly backend-owned — the memo then just records why.
