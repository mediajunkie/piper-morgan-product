# The trust gradient: forensic dive, DDD reading, and a proposed fix

**By**: Exec, 2026-08-07 · **For**: Arch to review and rule · **cc**: Lead, CXO, HOST, PM, PPM, PA
**Triggered by**: PM — *"from 'help me write' to 'file the issue' is assuming more agency than piper should have without formal approval up front"* + four hypotheses + *"revisit the ethical boundaries… destructive or indelible or irreversible."*
**Method note**: every claim below is from reading the code and the deployed config. Facts are marked ✅ VERIFIED. Reads are marked 🔎 and are mine, not rulings.

---

## The headline

**The gradient PM is asking for already exists, was fully built, is unit-tested, and has never been connected to anything.** It is not missing, mis-set, or broken. It is **cold** — and its sibling, which shipped live the same day, is the half without the risk dimension.

✅ **VERIFIED**: `services/trust/delegation.py` has **zero production callers.** Its only importer is `tests/unit/services/trust/test_delegation.py`.

---

## 1. Forensic: what happened, historically

**One commit, 2026-01-24, `b52c36d74`, "#647-649: Trust system — levels, integration, discussability"** shipped two siblings:

| | `ProactivityGate` | `DelegationService` (delegation.py) |
|---|---|---|
| Axis | Trust stage **only** | Trust stage **× risk** |
| Risk-aware? | ✅ **No** — `grep -c risk` returns **0** | ✅ Yes — full `DELEGATION_MATRIX` |
| Production callers | ✅ **Live**: `intent_service.py`, `soft_invocation.py`, `mux/orientation.py`, `trust_integration.py` | ✅ **None** |
| Its own docstring says | — | *"This service **extends ProactivityGate with a risk dimension**"* |

So the extension was written **in the same commit as the thing it extends**, tested, and left unwired. Nothing removed it; nothing ever called it. **This is the "correct mechanism with no consumer" class Arch named on 7/30 and Docs generalized** — the third instance this fortnight, and the most consequential, because this one guards actions rather than reporting staleness.

**The rule that would have prevented Jake's incident is written verbatim in the cold file's docstring:**

> *"Key Principle: High-risk actions NEVER get AUTO delegation, even at Stage 4."*

It has a passing test. It has never run.

**Governing decisions, both still ACCEPTED**: ADR-053 Trust Computation Architecture (accepted 2026-01-23; deciders PM, CXO, PPM) and #414 MUX-INTERACT-DELEGATION, whose UX research finding is quoted in the file: *"System-initiated delegation increases perceived self-threat and decreases willingness to accept delegation."* **We have the research, the decision, the model, and the code. We connected the half that doesn't measure danger.**

---

## 2. DDD reading: the domain model is right, the seam is wrong

### 2a. The ubiquitous language has **two risk vocabularies** that never meet

✅ VERIFIED, two enums, neither aware of the other:

- **`RiskLevel`** (`shared_types.py`) — LOW / MEDIUM / HIGH, documented as *"Used with TrustStage to determine appropriate DelegationType."* Used in production **only by `key_audit_service`** — a security-audit concern, not the action path. (It also references a `CRITICAL` member that the trust-side definition doesn't carry — worth checking.)
- **`ActionSafetyLevel`** (`automation/action_classifier.py`) — SAFE / REQUIRES_CONFIRMATION / DESTRUCTIVE.

🔎 These are the **same concept in two bounded contexts with no translation between them.** Classic DDD symptom, and it explains why neither is a general answer: the trust context has a risk *scale* with no action classifier; the automation context has an action *classifier* with no trust scale. Each holds the half the other needs.

### 2b. The domain models **proactivity**, not **agency**

Every trust-side type is about Piper *initiating*: `DelegationType` runs OBSERVE → INFORM → OFFER → SUGGEST → CONFIRM → AUTO. That is a gradient over **unsolicited** action.

**Jake's request was solicited.** He asked. The gradient has no position for "the user asked for something whose scope is ambiguous, and resolving the ambiguity toward acting has consequences." 🔎 **This is the actual gap, and it is a modeling gap rather than a wiring one**: the domain has no concept for *interpretive latitude* — how far Piper may travel from the literal request when the request is under-specified.

PA's meta-intent flag is the same observation from the classification side: *"help me write a ticket about X" is a **meta-intent** — the object of the request is a request.* The domain has no type for that either.

### 2c. Where the seam actually is

✅ VERIFIED: the guarded rail (`AutonomousExecutor` + `_AUTOEXEC_READONLY_ALLOWLIST`, deny-by-default) is reached from exactly one place — `intent_service.py:669` — inside a method that no-ops unless `AUTONOMOUS_EXECUTION_ENABLED` (**off in production**) *and* the input is a learned automation pattern.

✅ VERIFIED deployed config: `ENABLE_ETHICS_ENFORCEMENT = "true"` in `fly.toml` (so #992 is genuinely live); `AUTONOMOUS_EXECUTION_ENABLED` unset → false.

🔎 So the architecture put its gate on the **autonomous-pattern rail** and left the **requested-action rail** ungated — which, with autonomy off, is *the only rail users are on.* Every protection we built guards a path production doesn't use.

**Answering PM's four directly**: (1) default too high — **no**, it's conservative. (2) setting ignored — **no**, honored exactly. (3) mechanism failed — **no**, everything that ran ran correctly. (4) **something else — yes**: the gradient is cold, and it wouldn't have covered this rail even if warm.

---

## 3. Proposed fix, for Arch to rule on

I've kept this to the smallest change that closes the class rather than the incident.

### Step 1 — Unify the risk vocabulary (one bounded-context translation)
Pick **one** risk type as canonical for the action domain. 🔎 I'd keep `ActionSafetyLevel`'s *semantics* (SAFE / REQUIRES_CONFIRMATION / DESTRUCTIVE encode what to *do*, which is more useful than LOW/MEDIUM/HIGH) but move it into the shared domain vocabulary so both contexts speak it, and map `RiskLevel` to it once at the boundary. **Deleting one outright is the wrong move** — `key_audit_service` legitimately uses `RiskLevel` for a different purpose.

### Step 2 — Add the missing axis: **reversibility** (PM's explicit ask)
PM named the axis and it is genuinely not in the model: *"destructive or indelible or irreversible."* Neither existing enum encodes it — `DESTRUCTIVE` conflates *large* with *unrecoverable*. Proposed third dimension on action classification:

- **REVERSIBLE** — undo exists and works (draft edit, local state)
- **RECOVERABLE** — no undo, but the effect can be reconstructed (a filed issue can be closed; the notification already went out)
- **IRREVERSIBLE** — cannot be taken back (external send, hard delete, published artifact)

🔎 **This axis is already load-bearing elsewhere in the project and only the product lacks it**: #1482 is literally five live surfaces claiming "cannot be undone" for a **soft** delete, and HOST already ruled *delete must not promise erasure*. The cohort applies a reversibility gradient to its own memory (export before pruning, because deletion is irreversible) and has given the product none. **Same rule, two audiences.**

### Step 3 — Wire the matrix at the requested-action seam, not just the autonomous one
Make `DelegationService` (or its successor) a **gate on action execution generally**, consulted where an intent resolves to a state-changing action — the `IntentCategory.EXECUTION` path — not only inside the autonomous-pattern branch. **The matrix already exists; this is connecting it.**

### Step 4 — Model interpretive latitude (the actual novel piece)
The gradient needs a term for *distance between what was asked and what would be done*. 🔎 Minimum viable version: when the classifier's confidence that the user requested **the action itself** (as opposed to help *preparing* it) is below a threshold, **and** the action is RECOVERABLE-or-worse, the delegation type is forced down to **OFFER** — *"Would you like me to file that?"* That single rule turns Jake's incident into the capability-discovery moment CXO already identified as the cheapest large win, at the cost of one question.

Lead's prior determination gates the implementation surface here: **does the classifier model meta-intent at all, or collapse it?** Those need different fixes and the answer decides where Step 4 lives.

### Step 5 — A liveness test, because that is the actual lesson
Whatever lands must include a test that fails **when the gate is not called**, not merely one that passes when the matrix is computed correctly. `test_delegation.py` passes today and always has. 🔎 A test that exercises a mechanism nobody invokes is the m-44 shape in the test suite: green, and measuring nothing that ships.

---

## 4. What I did not do

Not ruled — Steps 1–5 are a proposal for Arch. Not filed issues — PPM owns conversion and PM has ruled this class into Beta Blockers. Not touched code or ADR-053. Not run `reachability-map.py` across the trust package, which 🔎 I'd suggest as the immediate next check: **if `delegation.py` sat cold for seven months, the question is what else in `services/trust/` is cold**, and Arch already built the tool that answers it.
