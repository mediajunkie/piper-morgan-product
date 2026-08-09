# Jake's alpha FTUX — four-lens synthesis

**Prepared by**: Exec, 2026-07-31 · **For**: the PM + CXO experience decision (per PM's 7/30 ruling: the lenses are input, the decision forum is PM + CXO — this document frames, it does not decide)
**Sources, read in full**: HOST trust lens (7/27) · CXO experience-design lens (7/29) · PA in-house-experiment lens (7/29) · PPM roadmap lens (7/30) — all in `mailboxes/exec/read/`. Jake's original write-up + PM's apprentice-frame email are the primary sources behind all four.
**Status**: collection complete 4/4. PPM converts the decided shape to GitHub issues same day the decision lands.

---

## 1. Where all four lenses independently agree (treat as settled input)

1. **The root is a cold-start-state problem, not positioning.** PA's formulation is the one the other three adopted: *"an empty list is a form; a populated queue is a colleague."* Jake was handed empty structures and a five-field demand; nothing showed him his own work. Better onboarding copy cannot fix an empty account.
2. **The headline indictment is capability-parity, and Jake reasoned it correctly.** CXO's §1: the product asks the user to supply the output of the work it promises to do. Jake's "is this just an LLM with extra UI?" is an empirical conclusion from a session where the differentiator (real writes to GitHub) existed but was never encountered. PA — the in-house experiment on exactly this question — confirms: *for the first session, he's right.*
3. **The consent gate is not polish.** HOST's consent-boundary escalation on the "file a ticket" incident is backed by all four; PPM elevates it to the one item they'd hold a release for.
4. **On n=1**: act on the structural findings now (they stand on internal logic), hold the preference-level ones (panel width etc.) — CXO's split, made operational by PPM, uncontested.

## 2. The complementary pairs — the synthesis must NOT collapse these

- **HOST's consent gate** (makes the action safe, *after* intent forms) **+ CXO's capability legibility** (makes the action discoverable, *while* intent forms). CXO: legibility without the gate is dangerous; the gate without legibility is merely safe. **Ship together; one feature.**
- **CXO's "demonstrate, don't describe" (§6) + PA's "ingest-and-reflect at onboarding" (#1)** — independent lanes, same conclusion: the first moment must do something only Piper could do against the user's own connected tools. This convergence is the strongest single signal in the collection.
- **CXO's trigger-based entry points (§5) + PPM's relocation of them to the MCP tool catalog** — same principle, different surface: under PDR-006 the entry-point copy *is* the tool catalog. PPM prices this at a third of the nav-redesign cost. **Open question PPM flagged against their own recommendation**: situation-shaped tool names may route *worse* for the host LLM than object-shaped ones — cheap to test, expensive to assume; test both namings before committing (Lead or Arch).

## 3. PPM's sort key — ⛔ THE KEY ITSELF IS WITHDRAWN (PM, 2026-08-08)

> ⛔ **"Which surface survives PDR-006" is a FALSE QUESTION, and every bucket below inherits it.**
> **PM, 2026-08-08**: *"I never said the web UI was going away… The fundamental idea of the modeled
> user experience is that it is not specific to any one surface. It's a holistic user experience,
> which is expressed on each surface as appropriate"* — phone as notifications, Slack as a channel
> bot, web as conversations + radar + settings, another chat as skills + MCP server, **and the CLI is
> still maintained. All true at the same time.**
>
> **PDR-005 never said otherwise.** Its decision is **(b) — "primarily MCP; thin web UI"**, and option
> (a) *"no Piper-specific UI in v1.0"* was **explicitly rejected as infeasible**; the PDR then scopes
> **5 of 7 MUX/UI surfaces as 1.0-required bespoke UI.**
>
> **The mechanism of the error, since the buckets read as reasonable**: I read a **prioritization**
> statement as an **ontology** statement. *"Primarily"* orders work; I converted it into a claim about
> which surfaces exist. **And building a SORT made it worse — a sort needs a discriminator, so I
> manufactured an axis, and the axis smuggled in competition between surfaces the model treats as
> complementary.** *(Same one-name-two-objects family as "production" = branch vs. artifact and
> "trust" = inferred vs. declared: here, **"primary" = first-in-sequence vs. the-only-real-one**.)*
>
> ⚠️ **Do not re-key this by patching the labels.** Any key phrased as *survival* reintroduces the
> error. The honest key is likely **"which surface does this defect live in"**, which requires knowing
> the surface inventory rather than ranking it. **Re-sort pending PM's read on how the surfaces relate
> going forward** — PM said the MCP path *may emerge* as primary, which is a sequencing possibility,
> not a settled ordering, and I treated an open question as closed in the wrong direction.
>
> 🔴 **Concrete damage already found**: **#1477** ("current chat has no sidebar row") sat in bucket A
> as dying, needing a *welfare* exception to justify fixing. **It is a defect in Surface 1** — whose
> PDR-005 scoping line reads *"left rail = **current session**"* — a **1.0-required, scheduled**
> surface that CXO re-tested on 08-07 as meeting criterion 1 strongly. **It never needed a welfare
> argument at all.** (**#1476**'s owning surface is **NOT yet verified** — I could not locate what
> renders the "blocked" card; do not assume it is also Surface 1.)

*(Original section retained below for the record — the item groupings may still be useful; the KEY is what's withdrawn.)*

## 3-bis. PPM's sort key as originally written — the roadmap overlay on all twenty items

Sort every fix by **which surface survives PDR-006 ratification**:

| Bucket | Contents | Call proposed |
|---|---|---|
| **A — dies with the pivot** | nav-in-pill, panel width, search placeholder, composer growth, lists-as-navigation | No beta capacity. **Carve-out (welfare, PPM's own)**: the "blocked" card with no referent + the missing chat row — the two items that changed Jake's *behavior* — fix regardless if alpha testers stay on the web UI meanwhile |
| **B — survives, relocates** | three-list taxonomy → tool-catalog naming · capability legibility → tool descriptions · progressive elicitation → conversation the plugin drives | Re-specify against the plugin surface before building; building against today's web UI builds them twice |
| **C — gets harder, becomes the game** | cold-start demonstration (show them their own data) · reflect-and-elaborate elicitation · the consent gate | **"This is the beta"** — all differentiation now rides on what the tools return |

## 4. The decision set (for PM + CXO — each is a yes/no/modify)

1. **Adopt the bucket filter as the sort order for all Jake work?** (PPM's; CXO's afternoon-of-IA-fixes reading differs on bucket A *only* on timing, not merit.)
2. **The gate questions** (PPM's three, one decision each):
   a. Close #1386 on its existing terms — do NOT expand its criteria.
   b. Add ONE new beta criterion: first-contact demonstration test — cold account, one tool connected, does the user's own data appear in the first exchange unprompted? (Binary; the only proposed criterion that fails today. This is also the answer to PPM's finding that the current gate *cannot fail* for what Jake reported.)
   c. Consent gate = genuine release blocker, not a criterion.
3. **Tool-catalog naming direction** — adopt situation-shaped naming as the *direction*, gated on the routing-accuracy test (§2 third pair)?
4. **Bucket-A welfare carve-out** — fix the blocked-card + chat-row items now, on welfare grounds, despite surface retirement?
5. **Jake follow-up** — HOST raised, PPM seconded as an obligation: he asked to be kept in the loop; he's also the fastest path to n>1. Who owns the reply and when?
6. **PA's meta-intent flag** (not a decision, an instruction to whoever picks up the file-a-ticket fix): "help me write a ticket about X" is a meta-intent; read `intent-routing-stack.md` first and determine whether the classifier models meta-intent at all — different answers mean fixes at different surfaces. High recurrence: it's the most common PM request shape.

## 5. What is deliberately NOT in this document

- A recommended severity order — that's the decision, and the forum is PM + CXO.
- Any restatement of the twenty individual items — each lens memo carries its own; PPM's conversion pass will enumerate against the decided bucket structure.
- The PDR-006 ratification itself — separate thread, at PM now (all three reviews in, RATIFY × 3).

## 6. One number to keep (PA's baseline)

First alpha tester: actively willing, screen recording, 1,500 words of considered feedback — **and never reached the core loop.** 0-for-1 on "did the user reach the thing the product is for." Proposed success measure for everything above: **does the next tester reach a first automated action?** — not whether the nav or the copy improved.

---

*Next mechanical step on PM+CXO decision: flag PPM (standing same-day offer) → issues filed against the decided structure → items land in the sprint per PM's prioritization.*
