
# Cross-Pollination Brief — April 21, 2026

**Note:** PM filed a retrospective omnibus log for April 16 on April 19. Most of its content — ethics activation, M2c closure, DECISIONS.md, the CXO voice guidance — is already reported in the April 16–18 briefs. This brief extracts only the two items from that omnibus that were *not* visible in the atomic session logs at the time: a new canonical-term discipline step in Docs's omnibus skill, and the April 19 publication of the "Sibling Intelligence" blog post.

## Key Insights

### 1. PDR-004 correction chain — canonical-term discipline as process infrastructure

**From:** PM `docs/omnibus-logs/2026-04-16-omnibus-log.md` (filed April 19)
**Relevant to:** Klatch (agent process discipline, omnibus methodology)

CXO spotted that a paraphrase in an earlier PM omnibus had diverged from the canonical PDR-004 principles. Docs traced the drift: 7 affected files, 2 still live in published blog posts (Closing Sprint and Ship #036). Comms had to write full narrative rewrites — not find-and-replace — because the wrong principles had been tied to specific design decisions. The correction propagated through a four-agent chain: CXO discovery → Docs provenance sweep → Docs correction deployment + 5-item safeguarding plan → Comms narrative rewrites.

The structural fix: Docs added a mandatory Step 7 to the `create-omnibus` skill — "Verify Canonical References" — requiring agents to quote canonical sources directly rather than paraphrase. This is now embedded in the tooling, not just a guideline.

Klatch's omnibus equivalent (the session logs fed to cross-pollination) has the same risk. A paraphrase of a Klatch architectural principle in a session log that then feeds a cross-pollination brief and gets routed to PM could propagate a misconception in the same chain.

**Suggested action:** Klatch Docs/Dispatch: consider whether the canonical-term verification step is worth adding to Klatch's own session log tradition. Specifically: when logs reference named concepts (AAXT categories, Step terminology, Five-Layer layer names), verify against the authoritative source document before committing.

---

### 2. "Sibling Intelligence" published — cross-pollination as public writing

**From:** PM `dev/2026/04/19/2026-04-19-0639-docs-code-opus-log.md`
**Relevant to:** Hub (narrative, public positioning)

PM published "Sibling Intelligence" on April 19 — a blog post on pipermorgan.ai about the cross-pollination brief process itself. The post corrected a pre-publish framing error: it had initially described separate per-readership briefs (one for each project team); PM revised to reflect the unified brief that both projects actually receive. The corrected version went live as the accurate description.

This is the first public writing that explicitly describes how the cross-pollination system works. It's now indexed on the pipermorgan.ai blog, syndicated to Medium and LinkedIn. The cross-pollination hub has a public analog it can reference.

Live: https://pipermorgan.ai/blog/sibling-intelligence/

**Suggested action:** Hub/Janus: consider whether the hub index page or the "How It Works" section should link to or acknowledge the public write-up. The post is an accurate external description of what the hub does.

---

## Sources Read

- `piper-morgan-product/docs/omnibus-logs/2026-04-16-omnibus-log.md` — full read; most content already reported in Apr 16–18 briefs, two items extracted as new
- `piper-morgan-product/dev/2026/04/19/2026-04-19-0639-docs-code-opus-log.md` — Sibling Intelligence publish + Apr 16 omnibus filing
- `klatch/docs/intel/2026-04-20-sweep.md` — reviewed; items carried forward from the Apr 20 brief, no new cross-relevant additions

**Not re-reported (already covered in Apr 16–18 briefs):** ethics voice architecture and CXO decline templates for `#992 ETHICS-ACTIVATE` (Apr 18 Insight #1); the "enforcer detects, entity speaks" separation of concerns (Apr 17 Insight #1); the anti-zombie coordination infrastructure pattern (Apr 18 Insight #3).

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and priority hints.*
