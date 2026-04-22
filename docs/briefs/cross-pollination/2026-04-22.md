# Cross-Pollination Brief — April 22, 2026

PM published "Four Roles, Ninety Minutes" on April 21 — its second narrative blog post in four days, describing how a 90-minute async memo session among four roles produced a design document and closed Issue #717. A weekly docs audit flagged 4 days of unsynthesized omnibus logs (Apr 17–20) deferred to today; the next brief should apply the retrospective log rule when those files land. Klatch watch paths are silent in the 48h window; Phase 5c remains at the decision point established in the April 20 brief.

## Key Insights

### 1. "Four Roles, Ninety Minutes" published — async multi-role design session as public narrative

**From:** PM `dev/2026/04/21/2026-04-21-2205-docs-code-opus-log.md`; `docs/public/comms/drafts/published/four-roles-ninety-minutes.md`
**Relevant to:** Klatch (narrative template for multi-agent coordination work), Hub

PM published this April 21 on pipermorgan.ai and Medium. The post narrates the March 23 session where Lead Dev sent five memos to Architect, CXO, and PPM to settle the product/project data model. The CXO/PPM disagreement was productive: CXO favored products as a section within projects (emergence model); PPM favored products as top-level navigation (orchestration model). PM pushed back on the false dichotomy; PPM synthesized both into a navigation design where products appear as a section but with a clickable header supporting the orchestration path. Issue #717 closed with a full design document in 90 minutes.

This is now PM's second public-facing blog post describing how the multi-agent system works from the inside. "Sibling Intelligence" (April 19) described the cross-pollination brief mechanism; "Four Roles, Ninety Minutes" describes the design memo session pattern. Both posts make the internal coordination model legible to outside readers without requiring readers to understand the technical substrate.

The memo pattern described in the post is structurally identical to Klatch's context interchange pattern: structured context passed between roles, each responding from domain expertise, synthesis at the end — no real-time synchronization required. Klatch's own Phase 5 development sessions (Daedalus memo to PM Architect on MCP surface, Calliope routing Pattern-062 to Argus) have exactly this shape. Klatch currently has no public blog presence. The post is a template for how that work could be narrated: specific session, specific productive disagreement, specific synthesis, measurable result.

**Suggested action:** Klatch — Calliope: two PM blog posts now narrate multi-agent coordination in concrete terms. If Klatch blog presence becomes a priority, the "Four Roles, Ninety Minutes" template is the pattern: name the session, name the disagreement, name the synthesis, name the result. Phase 5 MCP development has at least one story of that shape (Daedalus/Argus round-trip, cross-producer alignment resolved in a single day).

---

### 2. PM omnibus backlog — 4 days unsynthesized, retrospective rule applies when they land

**From:** PM `dev/2026/04/21/weekly-docs-audit-2026-04-20-findings.md` (issue #996)
**Relevant to:** Hub (brief process continuity)

The weekly docs audit confirmed omnibus coverage is complete through April 16. Four days remain unsynthesized:
- **Apr 17 and 18**: explicitly deferred by PM to April 22 (today)
- **Apr 19**: light day (xian traveling + Sibling Intelligence publish) — a Docs session log exists but no omnibus
- **Apr 20**: no session logs found in the file system

When these logs commit, their content dates will precede this brief. Apply the retrospective log rule: use them to fill in detail on already-reported items, but do not generate new Key Insights from events already visible in the atomic session logs. Items already reported in the April 17–21 briefs include: Pattern-062 AAXT routing (Apr 17), ethics activation #992 and M2c closure (Apr 18), Sibling Intelligence publication (Apr 19), session log maintenance hook pattern (Apr 20).

One item worth watching for: if an Apr 17–18 omnibus captures a response from Argus on the Phase 5c write-path decision point, or a PM Architect position on write-path coordination timing, that would be reportable — both were open asks at the time of their respective briefs, and a response may not have been visible in the atomic logs when they ran.

**Suggested action:** Hub (next brief writer): when the Apr 17–20 omnibus commits land, check content dates before extracting insights. Treat any Apr 17–20 activity as confirmatory unless it specifically addresses an open ask (Phase 5c position memo, Argus Pattern-062 checklist, probe-set coordination response) that was unresolved in the atomic logs.

---

## Sources Read

- `piper-morgan-product/dev/2026/04/21/2026-04-21-2205-docs-code-opus-log.md` — Docs session: Four Roles publish + weekly docs audit #996
- `piper-morgan-product/dev/2026/04/21/weekly-docs-audit-2026-04-20-findings.md` — audit findings, omnibus coverage table
- `piper-morgan-product/docs/public/comms/drafts/published/four-roles-ninety-minutes.md` — published post, full read
- `klatch/docs/logs/`, `klatch/docs/mail/` — most recent files dated April 18; no new activity in 48h watch window

**Not re-reported (already covered in prior briefs):** PDR-004 canonical-term discipline (Apr 21), ethics voice architecture (Apr 21, 18, 17), Phase 5c write-path decision point (Apr 20), Opus 4.7 GA and deprecation deadlines (Apr 20), session log maintenance hooks (Apr 20), Klatch MCP server Phase 5a+5b (Apr 19), cross-producer protocol alignment (Apr 19), Pattern-062 AAXT diagnostic (Apr 19).

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and priority hints.*
