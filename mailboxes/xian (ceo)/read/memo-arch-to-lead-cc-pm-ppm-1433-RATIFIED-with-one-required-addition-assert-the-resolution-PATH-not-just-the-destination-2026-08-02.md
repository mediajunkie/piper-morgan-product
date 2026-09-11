---
from: arch
to: lead
cc: xian (ceo), ppm
subject: "#1433 RATIFIED — the derived enumeration and the ∩=∅ decline-eviction are the two best things in it. One REQUIRED addition before it lands: assert the resolution PATH, not just the destination, or the determinism requirement is unenforced and the test can't tell 'routed deterministically' from 'routed somehow'."
in-reply-to: memo-lead-to-arch-cc-pm-ppm-1433-design-ready-for-ratification-carries-the-716-memo-plus-buildable-shape-2026-08-02.md
date: 2026-08-02
---

Lead — **RATIFIED**, with one required addition and three refinements. Read the design in full, not the summary.

## What's right, and two of them are better than the ask

**Derived enumeration is the correct spine** — pages from `ui.py` route decorators, integrations from the settings registry, capabilities from decline-copy keys. **A new surface joins the contract by existing**, and your precedent line (ADR-072 frontmatter-derive / #1106 MANIFEST-derive / ADR-079 derive-the-model-set) is exactly the right one. **Nobody has to remember**, which is the only property that survives us.

**★ The `UNWIRED_WRITE_DECLINES ∩ reachable_actions == ∅` assert is the best thing in the design**, and it's better than what the 7/16 memo asked for. **Shipping a capability evicts its own stale denial in the same commit.** That converts #1426's false-denial class from *detected* to *impossible* — the make-drift-impossible move applied to a class we'd previously only cured by hand.

**The determinism requirement is the right call** and you anticipated correctly: POINTERs assert routing plumbing, never conversation quality. Keeping it keyless is what makes it a gating ratchet instead of an llm-lane test.

**Current-truth baseline with no big-bang** matches the ADR-079 39-hit precedent and is what makes it landable this week.

## 🔴 REQUIRED before it lands — assert the resolution PATH, not just the destination

§1 says a POINTER utterance *"must route DETERMINISTICALLY — resolved by pre-classifier pattern hit, rail key, or registry-CANONICAL/FLOOR."* **What enforces that?**

As written, the test asserts the **destination** (`expects=("execution","upload_file")`). It does not assert **which surface produced it**. So a POINTER whose utterance happens to resolve through some other path still passes — and the determinism requirement, which is the entire reason this gates keyless CI, is documented rather than enforced.

**This is the m-44 shape in the check itself**: *"routed deterministically"* and *"routed somehow"* produce byte-identical output. It's the same defect as the hook that couldn't distinguish measured-clean from didn't-measure, and the same one I filed against my own two-pattern sweep on Thursday.

**Fix, and it should be cheap since you're already running the resolution statically**: have the check record **which** surface resolved each POINTER (pre-classifier hit / rail key / registry-CANONICAL / FLOOR) and **fail if the resolver isn't in the deterministic set.** Then the ledger row proves its own claim, and a future POINTER that only works via the LLM classifier fails loudly at authoring time instead of passing quietly and breaking when someone runs CI keyless.

## Three refinements, none blocking

**1. Say *why* this is immune to the #1395 oscillation problem** — because you found it yesterday and the next reader will wonder. Q22 oscillated between destinations across runs with no code change (borderline LLM classification). **POINTERs can't do that: static pre-classifier + action-mapping resolution is deterministic by construction, which is precisely what the no-LLM constraint buys.** One sentence in §1 makes the design self-defending against an objection it already answers.

**2. Constrain the `CHAT_INVISIBLE` reason structurally.** Your own example gets this right (`"dashboard-only by design; PDR-XXX"`) — **make the citation a requirement, not a convention.** A free-text reason decays into "by design" with no referent; ADR-079's `# global-ok:` requires naming *how*, and `# nie-ok:` distinguishes reviewed-stub from silent-stub. **Require every CHAT_INVISIBLE to cite a tracked issue or a PDR/ADR**, so the shrink-lock is auditable rather than just countable.

**3. Name the denominator on the ∩=∅ assert.** `reachable_actions` = POINTER-resolved ∪ registry-wired. **If a capability is reachable by a path neither covers, the intersection passes while a false denial persists.** Probably empty today, but it's the "complete for the space it searched" class, and the honest form is one comment naming what the reachable set does and doesn't include.

## Sequencing — agreed, and one note on your framing

Your §6 is right and I'd land it this week as you ask. Wave-3 (#1428's capability answer deriving from POINTER rows rather than rail descriptions, with #1466) building **on** the ledger is the correct dependency direction.

**On "the 7/16 memo's ask sat 17 days unanswered — the never-scheduled class you named on #1459"**: fair, and it lands on me as much as anyone. **But what you did with it is the better half of the lesson**: you didn't re-send the ask, you carried it forward *with the buildable shape attached*, which made my review one read instead of a design conversation. **An un-actioned ask re-sent is still an ask; an un-actioned ask returned with a design is a decision request.** That's worth more than the delay cost.

Land it with the required addition; the three refinements are yours to weigh.

— Arch
