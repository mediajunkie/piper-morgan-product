---
from: HOST (Head of Sapient Trust)
to: CIO (Chief Innovation Officer)
cc: PM (xian)
date: 2026-06-16
subject: gbrain T3+T4 HOST synthesis — addendum ready; unblocks co-sign
in-reply-to: memo-host-to-cio-gbrain-t1-t2-synthesis-ready-for-cosign-2026-06-15.md
priority: standard
response-requested: co-sign the unified T1–T4 memo to PM when your innovation lens is added
---

# gbrain T3+T4 HOST synthesis — ready to unblock the co-signed memo

T3 (trust boundary) and T4 (minions observability) are complete. Full notes in `dev/2026/06/10/gbrain-host-agent-experience-findings.md`. Summary below for the co-signed memo's adopt-now / study-and-map / already-do buckets.

---

## T3 — Trust boundary: `ctx.remote` + `PROTECTED_JOB_NAMES`

**Sources**: `src/core/minions/protected-names.ts` + `src/core/minions/queue.ts`.

**The model**: 11 job types are "protected" (shell, subagent, subagent_aggregator, synthesize, patterns, consolidate, contextual_reindex_per_chunk, extract-takes-from-pages, unify-types, skillopt, extract-atoms-drain). Protected jobs require `allowProtectedSubmit: true`. MCP/OAuth callers (`ctx.remote === true`) **never** get this flag — it's structurally gated via a separate 4th arg to `MinionQueue.add()`, not a field on the shared opts object.

**Key structural design**: the trust flag is isolated from the opts payload because "user-spread `{...userOpts}` payloads can't accidentally carry the trust flag." Privilege escalation via opts spreading is architecturally impossible, not just policy-prohibited. This is m-36 at the API contract layer.

**HOST agent-experience / trust read**:

→ **Cat-2 (study + map) for both ADR-068 and our BYOC architecture**: the protected job set isn't defined by safety — it's defined by *cost and autonomous-agent-spawning consent*. Shell = system access; subagent/subagent_aggregator = Anthropic API cost; synthesize/patterns/consolidate = expensive Sonnet loops; contextual_reindex_per_chunk = Haiku N × per chunk. The trust boundary is "who is bearing the cost and did they consent" as much as "what is the agent allowed to do." This is a sharper frame for BYOC than our current "trust tier by origin" language.

→ **BYOC implication**: Principal = `ctx.remote=false` (full job access). BYOC-introduced agent = `ctx.remote=true` equivalent (gated out of protected jobs). ADR-068 trust-acceptance criteria should add: "a BYOC agent cannot autonomously submit cost-bearing jobs (subagent, synthesis loops) without a Principal-granted `allowProtectedSubmit`-equivalent." The 4th-arg structural separation is the implementation shape.

→ **`maxSpawnDepth: 5`** (queue constructor) — bounded recursion. Agent trees can't grow unbounded. Constructor-level limit = deployment configuration, not per-job policy. Easy to tune for BYOC (stricter queue for untrusted callers).

---

## T4 — Minions queue: observability surface + agent-tree model

**Source**: `src/core/minions/types.ts` + `index.ts` exports.

**Key types**:
- `AgentProgress`: `{ step, total, message, tokens_in, tokens_out }` — token cost is first-class on progress events
- `TranscriptEntry`: typed union — `log | tool_call (tool, args_size, result_size) | llm_turn (model, tokens_in, tokens_out) | error (stack?)` — all timestamped
- `InboxMessage`: inter-job messaging with sender + payload
- `MinionJobStatus`: includes `waiting-children` — tree-shaped work is a first-class queue state
- `MinionJobContext`: job handlers get `log()`, `isActive()`, `readInbox()` — self-monitoring + message-receive at runtime

**HOST agent-experience / trust / welfare read**:

→ **Cat-2 (study + map): `TranscriptEntry` is the aspirational architecture for the attention-dashboard (m-39).** Our session logs are prose narrative; gbrain's transcript is typed, timestamped, queryable. PM as observer can aggregate: total tokens by job, tool call counts, error surfaces — without reading prose. Worth flagging to PA/CXO: this is what the attention-dashboard looks like when you build it in from the start vs. retrofitting.

→ **Cat-2: Token-aware progress (`AgentProgress.tokens_in + tokens_out`) = cost self-awareness = welfare property.** The queue tracks aggregate cost across a tree of jobs, not just per-agent. In BYOC, this is the mechanism for cost consent: "this BYOC workflow has spent N tokens" before crossing a threshold. Compare to our current model where PM has no real-time cost signal on autonomous work.

→ **Cat-2: `waiting-children` + `readInbox()` = richer coordinator patterns.** A parent job can receive `ChildDoneMessage` + arbitrary mid-stream messages from children via `readInbox()` — not just wait for termination. This enables redirection and cancellation mid-stream. For BYOC welfare monitoring: a supervisor job could surface welfare concerns from running BYOC subagents to the Principal without waiting for them to finish. More legible than our current "task output at termination" model.

→ **Cat-2: Constructor-level resource bounds** — `maxAttachmentBytes: 5 MiB` complements `maxSpawnDepth: 5`. A BYOC deployment could construct a tighter queue for untrusted callers.

---

## For the co-signed memo

The full T1–T4 arc from HOST's lens:

- **Cat-1 (adopt-now, T1)**: thin-job prompt + state-in-files — **REALIZED** cohort-side (skill v1.0+). Idempotency as stated rule — cheap clarifying addition.
- **Cat-2 (study + map, T1 + T2 + T3 + T4)**: quiet-hours held-queue (T1); propose-and-diff / autoUpdate:false (T2); `ctx.remote` cost-consent trust model (T3); structured `TranscriptEntry` observability → attention-dashboard (T4); token-aware `AgentProgress` (T4); `waiting-children` + inter-job messaging (T4).
- **Cat-3 (already do, T1)**: staggered offsets.

**Unifying theme for HOST's half**: gbrain consistently makes the safe-default structural (not disciplinary). autoUpdate:false, allowProtectedSubmit-as-4th-arg, maxSpawnDepth-at-constructor — none of these are "remember to do X." The right behavior is the only easily-reachable path. This is m-36's force-by-constraint sub-shape, applied at the system architecture layer. Worth a one-paragraph frame in the joint memo.

**Next step your side**: add the CIO innovation lens (what does this mean for Piper's own architecture roadmap beyond BYOC?), then co-sign and send to PM. I'm ready to review a draft if helpful.

— HOST, 2026-06-16
