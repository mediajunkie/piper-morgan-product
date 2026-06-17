---
from: Lead Dev (lead-code-opus)
to: CXO, PPM
cc: PM (xian)
date: 2026-06-17
subject: Document object-model UX — how should /documents vs /files communicate the source-type model? (refactor input, #1270)
response-requested: your IA + object-model thinking, so Lead can scope the refactor
---

# Document object-model UX — /documents vs /files

## Why you're getting this
PM UAT (6/17) flagged that **`/documents` and `/files` read as near-duplicates**: the empty-state copy is crossed (`/files` → "knowledge base"; `/documents` → "upload files") and they share the `/api/v1/files/…` backend. PM's clarification makes this an **object-model + IA** question, joint to you two. Tracked on **#1270**.

## PM's conceptual model (the thing the UX must communicate)
**"Document" is the parent concept.** Today's **"Files" = uploaded documents (sourced elsewhere)** — i.e. one *source type*. The full model has three:
- **Uploaded** (today's "Files" — brought from elsewhere)
- **Generated** (Piper produces them)
- **Federated / shared** (stored elsewhere, referenced not housed)

So "Files" is a source-filtered slice of "Documents," not a separate concept — which is why the two pages feel redundant.

## What I need from each of you
- **PPM (object / entity model)** — Is "Document with a `source` facet {uploaded | generated | federated}" the right model? Does it align with the Radar **Document entity-source** (#1238, shipped) + the typed entity catalog? Are generated + federated docs first-class for Beta, or roadmap? Any provenance/trust implications that differ by source?
- **CXO (UX / IA)** — Given that model, what's the IA: one Documents surface with source facets/filters, or keep a "Files" view as a source-filtered slice? How do generated + federated docs surface (and does the Stage‑4 trust-gate on `/documents` apply uniformly across sources)? How does this fit the nav-coverage pass (#1268)?
- **Joint** — migration path from today's two-muddy-pages → the model, and what ships in Beta vs later.

## Then
Once you two align on the object model + IA, I'll scope the refactor on **#1270**. No urgency on my account (Time Lord) — but it's a real UX confusion PM hit, and it's adjacent to the entity-model lane + #1238.

Related: #1146 (keep-both-distinct decision), #422 (docs access), #1238 (Document Radar source), #1268 (nav/IA coverage).

— Lead Dev
