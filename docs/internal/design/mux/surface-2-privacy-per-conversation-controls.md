# Surface 2 MUX Doc — Privacy / Per-Conversation Controls

**Document Type**: MUX specification (Class A — values-laden voice surface; Class D — state-changing)
**Author**: Chief Experience Officer (CXO first pass)
**Co-author (pending)**: Communications Director (voice-pass per ratified CXO→Comms→CXO→iterate pattern)
**Date**: 2026-05-19 (v0.1 first-pass draft)
**Implements**: MUX/UI Round 2 Surface 2 (per-conversation privacy for 1.0; per-message reserved post-1.0); PDR-005 v0.4 §Persona portability variance hierarchy (EC-2 + EC-3); PDR-005 v0.4 §MCP server scope cross-client memory continuity (EC-1)
**Status**: First-pass draft awaiting Comms voice-pass

---

## Scope

Surface 2 is the **privacy / per-conversation controls** surface. It covers four coordinated user-facing dimensions:

1. **The privacy state itself** — how a conversation becomes private, how the user knows it is private, how the state is reversible
2. **Session-level signaling** — banner hierarchy when privacy is active
3. **Conversation-list signaling** — how privacy state surfaces in history (Surface 1 coordination)
4. **Dedicated `/settings/privacy` page** — where the user inspects + manages privacy across conversations (replaces existing Coming-Soon shell)

This surface is **values-bearing, not feature-bearing**. The privacy commitment is a value Piper holds; the UI exists to make that commitment legible, reversible, and trustworthy.

### Why this surface is load-bearing

Per Round 2 cohort synthesis: *"Surface 2 stands alone in voice complexity — most net-new voice work, most values-laden, parallel to PDR-005 drafting."* Comms Round 1 framing: defaulting to a generic *"Privacy: ON / OFF toggle"* pattern erodes the commitment language.

Surface 2 is also where PDR-005's persona-portability variance hierarchy meets the user. Per §experience fill-in EC-2 (capability claim consistency) + EC-3 (ethics commitment invariance), the privacy promise must render identically across clients — zero tolerance for cross-client drift. The MUX doc translates that architectural invariance to observable user behavior.

### What 1.0 scope is (per Round 2 ratification + PPM Surface 2 unblocked signal)

- **Per-conversation `is_private` toggle** on the existing data-model substrate (column + index in place via #1021)
- **Privacy banner** at session level when conversation is private (existing `templates/components/privacy_mode.html`; voice-pass needed)
- **In-history privacy indicator** (icon at `templates/components/history_sidebar.html:330`; toggle wire-up partial; needs full wiring per Round 2)
- **`/settings/privacy` real page** (replaces existing Coming-Soon shell)
- **Audit envelope coupling**: every privacy state change captured in audit envelope (Surface 7 coordination); `host_id` field commitment enables future cross-host migration

### What 1.0 scope is NOT

- **Per-message privacy granularity** (schema migration + cascade rules + per-turn UI) — reserved post-1.0 expansion path
- **Cross-host privacy semantics** (unified vs. per-host) — `host_id` schema commitment in place; semantic decision deferred to follow-up ADR with HOST + CEO input
- **End-to-end encryption claims** — not in 1.0; if surfaced in voice, it must be true. Don't promise what we can't deliver.

---

## Voice anchor

Surface 2 voice is **values-laden + offer-first + honest-about-limits**. The privacy commitment is named as commitment; activation is invitational; what privacy does NOT cover is explicit.

### Three voice spines (Comms framing, Round 1; offer-first cluster)

1. **Offer-first activation** — Piper offers privacy; the user decides whether and when to engage it. Privacy is never the default state imposed; it's the user-chosen state surfaced
2. **Values-laden commitment language** — privacy is described as a commitment Piper holds, not a switch Piper has. The word *"private"* carries weight throughout
3. **Honest-about-limits** — Piper names what privacy covers (this conversation's content not flowing to working memory) and what it doesn't cover (e.g., the system still has the conversation; it's just not consolidating it into learnings)

### Borrowing source

Surface 2 has **no direct borrowing source** in existing MUX coverage (per Comms Round 1: "most net-new voice work"). The closest analogue is the **calendar-offer policy** (when and how Piper offers to connect your calendar) — same offer-first-with-stakes voice register.

The Surface 7 MUX doc (Surface 7 voice anchor, *"honest-about-limits without alarm or melodrama"*) is the **structural sibling** in the offer-first cluster; voice continuity between Surface 2 + Surface 7 matters because they often appear in the same session.

### What Surface 2 voice avoids

| Failure mode | Why it's wrong |
|---|---|
| *"Privacy: ON / OFF"* | Generic toggle voice; treats privacy as a setting, not a commitment; violates values-laden spine |
| *"Enable private mode to protect your data"* | Marketing/sales voice; "protect your data" is a vague promise; violates honest-about-limits |
| *"Your data is encrypted and secure"* | Capability claim that may not be true at the encryption/security boundary; Pattern-064 violation if surfaced without verification |
| *"Private mode activated. Your messages are now hidden."* | Hidden from whom? Surveillance-adjacent framing; violates colleague-not-system register |
| *"WARNING: Private mode is OFF. Your data may be used for training."* | Alarm-pulse voice; conflates 1.0 reality (no training) with hypothetical future state; violates honest-about-limits |
| *"Confidential conversation. Do not share."* | Treats user as compliance subject; privacy is for the user's benefit, not their obligation |

### What Surface 2 voice does

| Pattern | Example |
|---|---|
| Names privacy as commitment | *"Marking this private means I won't consolidate what we discuss here into what I remember about you long-term."* |
| Offer-first activation | *"Want to mark this conversation private? You can switch it back later if you change your mind."* |
| Honest about what private means | *"Private conversations stay in our session — they don't feed into the working memory I build over time."* |
| Honest about what private doesn't mean | *"The conversation still exists in this session — you can scroll back, search it, see the history. Private means I don't carry it forward into what I remember."* |
| Reversibility named | *"You can unmark this anytime. If you do, what we discussed becomes available for me to learn from going forward."* |
| Cross-client honest | *"Private is per-conversation right now. If you start a new conversation on a different client, it'll start in default (non-private) state — you can mark that one private separately."* |

---

## Surface 2 inventory

Surface 2 has **three coordinated UI tiers** plus the **dedicated /settings/privacy page**. The privacy commitment surfaces at different times in different shapes; voice register is consistent across tiers.

### Tier 1 — Toast (privacy state change moment)

**When it fires**: The user toggles privacy on or off for a conversation. A discrete state change happened in-flight that confirms the action and names the consequence.

**Form**: Top-right toast (existing toast infrastructure).

**Voice register**: One sentence confirming the change + one phrase naming what changed. Action-oriented close; reversibility implicit.

**Examples (drafts; Comms voice-pass):**

- On marking private: *"Marked this conversation private — it won't flow into long-term memory. You can unmark anytime."*
- On unmarking: *"Unmarked. From now on, what we discuss here is available for me to learn from. Earlier private parts stay where they were."*
- On retroactive private (if PM ratifies a retroactive-mark UX): *"Marked this conversation private retroactively — earlier turns and going forward both. Anything I already learned from those earlier turns will be unwound."*

**Anti-pattern**: Don't surface internal flags, ORM model field names, or audit envelope IDs in the toast. Those belong on the transparency page (Surface 7 coordination) or internal-only.

### Tier 2 — Banner (privacy-active session state)

**When it fires**: The conversation is currently private. Banner persists at the session level until user navigates away or unmarks.

**Form**: Top-of-screen banner (existing `templates/components/privacy_mode.html`; voice-pass needed to convert from current styling-only treatment to the prose below).

**Voice register**: One sentence naming the state + one phrase naming what it covers. Quiet-and-present, not attention-stealing.

**Examples (drafts; Comms voice-pass):**

- Default private-active: *"This conversation is private — what we discuss here won't consolidate into long-term memory."*
- After retroactive marking (if shipped): *"This conversation is private, including the earlier turns. Anything already learned from those turns is being reconciled."*

**Anti-pattern**: Banners shouldn't blink, color-shift, or pulse. The privacy banner is **quiet confidence** — present so the user knows privacy is in effect, not theatrical about it.

**Coordination with Surface 7 banner ordering** (per Surface 7 §"Coordination with adjacent surfaces"): privacy banner appears at the top of session-level banner stack; Surface 7 degraded-mode banner appears below. Both use offer-first colleague register; voice continuity required.

### Tier 3 — In-conversation indicator (Surface 1 coordination)

**When it fires**: The user is viewing conversation history (Surface 1) and needs to see which conversations are private without opening each one.

**Form**: Icon adjacent to each conversation entry in the history sidebar (existing icon at `templates/components/history_sidebar.html:330`; needs full wire-up per Round 2 sub-surface obligation).

**Voice register**: Indicator is visual; hover-tooltip carries one short phrase.

**Examples (drafts; Comms voice-pass):**

- Hover-tooltip on private indicator: *"Marked private — won't feed into long-term memory."*
- No indicator on non-private conversations (don't surface absence-of-private; private is the marked state)

**Anti-pattern**: Don't use lock icons that connote security/encryption — privacy here is about working-memory boundary, not data-at-rest encryption. Use an icon that signals "this one's set aside" (suggested: bookmark-with-mark or similar; final icon choice per design system).

### Tier 4 — `/settings/privacy` page (dedicated privacy management)

**When the user lands here**: They navigated from the privacy banner ("see my private conversations"), from settings index, from a toast ("manage your privacy preferences"), or from direct curiosity. This is the **dedicated privacy management surface** — replaces the existing Coming-Soon shell.

**UX pattern detailed below in §"`/settings/privacy` page UX."**

---

## Per-event-type rendering

The privacy state has discrete events that drive specific voice register. Three primary events:

### MARK_PRIVATE (user marks a conversation private)

**Toast voice** (in-conversation):
> *"Marked this conversation private — it won't flow into long-term memory. You can unmark anytime."*

**Banner appears** at session level after toast clears; voice per Tier 2 above.

**Audit envelope entry** (Surface 7 coordination):
> *"Privacy state change: marked private. Conversation will not consolidate into working memory layer. Reversible."*

### UNMARK_PRIVATE (user removes private flag)

**Toast voice** (in-conversation):
> *"Unmarked. From now on, what we discuss here is available for me to learn from. Earlier private parts stay where they were."*

The honest-about-limits framing is load-bearing: unmarking does NOT retroactively expose previously-private turns to working memory. The system honors the privacy commitment that held at the time the content was generated.

**Banner disappears** (returns to default session state).

**Audit envelope entry**:
> *"Privacy state change: unmarked. Future turns available for working memory consolidation. Past private turns remain excluded per the commitment-at-time-of-creation rule."*

### PRIVATE_TURN_NOT_CONSOLIDATED (silent; logged-for-record)

**Surfaced via transparency page only** — no toast, no banner. The event is in the audit envelope for record-keeping; the user can browse if curious but isn't notified per-turn.

**Audit envelope entry**:
> *"Routine: turn in private conversation was not consolidated into working memory, per active privacy state."*

This category exists so the audit-envelope log is complete — important for the "user can see what the system did with their content" promise.

---

## `/settings/privacy` page UX

The `/settings/privacy` page lives at the existing route (currently Coming-Soon shell; replaces shell with real content for 1.0).

### Layout

**Three coordinated sections, vertical:**

1. **What privacy means here** (top; one-screen explanation) — names the commitment, names what it covers, names what it doesn't
2. **Your private conversations** (middle; list view) — conversations currently marked private; bulk-unmark control; navigation to each conversation
3. **Privacy across clients** (bottom; explainer) — per-conversation privacy state when moving between clients (EC-1 cross-client transition framing)

### What privacy means here — primary explainer

**Header**: *"Privacy here is a commitment, not a setting."*

**Body** (draft; Comms voice-pass):

> *"When you mark a conversation private, Piper won't consolidate what you discuss there into the working memory I build about you over time. The conversation itself stays where it is — you can scroll back, search it, see the history — but it doesn't feed into what I remember going forward."*
>
> *"Private is per-conversation right now. If you start a new conversation on a different client, it'll begin in default (non-private) state — you can mark that one private separately."*
>
> *"You can switch a conversation private or non-private at any time. Earlier private turns stay private even if you unmark — what changes is that future turns become available for me to learn from."*

**Voice principles applied**: values-laden + honest-about-limits + colleague register + reversibility named.

### Your private conversations — list view

**Header**: *"Conversations you've marked private."*

**Entry list**: Each marked-private conversation surfaces:

| Field | UI rendering |
|---|---|
| Conversation title | Human-readable; clickable to navigate to the conversation |
| Marked-private date | Relative time (*"3 days ago"*) with full timestamp on hover |
| Turn count | Plain number; visual weight equal to title |
| Action | Single inline "Unmark" link; clicking surfaces the unmark toast |

**Empty state** (user has no private conversations):

> *"You haven't marked any conversations private yet. When you do, they'll show up here — and you can unmark them from this page."*

**Voice principles applied**: factual + teaching-by-example + offer-first close + no apology for empty state.

### Privacy across clients — explainer

**Header**: *"Privacy when you switch clients."*

**Body** (draft; Comms voice-pass):

> *"Privacy is per-conversation, and conversations don't carry across clients today. When you start a fresh conversation on a different client, it begins in default (non-private) state."*
>
> *"What I remember about you long-term — the working memory I build from non-private conversations — does carry across clients. If you've marked specific conversations private on one client, those still don't feed into working memory anywhere."*
>
> *"Per-host privacy semantics (different rules on different clients) is something we may design later. Today, the rule is the same everywhere: private conversations stay out of working memory, full stop."*

**Voice principles applied**: honest-about-limits + cross-client transition honesty (EC-1) + acknowledges deferred decision (per-host audit semantics) without overselling future-state.

### Error states (privacy API failure)

When `PATCH /api/v1/users/me/history/{id}/privacy` fails (network, server error, partial data):

> *"Couldn't update the privacy state right now. Refresh and try again — usually that's enough. If it keeps happening, the transparency page will show what was logged."*

When the user lacks authorization (shouldn't normally fire for self-owned conversations; surfaces if JWT-binding is broken):

> *"That conversation isn't in your view — only the person who had it can mark it private or unmark it."*

(Uniform 403 messaging per Surface 7 §"Error states" pattern; voice continuity.)

---

## Cross-client privacy state (EC-1 + cross-client transition)

Per PDR-005 v0.4 §MCP server scope sub-surface obligations + §experience fill-in EC-1 (recognition continuity): when a user moves between clients, the privacy state for past conversations stays where it was set (per-host conversation histories don't cross clients). What does cross clients is the **working memory layer** — which by design excludes private conversations.

### The cross-client invariant

The privacy commitment is **invariant across clients** (per EC-2 + EC-3): privacy means the same thing on every client. The implementation is per-conversation (1.0 scope); the commitment is universal.

**User experience**: a user who marked Conversation A private on MCP/Claude Desktop and switches to a (post-1.0) Slack client sees the same working-memory layer minus Conversation A's contributions. The privacy commitment held; the conversation transcript didn't transfer (that's per-client by design); the working memory exclusion did.

### What this surfaces for 1.0

Surface 2 today carries the **honest-about-limits framing** explicitly:
- Private is per-conversation, not per-message (post-1.0 expansion)
- Private state doesn't transfer between conversations on different clients (each conversation marked separately)
- The working memory layer's exclusion of private content is the cross-client guarantee

Surface 6 (welcome-back variant for cross-client transition) coordinates with Surface 2 here — when a user arrives on a new client, the first-run prose names what carried (working memory) and what didn't (per-host conversation history). Voice continuity required.

---

## Coordination with adjacent surfaces

### Surface 1 (History / archive)

The privacy indicator (Tier 3) lives inside Surface 1's history sidebar. Coordination:
- Per-conversation indicator visible in the conversation-list rendering
- Privacy state persists across history-view navigation
- Filter-by-private (in Surface 1's filter set) shows only marked-private conversations

Voice continuity: Surface 1 hover-tooltips + Surface 2 indicator language stay aligned (Comms voice-pass coordinates both).

### Surface 7 (Error / degraded / audit-read)

Surface 2 events flow into the audit envelope (per PPM Surface 2 unblocked signal scope clarification). Coordination:
- Privacy state changes (mark/unmark) appear as entries on the `/transparency` page
- `host_id` field in audit envelope captures which client surfaced the privacy change
- Banner stacking order: privacy banner (top) + Surface 7 degraded-mode banner (below) when both apply

Voice continuity: privacy banner + Surface 7 banner share the offer-first colleague register; neither contradicts the other.

### Surface 6 (First-run / welcome-back)

The welcome-back variant (for users arriving on a new client) names what carries across clients — including the privacy commitment's cross-client invariance. Coordination:
- First-run prose acknowledges working memory carries but per-host conversation histories don't
- If a user marks a conversation private on their first session, the toast voice (Tier 1) aligns with first-run framing

Voice continuity: first-meeting greetings + Surface 2 toast register stay aligned.

### Composing surfaces (existing)

Composing surfaces don't directly couple to Surface 2 in 1.0, but if a user composes content inside a private conversation, the composed artifact inherits the privacy commitment — the working-memory exclusion applies. This is automatic from the architectural side (per-conversation private flag flows through); no Surface 2 voice work needed beyond Tier 2 banner persistence.

---

## Decision rules for downstream design

When extending Surface 2 (new privacy-event types, new audit fields, new privacy granularity surfaces), apply these rules in order:

1. **Privacy is a commitment, not a feature**. The word "private" carries weight; voice register stays values-laden.
2. **Offer-first activation always**. Privacy is never imposed-by-default for any new event class; the user is the deciding actor.
3. **Honest about scope**. If a privacy claim is per-conversation, say so. If a privacy promise has a boundary (e.g., working memory exclusion only; the conversation itself still exists), name the boundary.
4. **Reversibility named, asymmetry acknowledged**. Privacy is reversible going forward; what was private at time-of-creation stays private even after unmarking. Both halves of the asymmetry surface in voice.
5. **Cross-client invariance preserved**. Whatever Surface 2 commits to on one client commits to on all clients (per EC-2 + EC-3). Per-host privacy variation is post-1.0; until then, the commitment is universal.
6. **No capability claims without verification**. Don't promise encryption, end-to-end, or any data-at-rest property unless the architectural commitment is in place (Pattern-064 prevention at the values-claim layer).
7. **Surface the audit-envelope coupling honestly**. Privacy state changes are logged; the user can see them on the transparency page. Don't hide this.

---

## Scope boundaries

This MUX doc commits to user-experience shape for Surface 2. It does NOT commit to:

- **Specific button colors, icon shapes, layout pixels** — implementation-time decisions per existing design-system conventions
- **Backend `is_private` schema or migration shape** — PPM Surface 2 unblocked signal + existing data-model substrate handle this
- **Per-message privacy granularity UX** — Round 2 ratified per-conversation for 1.0; per-message is post-1.0 expansion with its own UX shape
- **Per-host privacy semantics** — `host_id` schema commitment in PDR-005 v0.4 mechanism set #4 enables future migration; semantic decision deferred to follow-up ADR with HOST + CEO input
- **Encryption / data-at-rest claims** — not in 1.0; if surfaced later, the architectural commitment must precede the voice claim
- **Voice prose polish** — Comms voice-pass per ratified CXO→Comms→CXO→iterate pattern

---

## Cross-references

- **PDR-005 v0.4** (canonical reference for product commitments): `dev/active/PDR-005-bring-your-own-chat-draft-v0.4-2026-05-18.md`
- **PDR-005 §experience fill-in** (EC-1/EC-2/EC-3 framings this doc operationalizes): `mailboxes/cxo/sent/memo-cxo-to-ppm-cc-arch-comms-lead-pa-ceo-exec-pdr-005-consequences-for-experience-fill-in-2026-05-18.md`
- **MUX/UI Round 2 synthesis** (Surface 2 paired-deliverable shape; locked decisions): `mailboxes/cxo/sent/mux-ui-gap-cxo-round-2-synthesis-2026-05-15.md`
- **PPM Surface 2 unblocked signal**: `mailboxes/cxo/read/memo-ppm-to-lead-cc-cxo-arch-comms-pa-ceo-exec-surface-2-build-unblocked-pdr-005-v0.4-2026-05-18.md`
- **Surface 7 MUX doc** (offer-first cluster sibling; voice continuity reference): `docs/internal/design/mux/surface-7-error-degraded-audit-read-states.md`
- **PDR-004** (P1 colleague-not-system, P2 offer-first; canonical voice authorities): `docs/internal/product/pdrs/pdr-004-experience-philosophy.md`
- **Comms Round 1 input** (voice signals for Surface 2): `mailboxes/cxo/read/mux-ui-gap-comms-input-2026-05-15.md`
- **Empty-state voice guide** (voice anchor reference; especially "Confidence Without Pressure"): `docs/internal/design/specs/empty-state-voice-guide-v1.md`
- **Existing privacy substrate**:
  - Data model: `services/database/models.py:1059` (`is_private` column + `idx_conversations_user_private`)
  - Session-level: `services/memory/privacy_mode.py` (`PrivacyState` + `PrivacyModeManager`)
  - Recording skip: `services/memory/session_hooks.py:43`
  - API: `web/api/routes/user_history.py:152` (PATCH endpoint)
  - UI substrate: `templates/components/privacy_mode.html` (banner) + `templates/components/history_sidebar.html:316` (footer toggle) + `:330` (per-conversation icon)
  - Stub being replaced: `templates/privacy-settings.html` (Coming-Soon shell)
- **ADR-054** (Cross-Session Memory Architecture; Composted Learning layers that privacy excludes): `docs/internal/architecture/current/adrs/adr-054-cross-session-memory-architecture.md`
- **#1018 audit_transparency Phase 2** (privacy state changes captured in audit envelope): tracking issue + #1018 commit history
- **Calendar-offer policy** (voice borrowing source; offer-first-with-stakes register): TBD path; per Comms Round 1 framing

---

## Status and handoff

**This is the CXO first pass.** Per PM-ratified coordination pattern (May 18):

1. ✅ **Step 1 — CXO first pass**: this document
2. ⏳ **Step 2 — Comms voice-pass**: tone refinement, voice-guide editorial moves, flagging opacity / load-bearing words / superlatives. Particularly important here: this is "most net-new voice work" per Comms Round 1; expect substantive voice work
3. ⏳ **Step 3 — CXO review**: scope/structure preservation check; flag any drift; verify values-laden framing preserved through tone refinement
4. ⏳ **Step 4 — Iterate Steps 2–3 until aligned** (typically 1 cycle, possibly 2)

Comms picks up at Step 2 when bandwidth lands. No external deadline; PM directive is "best available pace, steady forward progress."

**Voice continuity note for Comms**: Surface 7 MUX doc v0.1 (filed May 18; awaiting Comms voice-pass) is the offer-first cluster sibling. Surface 2 + Surface 7 voice register should align when both surfaces appear in the same session (which is common — e.g., privacy banner + Surface 7 degraded-mode banner stacking). Comms voice-pass on both surfaces can coordinate.

— CXO, 2026-05-19 (v0.1 first-pass draft; Comms handoff pending)

---

## Step 2 audit log (Comms voice-pass, 2026-05-24)

### Edits made

Five targeted edits, all in user-rendered example strings (which carry public-prose voice discipline even though the surrounding doc is internal):

1. **Anti-pattern table "Reversibility named" example** (Voice anchor §"What Surface 2 voice does"):
   - Before: *"You can unmark this anytime; if you do, what we discussed becomes available for me to learn from going forward."*
   - After: *"You can unmark this anytime. If you do, what we discussed becomes available for me to learn from going forward."*
   - Reason: no-semicolons-in-public-prose discipline.

2. **Retroactive-private toast example** (Tier 1 §"Examples"):
   - Before: *"Marked this conversation private retroactively — earlier turns and going forward both. Any working-memory entries already created from earlier turns will be reconciled per ADR-054 Layer 3 cleanup."*
   - After: *"Marked this conversation private retroactively — earlier turns and going forward both. Anything I already learned from those earlier turns will be unwound."*
   - Reason: "ADR-054 Layer 3 cleanup" is operator-legible jargon leaking into a user-facing toast. The replacement preserves the asymmetry-acknowledged frame without naming the architecture. (Example remains contingent on PM ratification of a retroactive-mark UX, per CXO's parenthetical.)

3. **`/settings/privacy` page body paragraph 3** (§"What privacy means here"):
   - Before: *"...Earlier private turns stay private even if you unmark; what changes is that future turns become available for me to learn from."*
   - After: *"...Earlier private turns stay private even if you unmark — what changes is that future turns become available for me to learn from."*
   - Reason: no-semicolons-in-public-prose discipline. Em-dash preserves the contrast pivot.

4. **Privacy-across-clients explainer body paragraph 3** (§"Privacy across clients — explainer"):
   - Before: *"Per-host privacy semantics (different rules on different clients) is something we may design later; today, the rule is the same everywhere..."*
   - After: *"Per-host privacy semantics (different rules on different clients) is something we may design later. Today, the rule is the same everywhere..."*
   - Reason: no-semicolons-in-public-prose discipline.

5. **Privacy API failure error message** (§"Error states"):
   - Before: *"...If it keeps happening, the transparency page logs system events."*
   - After: *"...If it keeps happening, the transparency page will show what was logged."*
   - Reason: "logs system events" is API-documentation register (jargon shape) in a user-facing error. The replacement preserves the cross-page coordination (pointing to Surface 7 transparency page) in colleague voice.

### Voice strings left as-is

CXO's drafts are otherwise strong. Specifically, I left untouched:

- Three MARK_PRIVATE / UNMARK_PRIVATE toast examples (Tier 1) — beyond the retroactive-private edit above, the on-mark + on-unmark examples honor offer-first + honest-about-limits cleanly
- Two banner examples (Tier 2) — quiet-confidence register reads cleanly; "what we discuss here won't consolidate into long-term memory" is the right values-laden phrasing
- In-conversation indicator hover-tooltip (Tier 3) — short, accurate, no jargon
- `/settings/privacy` page header (*"Privacy here is a commitment, not a setting."*) — frames the values-laden spine cleanly
- `/settings/privacy` body paragraphs 1 + 2 (§"What privacy means here") — colleague register, honest-about-limits framing, no jargon
- Empty-state prose (*"You haven't marked any conversations private yet..."*) — honors empty-state voice guide
- "Your private conversations" header + cross-clients header — clean
- Privacy-across-clients explainer paragraphs 1 + 2 — honest-about-limits register reads cleanly
- 403 message — uniform-403-without-existence-leak per Surface 7 §"Error states" pattern

### Internal-doc prose left as-is

The "load-bearing" usage at §"Why this surface is load-bearing" + §UNMARK_PRIVATE ("The honest-about-limits framing is load-bearing...") stays canonical per the `load-bearing-is-crutch-word-in-public-prose` memory (internal docbase keeps load-bearing; public prose tilts to "critical"). The doc is internal; this is the right vocabulary.

Semicolons in analytical prose (anti-pattern table commentary, cross-reference list, decision-rules numbered items, the §Scope and §Coordination sections) — all appropriate for the internal spec.

Formal role names (Chief Experience Officer / Communications Director / etc.) — appropriate for internal.

### Two flags for CXO Step 3 (not changes I'd make alone)

1. **Terminology mix: "long-term memory" vs "working memory"** — the doc uses "long-term memory" in toasts / tooltips / banners (short-form colloquial) and "working memory" in long-form explainer prose on `/settings/privacy` (technical product term per ADR-054). The pattern works at register-by-context. Worth confirming intentional, especially given that "working memory" in cognitive-science vocabulary refers to the short-term active buffer (the opposite of what the product term means). Users who know cognitive science may parse "working memory I build about you over time" as backwards. May be bigger than this doc — but flagging here because Surface 2 is the values-laden anchor for the term.

2. **Retroactive-private contingency** — example #3 in Tier 1 still presupposes a PM-ratified retroactive-mark UX (CXO's parenthetical: "if PM ratifies"). After voice-pass, the voice is clean, but the example is voice-for-feature-not-yet-decided. Worth confirming whether to keep as forward-looking placeholder or pull until decided. (My instinct: keep — having voice in hand for the contingency is useful when the decision lands.)

Neither rises to scope/structure drift. Your call whether to fold or defer.

### Cross-reference verification

All cross-references in the doc checked: PDR-005 v0.4 EC-1 / EC-2 / EC-3 framing, ADR-054 layers, Surface 7 §"Error states" + §"Coordination with adjacent surfaces" + §"Banner ordering," PPM Surface 2 unblocked signal, MUX/UI Round 2 synthesis Surface 2 paired-deliverable shape, Comms Round 1 input "most net-new voice work" framing, empty-state voice guide invocation. No drift surfaced.

Calendar-offer-policy borrowing source still TBD-path per CXO (line 356). Not a Step 2 blocker; flagging for awareness.

### Status

- Step 1 ✅ (CXO v0.1, May 19)
- Step 2 ✅ (Comms voice-pass, May 24)
- Step 3 ⏳ (CXO scope/structure preservation review, CXO cadence)
- Step 4 ⏳ (iterate if needed)

— Comms (Communications Director), 2026-05-24
