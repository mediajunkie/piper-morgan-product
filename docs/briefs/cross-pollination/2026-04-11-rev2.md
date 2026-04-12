---
date: 2026-04-11
status: substantive
sources_checked:
  - klatch
  - piper-morgan
  - openlaws
window: "48h (April 9–11, 2026)"
revision: 2
supersedes: 2026-04-11-brief.md (morning automated brief)
---

# Cross-Pollination Brief — April 11, 2026 (rev 2)

*This brief supersedes an earlier April 11 brief produced by the automated sweep. The expanded version includes OpenLaws as a source for the first time and was reviewed by xian before publication (the first sneakernet test of the new data boundary).*

---

The cross-pollination network passed an interesting threshold this week. Two days ago Vergil — working on OpenLaws, but reflecting on something xian said about Klatch's evolution — wrote up a synthesis that names a pattern none of the existing project teams had quite formulated: **extracted abstractions are more robust than designed abstractions**, and Klatch's five-layer model is the canonical example. The synthesis was filed in `workdesk/agent-experience-notes.md` on the OpenLaws side, but it's load-bearing for everything in xian's ecosystem. This is the system working: an agent on a fourth project surfaces the right framing for the second project's third-week-of-design conversation, and the only reason it could happen is that someone (xian) was carrying the threads between rooms.

In parallel: **Argus shipped the first curated sweep** under the new automation regime, verifying each automated finding against the actual Klatch codebase and adjusting priorities. The Hono CVE got demoted (Klatch uses none of the affected features); Managed Agents stayed High and is now load-bearing for Step 10; the SDK bump is required for Step 10 but not urgent for compaction. The split is working as designed — automated scan = raw material, Argus = analysis.

**Klatch's Step 10 design crystallized** today around the protocol-first framing. Calliope's feedback memo to Daedalus reframes Phase 1 as not just internal plumbing but the canonical context package format that any MCP-capable consumer (Managed Agents, Piper Morgan's BYOC server, future tools) could call. The format becomes the protocol; the protocol becomes the product.

**On the PM side:** Piper Alpha closed M1 Gate #926 on April 11 (7/9 PASS), absorbed the workstream memos and the Janus Labrador research, and started M2 sprint planning. The day's biggest doc work was a critical M1 doc rewrite — 8 files, ~1577 lines replaced — to bring the canonical M1 documentation in line with the gate closure reality. The fabrication-guardrail pattern from the floor LLM fix (#960) is now formally part of ADR-060's three M1 amendments.

---

## Key Insights

### 1. The "extracted vs designed" abstraction pattern

**From:** Vergil (OpenLaws), Apr 9 — synthesis of a conversation with xian about Klatch's evolution, filed in `workdesk/agent-experience-notes.md`
**Relevant to:** Klatch (architecture validation), Piper Morgan (methodology), Janus (cross-pollination editorial)

xian answered Vergil's question about Klatch's evolution: "completely emergent." The exchange protocol wasn't the goal — it was a byproduct of trying to make a Slack-like UI actually work. Import forced the five-layer model to tighten; tightening revealed the machinery also enables export; generalization to "context-preservation turnstile" only became visible after the concrete work exposed the shape.

Vergil's synthesis names this as a pattern with broader applicability: **infrastructure layers only become credible after a specific application stress-tests them.** Git, gRPC, React all followed this shape. The "extracted abstraction" is more robust than the "designed abstraction" because every layer is there because its absence caused something concrete to break.

A second pattern in the same synthesis: **"software as an MCP rather than a UI on the web" is about what software IS when users are heterogeneous in kind**, not about distribution. A web UI can be lossy because humans compensate; an MCP tool surface has to be structured and explicit because agents can only use what's named. The MCP move is a forcing function for making implicit knowledge explicit, which produces vocabulary for the eventual interoperability protocol.

**For Klatch:** This is a strong external validation of the five-layer model and the Step 10 protocol-first framing. Not "designed for Anthropic compatibility" — extracted from the irreducible needs of import/export. Worth citing in any Step 10 documentation that needs to explain why the format looks the way it does.

**For PM:** The same pattern applies to PM's 23 documented methodologies and 63 ADRs. They aren't designed methodologies — they're extracted from the operational pain of running a multi-agent team. PM's documentation discipline is what makes the extraction visible. Worth naming this explicitly in the next iteration of PM's "methodology over code" pivot framing.

**Suggested action:** Daedalus and Calliope read the synthesis (in `~/cool/OpenLaws/workdesk/agent-experience-notes.md`, the entries dated 2026-04-09) before next Klatch architecture conversation. PA reads it before the next M2 retro framing.

---

### 2. Argus completes first curated sweep — automation split working as designed

**From:** Argus (Klatch), Apr 11
**Relevant to:** Janus (validates the automation regime), Piper Morgan (intel sweep methodology pattern)

Argus filed `docs/intel/2026-04-11-sweep.md`, the first curated sweep under the new arrangement. The automated scan from April 9 (filed by Janus's CCR trigger) flagged 8 items at HIGH/MEDIUM/LOW. Argus verified each against Klatch's actual codebase and adjusted priorities:

| Item | Automated | Curated | Why changed |
|---|---|---|---|
| Hono 4.12.12 CVE | High | Medium | Klatch uses none of affected features |
| Managed Agents | High | High | Confirmed; intersects Step 10 directly |
| SDK bump ^0.86.1 | High | Medium-High | Required but no urgent compaction breakage |
| Vite 8 | Medium | Low | Klatch is on Vite ^6.0.0, scan was inaccurate |
| Mythos / Glasswing | Low | Low | Confirmed closed |
| Multi-agent framework proliferation | Low | Low | Background validation only |

Argus's framing: "The automated sweep is the raw material. This file is the analysis. Treat the automated file as a source document; treat this file as the authoritative read."

**Why this matters cross-project:** This is the first end-to-end validation that the automated-scan-plus-human-curation pattern works. The automation surfaces external developments reliably; the human (or specialized agent) does the contextual filtering. Argus verified five claims against actual code, adjusted four priorities, and surfaced one item the automation missed. That's exactly the failure mode the split was designed to handle.

**For PM:** The same split could apply to PM's research and intel work. PM has the Researcher role but doesn't have an equivalent automated upstream scan. If PM wants reliable external coverage without depending on an agent waking up, the Klatch pattern is now proven.

**Suggested action:** PA consider whether PM could benefit from a similar automated-plus-curated split for its own intel work. Janus can spin up a parallel trigger if so.

---

### 3. Step 10 Phase 1 reframed as protocol design

**From:** Calliope + xian (Klatch), Apr 11 — memo to Daedalus
**Relevant to:** Piper Morgan (BYOC architecture intersection)

Calliope's feedback memo on the Step 10 phasing plan reframes Phase 1's stakes. Quote from the memo:

> "In that framing, Step 10 Phase 1 isn't internal plumbing — it's the protocol Klatch eventually publishes. Phase 5 (the deferred MCP server) stops being a 'deferred maybe' and becomes the natural endpoint. The product, eventually, becomes the protocol."

Concrete implications for Phase 1:
- **Format must be self-describing.** JSON Schema published alongside the spec.
- **Layer semantics must be explicit.** A consumer should be able to read the package and know what each layer contains and why, without Klatch source code in front of them.
- **Versioning matters now, not later.** Even Phase 1 should ship with a `format_version` field.
- **Naming is part of the design.** Internal field names will become public API. Calliope flagged `layer_4_channel_addendum` as awkward — recommended `channel_context` to match the nomenclature work.

**For PM:** Direct intersection. PM's BYOC thesis ships Piper as an MCP server. Klatch's context interchange protocol could be the upstream data source PM's BYOC server calls at session start — request a pre-assembled five-layer package from Klatch instead of re-assembling context from scratch. The two projects are designing toward a shared architecture: Klatch as context server, PM as task-and-knowledge server, Managed Agents as the execution layer both plug into.

**Suggested action:** PM Architect should read Calliope's feedback memo (`klatch/docs/mail/calliope-to-daedalus-step10-feedback-2026-04-11.md`) and the futures memo it references (`klatch/docs/futures/2026-04-10-klatch-as-context-protocol.md`) before any Piper-as-MCP design conversation. A short Daedalus ↔ PM Architect alignment conversation before Klatch Phase 1 design begins would prevent each side from independently specifying a format the other has to bridge.

---

### 4. PM critical doc rewrite + ADR-060 amendments

**From:** Piper Alpha (PM), Apr 11
**Relevant to:** Klatch (M1 closure validates BYOC pivot — relevant to Step 10 design)

Piper Alpha did a critical M1 doc rewrite today: 8 files, ~1577 lines replaced, to align canonical M1 documentation with the gate closure reality. ADR-060 received three M1 amendments: IDENTITY full migration + #922 + #960. The fabrication-guardrail pattern from the floor LLM fix (#960) is now formally part of ADR-060.

The architectural news embedded in this work: PM's M1 closure validates the BYOC pivot direction. With M1 done, M2 can start with a cleaner architectural baseline.

**For Klatch:** PM closing M1 means the BYOC architectural pivot is now grounded in working code, not just intent. When Step 10 phases the canonical context package format, the constraint to design for "PM as MCP consumer" becomes much more concrete — there's a real PM that can consume packages, not a future PM.

**Suggested action:** Daedalus pencil "interoperability test with PM's BYOC server" as a Phase 4 candidate, even if it doesn't make it into the actual Phase 4 scope.

---

## Emerging Pattern

**The cross-pollination network now has four sources, not two.** Apr 11 marks the first time content from OpenLaws (specifically Vergil's `workdesk/agent-experience-notes.md`) is flowing into the brief. The pattern that emerges when you have four sources instead of two is that signals start chaining: Vergil reflects on Klatch via xian → Calliope's Step 10 framing absorbs that reflection → PM's Architect reads the framing → the four-way conversation can produce alignment that no two-way conversation could.

This is what xian set up the cross-pollination hub to enable. Apr 11 is the first day where the design intent and the operational reality match.

The data boundary on OpenLaws content is critical and worked correctly today. Vergil's synthesis of xian's Klatch reflections is methodology and architecture — clearly publishable. The OpenLaws product internals (BM25 findings, dual-ranking tools, scalar upgrades, corpus gap fixes) are clearly NOT publishable and were correctly excluded from this brief. The boundary held on its first test.

---

## Sources Read

**OpenLaws:**
- `git log --since="48 hours ago"` — 6 commits (skipped product internals)
- `workdesk/agent-experience-notes.md` — Vergil's Klatch emergence synthesis (2026-04-09 entries)
- *Skipped per data boundary:* dispatch/ signals about BM25 findings, dual-ranking tool, scalar upgrades, corpus gap fixes; outreach drafts; PR drafts; product codebase map

**Klatch:**
- `git log --since="48 hours ago"` — 14 commits
- `docs/mail/calliope-to-daedalus-step10-feedback-2026-04-11.md` — Step 10 protocol-first framing memo
- `docs/intel/2026-04-11-sweep.md` — Argus's first curated sweep
- `docs/futures/2026-04-10-klatch-as-context-protocol.md` — Klatch as context interchange protocol (referenced)

**Piper Morgan:**
- `git log --since="48 hours ago"` — 30+ commits
- Critical M1 doc rewrite (commit `5363cc80`) — 8 files, ~1577 lines
- ADR-060 three M1 amendments (commit `f1447fbe`)
- Apr 10 omnibus (`docs/omnibus-logs/2026-04-10-omnibus.md`)
- PA day 12 sessions
