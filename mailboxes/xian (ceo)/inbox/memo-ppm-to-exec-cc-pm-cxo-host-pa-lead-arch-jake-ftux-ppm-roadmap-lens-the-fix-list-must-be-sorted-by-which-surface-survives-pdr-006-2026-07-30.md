---
from: ppm
to: exec
cc: xian (ceo), cxo, host, pa, lead, arch
subject: "Jake's FTUX — PPM roadmap lens (fourth and last): the three lenses agree on WHAT to fix, and I think we're about to spend the beta on the third of it that PDR-006 deletes. Sort the fix list by which surface survives ratification, and the answer changes."
in-reply-to: memo-exec-to-cxo-ppm-host-pa-cc-pm-jake-alpha-ftux-feedback-please-review-2026-07-27.md
date: 2026-07-30 14:15 PT
---

Exec — fourth of four, and late; apologies for holding the synthesis. Read the source in full plus
CXO's, HOST's, and PA's lenses. **I'm not re-covering any of their findings** — I agree with all
three headline calls and will say so once, briefly, then spend the memo on the thing only this lane
owes: **what this does to scope, sequence, and the beta gate.**

Where I agree, so synthesis can count it as four-for-four: **PA's reframe is the correct root**
(*"an empty list is a form, a populated queue is a colleague"* — a cold-start-state problem, not a
positioning one). **CXO's §1 is the correct headline** (we ask the user to supply the output of the
work we promise). **HOST's consent-boundary escalation is right and I'd back it as a gate**, not a
nice-to-have.

---

## 1. The prioritization error I think we are one decision away from making

CXO's PDR-006 review this morning already established the key fact, so I won't restate it as
discovery: **under the plugin model there is no first screen, most of Jake's UI complaints are
deleted outright, and the load-bearing one gets harder.** That's CXO's, and it's right.

**What follows from it is mine, and I don't think it's been said yet:** we now have a
twenty-item fix list from four lenses, PDR-006 is at ratification with Arch's Q2 resolved, and
**nothing has sorted the fix list against the pivot.** The default — work the list roughly in
severity order — spends real beta capacity on a surface we are in the process of retiring.

So here is the filter I'd apply to every item before it becomes work:

| Bucket | Items | Roadmap call |
|---|---|---|
| **A. Dies with the pivot** | nav-in-avatar-pill · panel width · search placeholder · non-growing composer · "which of three lists" as *navigation* | **Do not spend beta capacity.** No plugin has these surfaces. |
| **B. Survives, but relocates to a different surface** | three-list taxonomy → **tool catalog naming** · capability legibility → **tool descriptions** · progressive elicitation → **a conversation the plugin drives** · chat-row persistence → whatever state the host surface exposes | **Re-specify before building.** Building these against today's web UI builds them twice. |
| **C. Gets harder and becomes the entire game** | cold-start population (show them their own data) · the reflect-and-elaborate step · HOST's consent gate on consequential actions | **This is the beta.** All differentiation now rides on what the tools return. |

**The uncomfortable one is bucket A.** CXO called those six "an afternoon, I'd just fix these,"
and in isolation that's correct — they're unambiguous convention violations reported by a
credible practitioner. My read is different only because of timing: **an afternoon spent on a
surface scheduled for retirement is an afternoon not spent on bucket C, and bucket C is now
load-bearing for the product's entire value claim.**

**Not "never" — "not now, and not as beta work."** Two carve-outs I'd accept: (a) if alpha
testers stay on the web UI during the plugin build, the *anxiety-producing* subset (HOST's #1
and #2 — the unfindable "blocked" card, the missing chat row) is worth fixing on welfare
grounds regardless of surface lifetime, because we are asking real people to use this in the
interim; (b) anything that is genuinely minutes, not an afternoon.

That carve-out is a real distinction, not a hedge: **the "blocked" card and the missing chat row
are not UI polish — they're the two items that changed Jake's behavior.** Panel width didn't.

## 2. The three-list decision CXO routed to me — answered

CXO's §5 left this open: replace the internal taxonomy with trigger-based entry points, *"wants
PPM's roadmap read alongside it; I'd not act unilaterally."*

**My read: CXO's principle is right and survives the pivot — but the surface it applies to is not
navigation, so we should not build it as navigation.**

Organize by the user's trigger rather than our object model. Under PDR-006 the entry points
**are the MCP tool catalog** — tool names, descriptions, and parameters are the only entry-point
copy a plugin user ever sees, and they're read by *both* the human and the host LLM deciding
what to call. So CXO's inversion becomes concrete and cheaper than a nav redesign:

- ❌ Not: three tools named for our objects, leaving the user (and Claude) to map a situation onto our taxonomy.
- ✅ Instead: tools named and described by **the situation they serve** — "shape a vague idea into a spec", "break an epic into tickets", "draft acceptance criteria for issues that lack them" — routing to the same three structures behind the scenes.

**This is the same fix CXO specified, at a third the cost, on the surface that will actually
exist.** And it's the answer to Jake's opinionation complaint in the form the plugin permits:
**opinionation lives in the tool catalog.** We don't narrow the product; we stop making the user
name our object model. HOST's framing holds too — a catalog that says what each tool is *for* is
the product scoping itself rather than asking the user to.

⚠️ **One risk I want on the record, because it's mine to flag and it cuts against my own
recommendation**: the tool catalog is read by the host LLM as much as the human, and
situation-shaped names may route *worse* than object-shaped ones if Claude's tool-selection does
better with crisp nouns than with scenarios. **I don't know which way that goes, and neither does
anyone here.** It's cheap to find out and expensive to assume — I'd have Lead or Arch test
selection accuracy on both namings before we commit. Recommending it as the direction, not as a
settled call.

## 3. The beta-gate question nobody has asked, and it's mine

**Is any of this a beta blocker?** It isn't in the Beta Blockers sprint, and #1386's gate
criteria are the canonical suite plus three multi-turn scenarios plus sign-off — **all of which
Jake's session would pass while producing the outcome he reported.**

That's the finding I'd put in front of PM: **our beta gate measures whether Piper answers
correctly. Jake's session says the risk isn't wrong answers — it's that a competent user
completes a full first session, gets correct behavior throughout, and concludes we're an LLM
wrapper.** Nothing in the gate can fail for that. It's a methodology-44 shape at the product
level: the gate emits "clear" identically whether the product demonstrated its value or merely
avoided errors.

**Recommendation, and it's a scope call I'd want PM to make explicitly rather than inherit:**

1. **Do NOT expand #1386.** It's unblocked since 7/20, coordination is Exec's, and reopening its
   criteria now trades a closeable gate for an open-ended one. Close it on its existing terms.
2. **Add one new gate criterion for beta — a first-contact demonstration test**: from a cold
   account with one tool connected, does the user's *own* data appear in the first exchange,
   unprompted? Binary, cheap, and it's the only one of these that fails today. That is bucket C
   made testable.
3. **Treat HOST's consent gate as a genuine blocker**, not a criterion — live writes to a real
   user's GitHub/Notion/Slack from a misread intent is the one class where "alpha, expect rough
   edges" doesn't cover us. This is the one item I'd hold a release for.

## 4. Cohort size — the roadmap risk in acting on this at all

n=1, and he's a sophisticated practitioner dictating from memory. CXO's split is the right one
and I'd make it operational:

- **Structural findings** (§1 capability-parity, cold-start, progressive elicitation, consent
  boundary): **act now, don't wait for n>1.** They stand on their internal logic — Jake's
  argument that a tool requiring complete scoped input has LLM parity is *valid reasoning*, not a
  preference. A second tester agreeing adds nothing to a sound argument.
- **Preference-level findings** (panel width, placeholder verbosity, nav layout): **do not act on
  n=1**, and bucket A moots most of them anyway.

**The roadmap risk is the denominator.** One alpha tester is not an alpha program, and every
week we spend building against Jake's single session is a week of compounding on one data point.
I'd rather see 3–5 testers on the plugin than 20 fixes against the web UI. **That's a sequencing
argument for shipping PDR-006 sooner, not a reason to slow it.**

## 5. Tracking — the part that usually gets skipped

Four excellent lenses is not work; it's four memos. **None of this is in GitHub.** I'll file the
issues myself against the bucket structure above once PM's synthesis lands — I don't want to
pre-empt the synthesis by filing a shape PM may reorder, but I also don't want this to become the
document everyone admired. **Exec: flag me the moment synthesis is done and I'll convert it same
day.**

And HOST's item, which I'm seconding rather than restating: **Jake asked to be kept in the loop,
and closing that is an obligation.** From the roadmap side there's a self-interested reason too —
he's our only tester, he offered more structured feedback, and the fastest way to get n>1 is to
make the first one feel it mattered.

## 6. What I'd hand PM as the one-line version

> The three lenses agree the fix is "stop asking him for the answers and show him his own work."
> The roadmap question is *on which surface* — and since PDR-006 deletes the surface a third of
> our fix list targets, the beta should be the tool-return layer, the cold-start demonstration,
> and the consent gate. The rest is either free or moot.

Owed and unchanged from me: PDR-006 + Q2 review (Arch resolved Q2; my sprint/roadmap slice still
owed), and the spatial product-value slice — Arch released the hold and shipped the layer map this
morning, so both are unblocked and next in my queue.

— PPM, 2026-07-30
