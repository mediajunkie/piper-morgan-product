---
type: design-mapping
role: CXO (Chief Experience Officer), lead
status: v0.1 — DRAFT. Routed to Lead (buildability/sequencing) and PPM (scope coherence); PM co-owns the model this maps.
authored: 2026-08-28
authored_by: CXO
co_owner: xian (ceo)
purpose: Map the ratified FTUX experience model onto actual surfaces — the named next phase after the model. Deliberately small, per PM's no-optional-complexity lens.
consumes: ftux-experience-model-2026-08-21.md (PM-aligned) · surfaces-taxonomy-2026-08-16.md (RATIFIED v1.0) · no-optional-complexity-standing-lens-proposal-2026-08-27.md (PA/PM) · PA's connector-architecture finding + Slack descope (2026-08-27)
---

# FTUX surface mapping — where the model actually lands

**The model said what meeting Piper should be. This says where.** Per PM's framing on 2026-08-21: model
first, then map.

> 🔴 **AMENDED 2026-08-29 — the architectural review changed one of this document's two live cells.**
> PM ratified the same day (`decisions.log`, Arch's review): **web-chat is in explicit maintenance mode —
> bugs fixed, nothing new built — and all NEW build effort goes to the MCP/BYOC path.** Two consequences
> for this mapping, one narrowing and one *strengthening*:
>
> - **§1 (F-FirstRun × Web) is SUPERSEDED as a build target.** Its recommendation — "Piper speaks first"
>   in the existing chat view — is new build on a maintenance-mode surface. It stands as a *design record*
>   of what Web's first-run should be if and when Web builds again; it is **not** something to sequence
>   now. My 08-28 lens-driven position (smaller move, no new home view) was correct *and* is now moot for
>   scheduling purposes.
> - ⭐ **§2 (F-FirstRun × MCP) is PROMOTED, explicitly.** ESSENCE.md's build-surface line orders the MCP
>   path *"in roughly the clean-room agent's increment order: **cold-start reflection first**"* — which
>   **is this mapping's §2 gap**, named as the first increment on the only surface now taking new build.
>   The empty-state interview (#1688) is therefore not merely still valid; it is the leading item.
>
> **Net**: this mapping's central finding survives the review intact and gets sharper — one live cell
> instead of two, and it's the one ESSENCE puts first. **The two-cell framing was right; the count is now
> one.** Caught by reading ESSENCE against my own shipped doc rather than filing the broadcast as FYI.

## 0. The lens applied FIRST, which is why this document is short

📌 **PM's principle, named 2026-08-26**: *"No optional complexity. It's a rule because it is so easy to
forget. Repeatedly on this project the pull toward scope creep in the name of an ideal vision has weighed
and slowed us down."* Its test: **has one real case already proven this is needed?**

A surface mapping is exactly the artifact that lens exists to catch. The tempting version crosses all eight
functional surfaces with all five platforms and produces forty cells of mostly-speculation. **So the first
move here is subtraction, not enumeration.**

**FTUX is one functional surface — F-FirstRun.** Everything else in the taxonomy's Axis 1 is a different
interaction moment. So the mapping's real space is *F-FirstRun × platform*, five cells, of which:

| Platform | In scope for this mapping? | Why |
|---|---|---|
| **Web** | ✅ **YES** | We control the landing surface; it's the primary bespoke-UI surface per PDR-005. |
| **Chat host (MCP/Claude Desktop)** | ✅ **YES** | Primary distribution per PDR-005 (b); **#1536 already shipped a first-contact rail here** — a proven case, not a projection. |
| **Chat host (Slack)** | ❌ **NO** | Descoped to Fast Follow (PM-ratified 08-27, PA's connector finding); already outside the ratified F-Integrations set. Mapping it now is textbook optional complexity. |
| **CLI** | ❌ **NO** | Maintained, not a primary onboarding surface (taxonomy §4, PPM's ratified reasoning). No proven first-run case. |
| **Notification layer** | ❌ **NO** | Out-of-session by construction → #1174's domain (taxonomy §4's structural routing). A notification is not a first meeting. |

**Two live cells. That is the whole mapping.** The rest is recorded as deliberately-not-mapped (§3) so a
future reader sees a decision, not an omission.

## 1. F-FirstRun × Web — structured-first, and mostly unbuilt

**The model's shape here**: Piper speaks first, unprompted, because we own the landing surface. Radar/Files
lead; chat is one register among several, not the front door.

| Model element | Web expression | Build state |
|---|---|---|
| **Piper speaks first** | The landing view opens with Piper's move already made — not an empty composer awaiting input | **Unbuilt.** Today's landing is chat-shaped. |
| **Empty state → the interview IS the value delivery** | One good question, prominent, answerable in place ("what's the thing most on your mind at work right now?"); the answer becomes a real held thread, visible immediately in Radar | **Unbuilt** — the mechanism family exists (standup interview, #1510 rail); the FTUX framing of it does not. |
| **Partial/rich → demonstrate what's held** | Radar shows real held state with honest denominators; the demonstration is the surface itself, not a message about it | **Partially built** — Radar exists; the FTUX-shaped first-run presentation of it does not. |
| **The enrichment offer** | Connector offer appears *after* the first thread is held, not as a gate before it — the wizard becomes an offer inside FTUX | **Unbuilt as sequencing.** The wizard exists and is currently the de facto FTUX (the thing the model displaces). |
| **Radar never reads empty** | First interview populates it; #1625's upcoming-reminders lean and the #1635 false-door placement rules both bear here | **In flight** (#1625 lean posted; #1635 position delivered). |

✅ **RESOLVED 2026-08-28 (PM, in conversation)** — the one genuinely load-bearing open question in this
mapping: whether Web's first-run landing is *the chat view with Piper having spoken first*, or *a distinct
home/rollup view with chat as one door*. The model supports either; PM has called the home-screen idea
"dormant, eventually." **Under the no-optional-complexity lens I took the smaller move**: Piper speaks
first *in the existing chat view*, with Radar visible — no new view required, and the home-screen decision
left for a real case rather than smuggled in as part of a mapping. 📌 **PM: *"I agree with the position
that you took. I do not need to override it."*** So this is decided, not pending — build against the
existing chat view.

## 2. F-FirstRun × Chat host (MCP) — largely built, and the rest is copy

**The model's shape here**: Piper *cannot* open (the host owns turn-taking), so the same move arrives as
the **response to the user's first utterance** — 📌 PM's own refinement, 08-21.

| Model element | MCP expression | Build state |
|---|---|---|
| **The greeting variant** | First-exchange append on the greeting path + the category-independent floor rail | ✅ **BUILT and closed** (#1536, PM live-verified v58, closed 08-22 with cold-account pins). |
| **Rich state → demonstrate** | The connector demonstration with real entities, honest denominators, inline scope | ✅ **BUILT**, and the purpose-line copy shipped 08-22 (#1539) so it reads as reassurance not capability. |
| **Empty state → the interview** | ⚠️ **THE GAP.** #1536's honest behavior with nothing connected is *"unchanged"* — a plain greeting, correctly no fake demo. But the model says the empty state is where the **interview** should happen; a cold MCP user currently meets an ordinary greeting, not the value-delivering question. | **Unbuilt — and this is the mapping's main finding.** |
| **The enrichment offer** | Connector-general offer after the first held thread | **Unbuilt** on this platform (no wizard here; the offer would be conversational). |

⭐ **The finding worth the whole exercise**: **#1536 solved the rich case and honestly declined the empty
case; the model says the empty case is where the most important work happens** (a brand-new user with
nothing connected is exactly who forms the "just an LLM with extra UI" verdict). The two are consistent —
#1536's AC3 *requires* honest failure rather than a fabricated demo — but "honest silence" is where the
model asks for "one good question." **That's a real, small, well-shaped gap, and it's the same mechanism on
both platforms** (§1's empty-state row), which is what makes it worth building once.

## 3. Deliberately NOT mapped (a decision, not an omission)

- **Slack** — Fast Follow (PM-ratified 08-27). Re-enters when #1481's hold clears, as a batch with the
  taxonomy's other Slack cells (PPM's inherited-hold rule).
- **CLI** — maintained ≠ gets a first-run build. No proven case.
- **Notification layer** — #1174's domain by construction.
- **Every other functional surface × platform cell** — this is an FTUX mapping, not a general UI plan; the
  taxonomy already holds the general shape.
- **The home-screen/rollup view** — named as a fit in the model, still not scheduled; §1 takes the smaller
  move instead.

## 4. What this implies for sequencing (Lead's call, not mine)

If the mapping is right, the natural order is:
1. **The empty-state interview** — one mechanism, serves both live platforms, closes the mapping's main gap.
2. **Web's "Piper speaks first"** in the existing view (no new view), with Radar visible.
3. **The wizard-as-offer-inside-FTUX** resequencing (mostly a matter of *when* it's shown, not new UI).
4. Everything else already in flight (#1625, #1635) lands where it lands.

**Not proposing milestones or issues** — that's PPM's and Lead's lane; this is the design ordering, offered
as input.

## 5. Open questions — routed

**For Lead**: is the empty-state interview genuinely one mechanism across both platforms, or does the Web
form (prominent, in-place) and the MCP form (conversational turn) diverge enough to be two builds? My read
is one mechanism with two presentations; you'd know better.

**For PPM**: does §4's ordering fit the current milestone shape, and does the empty-state interview want an
issue of its own or is it a scope-addition to something extant?

✅ **For PM — ANSWERED 2026-08-28, same day**: §1's flagged decision (existing chat view vs. a distinct
home view). PM endorsed the lens-driven smaller move and explicitly declined to override. **§1 updated in
place; no longer open.** Recorded here because the ruling was given in live conversation — a decision that
exists only in chat is one the next reader can't find.

---

*CXO v0.1, 2026-08-28. Short on purpose: the no-optional-complexity lens was applied before the mapping,
not after, which reduced a potential forty cells to two live ones and one real gap.*
