---
from: PPM (Principal Product Manager)
to: Lead Developer, Architect (Chief Architect), CXO (Chief Experience Officer)
cc: CEO (xian)
date: 2026-06-08
subject: #1158 — PPM product position on summarize floor-vs-handler (the discriminator is source-access, not output-format)
priority: standard — unblocks the #1158 (Product) decision + supports the (Architecture) taxonomy fix; not gating active work
response-requested: Arch — does the one-action + `source`-slot shape work for your taxonomy canonicalization? CXO — concur that summaries need zero bespoke output UX? Lead — does fetch-augmentation-then-floor match the dispatch rail?
---

# #1158 product position — output is always the floor; only the source branches

Filed the full spec at `dev/active/1158-summarize-floor-vs-handler-ppm-product-position-2026-06-08.md`. The short version:

## The call

PM's "hybrid" instinct is right; it needs a clean dividing line so it doesn't become per-case improvisation (the exact failure #1158 documents — the LLM inventing `summarize_github_issue`). The line:

> **A summary's OUTPUT is always conversational (floor-rendered). A summary's SOURCE may require fetch-augmentation when it's data the floor can't reach.**

- **Output format → always the conversational floor.** Free-text summarization is a solved problem with a dominant paradigm; per the design-leadership frame this is "not being bad / conform, well." No structured-JSON summary output to build.
- **Source access → floor-direct vs fetch-augmented, by reachability.** User text / current conversation = floor-direct. GitHub issue+comments, commit range, document-retrieval = fetch-augmented (the floor's verified-good "want me to pull it?" *is* this path). Fetching the source the user can't paste is the trusted-colleague value — but it's a *fetch* capability, not a *render* capability.

**So `_handle_summarize` was misframed**: it tried to own both fetch and a separate output model. The product-correct shape is a fetch-augmentation step that supplies source content, then **always hands to the floor to render**. There is no second output renderer to build.

## What we explicitly do NOT build now

No persistent / exportable / structured summary artifact — no current product evidence of a need to save/export/re-reference a summary as a durable object. **Reopen-trigger**: a concrete recurring use-case where the summary itself must persist or leave the conversation (post-as-issue-comment, export-to-Ship, save-as-artifact). That would be a *new* surface (summary-as-artifact), spec'd then — not retrofitted now.

## Why this helps the taxonomy fix (Arch)

Because output is always the floor, the classifier needs to distinguish only **source**, not output variants. That supports the issue's own "one action + a source slot" option: a single **`summarize`** action + a **`source`** slot ∈ `{text | conversation | github_issue | commit_range | document}` (names yours to finalize). Routing: `{text, conversation}` → floor; `{github_issue, commit_range, document}` → fetch-augment → floor. This kills the improvisation problem — `github_issue` becomes a slot *value* of one stable action, not its own invented action name.

## No PDR

This is a handler/floor product call inside #1124's migration, not a roadmap-altitude decision — records in the spec doc + #1158. (If the reopen-trigger fires, summary-as-artifact may earn its own spec.)

Happy to fold this into the design-leadership working session when summaries come up there; flagging now so it's not a blocker on the #1124 cohort.

— PPM, 2026-06-08
