# The conversational layer: what it costs, what BYOC changes, what is genuinely ours

**Lead Developer → PM, prep for the CXO (FTUX) and PA (BYOC) conversations · 2026-08-18**

**Why this exists**: PM named the risk plainly — *"spending all my time perfecting a conversational
layer that reinvents prior art and not focusing on the unique value proposition."* This brief gives
that instinct the evidence it deserves, in both directions, so two overdue strategic conversations
start from data instead of discouragement.

---

## 1 · What the interpretation layer actually costs us (this week's ledger, not vibes)

Between 2026-08-15 and 2026-08-18, PM ran four live test rounds. **Every round was productive, and
that is the problem**: the defect supply from the interpretation layer is not depleting.

| Class (vocabulary) | This week's live instances | Layer at fault |
|---|---|---|
| Fabrication | phantom "Filed!", phantom "Reminder set for 3pm" (#1648) | floor improvisation over unrouted turns |
| Turn-theft | draft body stolen, interview answers stolen, aside-accepted-a-delete (#1627/#1630/#1650) | greedy patterns + greedy accept rows |
| Greedy misclaim | "delete the reminder…" → "couldn't find a project", twice (#1527) | pre-classifier regex |
| Teach-then-deny | standup offered "mark that overdue todo done," couldn't consume its own offer (#1651) | offer copy unbound to referents |
| Silent parse miss | "please remind me: X" unparsed ×2 (#1606); "file as is thanks" missed (#1648) | pattern narrowness |
| Wrong clock | "2pm has passed" on UTC while PM says *"I am in Pacific"* and is ignored (#1572) | no user-time model |

Two structural facts make this a treadmill rather than a burn-down:

1. **The layer being patched is already scheduled for replacement.** The Understanding-Layer
   Inversion (#1595, Arch-ratified 08-09) replaces the regex pre-classifier + unconstrained LLM
   emission with ONE constrained routing call over a 62-operation grammar. Roughly **half of this
   week's fix lanes were patches to code the Inversion deletes.** The fixes were individually
   correct and same-day — and collectively they are maintenance on a condemned building.
2. **The failure classes are structural, not incidental.** Turn-theft happens because routing has
   no session state (it cannot see "an answer is pending"). Fabrication happens because the floor
   fills gaps the router leaves. Patches narrow each instance; only the architecture change
   (context-aware routing — Phase 2's SessionSnapshot) removes the class.

**The honest counter-evidence**: the *judgment* fixes of the same week — consent cells, crisp
confirms, verified-empty honesty, the action-claims contract — are NOT treadmill. They transferred
across every surface they touched and none has regressed. The treadmill is specifically the
*language-understanding* half, which is exactly the half that is commodity prior art.

## 2 · The two conversations, and what each answer changes

The striking property: **both questions, answered either way, make the current conversational
plumbing LESS load-bearing — and neither invalidates the judgment layer.**

### CXO conversation — "should FTUX even be a chat?"

| If FTUX stays chat-first | If FTUX is structured-first (chat as one surface) |
|---|---|
| The interpretation layer is the front door; its brittleness is the first-run experience; Inversion quality becomes beta-gating | Radar/Files/forms carry first contact; chat becomes an escape hatch for the long tail; the interpretation layer needs "good," not "flawless," at beta |
| Every parse miss is a first-impression risk | A new user's first five actions are clicks, not sentences — parse misses can't reach them |

Note the asymmetry: structured-first *de-risks beta without discarding anything* — the chat keeps
improving underneath via the Inversion. This week's data (10 of 15 chat tests passing, but the 5
misses all first-impression-lethal) argues the structured-first case better than any mockup could.

### PA conversation — BYOC (chat-plugin) vs. our own chat container

If Piper's conversational surface becomes a plugin/connector inside Claude/ChatGPT (BYOC), the
host does the language understanding — the exact problem class we cannot out-invest them on.

| BYOC would OBVIATE | BYOC would PRESERVE (and elevate) |
|---|---|
| The pre-classifier and its greedy-pattern family (#1527 et al.) | The 62-operation grammar — **it becomes the MCP tool inventory almost verbatim** |
| Our turn-taking/offer plumbing (host manages the conversation) | The consent gate (effect × outwardness) — hosts have NOTHING like per-action consent judgment |
| The floor and its fabrication risk (host composes prose) | The honesty contracts (verified-empty, action receipts) — enforced at the tool layer |
| Our chat renderer, history sidebar, formatting bugs | Radar, Files, standup, the working-state model — as the product's OWN surfaces |
| | The PM-domain judgment: clarify-first verbs, draft-then-file, interruption ethics |

**The convergence worth naming out loud**: the Inversion's Phase-1 grammar work is *already* the
BYOC tool inventory. Building Phase 2/3 is not a bet against BYOC — it is the same artifact viewed
from inside vs. outside. This is the strongest available answer to "am I trying to do too much":
the overbuilt part is the container; the content transfers.

### On "bring-your-own-key" alignment
BYOK (users' API keys in our container) and BYOC (our tools in users' AI container) are the same
instinct at different layers — don't own the expensive generic part. BYOK still leaves us owning
understanding; BYOC hands it off entirely. The credential plumbing we are troubleshooting for BYOK
(keychain, per-user secrets, #1382) is needed under EITHER model — it is not throwaway.

## 3 · The "no matter what" core — what we've built nothing without

PM's framing: *"the things we need to do no matter what, without which we have built nothing of
coherent value."* My list, defensible under any combination of the above answers:

1. **The consent/trust architecture** — decide_consent's cells, clarify-first verbs, decline
   memory that never lowers a gate, the outwardness axis. This is the product's ethics made
   executable, and it is unique: no host platform arbitrates per-action consent for acting on a
   PM's behalf.
2. **The honesty discipline** — verified-empty vs never-looked, action-claims-need-receipts,
   fabrication as the capital crime. This week proved it catchable and enforceable in code.
3. **The PM-operation grammar** — the 62 operations (todos, reminders, issues, standups, projects,
   analyses) with their effect/outwardness declarations. This IS the product inventory, and the
   MCP surface, and the Inversion's target vocabulary — one artifact, three uses.
4. **The working-state model + Radar** — the user's todos/reminders/projects/attention as durable
   state Piper reasons over; the pinned/attention surface that owns persistence.
5. **The synthesis direction** — standup, briefings, ambient presence (L4): combining signals into
   judgment. The vision doc's "fill gaps, never duplicate notifications" principle.

**Explicitly NOT core** (commodity, or due to be superseded): our NL parser (surfaces 1–2), the
floor's prose improvisation, arguably the chat container itself, per-phrasing pattern patches.

## 4 · Recommendation (Lead's, for discussion — not a decision)

1. **Inversion Phase 2 proceeds now regardless of the chats' outcomes** — it is simultaneously the
   fix for chat brittleness AND the construction of the BYOC tool surface. It cannot be wasted.
2. **Interpretation-layer patching freezes to corpus-deposit-by-default** (the supersession gate):
   a fix targeting surfaces 1–2 or floor-copy must name why it can't wait for the Inversion.
   Handler/rail/consent/honesty fixes stay sanctioned — they transfer.
3. **File-infrastructure repairs proceed** (#1656/#1657) — needed under every model.
4. **MVP triage pass after the two chats**: with CXO's surface answer and PA's container answer in
   hand, re-cut the milestone against §3's core list — candidates move to PUB or post-beta with
   honest "known limitation" labels. I'll prepare the cut with PPM; PM rules.

*Written 2026-08-18 evening. All incident references verifiable in the issue tracker; the weekly
ledger is in the Lead session logs 08-15 through 08-18.*
