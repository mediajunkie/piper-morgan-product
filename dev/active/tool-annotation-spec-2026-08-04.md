# Tool Annotation Spec — MCP `readOnlyHint` / `destructiveHint` / `openWorldHint`

**Author**: PA · **2026-08-04** · **For**: Lead (implementation), Arch (condition 2 owner), PPM (catalog opinionation)
**Tracks**: distribution plan item **(2)**, Phase 0 · **Governed by**: PDR-006 (RATIFIED 2026-07-31)

---

> ✅ **UNBLOCKED 2026-08-04 16:1x — Arch answered both asks. `readOnly` ≠ `resource`; nothing leaves the
> catalog; build ONCE. A defaultless registry field satisfies condition 2. See §9.**

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
| `readOnlyHint` | ⚠️ *unverified* | **May skip the user-confirmation prompt.** This is the load-bearing one. |
| `destructiveHint` | ⚠️ *unverified* | Strengthens the confirmation; may add a distinct warning |
| `openWorldHint` | ⚠️ *unverified* | Signals the tool touches systems outside our control |

⚠️ **The defaults column is marked unverified deliberately.** I originally wrote concrete values here from
recollection. I checked the published spec page for tools (2025-06-18) — **it documents the `annotations`
field's existence but does not enumerate the hint defaults**, and the schema page I fetched was truncated
before `ToolAnnotations`. **Rather than restate remembered values in a spec, they stay marked.**

✅ **And our design makes them moot**: §6 requires us to emit every hint **explicitly** and to refuse to
emit a tool whose effect can't be resolved. **A default only ever applies to a field you didn't set.**

🔴 **One thing the spec DOES say, verbatim, and it belongs here**:

> *"For trust & safety and security, clients **MUST** consider tool annotations to be **untrusted** unless
> they come from trusted servers."*

**So annotations are advisory to the client, exactly like our own pre-commit hooks are advisory to us.**
They are a declaration of intent, not an enforcement boundary. Getting them right matters for the client
that *does* trust us; it is not a substitute for server-side authorization.

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

Rows marked ✅ **VERIFIED** were confirmed by reading the handler. **Unmarked rows are still inferred from
entry names and must be confirmed by whoever adds the field** — recorded as a starting point rather than
implying an audit I did not do. ⚠️ **And this table covers 12 of the registry's 38 entries** (see §4b);
the other 26 arrive via the cohort writers and are unexamined.

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
| `document_update` | ✅ **`WRITE`** | ✅ **`True`** | **VERIFIED** — `run_update_document_workflow` → `_handle_update_document_notion`. **Writes to Notion.** |
| `generate_content` | ✅ **`READ`** | ✅ | **VERIFIED** — status-report / readme-section / issue-template *generation*; `_generate_status_report` reads the default repo and returns content. **Produces, does not persist.** |
| `prioritization` | ✅ **`READ`** | ✅ **`False`** | **VERIFIED — and my "sleeper" flag was WRONG.** See §4a. |
| `meeting` | ❓ | ❓ | offer-only (`action_triggered=False`) |

### 4b. 🔴 The registry is keyed by ALIAS, not by tool — a naive derivation emits 31 tools for 12 operations

⛔ **CORRECTED — my first measurement covered under a third of the registry.** I reported **31 keys → 12
entries**. That is right *for the literal dict* and **the literal dict is one of FIVE writers to
`_default_entries`** (Arch caught it; three `*_COHORT` dicts and two local `(entry, aliases)` lists also
write). **The real numbers, which I then re-derived independently by a different method — union of all
five writers with overwrite semantics, mirroring runtime — agreeing exactly with Arch's:**

| | aliases | entries |
|---|---|---|
| literal dict *(what I first measured)* | 31 | 12 |
| **REGISTRY (all five writers)** | **103** | **38** |

**≈2.71 names per operation — my ratio essentially unchanged across 3× the surface.** So the naive
derivation ships **103 tools for 38 operations**, not 31 for 12. **The argument got stronger, not weaker.**

⚠️ **Arch's warning, which belongs in the derivation code**: they found this only because their first two
AST passes *disagreed with each other* — the first returned nothing (the dict is an `AnnAssign` inside a
function; they walked `ast.Assign`). **Any audit reading only the literal dict covers under a third of the
registry and looks complete while doing it. Count from the assembled dict at runtime, not from any one
literal.** *(My own count is static, so it carries this caveat too — I could not run the app's importer
from this worktree, which has no venv. It agrees with Arch's runtime-informed figure, which is corroboration,
not proof.)*

Several entries are reachable under many names:

| entry | aliases |
|---|---|
| `create_issue_entry` | **6** |
| `_query_cohort:2` | **6** |
| `_READ_QUERY_COHORT:_handle_stale_prs` | **5** |
| `changes_query_entry` | 4 (`changes_query`, `what_changed`, `show_changes`, `changes_since`) |
| `update_issue_entry` | 4 |
| `document_update_entry`, `comment_issue_entry` | 3 each |
| `close_issue` / `reopen_issue` / `prioritization` / `generate_content` | 2 each |

**Condition 2 says derive the catalog from the registry. Derived naively — one tool per key — the catalog
ships 103 tools for 38 operations, including six ways to file the same issue.**

⭐ **This is not cosmetic, and it is the finding I'd carry forward even if everything else here is rebuilt.**
The aliases exist because they are **classifier surface** — natural-language phrasings the intent
classifier maps to one handler. **A host LLM's tool list is not a classifier surface.** Handing Claude or
GPT four differently-named tools that do the same thing makes routing *worse*, not more forgiving: the
model must now disambiguate between synonyms that carry no real distinction.

**Derivation rule: the catalog MUST be keyed by entry identity, deduped across aliases** — one tool per
`WorkflowEntry` object, with a single canonical name. **Aliases are input-side vocabulary and must not
leak into the tool list.**

⚠️ **And this is exactly Probe B's question arriving early**, from a direction I didn't expect. Probe B
asks whether *situation-shaped* tool names route worse than *object-shaped* ones. The alias set is a
natural experiment sitting in the codebase: `what_changed` / `show_changes` / `changes_since` are
situation-shaped; `changes_query` is object-shaped. **Whichever way B lands, the answer decides which of
the 12 canonical names we pick** — so B is now upstream of the catalog, not merely adjacent to it.

### 4a. ⚠️ The one row I checked by hand refuted the guess I made from its name

I flagged `prioritization` as *"the sleeper — if it writes board state it can move many items at once."*
**I read it. It writes nothing.** `_handle_prioritization` (`intent_service.py:10479`) is pure
computation: validate → extract items **from `intent.context`** → score (Impact/Urgency/Effort, RICE, or
Eisenhower) → rank → format → return. **No repository call, no persistence, no external write.** It does
not even read stored state — it scores what the caller supplied.

**Worth recording rather than quietly fixing the row**, because it is this spec's own caveat coming true
on its most confident line: the name `prioritization` suggested a bulk board mutation, and I gave it the
scariest reading available. **The guess and the fact pointed opposite ways.**

🔴 **And note the direction — it is the *reassuring* one, which is why it deserves flagging.** My error
would have over-restricted a harmless tool: needless confirmation prompts, not an unconfirmed write. That
is the cheap direction, **and it is the direction a cautious reviewer's errors will always take.** The
expensive direction is the row nobody found frightening. **Every remaining ❓ and every unread handler in
this table is a candidate for the error that runs the other way** — so the §6 enforcement (no default,
refuse to emit) is not belt-and-braces, it is the actual control.

## 5. ✅ RESOLVED — `close_issue` is `WRITE` (PPM ruling, 2026-08-04)

I surfaced this rather than picking one. **PPM ruled, and supplied a discriminator that decides the next
twenty cases rather than just this one:**

> **DESTRUCTIVE = the operation destroys information that cannot be recovered through the product.**

By that test `close_issue` is plainly `WRITE`: the issue, body, comments and timeline all survive, and
`reopen_issue` restores the state completely. **A `delete_*` is destructive; a state transition with an
inverse is not.** Adopted — and it resolves the ❓ rows in §4 by rule rather than case-by-case.

**Why the social concern does NOT go in `destructiveHint`** (PPM, and the argument is the load-bearing
part): closing notifies watchers, and so does `comment`, `add_label`, `assign` — **conflate the two and
every social write becomes DESTRUCTIVE, the flag stops discriminating, and a host LLM reading it learns
nothing. An annotation that marks everything is the same defect as one that marks nothing.**

**Two distinct properties, two homes:**

| property | question | home |
|---|---|---|
| **Destructiveness** | recoverable through the product? | `destructiveHint` |
| **Consequence** | visible to *other people*, outside the user's control? | **HOST's consent gate** (already a release blocker) |

The consequence is real — *"you closed my issue"* already happened and no `reopen_issue` unfires the
notification. It belongs in the **tool description** and the consent gate, not in a boolean that means
something else.

### 5a. ⭐ How the description must be written (CXO addendum, adopted as a catalog-wide rule)

My proposed string — *"closes the issue — visible to watchers; reversible with reopen"* — **puts its
safety clause in the position a recomposing client LLM drops.** A tool description is not rendered; it is
**input to a model that paraphrases before the user sees anything** (this is #1463's finding).

🔴 **And the asymmetry is the dangerous part**: *"reversible with reopen"* is reassuring, so a summarizer
keeping one trailing clause likely keeps **that** one — **preserving the reassurance and dropping the
exposure.** Same direction as every other error in this cycle.

**Adopted string:**

> *"Closes an issue in the user's tracker, notifying everyone watching it. `reopen_issue` restores the
> issue state — it does not unsend the notification."*

**The general rule, applied catalog-wide:** *the irreversible part of a reversible operation goes in the
same sentence as the reversibility claim*, and the scope goes **inside the primary claim, never as a
trailing caveat** — a summarizer cannot drop the notification without dropping the verb.

⚠️ **`prioritization` remains the sleeper.** If it writes board state it can move many items at once — a
bulk write auto-approved because nobody set the field is the concrete form of the §2 risk. **Still needs
a handler read; not resolved by PPM's rule.**

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
- ✅ **PPM — ANSWERED same day.** `close_issue` = `WRITE`; discriminator adopted into §5. `prioritization`
  still open (needs a handler read, not a rule).
- ✅ **CXO — ANSWERED same day**, unasked, in their lane. Description-string rule adopted into §5a.

## 9. ✅ STATUS 2026-08-04 16:xx — UNBLOCKED. Arch answered both asks; build once.

**Both answers came back, and both went my way. Recording the reasoning, not just the verdicts.**

### 9a. Condition 3 does NOT reach the workflow registry — nothing leaves the catalog

Arch: *"`changes_query`, `get_default_repo`, `generate_content` and `prioritization` all stay tools. So:
no double build. Make the `effect` change once, against the catalog you have."*

⭐ **The discriminator, which is the reusable part** — condition 3's scope is in its own first two words
(*"**Colleague-model access** splits…"*) and its tail (*"so serving context does not require the model to
decide to call something"*). **That describes context you want served unprompted: stable, addressable,
host-anticipatable. It does not describe an operation whose parameters the model must formulate.**

**`readOnly` ≠ `resource`. Two orthogonal axes:**

| axis | question |
|---|---|
| **resource vs tool** | addressable, host-anticipatable context — or an invoked operation? |
| **`readOnlyHint`** | does invoking it mutate state? |

**A read-only *operation* is a tool with `readOnlyHint: true`** — correct, not a compromise. `prioritization`
settles it: it writes nothing **and** scores caller-supplied input, so **there is nothing to address until
the model supplies it.** Read-only and un-resource-able at once — the two axes coming apart in one entry.

*(One honest edge, Arch's: `get_default_repo` genuinely is a stable addressable user fact and a legitimate
**future** resource candidate — but via the colleague-model bundle, not this registry. Gates nothing now.)*

### 9b. A registry field satisfies condition 2 — and "defaultless" is the half that matters

Arch: *"Do not let the defaultless part get softened in review — it's the whole thing."* **`WorkflowEntry`
has four of its five fields already defaulted**, so a defaulted `effect` would let every future entry
silently inherit a value nobody chose — **hand-maintenance wearing derivation's clothes**, since the
derived catalog would then derive from an unstated assumption. **The break at ~15 sites is the feature.**

### 9c. ✅ CXO's two-audience question — RESOLVED from the protocol, and it dissolves rather than trades off

CXO flagged that Probe B measures *routing*, while a tool name may also be a **rendered label** for the
user — and honestly marked it unverified: *"I have NOT verified how this specific host renders tool names."*

**Checked the MCP spec (2025-06-18) rather than reasoning about it. A Tool carries BOTH:**

> * `name`: Unique identifier for the tool
> * `title`: **Optional human-readable name of the tool for display purposes.**

**So the protocol already separates the two audiences.** `name` is the model-facing identifier Probe B is
about; `title` is the human-facing label. **They are different fields and can be optimised independently
— there is no tradeoff to resolve, and B's winner cannot be "the wrong pick for the other audience"
because it doesn't decide that field.**

**Consequence for the spec**: `title` moves from *"§7, not settled here, CXO's lane"* to **a required
output of the catalog, authored for legibility** — and CXO's lane is the right home for its copy.
**Adopting CXO's ask anyway**: Probe B should still state its denominator (*"measures routing accuracy for
`name`; does not measure legibility of the rendered `title`"*), because that sentence is what stops the
result being read as a naming ruling. **It costs nothing and it is now demonstrably accurate.**

### 9d. Still open

- **Lead** — the ~15-site breaking change (§3). Arch has explicitly backed defaultless; that was the part
  most likely to be softened in review.
- **26 of 38 entries unclassified** — everything arriving via the cohort writers (§4b). Mechanical, and
  the defaultless field forces each to be stated anyway.
- **`meeting`** — offer-only; unread.
