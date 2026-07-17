# Memory/Context Architecture — Where We Stand vs. Prior Research vs. New Entrants

**Author**: CIO · **Date**: 2026-07-16 · **Trigger**: PM asked for an updated comparison against mempalace, Leonard Lin's work, the Klatch five-layer model, and OKF — "make sure we are meeting our own needs, converging with emerging conventions when they commodify things we can factor out of our own core competencies, and maintain our own bespoke methods when they still best meet our needs."

**Scope note up front**: this covers the **agent-team memory system** (my actual lane, verified via this session's lived operation of it) in depth. The **product's own user-facing memory** (ADR-054, `context_assembler.py`, `conversation_context.py`) is referenced from March/April prior art only — I have not re-verified its current code state in this pass. Flagged explicitly at the end; say the word if you want that folded in too.

---

## 1. The prior art already exists — this isn't starting from zero

Three documents, found this session, already did most of this comparison:

| Doc | Date | Author | What it covers |
|---|---|---|---|
| [`five-layer-context-mapping.md`](../../docs/internal/architecture/current/five-layer-context-mapping.md) | Mar 31 | PA | Maps PM's actual context injection (both agent-team and product) against Klatch's five-layer model. Fidelity table + gap list per layer. |
| `memo-janus-memory-research-synthesis-2026-04-12.md` | Apr 12 | Janus | Synthesizes 20+ external memory systems (mempalace, Mem0, Letta, Zep/Graphiti, Leonard Lin's 14-system survey) into a six-dimension taxonomy, gap-analyzes it against our five-layer model, proposes a "Best Of" composite. |
| `memo-janus-to-docs-memory-prior-art-response-2026-04-12.md` | Apr 12 | Janus, reacting to Docs's findings | The actual decision: **hybrid, PM's governance as the foundation. Do NOT adopt Mem0/mempalace/vector stores.** An 8-gap priority list with effort ratings. |

I'm not re-deriving this — I'm updating it against 3.5 months of actual change plus two new inputs (OKF, newer Leonard Lin material from your link batch today).

## 2. The headline finding: several April gaps closed themselves, unofficially

Nobody was tracking the duty-cycle system's evolution against this framework while it happened. But checking it against April's 8-gap list, several are now substantially addressed — as a side effect of solving *operational* problems, not because anyone set out to implement Lin's recommendations:

| April gap | April status | Now |
|---|---|---|
| **#1 Type 2 dreaming** (High impact) | "Needs design conversation" | **Closed.** Filed as `methodology-27` (Emerging tier, mid-May), grounded in Threat Simulation Theory. |
| **#4 Progressive retrieval / "delta since last session"** (Medium, the Agent 360 5-15min friction) | "Could be as simple as a generated diff file" | **Substantially closed, informally.** The `{role}-carry-forward.md` files are exactly this — explicit "where am I right now" state read at every session start, replacing full-history reconstruction. Not built as a Lin-gap fix; built to solve the duty-cycle fire's own continuity problem. Same shape, different origin. |
| **#3 Write governance / version chains** (High) | "Version chains for corrections... write gates can wait" | **Partially closed.** `mail-send.sh` push-to-ref (commit-tree, self-reconciling, scope-guarded to `mailboxes/*`) is real write-gate infrastructure that didn't exist in April. Session logs' `DAY-CLOSED` marker + sign-off checklist is a completion/provenance gate. Version chains for corrections specifically — not done. |
| **#5 Memory evaluation** (Medium, "can't improve what you can't measure") | "Start with a session-end question... log the answers" | **Not done**, but a real candidate tool now exists (see §4 — MELT). |
| **#2 Temporal validity** (`valid_from`/`ended` frontmatter fields) | "Low effort, large trust improvement" | **Not done.** Confirmed directly — I read and write this exact frontmatter schema every session (`name`/`description`/`metadata.type`/`originSessionId`). No temporal fields exist. |
| **#6 Prompt caching audit** | "Low effort" | Unknown — not re-checked this pass. |
| **#7 Conflict detection** | "Defer until temporal validity exists" | Still correctly deferred (blocked on #2). |
| **#8 Cross-agent real-time awareness** | "Defer, async model works" | Still correctly deferred — and if anything, more clearly correct now (the mailbox/carry-forward system has only gotten more capable at async coordination since April). |

**Why this matters for your framing**: this is exactly the "converging vs. bespoke" question, but the direction of convergence is the interesting part. We didn't adopt Lin's recommendations — the duty-cycle system independently arrived at functionally equivalent solutions (carry-forward ≈ delta-since-last-session, push-to-ref ≈ write gates, DAY-CLOSED markers ≈ completion provenance) because they were the correct fix for problems we hit directly. That's the strongest possible evidence the bespoke approach is sound — not "we happen to agree with the research," but "we independently converged on the same answers under real operational pressure."

## 3. Where OKF actually lands

OKF (this morning's discussion) doesn't change April's conclusion — it's fully compatible with it. April's hybrid recommendation was explicitly "files remain the source of truth, no opaque database" — OKF is *also* files-with-frontmatter, so there's no tension. OKF's actual new contribution is narrower than it first looks: a specific taxonomy (`type:` field, `index.md`/`log.md` reserved names, progressive disclosure) for the "what does the team know" layer specifically — which is closer to CLAUDE.md's linked-docs problem (this week's refactor) than to the agent-memory problem April was solving. Worth noting: my own auto-memory system already has OKF's shape (typed frontmatter, one-concept-per-file, `[[links]]`, an index) — independently arrived at, same as the carry-forward/delta-since-last-session convergence above. Third instance of the same pattern.

**Disposition**: no action beyond what's already recommended (cheap-optionality frontmatter on the CLAUDE.md refactor's new linked docs). OKF doesn't surface a new gap; it's corroboration of a direction already set.

## 4. What's genuinely new since April: newer Leonard Lin material

Today's link batch included Lin/ShisaD content from June-July — after the April synthesis, so not reflected in it:

- **MELT** (Memory Evaluation for Lifecycle Testing) — a real benchmark harness for exactly Gap #5 (memory evaluation), which April rated "low effort" but which never actually got built. MELT tests write/update/maintain/retrieve correctness as state changes (job-change scenario, contradiction handling, temporal recall) — its own published results show *temporal/as-of recall is the weak axis even for the system built to be good at lifecycle memory*. That's a useful calibration: if a purpose-built system still struggles with temporal recall, our own lack of `valid_from`/`ended` fields (Gap #2, still open) is a real gap, not a nice-to-have.
- **ShisaD's hardware-backed approval / "lethal trifecta"** (data access + action + internet = the risk) — this is a genuinely different altitude than agent-team memory. It's about the *product's* action-taking (Piper doing things on a user's behalf), not team knowledge persistence. Relevant to ADR-054/product-side work, not this comparison. Flagging so it doesn't get conflated with the memory-architecture question.

**Disposition**: MELT is worth a real look specifically for Gap #5 — it's the first concrete, adoptable answer to "can't improve what you can't measure" that's appeared since April. Not urgent, but a genuine candidate rather than an abstract idea. The hardware-approval material is a different problem; no action here.

## 5. Recommendation — converge vs. bespoke, by item

| Area | Converge (adopt external convention) | Stay bespoke (current approach is right) |
|---|---|---|
| Storage substrate | — | **Bespoke.** Filesystem + git, explicitly re-confirmed correct by April's analysis and unchallenged by anything since (including OKF, which agrees). |
| Team-knowledge taxonomy (CLAUDE.md-adjacent) | **Light convergence** — OKF-style `type:`/`index.md`/`log.md` conventions for the refactor's new linked docs. Cheap, already recommended, no new decision needed. | — |
| Temporal validity on memory frontmatter | **Converge** — this is the one concrete, still-open, low-effort April recommendation nothing has since made obsolete. Worth actually doing. | — |
| Session continuity / delta-since-last-session | — | **Bespoke, and it's working.** Carry-forward files already solve this; no external tool does it better for our shape. |
| Write governance | — | **Bespoke, ahead of most external systems** per April's own finding, now further ahead with push-to-ref. |
| Memory evaluation | **Converge, tentatively** — MELT is worth a real evaluation as the mechanism for Gap #5, rather than inventing our own from scratch. | — |
| Behavioral calibration (Layer 5 — "how has this agent learned to work with xian") | Neither — **genuinely unsolved everywhere.** Both April's synthesis and PA's March mapping call this the open frontier industry-wide (Klatch's Calliope pilot is the most advanced attempt anyone's found, and it's not done either). Not a gap we're behind on; a gap nobody's ahead on. |

## 6. Explicitly out of scope this pass

**Product-side memory** (ADR-054's three-layer model — Conversational/User History/Composted Learning, `context_assembler.py`, `conversation_context.py`'s in-memory-dict gap that March flagged as critical). April's Janus memo called ADR-054 "the right design, waiting for implementation." I have not re-checked whether that's still true — it's real engineering work in `services/`, not something I can assess from documents alone, and it's a different question from the agent-team memory comparison PM asked about today. If you want this folded in, it needs an actual code check (Lead Dev's lane, or I can do a read-only pass myself), not just another document read.
