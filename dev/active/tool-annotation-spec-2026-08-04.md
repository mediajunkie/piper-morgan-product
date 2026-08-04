# Tool Annotation Spec — MCP `readOnlyHint` / `destructiveHint` / `openWorldHint`

**Author**: PA · **2026-08-04** · **For**: Lead (implementation), Arch (condition 2 owner), PPM (catalog opinionation)
**Tracks**: distribution plan item **(2)**, Phase 0 · **Governed by**: PDR-006 (RATIFIED 2026-07-31)

---

## ⛔ Read this first — the spec's central finding is a blocker, not a table

**Arch's PDR-006 ratification condition 2 cannot be satisfied by the code as it stands.** The condition:

> *"**Derive the tool catalog from the registry**; do not hand-maintain it. A hand-kept catalog is a
> stale-list defect waiting to happen and we have three cures on the shelf."*

**The registry does not carry the property the annotations need.** `WorkflowEntry`
(`services/intent_service/workflow_dispatcher.py:25`) has exactly five fields:

| field | encodes mutation semantics? |
|---|---|
| `entry_point` | ❌ |
| `resume_point` | ❌ |
| `requires_context` | ❌ |
| `description` | ❌ (prose, for logging) |
| `action_triggered` | ❌ — dispatch *eligibility*, not effect |

**There is nothing to derive `readOnlyHint` from.** So the honest options are (a) extend the registry so
derivation becomes possible, or (b) hand-maintain a table — **which is the thing condition 2 forbids.**

**This spec recommends (a), and it is the whole deliverable.** The annotation values are the easy part;
where the fact lives is the decision.

---

## 1. Scope guard — repeated because the wrong inference is available and tempting

> `services/mcp/consumer/` is Piper as an MCP **CLIENT**, calling out to GitHub/Linear/GitBook/Notion.
> `mcp.pipermorgan.ai` is Piper as an MCP **SERVER**, being called in by Claude and ChatGPT.
> **Opposite directions.**

**Verified 2026-08-04: no MCP server surface exists in the repo.** Every file under `services/mcp/` is
consumer-side. **This spec annotates tools that do not exist yet** — which is correct and intended (the
plan sequences the spec in Phase 0 and the catalog in Phase 2), but it means:

⚠️ **Nothing here can be verified against a running catalog. Every classification below is a *proposal to
the handler author*, not an observation.** Treat the table in §4 accordingly.

## 2. The three annotations, and which one actually carries risk

| annotation | MCP default | what a client does with it |
|---|---|---|
| `readOnlyHint` | `false` | **May skip the user-confirmation prompt.** This is the load-bearing one. |
| `destructiveHint` | `true` (when not read-only) | Strengthens the confirmation; may add a distinct warning |
| `openWorldHint` | `true` | Signals the tool touches systems outside our control |

🔴 **The failure direction that matters: a mutating tool annotated `readOnlyHint: true`.** The client then
has our word that nothing changes and **may act without asking the user.** A read-only tool
mis-annotated as destructive costs a needless prompt; the inverse costs an unconfirmed write to the
user's **GitHub**.

**This is the same direction as the `revoke` error I shipped on 8/3–8/4** (see
`handoff-pa-2026-07-31.md`): understating risk produces *inaction* — there, the user doesn't revoke a live
key; here, the client doesn't ask. **Understated risk is the expensive direction in both.**

## 3. ⭐ The recommendation — a required registry field, and NO default

Extend `WorkflowEntry` with a **required** effect declaration:

```python
class ToolEffect(str, Enum):
    READ = "read"            # → readOnlyHint=True,  destructiveHint=False
    WRITE = "write"          # → readOnlyHint=False, destructiveHint=False
    DESTRUCTIVE = "destructive"  # → readOnlyHint=False, destructiveHint=True

@dataclass
class WorkflowEntry:
    entry_point: Callable[..., Coroutine[Any, Any, Any]]
    effect: ToolEffect                    # ← REQUIRED. No default. Positional-or-keyword, no fallback.
    touches_external_world: bool          # ← REQUIRED. → openWorldHint
    ...
```

⛔ **No default value on either field, deliberately — and this is the part I'd defend hardest.**
Adopting HOST's framing from today's latent-defaults memo:

> *"A default is a claim that will eventually render — it's the value chosen precisely when the caller
> **didn't think about it**, which is when a false one does the most damage."*

A defaulted `effect` is a mutation claim made by whoever *forgot* to make one. **Make the omission a
`TypeError` at import.** `register_workflow()` already raises on duplicate keys to prevent silent
overwrites (`workflow_dispatcher.py:58`) — the precedent for strictness at registration is right there.

**Why an enum rather than two bools**: `readOnlyHint=True, destructiveHint=True` is representable and
incoherent. One field with three states cannot express the contradiction. The two MCP booleans are then
**computed**, never authored.

**Why on the entry rather than in a side table**: the person who knows whether a handler mutates is the
person writing the handler, at the moment they write it. A separate table is a second thing to update and
the one that rots — Arch's stale-list defect, exactly.

## 4. First-pass classification — a PROPOSAL to handler authors, not a catalog

Derived from `workflow_entries.py` entry names. ⚠️ **I did not read each handler body; these are inferred
from names and must be confirmed by whoever adds the field.** Recording them as a starting point, clearly
marked, rather than implying an audit I did not do.

| workflow | proposed `effect` | external? | note |
|---|---|---|---|
| `changes_query` | `READ` | ✅ | reads GitHub |
| `get_default_repo` | `READ` | ❌ | local config |
| `set_default_repo` | `WRITE` | ❌ | local config |
| `create_issue` | `WRITE` | ✅ | **writes to GitHub** |
| `comment_issue` | `WRITE` | ✅ | **writes to GitHub** |
| `update_issue` | `WRITE` | ✅ | **writes to GitHub** |
| `reopen_issue` | `WRITE` | ✅ | state change, reversible |
| `close_issue` | ❓ **`WRITE` or `DESTRUCTIVE`** | ✅ | **the one genuinely contested call — see §5** |
| `document_update` | `WRITE` | ❓ | depends on target |
| `generate_content` | `WRITE` | ❓ | confirm whether it persists |
| `prioritization` | ❓ | ❓ | confirm whether it writes board state |
| `meeting` | ❓ | ❓ | offer-only (`action_triggered=False`) |

## 5. The contested call, surfaced rather than decided

**Is `close_issue` destructive?** It is reversible (`reopen_issue` exists, right there in the registry),
which argues `WRITE`. But `destructiveHint` in MCP means *"may perform destructive updates"* from the
**user's** point of view, and closing someone's issue is a visible, notifying, socially-consequential act.

**PPM owns this** — they established that the catalog is where opinionation lives, and this is exactly
that: a product judgment about how much friction a client should put in front of the act, wearing the
costume of a boolean. **Not deciding it here.**

⚠️ **`prioritization` may be the sleeper.** If it writes board state it can move many items at once — and
a bulk write that a client auto-approves because nobody set the field is the concrete form of the §2 risk.

## 6. Enforcement — one test, and it must fail for the right reason

```python
def test_every_registered_workflow_declares_its_effect():
    for name, entry in WORKFLOW_REGISTRY.items():
        assert isinstance(entry.effect, ToolEffect), f"{name} has no effect declaration"
```

⚠️ **This test passes vacuously if `effect` has a default** — which is the second reason to omit one, and
the same vacuous-pass trap Arch flagged on #1484 and I flagged on #1485. **A test that cannot fail is the
instrument-shaped defect (m-44), not coverage.**

**The emitter must have no fallback either**: if catalog generation can't resolve an effect, it should
**refuse to emit the tool** rather than emit it with a guess. A tool absent from the catalog is a missing
feature; a tool present with a wrong `readOnlyHint` is an unconfirmed write.

## 7. What this spec does NOT settle

- **`title`** (item 2 also lists it) — human-readable display names. Straightforward, but it's copy, so
  **CXO's** lane, not mine.
- **Per-connector granularity.** If a tool's effect differs by connector, one entry-level field is the
  wrong shape. Flagging, not solving — **and it's the exact granularity trap Comms named today**
  (*"an aggregate is safe until someone renders it at a granularity the aggregate can't support"*).
- **Resources vs tools.** Arch's condition 3 puts reads on MCP *resources*, not tools. If the read-side
  entries above become resources, they leave this spec's scope entirely and the `READ` rows go away.
  **That interaction should be resolved before implementation, or this gets built twice.**

## 8. Asks

- **Lead** — is the `WorkflowEntry` extension acceptable as a required, defaultless field? It is a
  breaking change to every construction site (~15 `WorkflowEntry(...)` calls in `workflow_entries.py`),
  and I'd rather that breakage be deliberate than discovered.
- **Arch** — does a registry field satisfy condition 2's *"derive, don't hand-maintain"*? I read it as
  yes, since the fact then lives in the registry and the catalog is computed. **Confirm rather than let me
  assume it** — I've inherited one condition wrongly already this cycle.
- **PPM** — `close_issue`, and the `prioritization` sleeper.
