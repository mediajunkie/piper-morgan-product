# Surface 7 MUX Doc — Error / Degraded / Audit-Read States (User-Facing Audit Envelope)

**Document Type**: MUX specification (Class A — calibrated voice surface)
**Author**: Chief Experience Officer (CXO first pass)
**Co-author (pending)**: Communications Director (voice-pass per ratified CXO→Comms→CXO→iterate pattern)
**Date**: 2026-05-18 (v0.1 first-pass draft)
**Implements**: MUX/UI Round 2 Surface 7 (paired deliverable with ADR-063); PDR-004 P4 (LLM-floor guarantee — never apologize for missing capability)
**Status**: First-pass draft awaiting Comms voice-pass

---

## Scope

Surface 7 is the **error / degraded / audit-read** surface set. It covers three coordinated user-facing dimensions:

1. **In-conversation moments** when something the system did (decline, redact, fall back) becomes user-visible (toast hierarchy)
2. **Session-level state** when the system is operating in degraded mode (banner hierarchy)
3. **Audit-envelope read pages** — the dedicated `/transparency` surface where the user can inspect what the system decided about their content (page hierarchy)

This is the **READ-side complement to ADR-061's WRITE-side four-element principle**. ADR-063 codifies the architecture; this document codifies the user experience.

### Why this surface is load-bearing

Per MUX/UI Round 2 synthesis: *"This IS the load-bearing architectural piece — without it, ADR-061's four-element principle is observably 3.5 elements in user-facing terms."*

The audit envelope is being written into the system. Without the read surface, operator legibility is structurally one-sided: the system knows what it did; the user has no path to inspect what was recorded. Surface 7 closes that gap at the user experience layer.

---

## Voice anchor

Surface 7 voice is **honest-about-limits without alarm or melodrama**.

### Three voice spines (Comms framing, Round 1)

1. **Colleague, not system** — never apologize for missing capability (PDR-004 P4); never blame the user; never narrate the decline as failure
2. **Offer-first** — when the system declines, surface the alternative path; the user is the deciding actor
3. **Always useful** — every error/degraded/audit state leaves the user with a concrete next step

### Borrowing source

Surface 7 borrows from **compose** and **insights** surfaces, both of which already model degraded states (e.g., when sources are unreachable or the model is slow). The cross-cutting error voice should match what those surfaces already do — quiet, factual, action-oriented.

### What Surface 7 voice avoids

| Failure mode | Why it's wrong |
|---|---|
| *"An error occurred. Please try again."* | Dev-default voice; violates every voice spine; gives the user nothing actionable |
| *"Sorry, I can't help with that."* | Apology for missing capability (violates PDR-004 P4); shifts the problem to the user |
| *"I noticed you tried to share something sensitive."* | Implies user did something wrong; surveillance tone; violates colleague-not-system |
| *"Critical safety violation detected."* | Melodramatic; treats the user as adversary; alarming rather than honest |
| *"Service unavailable. Code: 500."* | Operator-legibility leak into user surface; the user doesn't know what to do with a 500 |

### What Surface 7 voice does

| Pattern | Example |
|---|---|
| Honest about what happened | *"I redacted what looked like an email address from that — let me know if I got something wrong."* |
| Honest about what's degraded | *"Running on the fallback model right now — answers might be slower or thinner than usual."* |
| Honest about what's outside scope | *"That's not something I'm in a position to weigh in on. Want to try a different angle?"* |
| Honest about what's logged | *"I logged this conversation as ethics-decision: harassment-redirect — you can see why on the transparency page."* |

---

## Surface 7 inventory

Surface 7 has **three coordinated UI tiers** plus the **dedicated transparency page**. The same audit-envelope content surfaces at different times in different shapes; voice register is consistent across tiers.

### Tier 1 — Toast (in-conversation moment)

**When it fires**: A discrete decision happened in the current conversation that the user should know about, but the conversation continues. Examples:
- A PII pattern was redacted from the system's output (the user can see the redacted form; the toast names what got redacted)
- An ethics decision fired (the system declined a path or routed to a safer one; the toast names the category)
- A tool call failed and a fallback was used

**Form**: Top-right toast (existing `templates/components/toast.html` + `web/static/js/toast.js`).

**Voice register**: One sentence, action-oriented close. The toast names what happened and points to the transparency page for detail.

**Examples (drafts; Comms voice-pass):**

- *"Redacted an email address in my reply — see why on the transparency page."*
- *"Declined that path — it landed inside the harassment boundary. Try a different angle?"*
- *"Couldn't reach GitHub — used cached results from earlier today."*

**Anti-pattern**: Don't surface internal request IDs, hash markers, or model version in the toast. Those belong on the transparency page (or internal-only).

### Tier 2 — Banner (session-level state)

**When it fires**: The system is operating in a degraded mode that affects the whole session — not a one-time decision, but a state. Examples:
- LLM fallback model is in use for the session
- A required integration is unreachable
- Audit-write is temporarily failing (rare; safety condition)
- Trust-stage 1 banner (existing pattern; coordinate with first-run state framing per Surface 6)

**Form**: Top-of-screen banner (coordinate with existing trust-stage banner + privacy banner conventions).

**Voice register**: One sentence stating the state + one sentence on what changes for the user. No alarm. No apology for the substrate.

**Examples (drafts; Comms voice-pass):**

- *"Running on the fallback model right now. Answers might come slower or feel thinner — usual model should be back soon."*
- *"GitHub's not reachable from here. I'll use what I cached this morning until it comes back."*
- *"Audit logging is paused right now — I'm keeping track separately and will reconcile when it's back."*

**Anti-pattern**: Banners shouldn't blink, color-shift, or pulse. Surface 7 banners are quiet-and-present, not attention-stealing.

### Tier 3 — Page (full-page error states)

**When it fires**: The session itself cannot proceed. Examples:
- Network error (existing `templates/network-error.html`)
- 404 (page not found — existing `templates/404.html`)
- 500 (server error — existing `templates/500.html`)
- Auth-required (route requires JWT user isn't bound to)

**Voice register**: Three lines max. Name what's happening, name what the user can do, name where to go next.

**Examples (drafts; Comms voice-pass):**

- 404: *"That page isn't around. Want to go back to your conversations, or start a new one?"*
- 500: *"Something went wrong on my end. Refresh — usually that's enough. If it keeps happening, the transparency page logs system events."*
- Auth-required: *"That page wants a sign-in. Want to head there now, or pick up where you left off?"*

**Anti-pattern**: No raw stack traces, no error codes in the headline, no "support@" email surfaces (the user is the colleague, not a customer with a help desk).

### Tier 4 — Transparency page (the dedicated audit-envelope read surface)

**When the user lands here**: They navigated from a toast ("see why on the transparency page"), from a banner ("see what got logged"), from settings, or from direct curiosity. This is the **dedicated read surface for audit envelopes** per ADR-063.

**Routes** (per ADR-063):
- `/api/v1/transparency/audit-log/{session_id}` (user-scoped, JWT-bound to session ownership)
- `/api/v1/transparency/audit-summary/{session_id}` (admin-summary form; structurally 403 in production until SEC-RBAC)
- `/api/v1/transparency/stats`, `/cleanup`, `/health` (admin-only; structurally 403 in production)

**UX pattern detailed below in §"Transparency page UX."**

---

## Severity → presentation hierarchy

The audit envelope has a `severity` field (CRITICAL / IMPORTANT / INFORMATIONAL). Severity drives presentation tier, not the content of voice.

| Severity | Tier | Voice register |
|---|---|---|
| CRITICAL | Banner if session-affecting; toast if discrete + transparency-page entry | Direct + action-oriented; no alarm-pulse |
| IMPORTANT | Toast + transparency-page entry | Brief + factual; one alternative-path offer |
| INFORMATIONAL | Transparency-page entry only (no toast/banner) | Logged-for-the-record; user can browse if curious |

**Decision rule**: CRITICAL severity does NOT mean "alarm the user." It means "the user should be aware in-flight." The voice stays steady; the surfacing is what shifts.

---

## Per-event-type rendering

The audit envelope's `event_type` and `action_taken` fields drive the specific voice register. Three primary action classes:

### DECLINE (the system declined an output path)

**Toast voice** (in-conversation):
> *"That came out wrong — let me try a different approach."*

This is the **CXO Q3 canonical phrasing** adopted by Lead Dev as the production constant for category-violation drops (per #1017). The toast surfaces alongside this in-conversation message — naming what category triggered, pointing to transparency page for detail.

**Toast example:**
> *"Declined that path — it landed in the harassment category. See transparency for the full envelope."*

**Transparency-page entry voice:**
> *"Ethics decision: harassment-redirect. The system declined to produce content that targeted a named third party with undermining advice. Action: redirected with safer framing."*

### REDACT (the system redacted content but allowed the rest)

**Toast voice:**
> *"Redacted what looked like an email address in my reply — see why on the transparency page."*

**Transparency-page entry voice:**
> *"PII redaction: email pattern detected in response. Original content kept. The matching string was replaced with `<REDACTED-email>`. The decision is automated — if it looks wrong, flag it."*

**Redaction-marker UX**: When redacted content appears in the user-visible read surface, render redaction markers explicitly — never silently drop content.

Format: `<REDACTED-{type}>` where `{type}` is one of: `email`, `ssn`, `phone`, `credit-card`, `api-key`, `bearer-token`, `url-with-credentials`.

The marker is **visible as a marker**, not styled to disappear. Users should be able to see that redaction happened.

### ALLOW (the system allowed the output but logged the decision)

**Surfaced via transparency page only** — no toast, no banner. The event is in the audit envelope for record-keeping; the user can browse if curious but isn't notified inline.

**Transparency-page entry voice:**
> *"Routine decision: output passed all filter gates. Logged for transparency."*

This category exists so the audit-envelope log is complete (not just decline/redact events) — important for the "user can see what the system decided about them" promise.

---

## Transparency page UX

The transparency page lives at `/transparency` (or similar; final route per Lead Dev Phase 2.1 build).

### Layout

**Two top-level views, toggled via tab:**

1. **My conversation transparency** (default; user-scoped) — shows audit-log entries for the current session or selected past session. Calls `/api/v1/transparency/audit-log/{session_id}`.
2. **System overview** (admin tab; structurally 403 in production until SEC-RBAC) — shows aggregated stats. Calls `/api/v1/transparency/audit-summary/{session_id}` + `/stats`.

### My conversation transparency — primary view

**Header**: Brief one-line context: *"Decisions the system made during this conversation, with reasons."*

**Entry list**: Each audit-log entry surfaces these user-visible fields (per ADR-063):

| Field | UI rendering |
|---|---|
| `timestamp` | Human-readable relative time (*"3 minutes ago"*) with full timestamp on hover |
| `event_type` | Plain-language label (e.g., *"Ethics decision"*, *"PII redaction"*, *"Tool fallback"*) — NOT the internal enum name |
| `boundary_category` (if present) | Plain-language label (e.g., *"Harassment boundary"*, *"Professional boundary"*) |
| `action_taken` | Plain-language phrase (*"Redirected with safer framing"*, *"Redacted from response"*) |
| `severity` | Visual weight, not labeled prose: CRITICAL = solid left border (color: muted; not alarm-red); IMPORTANT = thin left border; INFORMATIONAL = no border |
| Content excerpt (redacted) | Two-line preview of what got logged; redaction markers visible per Redaction-marker UX |

**Each entry expandable** for the full envelope detail (still user-visible fields only).

### Empty / no-events state

When the session has zero audit-log entries (the audit envelope is empty for this session):

> *"Nothing logged for this conversation yet. The system records ethics decisions, redactions, and tool fallbacks here as they happen."*

**Voice principles applied**: factual + teaching-by-example + no apology for the empty state. Compare empty-state voice guide §"Confidence Without Pressure."

### Sort / filter

- Default sort: most recent first
- Filter: by event_type (multi-select), by date-range, by severity (single-select)
- Per ADR-063 conventions, response model declares filter contract; UI just renders

### System overview (admin tab — 403 handling)

In production today (and until SEC-RBAC global-admin lands), this tab returns 403 for every caller. The admin endpoints (`/audit-summary`, `/stats`, `/cleanup`, `/health`) exist architecturally but no non-admin can reach them.

**The UI affordance**: Show the tab; click renders an empty-state with this voice:

> *"This view is for system-level transparency across all sessions. It's locked to administrators today — when role-based admin access lands, authorized users will see aggregated stats here. For your own conversation, the My Conversation tab has everything you can see."*

**Voice principles applied**: honest about the limit (locked to administrators today); honest about the future state (when role-based access lands); always useful (points the user back to the conversation-scoped view).

**Anti-pattern**: Don't hide the tab. Surface the existence of the admin view (transparency about transparency); explain the access boundary.

### Error states (transparency API failure)

When `/api/v1/transparency/audit-log/{session_id}` fails (network, server error, partial data):

> *"Couldn't load the audit log right now. Refresh — usually that's enough. If it keeps happening, something's off underneath — give it a few minutes and try again."*

When the JWT-binding rule fires (the user isn't authorized to view this session):

> *"That conversation isn't in your view — only the person who had it can see its transparency log."*

(Uniform 403 messaging per ADR-063 Commitment 3 — avoid existence-leak; don't distinguish "session doesn't exist" from "you can't see it.")

---

## Coordination with adjacent surfaces

### Surface 2 (Privacy controls)

Privacy banner already exists (`templates/components/privacy_mode.html`). Surface 7 banners coexist; **session-level state ordering**:
1. Privacy banner (top; if `is_private` for this conversation)
2. Trust-stage banner (if `window.trustStage = 1`)
3. Degraded-mode banner (Surface 7; if degraded state active)

Voice continuity: privacy banner + Surface 7 banner should not contradict each other. Both use offer-first colleague register.

### Surface 6 (First-run / empty states)

First-meeting flow (templated voice per CEO ratification of Round 2; NOT four-element-principle-bound at greeting composition layer). Coordinate so first-run users see Surface 7 banners appropriately — degraded-mode banner during first conversation should be quiet (the system shouldn't lead with "I'm degraded").

### Composing surfaces (existing)

Surface 7 borrows from composing and insights — both already gracefully degrade when sources are unreachable. Match their voice rather than inventing a new register.

---

## Decision rules for downstream design

When extending Surface 7 (new event types, new audit fields, new error states), apply these rules in order:

1. **Severity drives presentation tier, not voice**. CRITICAL means "user should be aware in-flight"; voice stays steady.
2. **Default new audit fields to internal-only** (per ADR-063 default-to-internal rule). Surfacing requires deliberate decision + voice register on how to render it.
3. **One sentence at the toast tier (with an optional inviting fragment); three lines max at the page tier**. Surface 7 voice is quiet-and-direct, not verbose. The inviting fragment is the close that turns a notice into a colleague handoff (*"Try a different angle?"*); it stays brief.
4. **Every state has a next step**. Apply "always useful" — even a 500 page suggests refresh; even a 403 message offers an alternative path.
5. **Never apologize for capability** (PDR-004 P4). Decline → name the limit + offer alternative. Don't say "sorry."
6. **Render redaction markers, don't silently drop content** — the user should know redaction happened, with what type.

---

## Scope boundaries

This MUX doc commits to user-experience shape for Surface 7. It does NOT commit to:

- **Specific button colors, font sizes, layout pixels** — implementation-time decisions per existing design-system conventions
- **Backend audit-envelope schema** — ADR-063 captures that; this doc captures the read-surface UX
- **SEC-RBAC global-admin shape** — separate ADR when it lands; this doc captures the 403-handling UX for the structural admin-403 state today
- **Per-message audit granularity** — Round 2 ratified per-conversation for 1.0; per-message is post-1.0 expansion path with its own UX shape
- **Voice prose polish** — Comms voice-pass per ratified CXO→Comms→CXO→iterate pattern

---

## Cross-references

- **ADR-063** (architectural companion): `docs/internal/architecture/adrs/adr-063-user-facing-audit-envelope-read-surface.md`
- **ADR-061** (WRITE-side four-element principle): `docs/internal/architecture/adrs/adr-061-llm-touch-boundary-enforcement.md`
- **Pattern-071** (Audit Logs as Attack Surface): `docs/internal/architecture/patterns/pattern-071-audit-logs-as-attack-surface.md`
- **MUX/UI Round 2 synthesis** (Surface 7 paired-deliverable shape; locked 6 decisions): `mailboxes/cxo/sent/mux-ui-gap-cxo-round-2-synthesis-2026-05-15.md`
- **MUX/UI Round 2 CEO ratification**: `mailboxes/cxo/read/memo-arch-to-cxo-lead-comms-ppm-cc-ceo-pa-exec-mux-ui-round-2-ceo-ratification-2026-05-16.md`
- **Empty-state voice guide** (voice anchor reference): `docs/internal/design/specs/empty-state-voice-guide-v1.md`
- **PDR-004** (P4 — LLM-floor guarantee; canonical voice authority for "never apologize for capability"): `docs/internal/product/pdrs/pdr-004-experience-philosophy.md`
- **Transparency route surface** (Lead Dev #1095, May 16; slices 1+2 May 17): `services/api/transparency.py`
- **Service layer**: `services/ethics/audit_transparency.py:343` (get_user_audit_log); `:33` (SecurityRedactor)
- **CXO Q3 phrasing** (#1017 canonical canned-response): *"That came out wrong — let me try a different approach."* (`mailboxes/cxo/sent/memo-cxo-to-lead-cc-arch-ceo-1017-q3-phrasing-q7-timing-2026-05-15.md`)
- **Comms Round 1 input** (voice signals for Surface 7): `mailboxes/cxo/read/mux-ui-gap-comms-input-2026-05-15.md`

---

## Status and handoff

**Step 1 + Step 2 complete.** Per PM-ratified coordination pattern (May 18):

1. ✅ **Step 1 — CXO first pass**: this document
2. ✅ **Step 2 — Comms voice-pass**: completed 2026-05-24. Edits + audit log below.
3. ⏳ **Step 3 — CXO review**: scope/structure preservation check; flag any drift
4. ⏳ **Step 4 — Iterate Steps 2–3 until aligned** (typically 1 cycle, possibly 2)

### Comms voice-pass audit (Step 2)

The CXO first pass already lands the voice cleanly. The doc names the three voice spines (colleague-not-system, offer-first, always-useful) and applies them consistently across all four tiers. The example strings are tonally aligned with the empty-state voice guide and with PDR-004 P4. My Step 2 pass was small.

**Edits made:**

1. **Semicolon split in PII-redaction transparency-page entry** (the entry voice that renders to the user on `/transparency`): *"Original content kept; the matching string was replaced... The decision is automated; if it looks wrong, flag it."* → split into separate sentences + one em-dash. Two semicolons removed. Rationale: user-rendered strings count as public-prose voice; the no-semicolons-in-public-prose convention applies even though this document is internal.
2. **Jargon leak in transparency API error state**: *"...something's off on the substrate side"* → *"...something's off underneath — give it a few minutes and try again"*. Rationale: "substrate side" is operator-legible language leaking into a user-rendered string. The replacement keeps the honest-about-limits register without the implementation-shaped vocabulary.

**Voice strings left as-is** (CXO's drafts are good):

- All four toast examples (DECLINE, REDACT, tool-fallback, ethics-decision) read with the colleague-not-system register cleanly.
- The three banner examples have the quiet-and-present quality the doc names; the "feel thinner than usual" phrasing in the fallback-model banner has a casual Xian-voice character worth keeping.
- The three page examples (404 / 500 / Auth-required) honor the "always useful" spine and avoid raw error codes.
- The CXO Q3 canonical phrasing for category-violation drops (*"That came out wrong — let me try a different approach."*) is the locked production constant per #1017; not subject to voice-pass.
- The empty / no-events state and admin-tab 403 entry both honor the empty-state voice guide.
- The JWT-binding 403 message (*"That conversation isn't in your view — only the person who had it can see its transparency log."*) is the right register — uniform 403 without existence-leak per ADR-063 Commitment 3.

**Voice characterizations in the prose (non-example text)** — left as-is:

- "Load-bearing" appears in the §"Why this surface is load-bearing" header + a quote from the Round 2 synthesis. Per the `load-bearing-is-crutch-word-in-public-prose` memory, this stays canonical in internal docbase. The doc is internal; this is the right vocabulary here.
- Semicolons in the doc's analytical prose stay — internal-doc convention.
- Role-names in formal long-form (Chief Experience Officer, Communications Director, Lead Developer, etc.) are appropriate for an internal spec document.

**Two small things Surface 7 doesn't yet specify** (flagged for CXO Step 3, not changes I'd make alone):

1. **Voice register for the "trust-stage 1 banner coordination with Surface 6"** is named but not exemplified. When this surface coexists with the first-run Surface 6 framing, an example sentence or two would help the implementer know how to harmonize the two registers without contradiction. Worth picking up in iteration if Surface 6 doc has matching examples to anchor against.
2. **Toast pacing rule** — the doc says "one sentence" for toast voice. Some of the examples are one sentence + one fragment ("Try a different angle?"). Worth specifying whether a trailing question-fragment counts as same-sentence or whether the rule is "one sentence + optional inviting fragment." Either way works; clarity helps the implementer.

Neither rises to scope/structure drift. CXO ratify or push back.

**Cross-references checked**: ADR-063 routes confirmed; ADR-061 commitments confirmed; PDR-004 P4 framing confirmed; empty-state voice guide invoked correctly; CXO Q3 phrasing attribution confirmed against `memo-cxo-to-lead-cc-arch-ceo-1017-q3-phrasing-q7-timing-2026-05-15.md`.

— Comms, 2026-05-24 (Step 2 voice-pass complete; CXO Step 3 review handoff)

— CXO, 2026-05-18 (v0.1 first-pass draft)
