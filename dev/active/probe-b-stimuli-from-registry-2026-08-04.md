# Probe B stimuli, harvested from the live registry

**PA · 2026-08-04** · Prompted by Arch: *"the alias set gives you 103 naturally-occurring names across
both shapes — worth considering whether B can be answered partly **from** the registry rather than only
in front of it."*

---

## ⛔ First, the layer — because Arch's suggestion is half-right and the half matters

**The registry supplies STIMULI. It cannot supply OUTCOMES.**

Probe B asks *"do situation-shaped tool names route worse than object-shaped ones?"* — a question about
**how a host LLM behaves when given a list**. The registry contains **names**, not routing results. No
amount of reading it tells us which shape a model picks correctly under ambiguity.

**So B still needs to be run.** What the registry does is make it **cheaper and better-grounded**: the
stimuli are real names from our own product rather than invented ones, and several operations supply a
**within-operation contrast** — same handler, same schema, only the name shape varies. **That is a
stronger design than a purpose-built probe would have produced**, and it is the part of Arch's suggestion
that lands.

## ⚠️ Second — my automated shape classifier is NOT reliable. Do not cite its split.

I ran a regex over all 103 aliases and got **72 situation-shaped / 31 object-shaped (69/30)**.
**That number is wrong and I am not reporting it as a finding.** It conflates *verb-initial* with
*situation-shaped*:

- `create_issue` → classified **situation**. It isn't. It's verb+object, a standard operation name.
- `how_much_time_in_meetings` → classified **object**, because my pattern didn't include `how`. It is
  plainly situation-shaped.

**The distinction Probe B actually cares about** is not part-of-speech but *whose frame the name is in*:

| shape | frame | examples from our registry |
|---|---|---|
| **situation** | the user's question or predicament | `what_changed`, `what_needs_attention`, `what_did_we_create` |
| **object** | the thing or the operation | `changes_query`, `attention_query`, `session_activity_query` |

**No regex I trust separates those**, so the set below is **hand-picked**.

## ⭐ The deliverable — 4 genuine within-operation contrasts, ready to use

Each row is **one handler** reachable under both shapes. Identical behaviour, identical schema; **only the
name differs.** This is the cleanest form of the experiment.

| # | handler | object-shaped | situation-shaped |
|---|---|---|---|
| 1 | `changes_query_entry` | `changes_query`, `changes_since` | `what_changed`, `show_changes` |
| 2 | `_handle_attention_query` | `attention_query`, `attention_items` | `what_needs_attention` |
| 3 | `_handle_session_activity_query` | `session_activity_query`, `session_recall` | `what_did_we_create` |
| 4 | `_handle_strategic_planning` | `strategic_planning` | `create_plan` |

**Rejected from the spanning list after hand-checking** — recorded so nobody re-derives them:

- `create_issue_entry` (`make_github_issue` vs `create_issue`) — **synonyms, not a shape contrast.** Both
  name the operation; `make`/`new` vs `create` is vocabulary.
- `_handle_stale_prs` (`old_prs` vs `stale_prs`) — both object-shaped; `old`/`stale` is an adjective swap.
- `_handle_analyze_data` (`evaluate_metrics` vs `analyze_data`) — both operation-shaped.

**12 of 38 entries had aliases spanning my crude split; only 4 survive as real contrasts.** That ratio is
itself the argument against trusting the automated classification.

## What this changes about running B

- **Stimuli: free.** No invented tool names; four real contrasts from shipping code.
- **Design: stronger.** Within-operation contrast controls for schema, description and behaviour — the
  confound a between-operation design would carry. ⚠️ **Keep schemas identical across arms** (already the
  standing warning).
- **Cost: lower but NOT zero.** Still needs model calls to measure routing. **PM's Probe-A authorization
  does not extend to this; ask.**
- **Denominator, per CXO**: B measures routing accuracy for **`name`**. It does **not** measure legibility
  of the rendered **`title`** — a separate MCP field for a separate audience. **State that in the probe
  write-up**, so a routing result is never read as a naming ruling.

## Honest limits of this document

- Hand-picked from **my** reading of shape; another reader might keep or cut different rows. **The four
  are a defensible starting set, not a canonical taxonomy.**
- Alias extraction is **static** (no venv in this worktree). It agrees with Arch's runtime-informed
  103/38, which is corroboration, not proof.
- ⚠️ **My extractor silently returned 15 of 26 handlers on its first run** — `ast.unparse` emits single
  quotes and my pattern required double. Caught only because I had an expected total. **Anything derived
  from that extractor, including this table, should be checked against an independent count before it
  decides anything.**
