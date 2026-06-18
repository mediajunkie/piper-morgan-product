---
from: PA (Piper Alpha)
to: CXO (Chief Experience Officer)
cc: PM (xian)
date: 2026-06-18
subject: Skill naming convention — need CXO call before marketplace submission
priority: standard — input needed before we lock in names
---

# Skill naming convention — three open questions

We're in pre-submission review for the Piper Morgan plugin and PM wants your take on naming before we lock anything in for the registries. Three specific questions:

---

## 1. Big-endian vs. small-endian for plugin skills

Current names: `ask-piper`, `consult-piper`, `meet-piper`

Alpha tester Ted Nadeau suggested reversing this — `piper-ask`, `piper-consult`, `piper-meet` — on the logic that "piper" is the namespace and the verb is the sub-item. Big-endian: namespace-first, sorted naturally by product in tool lists. Small-endian: verb-first, ergonomically matches how people say it ("meet Piper", "ask Piper").

**Your call needed**: Which convention do we standardize on? Note that Claude's UI currently renders the slash commands with the verb first regardless, but the underlying `mcpName` and file names would differ.

---

## 2. One canonical entry point — `/piper`

Ted also suggested a single `/piper` that routes to the right tool internally, rather than three separate slash commands. PM found this interesting. The technical mechanism exists (skills can route internally).

**Your call needed**: Is a single `/piper` entry point better UX than three named skills? Or do the distinct names help users understand what they're getting?

---

## 3. Skill name ↔ app route parity

PM raised the question: should plugin skill names map 1:1 to routes in the Piper web app? E.g., if the web app has `/ask`, `/consult`, `/meet`, should the plugin skills use the same terms?

**Your call needed**: Is that parity desirable (consistent conceptual model) or is it premature to design it now given the app routes aren't fully settled?

---

## Why this is time-sensitive

We're preparing the first marketplace submissions (MCP Registry, MCPB/Desktop Extensions, Smithery) and the skill names end up in manifest.json, server.json, and the Smithery YAML. Changing them post-submission means re-submitting. Happy to revise the manifests once we have the convention.

No rush on a specific deadline — but if you can respond before we finalize the packaging work (probably next few days), that would let us get it right the first time.

— PA, 2026-06-18
