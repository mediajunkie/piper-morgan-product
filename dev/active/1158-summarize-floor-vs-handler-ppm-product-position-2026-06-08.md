# #1158 Summarize — PPM Product Position (floor-vs-handler)

**Owner**: PPM · **Date**: 2026-06-08 · **Status**: PPM product spec — input to Arch (taxonomy) + CXO (UX) + Lead (build); folds into the design-leadership working session.
**Resolves**: the (Product) decision in #1158 ("Handler-vs-floor for summaries... what sources, what output"). PM leaned *hybrid*; this sharpens hybrid into a decisive discriminator.

---

## The decisive call: the discriminator is SOURCE-ACCESS, not OUTPUT-FORMAT

PM's "hybrid" instinct is right, but "hybrid" needs a clean dividing line so it doesn't become per-case improvisation (the exact failure #1158 documents — an improvised `summarize_github_issue` action). The line:

> **A summary's OUTPUT is always conversational (floor-rendered). A summary's SOURCE may require fetch-augmentation (handler-fetched) when it's data the floor can't reach.**

Two independent axes, and only one of them branches:

| Axis | Decision | Rationale |
|------|----------|-----------|
| **Output format** | **Always conversational floor.** No structured-JSON summary output path. | Free-text summarization is a *solved problem with a dominant paradigm* (Claude/ChatGPT/Gemini converged; our floor verified-good live). Per the design-leadership frame this is **"not being bad" → conform, well.** A structured summary renderer would be reinventing a solved element. |
| **Source access** | **Floor-direct** when the source is already reachable (user text, current conversation); **fetch-augmented** when it isn't (GitHub issue+comments, commit range, document retrieval). | Fetching the source the user *can't* paste is the **trusted-colleague value** — Piper knows the integration and pulls it. This is the only part with unique value; it is a *fetch* capability, not a *render* capability. |

**So the "handler" is misframed in the original code.** `_handle_summarize` tried to own both fetch AND a separate output model. The product-correct shape is: a **fetch-augmentation step** supplies source content, then **always hands to the conversational floor to render**. There is no second output renderer to build.

## Product spec — sources & output

**Sources (what can be summarized)** — classified by *does the floor already have it?*
1. **User-provided text** ("summarize this: …") → floor-direct. No fetch.
2. **Current conversation / thread** ("summarize what we discussed") → floor-direct. Already in context.
3. **GitHub issue (+ comments)** ("summarize issue 42") → **fetch-augmented** (the floor's verified-good fallback today is "I don't have access to that issue, want me to pull it?" — fetch-augmentation is exactly that "pull it" path).
4. **Commit range / PR** ("summarize the last 10 commits") → **fetch-augmented.**
5. **Referenced document** → floor-direct if already in context; **fetch-augmented** if it needs retrieval.

**Output (what a summary is / feels like)**: conversational text, every time. Trusted-colleague tone — the floor already does this well. No JSON, no structured artifact, no separate "summary object."

## What we are explicitly NOT building now (and the reopen-trigger)

**No persistent / exportable / structured summary artifact.** There is **no current product evidence** of a need to save, export, or re-reference a summary as a durable object. Per PDR-craft discipline (decisive, not aspirational), we do not build a structured-handler output path speculatively.

**Reopen-trigger** (when the floor-only-output call should be revisited): a concrete, recurring use-case where the *summary itself* must persist or leave the conversation — e.g. "post this digest as a comment on the issue," "export the weekly summary to the Ship," "save this as a reusable artifact." When such a use-case is named with a real user behind it, that's a *new* product surface (summary-as-artifact), spec'd then — not retrofitted onto the summarize action now.

## Why this unblocks Architecture (the taxonomy fix)

The load-bearing #1158 blocker is classifier-vocabulary canonicalization. This product position **collapses the decision space** the taxonomy must serve:

- Because **output is always the floor**, the classifier does **not** need to distinguish summary *output* variants. It needs to distinguish only **source**.
- That supports the issue's own "one action + a source slot" option: a single **`summarize`** action with a **`source`** slot ∈ `{text | conversation | github_issue | commit_range | document}`. (Names are Arch's to finalize; the *shape* is one-action-plus-source-slot.)
- Routing rule: `source ∈ {text, conversation}` → straight to floor; `source ∈ {github_issue, commit_range, document(retrieval)}` → fetch-augmentation → floor.
- This kills the improvisation problem: the LLM stops inventing `summarize_github_issue` because `github_issue` is a *slot value* of one stable action, not its own action name.

## Mapping to the design-leadership frame (§2–§4 of `design-leadership-framing-web-ui-2026-06-03.md`)

- **Summary output = "not being bad" / Standard 2 (paradigm conformance).** Dominant paradigm exists (conversational summaries); conform, well; don't reinvent.
- **Source-fetch for unreachable data = trusted-colleague value** but delivered *through* the conforming floor — not a bespoke output surface. (It's "being good" in *capability*, "not being bad" in *presentation*.)
- Net: summaries need **zero bespoke output UX**. The being-good investment for summaries is entirely in *reach* (what sources we can pull), not in *render*. Good news for the UX session — one less bespoke surface to design.

## Disposition

- **Output**: conversational floor, always. ✅ decided.
- **Source**: floor-direct vs fetch-augmented, by reachability. ✅ decided.
- **Structured/persistent artifact**: not now; explicit reopen-trigger above. ✅ decided.
- **Taxonomy**: product position supports one-action + `source` slot (Arch finalizes names/shape).
- **No PDR needed** — this is a handler/floor product call inside #1124's migration, not a roadmap-altitude decision. Records here + into #1158; if the reopen-trigger fires, *that* (summary-as-artifact) may earn a spec.

## Cross-refs
#1158 · #1124 (parent; pre-floor-handler migration) · `pre-floor-handler-migration-roadmap-1124.md` · design-leadership framing v0.3 (`dev/active/design-leadership-framing-web-ui-2026-06-03.md`) · methodology-30 (consumer-trace — Lead's pre-migration probe that surfaced this).

---
*PPM, 2026-06-08. Input to Arch (taxonomy) + CXO (UX) + Lead (build). Standing-items #9.*
