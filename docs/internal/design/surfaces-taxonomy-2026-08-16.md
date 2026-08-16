---
type: design-taxonomy
role: CXO (Chief Experience Officer), lead
status: v0.2, CONFIRMED by both Arch and PPM 2026-08-16 (each independently verified v0.2's applied fixes rather than trusting the summary — Arch checked §3's correction landed as described; PPM re-derived the notification-layer routing against the L4 vision doc and found it holds for a structural reason, now stated in §4). F-AuditTransparency split RATIFIED (Arch). §4 cross-matrix resolved (PPM). The only thing standing between v0.2 and full ratification is PM's word on §1's naming, per §5.
authored: 2026-08-16
authored_by: CXO
co_owner: xian (ceo) — per PM's 2026-08-15 brief, "PM will contribute directly as needed and wants to see the result"
supersedes: the "Surface 3 is a phantom" question (resolved below, §2) — that question is now subsumed by this larger taxonomy
purpose: Formally name and cross two axes that have been informally present — one fully named, one scattered and implicit — since May 2026, so "which surface" questions stop needing archaeology.
---

# Surfaces taxonomy — two axes, not one list

**Status: DRAFT v0.1. Not yet ratified.** Written per PM's 2026-08-15 brief (relayed by Exec): *"beware the
strong tendency to flatten it into semantically compact ideas that lose the modeling (M stands for
'modeled') done to articulate the essence of a holistic experience expressed uniquely as needed wherever it
appears."* This document is the rectification, not the flattening.

---

## 0. Why this exists, and what it replaces

"Surface 3 is a phantom" was the wrong question. The forensic answer (§2 below) is that Surface 3 is real,
CEO-ratified, and simply never got repeated in PDR-005's own citation. But answering *that* narrow question
would have missed the actual defect PM named: **"surface" has been doing two jobs under one word since
May 2026**, and every place that collapses them into one list — including my own MUX/UI Round 2 synthesis,
including PDR-005 — inherits an ambiguity nobody chose on purpose.

**The two jobs, split into two axes:**

1. **Functional surface** — *what kind of interaction moment this is*: history, privacy, settings,
   integration setup, search, first-run, error/degraded-state. This is the existing "7 MUX/UI surfaces"
   axis, fully named since May 2026 Round 2 (`mux-ui-gap-cxo-round-2-synthesis-2026-05-15.md`).
2. **Platform / touchpoint** — *where and how the interaction physically arrives*: a web browser, a
   desktop-native app, an OS notification, a terminal, a chat host, a voice assistant. **This axis has
   never been named as an axis** — but it has been operationally present, scattered across PDR-005's
   qualifier language, since the same week. §3 shows the receipts.

**PM's proof they're orthogonal, not competing lists**: Settings (functional surface) needs both a
web-app screen *and* a conversational path (platform) — the same functional surface, expressed on two
different platforms. A single flattened list has no way to represent that without either duplicating
"Settings" as two list entries or silently picking one platform and forgetting the other exists. Two axes
crossing is exactly what a genuine orthogonal relationship looks like; one list is what it looks like after
someone (unintentionally) picks a canonical platform and stops naming the axis.

---

## 1. Axis 1 — Functional surface (the existing seven, renamed for clarity)

Origin: Lead Dev's 2026-05-14 memo (7 genuine UI gaps hit organically doing dev work, not invented for a
round number) → CXO Round 1/Round 2 cohort synthesis (PPM + Architect + Comms + Lead Dev, four lenses) →
CEO-ratified 2026-05-16.

**Renamed from bare numbers to names** — this document's own contribution, per the standing rule (already
in `experience-across-surfaces.md` §5) that names survive a document reshuffle and numbers don't. The old
numbers are kept in parens for cross-reference during the transition; drop them once this ratifies.

| Name (was #) | What it is | 1.0 status (Round 2, CEO-ratified) |
|---|---|---|
| **F-History** (1) | Conversation history / archive — the paginated record of prior conversations | Yes, after sidebar reconciliation |
| **F-Privacy** (2) | Per-conversation privacy controls (`is_private`) | Yes — Class A |
| **F-Settings** (3) | Settings / preferences | Minimum-slice only — see §2 |
| **F-Integrations** (4) | Integration setup wizards (GitHub, Calendar, Notion; Slack deferred) | Yes — Class A |
| **F-Search** (5) | Cross-history search interface | Post-1.0; pre-1.0 index ADR (ADR-064) |
| **F-FirstRun** (6) | Empty / first-run states | Yes — Class A + C |
| **F-Errors** (7) | Error / degraded states — see §2 for the split question | Yes — Class A |

## 2. Two corrections to the record, both forensic, neither speculative

### 2a. F-Settings is not a phantom — it was always real, just never re-cited

**Verified via git history + mailboxes, not assumption** (Exec's forensic dive, 2026-08-15): Surface 3
originates in Lead Dev's 05-14 memo as one of the original seven, survives both synthesis rounds, and is
**CEO-ratified by name** in Round 2 (`mux-ui-gap-cxo-round-2-synthesis-2026-05-15.md`, deliberately scoped
tiny: *"account profile editing + basic notification opt-outs only. Explicitly defers model selection UI,
workspace prefs, advanced controls."*). It never got a full MUX doc or its own ADR the way the four Class A
surfaces did — a direct, intended consequence of its minimum-slice scoping, not neglect.

**The actual defect**: PDR-005 §"1.0 bespoke-UI surfaces" (line ~74) cites *"5 of 7 MUX/UI surfaces"*
without repeating the ratified list of seven names, and its 3-criterion test discussion (line ~84) says
*"Surfaces 1/3 meet weaker forms"* — again by number, with no adjacent pointer to where the names live.
**A reader who only has PDR-005 in view has no way to discover Surface 3 was ever named**, which is exactly
how "phantom" became a plausible-sounding read for something that was ratified fourteen weeks ago.

**Fix, small and mechanical**: PDR-005 should cite this document (once ratified) by name wherever it
currently says "5 of 7" or "Surfaces N/M" bare. Not proposing to rewrite PDR-005's decisions — only its
citations, so the next reader doesn't have to reconstruct this same forensic trail.

### 2b. F-Errors genuinely carries two different kinds of thing — proposing a split, not deciding one

**The finding** (Exec's dive, confirmed against ADR-063): Surface 7 started as "error/degraded states"
(matching F-Privacy/F-Integrations/F-FirstRun/F-Errors' original character). Mid-Round-2, Architect named
the audit-transparency **read**-surface as *"the highest single-priority architectural gap among the seven
surfaces"* and it was folded into Surface 7 as a "keystone" rather than becoming its own surface.

**Independent evidence this was already structurally two things, not one, even before this taxonomy
question came up**: the audit-transparency read-surface has **its own ADR** — ADR-063, *"User-Facing Audit
Envelope Read Surface"* — with its own routes (`/api/v1/transparency/*`), its own auth model (user-binding
+ admin-scope), its own Pattern (071, audit-as-attack-surface). General error/degraded-state handling
(a failed integration, a slow model, a tool error) has no comparable architectural document — it's
presentation-and-voice work, not a distinct backend surface with its own auth model. **An ADR that exists
only for half of a "surface" is itself evidence the surface was never really one thing.**

**✅ RATIFIED 2026-08-16 (Arch)**: split F-Errors into **F-Errors** (general degraded/failure states —
presentation + voice, no dedicated backend surface) and **F-AuditTransparency** (the ADR-063 read-surface —
has its own routes, auth, and architectural commitments). Arch verified ADR-063 directly (own routes in
`services/api/transparency.py`, own module `services/ethics/audit_transparency.py`, own auth model) and
confirmed the split rather than deferring to the original framing: *"This was my own original 'keystone'
framing under-differentiating two things that don't share a mechanism — good catch, and I should have
drawn this line the first time."*

---

## 3. Axis 2 — Platform / touchpoint (new as a named axis; not new as a concept)

**PM's working catalog, explicitly non-exhaustive** (PM's own caution: *"not exhaustive… more a catalog of
dimensions of complexity to be acknowledged but not chased obsessively for 100% (asymptotically infinite)
support"*):

| Platform | Sub-forms named so far |
|---|---|
| **Desktop** | native app · web browser · OS/web/app notification layer |
| **Mobile** | native app · web · OS notifications (especially) |
| **Terminal / CLI** | any device |
| **Chat host** | Slack-class — channel and/or bot integration |
| **Voice-class** (future, unscoped) | Siri/Alexa-class assistants |

### This axis is not an invention — PDR-005 already operates on it, just without a name

**The receipts**, all from `PDR-005-bring-your-own-chat.md`, none of them new reasoning, all of them
scattered rather than organized under one axis name:

- **"Capabilities are conditionally claimable per host"** (AC-1, surface-presence detection) — a real
  architectural mechanism: *"the persona core's capability map is host-aware at the claim layer… the
  persona only surfaces capability claims the current host supports."* That's platform-axis logic, encoded
  in the claim layer, with no name for the axis it's reasoning about.
- **"Runtime persona-template dispatch by client identifier"** — *"the server detects which client surface
  is invoking the request and loads the corresponding adapter template at request time."* This is not
  presentation-only — it's a routing/dispatch mechanism keyed on exactly the dimension this document is
  naming.
- **The platform-affordance-bounded qualifier** (EC-2, folded v0.6): *"capabilities are conditionally
  surfaced per host where the platform structurally supports the capability surface (e.g., Slack
  thread-summarization claimed only where threads exist; voice transcription only where an audio surface
  is present)."* Concrete, per-platform architectural asymmetry — MCP is *"structurally request-response
  only,"* Slack has *"DM/channel writes, scheduled messages, Socket Mode event triggers."*
- **A stated voice-register budget per platform** (~5%, cited three separate times): *"Voice register may
  adapt per platform; the underlying decision and the canned response phrasing are invariant."*
- **Named cross-platform variants of two functional surfaces, already ratified**: *"Surface 1 (history)
  needs a cross-client variant: 'what I learned about you across all hosts'"*; *"Surface 6 (first-run)
  needs a 'welcome back' variant."* **These are literally F-History × platform and F-FirstRun × platform
  cells in the cross-matrix this document formalizes** — decided in May, never labeled as what they are.

**⚠️ CORRECTED 2026-08-16 (Arch) — the paragraph above overstated what the receipts prove, and this
correction matters more than the finding it corrects.** Arch dispatched an actual code check before
answering rather than taking the PDR-005 quotes at face value: **the capability-claim layer and
client-identifier template dispatch cited above do not exist in code** — zero references anywhere in
`services/` for `capability_claim`, `capability_map`, `host_aware`, `client_identifier`, or
`adapter_template`. PDR-005 itself explains why (line ~178): it commits to **one** template at 1.0
(MCP/Claude Desktop) — Slack is post-1.0/demand-gated, so there has been nothing to dispatch *between* yet.

**The receipts are real, accurately quoted PM/Arch design commitments — they are not evidence the mechanism
runs.** This document's first draft cited the prose as if citing it settled the question, which is the
exact shape of CIO's methodology-49 ("Described Is Not Running"), filed this same week from an unrelated
incident. Caught in review, not shipped uncorrected — but worth being explicit that it needed catching.

**What IS built, and it's genuinely informative**: `services/commands/registry.py`'s
`CommandDefinition.interfaces: Dict[CommandInterface, InterfaceConfig]` already has the right *shape* for
"one functional thing, multiple simultaneous platform implementations" — exactly this document's Settings
example. But it's narrower than this taxonomy (slash-command-style actions only; no Notification-layer or
Mobile axis at all), and — the sharper point — `CommandCategory.SETTINGS` is a **declared, unused** enum
value. The worked example in §0/§4 maps onto an empty registry slot with the right type and no registration.

**Corrected conclusion**: formalizing Axis 2 does not require *new conceptual* architecture — PDR-005 was
genuinely already reasoning about this dimension, and that part of the argument stands. But it is not free
of architectural consequence: **the platform axis is decided, not enforced.** Extending
`CommandRegistry`/`CommandInterface` (or an equivalent) to actually cover the full functional-surface ×
platform space is real, unstarted work, not already-built infrastructure missing only a name. Today there
is no automated check for "every MVP-required cell has a real code path" outside slash-commands. Whoever
scopes the ✏️-marked cross-matrix cells below should read them as *decided intent*, not *verified
capability*.

---

## 4. The cross-matrix — illustrative, not exhaustive

**Deliberately not attempting all 7 (or 8) × 5+ cells.** PM's own caution against chasing 100% coverage
applies here directly — most cells are either N/A (Settings has no meaningful CLI form yet) or genuinely
undecided (does F-Errors need a distinct Slack voice, beyond the ethics-invariant baseline?). This section
shows the shape with real, already-decided cells, and marks the undecided ones as questions rather than
guessing at answers.

| Functional surface | Web | Chat host (Slack-class) | CLI | Notification layer |
|---|---|---|---|---|
| **F-History** | Primary — the #1021 archive UI | Cross-client variant, ratified (PDR-005); **deferred for MVP** — #1481's Slack hold | Deferred for MVP — CLI's non-primary role | N/A |
| **F-Settings** | Primary (minimum-slice, ratified) | **Deferred for MVP** — #1481's Slack hold, not a fresh judgment (see caution below) | Deferred for MVP — CLI's non-primary role | N/A |
| **F-FirstRun** | Primary — full MUX doc | "Welcome back" variant, ratified (PDR-005); **deferred for MVP** — #1481's Slack hold | Deferred for MVP — CLI's non-primary role | N/A |
| **F-Errors** | Primary — full MUX doc, ethics-invariant | Ethics decisions invariant; voice register may adapt ~5% (ratified — NOT gated by #1481, this is about voice register once Slack inbound exists, not whether it exists) | Deferred for MVP — CLI's non-primary role | **Routed to #1174**, not decided here — see note below |
| **F-AuditTransparency** (§2b, ratified) | ADR-063 routes, user-facing | Deferred for MVP — #1481's Slack hold | N/A (no user-facing route surface) | N/A |
| **F-Integrations** | Primary — full MUX doc, 3 wizards | N/A — you don't OAuth-connect a service from inside Slack | N/A | N/A |

**✅ Resolved 2026-08-16 (PPM consult)**: all seven originally-✏️ cells are aspirational-and-fine-to-defer
for MVP — six for a shared *structural* reason, not seven independent guesses:

- **The general rule** (PPM's, worth keeping as the durable rule rather than re-litigating per cell): *any
  cross-matrix cell gated by an already-ratified hold inherits that hold's status automatically.* Four of
  the chat-host cells above inherit **#1481's ratified hold** (Arch, 08-04, `decisions.log`: *"Slack inbound
  is not a beta surface... moves to Production with #1419"*) directly — they don't need their own
  MVP-vs-aspirational judgment because the platform itself isn't in scope yet. If #1481 clears, re-evaluate
  those cells as a batch at that point, not before.
- **The four CLI cells** defer for a different shared reason: CLI is *maintained* (nobody's deprecating it)
  but isn't a primary onboarding/discovery surface for beta, consistent with PDR-006's primarily-MCP
  decision. "Maintained" implies "doesn't regress," not "gets every functional surface built out by launch."

**⚠️ A caution worth stating outright, since the document itself invites the mistake**: §0 and §3 use
F-Settings × Chat-host as the **illustrative example of why the two axes are orthogonal** (Settings needing
both a web screen and a conversational path). That is PM using the pairing to prove a *conceptual* point —
it is not a signal that this specific cell is required scope. The table above correctly defers it per
#1481; don't let "it was PM's own example" quietly launder into "PM wants this built now." (PPM's catch,
2026-08-16 — flagged as exactly the kind of inference that looks harmless and isn't.)

**F-Errors × Notification layer, resolved by routing rather than ruling**: this isn't actually a new open
question — it's a special case of **#1174**'s own discovery scope (when + how Piper proactively notifies),
which just approved a phased plan (08-15) whose core principle is that any Piper notice must fill a genuine
gap or provide a synthesized briefing, never duplicate an existing notification source. Whether a failure
ever clears that bar is #1174's question to answer, not a separate ad hoc call inside this taxonomy — this
cell defers to that thread rather than staying open indefinitely or getting decided twice.

**✅ Verified 2026-08-16 (PPM)**: this isn't a loose analogy — the routing follows from the column's own
definition. The **Notification layer** column only ever applies when the user isn't in an active session:
a failure during a live turn is just a normal reply, already covered by F-Errors × Web/Chat's primary
cells, with no notification-layer question at all. Anything that actually reaches this column is, by
construction, the out-of-session case — which is exactly and only #1174's domain. PPM checked this against
`ambient-presence-l4-vision-2026-08-15.md` directly rather than accepting the routing at face value, having
first suspected a reactive-vs-proactive category mismatch and then finding the column's own scope resolves
it.

---

## 5. Open questions

**✅ Arch, answered 2026-08-16**: F-AuditTransparency split ratified (§2b). Platform axis carries real
architectural consequence — it's decided, not enforced; `CommandRegistry`/`CommandInterface` extension is
real unstarted work (§3's correction).

**✅ PPM, answered 2026-08-16**: all seven originally-open cross-matrix cells resolved to defer-for-MVP,
with a general rule for future cells gated by an already-ratified hold (§4).

**Still open — for PM**: does the renamed Axis-1 table (§1) read right, or does "MUX/UI surface" deserve
different language now that it's paired with a second axis? Naming is cheap to get input on now and
expensive to revise after downstream docs cite it. This is the one thing standing between v0.2 and a fully
ratified v1.0.

---

## 6. Relationship to `experience-across-surfaces.md`

My own `docs/internal/design/experience-across-surfaces.md` (2026-08-09) already has an informal,
coarser version of Axis 2 in its §4 table (Web / Chat hosts / Slack / Phone / CLI — "the one experience,
expressed here"). **That table predates this document and used a coarser platform split** (one "Web" row,
rather than PM's finer native-app/browser/notification-layer breakdown; "Phone" as its own row rather than
mobile's sub-forms). Once this taxonomy ratifies, `experience-across-surfaces.md` §4 should be updated to
either adopt this document's finer platform names or explicitly note it's using a deliberately coarser
grain for a different purpose (that document is about *felt experience*, not build/architecture scoping —
the coarser grain may be the right one for its purpose, but the two should say so explicitly rather than
silently disagree). **Not doing that reconciliation in this document** — it's downstream of ratification,
not a precondition for it.

Also: `experience-across-surfaces.md` §5 already names the exact failure mode this document fixes —
*"'Surface N' is ambiguous across three schemes... prefer names to numbers."* This document is that advice,
applied to itself.

---

## What this document does NOT do

- **Does not re-decide any Round 2 CEO ratification** (F-Integrations pick, F-Privacy granularity,
  F-FirstRun framing, F-History reconciliation approach) — those stand as ratified.
- **Does not build the platform axis's enforcement mechanism** — the axis is decided; extending
  `CommandRegistry`/`CommandInterface` to cover it is real, unscoped follow-up work (§3).
- **Does not fill every cross-matrix cell** — deliberately illustrative, per PM's own anti-obsessive-
  coverage caution. The cells it does fill are resolved (§4); it doesn't claim completeness beyond them.
- **Does not rewrite PDR-005** — names a small citation fix (§2a) for PDR-005 to make once this ratifies;
  does not touch PDR-005's actual decisions.
- **Does not reconcile `experience-across-surfaces.md`'s coarser platform table** — flagged as downstream
  work, §6.

---

*Surfaces taxonomy v0.1, 2026-08-16. Written per PM's 2026-08-15 brief. Supersedes "Surface 3 is a
phantom" as the operative question — that question's answer lives in §2a; the document exists because the
question itself was too narrow.*
