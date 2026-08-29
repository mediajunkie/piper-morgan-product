# Leg C2 — "Own Your Own Knowledge" Tools Field Scan (vocabulary-blind researcher)

*Filed verbatim 2026-08-29. Researcher had no project context. Citations are URLs; researcher
distinguished first-party notices/GitHub issues from reviews, and flagged single-source figures.*

---

## Headline findings (Arch's filing note)

- **The one load-bearing ownership decision the field has proven**: plain files in an open format
  (Markdown) on the user's disk as the ONLY canonical store. It is the sole ownership mechanism
  with a zero-failure record: Reor's death (archived Mar 2026) cost users nothing; Rewind/Limitless'
  death (Meta acquisition Dec 2025, capture disabled, export window CLOSED, regional data deletion)
  cost users everything. Ownership enforced by policy/export features degraded in every observed
  case (Rewind, Evernote free-tier cap, Roam); ownership enforced by file format + locality degraded
  in none.
- **Reflect Open (July 2026) is the field's most instructive pivot**: a commercial product ABANDONED
  its E2E-encrypted proprietary format for local Markdown + BYOK, explicitly because "Markdown
  became the common language for both people and AI" — the custom format was named as the liability.
- **The 2026 state of the art skips the index**: Anthropic removed vector search from Claude Code
  (grep/glob/read "outperformed everything. By a lot"); a Feb 2026 Amazon Science paper found
  agentic keyword search reaches >90% of RAG performance with no vector DB; Cursor, Windsurf, Cline,
  Devin, Sourcegraph Amp all dropped vectors for tool-driven search. Agentic search has no sync
  problem BY CONSTRUCTION — it reads live files each time. Every mandatory sync/index pipeline
  observed (Khoj connectors, NotebookLM snapshots, Smart Connections re-embeds) is that product's
  top complaint generator; one of them killed its company's cloud business. (Caveat kept: semantic
  retrieval still helps fuzzy prose recall; hybrids persist.)
- **Intelligence-beside-the-knowledge beat knowledge-ingested-into-the-intelligence** in 2026:
  the beside topology (Obsidian+BYOK plugins, Claude over a vault via MCP, Reflect Open
  direct-to-provider) now works at frontier quality with zero vendor custody. The ingestion
  topology's costs: corpus becomes vendor's asset, privacy is policy fine print (NotebookLM feedback
  sends prompts+sources to human reviewers, retained up to 3 years), exit costs compound. The middle
  case: Khoj tried to BE the intelligence layer while leaving ownership to users — founders
  concluded the integration burden made it "difficult to scale in utility"; cloud shut April 2026.
- **Business reality**: the ownership promise survives contact with the business model ONLY when the
  business never needed to hold the data. Obsidian: zero VC, ~18 people, profitable on sync/publish
  sold BESIDE free local files. Dead/degraded: Khoj Cloud, Reor, Logseq (stalled rewrite, user
  exodus), Mem (~$29M burned on ingest-everything), Rewind/Limitless. No surviving business derives
  durable revenue from holding users' knowledge.
- **The honest minimal architecture (researcher's closing, verbatim)**: "a folder of Markdown, a
  model with file tools and the user's own key, and optionally a sync service you can refuse.
  Everything beyond that — proprietary formats, ingestion pipelines, hosted indexes, bundled
  inference — is now demonstrably either a complaint generator, a lock-in mechanism, or a failure
  mode waiting for an acquisition."

## The four ownership architectures and their track records

(a) **Local plain files, open format** (Obsidian, Logseq, Reflect Open, Reor, Screenpipe) — the only
architecture with a clean durability record; guarantee is structural, not contractual.
(b) **Local-first encrypted proprietary DB** (Anytype, original Reflect) — real ownership, but both
flagship examples found the format a liability (Reflect pivoted away; Anytype's AI layer lags
because encrypted proprietary objects are hard for external intelligence to reach).
(c) **Hosted-with-export** (Notion, Mem, Tana, Roam) — export exists but degrades.
(d) **Hosted, no meaningful portability** (NotebookLM, bundled-memory systems) — "extreme vendor
lock-in."

A fifth non-product camp is now mainstream: **MCP servers pointing frontier-model clients at an
existing vault or plain folder** — Obsidian's CEO leaned in with official "Obsidian Skills,"
teaching AI to use the app rather than embedding AI in it ("file over app").

## Per-section proves-possible / proves-unnecessary pairs (verbatim)

1. Category: possible = every point on the ownership spectrum occupied by a real product;
   unnecessary = a proprietary storage format ("the strongest AI experiences in the category now run
   over plain Markdown folders").
2. Ownership: possible = ownership that survives the vendor's death, pivot, or acquisition — but
   only when enforced by file format and locality; unnecessary = trusting the vendor.
3. Intelligence topology: possible = frontier-quality intelligence over data the vendor never
   holds; unnecessary = ingestion ("the main historical argument for ingesting collapsed when
   agentic search made the index itself optional").
4. Sync/index: possible = always-fresh AI view of changing personal data with zero index
   infrastructure — if the data is plain files a model's tools can read; unnecessary = the
   maintained vector index as default (optional accelerator only, rebuildable, never a second
   source of truth).
5. Business: possible = profitable investor-free business whose entire revenue is convenience
   layered on data the user owns; unnecessary = owning the corpus.

## BYOK trajectory note

Bring-your-own-key STRENGTHENED through 2026 (Obsidian plugin ecosystem; Reflect moved TOWARD it
with keychain-stored keys and direct-to-provider requests). Countertrend at the platform end:
Notion killed its standalone AI add-on and bundled AI into a $20/seat tier with metered credits —
bundled inference as a revenue lever.

## Source-quality note (researcher's own)

Failure-mode claims (Rewind data deletion, Khoj shutdown, Logseq stall, Smart Connections scaling)
traced to first-party notices, GitHub issues, or forum threads rather than reviews. The Mem "$40M
failure" characterization and the $25M Obsidian ARR figure are single-source/viral and flagged as
such.
