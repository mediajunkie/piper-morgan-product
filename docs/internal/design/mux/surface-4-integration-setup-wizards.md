# Surface 4 MUX Doc — Integration Setup Wizards (GitHub + Calendar + Notion)

**Document Type**: MUX specification (Class A — calibrated voice surface; Class D — state-changing)
**Author**: Chief Experience Officer (CXO first pass)
**Co-author (pending)**: Communications Director (voice-pass per ratified CXO→Comms→CXO→iterate pattern)
**Date**: 2026-05-20 (v0.1 first-pass draft)
**Implements**: MUX/UI Round 2 Surface 4 (GitHub + Calendar + Notion wizards for 1.0; Slack deferred post-1.0); PDR-005 v0.5 §Decision §Bespoke UI commitment depth + §Persona portability + §Consequences for experience EC-2 + EC-4
**Status**: First-pass draft awaiting Comms voice-pass

---

## Scope

Surface 4 is the **integration setup wizards** surface. It covers the first-time-connect moment for each of three 1.0-scoped integrations (GitHub + Calendar + Notion) plus the ongoing connection-state surfaces those wizards leave behind.

The wizard pattern is **template-driven**: one MUX doc shape covers all three wizards. Per-integration voice + scope-explanation language varies, but the template is shared.

Surface 4 covers five coordinated user-facing dimensions:

1. **The pre-connect moment** — how Piper offers an integration before connection (offer-first activation)
2. **The OAuth flow itself** — the consent screen, the scope explanation, the redirect handling
3. **The post-connect confirmation** — what Piper says immediately after a successful connection
4. **The connection-state surface** — how the user inspects + manages connected integrations going forward
5. **The disconnect moment** — how the user removes an integration and what that means

This surface is **trust-extension-bearing**. Per Comms Round 1: *"First-time-Notion-connect or first-Slack-OAuth is a moment of trust extension. The story is 'Piper asks before it looks; here's what it's looking at; here's what changes when you connect.'"*

### Why this surface is load-bearing

Per Comms Round 1: *"OAuth wizards default to system-utility voice everywhere on the web. Letting the dev default fill in here is the highest-risk option in the set per Lead Dev's framing. Without explicit guidance, Notion/GitHub/Slack/Calendar wizards will read like 2015 SaaS onboarding."*

Surface 4 is also where PDR-005's persona portability variance hierarchy meets a concrete capability boundary. Per §experience fill-in EC-2: *"Whatever Piper says it can do, it can do identically across clients."* Integration wizards are the surface where capability claims become consent surfaces — what the wizard asks permission to do must match what the integration actually does. Pattern-064 prevention applies at the values-claim layer.

### What 1.0 scope is (per Round 2 ratification + PPM Surface 4 unblocked signal)

- **Three integration wizards**: GitHub + Calendar + Notion (each with OAuth flow + scope selection + connection state surface)
- **Shared template**: one wizard shape with per-integration prose customization
- **Connection-state management surface**: `/settings/integrations` (existing overview at `templates/integrations.html` with status dots; needs full wire-up per Round 2)
- **Per-integration page**: `/settings/integrations/{name}` (existing per-integration pages need voice-pass + wire-up to wizard flow)
- **First-run wizard**: `/setup` (existing `templates/setup.html`; coordinates with Surface 6 first-run)
- **Audit envelope coupling**: connect/disconnect events captured in audit envelope with `host_id` field (Surface 7 coordination); `host_id` commitment enables future cross-host migration

### What 1.0 scope is NOT

- **Slack wizard** — deferred per Round 2 (12,213 LOC substrate; explicit defer rather than half-wizard)
- **Token rotation / re-auth flow UX** — partially in scope (basic re-auth-required state surfaced); full automated rotation post-1.0
- **Cross-integration aggregation** — each integration manages its own state; cross-integration views are post-1.0
- **End-to-end encryption claims** — not in 1.0; if surfaced in voice, it must be true (Pattern-064 prevention)

---

## Voice anchor

Surface 4 voice is **trust-extension-moment + offer-first + capability-claim-truthful**. Each wizard is a moment where Piper asks permission, names what it will do with the access, and confirms what changes when the user agrees.

### Three voice spines (Comms framing, Round 1; offer-first cluster)

1. **Offer-first activation** — Piper offers the integration; the user decides whether and when to connect. Integration is never the default state imposed; it's the user-chosen state surfaced
2. **Capability-claim truthful** — whatever the wizard says Piper will do with the access matches what the integration actually does (Pattern-064 prevention at the consent surface)
3. **Always-useful close** — every wizard state (offer / consenting / connecting / connected / failed / disconnect) leaves the user with a concrete next step

### Borrowing source

Surface 4 has two sources:

- **Compose surfaces** (per Comms Round 1) — already gracefully degrade when integrations are unreachable. Surface 4 inherits this register — connection failure during setup is not an error message; it's *"we'll try again, here's what works without it."*
- **Calendar-offer policy** (offer-first-with-stakes voice register) — Surface 4 borrows the same posture across all three wizards. Surface 4 IS where the calendar-offer policy lives, formalized

The Surface 7 MUX doc + Surface 2 MUX doc are **structural siblings** in the offer-first cluster; voice continuity across Surfaces 2/4/7 matters because they often appear in the same session.

### What Surface 4 voice avoids

| Failure mode | Why it's wrong |
|---|---|
| *"Click here to authorize access to GitHub"* | 2015 SaaS onboarding voice; treats the user as configuring software, not a colleague extending trust |
| *"GitHub integration successfully configured. ✓"* | Status-message voice; gives the user nothing about what changes for them |
| *"Connect GitHub to unlock powerful features"* | Marketing voice; "unlock powerful features" is a vague promise; violates capability-claim-truthful |
| *"Required scopes: repo, read:user, write:issues"* (without explanation) | Operator-legibility leak; tech voice; doesn't say what the user is consenting to in their own terms |
| *"⚠️ This integration requires the following permissions"* | Alarm-pulse voice; treats permissions as warnings rather than the user's deliberate grant |
| *"Connection failed. Error: 401 Unauthorized."* | Stack-trace voice; gives the user no path forward |
| *"You don't have permission to disconnect this integration"* (without explanation) | Power-asymmetry voice; treats the user as needing approval from the system |

### What Surface 4 voice does

| Pattern | Example |
|---|---|
| Trust-extension framing | *"Connecting GitHub means I'll be able to look at your issues, branches, and PRs when you ask me about them. I won't push code or open PRs unless you ask me to."* |
| Capability-claim explicit | *"What this lets me do: pull recent issues into our conversation when you reference them. What this does NOT do: post comments, close issues, or change repository settings."* |
| Offer-first phrasing | *"Want to connect Calendar? I can offer to schedule things and check your availability when you mention dates. You can disconnect anytime."* |
| Scope-explanation in user terms | *"GitHub will ask for these accesses: read your repos (so I can find the right ones), read issues + PRs (so I can pull them into our conversations), write issues (only when you ask)."* |
| Connection-failure useful | *"Couldn't reach GitHub right now. We can try again, or pick up without it — most of what you ask me works without GitHub connected."* |
| Disconnect honest | *"Disconnected GitHub. I'll stop pulling from your repos. The conversations we had with GitHub context stay where they are; I just won't reach back to GitHub going forward."* |

---

## Surface 4 inventory (the shared wizard template)

Each integration wizard follows the **same 5-step template** with per-integration prose customization:

### Step 1 — Offer (pre-connect moment)

**When it fires**: User encounters an integration entry-point — either via `/setup` first-run flow (Surface 6 coordination), via `/settings/integrations` overview, or via Piper offering the integration in-conversation (e.g., user mentions GitHub repos and Piper offers to connect).

**Form**: Inline offer in conversation OR card on integrations page OR step in setup wizard.

**Voice register**: One-to-three sentences naming what the integration does + offer-first close. No alarm; no marketing.

**Per-integration prose (drafts; Comms voice-pass):**

- **GitHub offer**: *"Want to connect GitHub? I can pull issues, look at PRs, and reference your code when you ask. I won't push anything unless you tell me to."*
- **Calendar offer**: *"Want to connect Calendar? I can check availability and offer to schedule things when dates come up. Read-only by default — I'll ask before adding anything."*
- **Notion offer**: *"Want to connect Notion? I can pull from your docs and databases when you reference them. Read-only by default — I won't change anything unless you ask."*

**Anti-pattern**: Don't auto-trigger the OAuth flow from the offer. The offer leads to Step 2 (review scope), not directly to consent.

### Step 2 — Review scope (the consent surface)

**When it fires**: User has accepted the offer from Step 1. Before the OAuth redirect, Piper shows what the user is about to grant.

**Form**: Modal or dedicated page (per design system convention); cannot be skipped.

**Voice register**: Plain-language scope list + capability-claim explicit + cancel-anytime close. This is the **load-bearing consent surface** — what gets said here is what the user is consenting to. Pattern-064 prevention: every claim here must match actual integration behavior.

**Per-integration prose (drafts; Comms voice-pass):**

**GitHub Step 2 (consent surface):**
> *"GitHub will ask for these accesses on the next screen:*
>
> *— **Read your repos** (so I can find the right ones when you mention them)*
> *— **Read issues and pull requests** (so I can pull them into our conversations)*
> *— **Write issues** (only used when you explicitly ask me to file one)*
>
> *What this lets me do: pull recent issues + PRs into our conversation when you reference them. What this does NOT do: push code, close issues without your say-so, change repository settings.*
>
> *Ready to head to GitHub to grant these? You can cancel from there if you change your mind."*

**Calendar Step 2 (consent surface):**
> *"Calendar will ask for these accesses on the next screen:*
>
> *— **Read your calendars** (so I can check availability)*
> *— **Read your events** (so I can reference what's scheduled when you ask)*
>
> *Write access (creating, editing, deleting events) isn't included in the initial connect — if you want me to schedule things directly, we can add that later.*
>
> *What this lets me do: check what you have scheduled and offer to coordinate around it. What this does NOT do: create events, send invites, or modify your calendar.*
>
> *Ready to head to Calendar to grant these?"*

**Notion Step 2 (consent surface):**
> *"Notion will ask for these accesses on the next screen:*
>
> *— **Read pages and databases** in workspaces you choose (so I can pull from your docs when you reference them)*
>
> *Notion's permission model is workspace-scoped — you'll pick which workspaces I can see. Write access isn't included; I won't change anything unless we add it later.*
>
> *What this lets me do: reference content from the workspaces you grant access to. What this does NOT do: create pages, edit existing pages, or move things around.*
>
> *Ready to head to Notion to grant these?"*

**Anti-pattern**: Don't list scope identifiers (e.g., `repo`, `read:user`) without plain-language explanation. The scope is what the user is consenting to; the user must understand it in their terms, not the OAuth provider's.

### Step 3 — Redirect to provider (out-of-band OAuth flow)

**When it fires**: User clicks "Continue to {provider}" from Step 2. The user is now on the provider's OAuth screen.

**Form**: The user is OUT of Piper UI on the provider's surface. Piper has no voice here.

**What Piper does**: Wait for the redirect back. If the redirect doesn't return within reasonable time, surface a re-engagement state on next Piper visit ("did the connection go through?").

**No Piper voice in this step** — the user is in the provider's UI by design.

### Step 4 — Confirm (post-connect moment)

**When it fires**: User completes OAuth on the provider's side and is redirected back to Piper. Token is now in `integration_config_service.py`; integration state changes from "connecting" → "connected".

**Form**: Toast (in-conversation) OR confirmation page (if coming from `/setup` or `/settings/integrations`).

**Voice register**: One sentence confirming the connection + one phrase naming what's now possible + first-use suggestion. Always-useful close.

**Per-integration prose (drafts; Comms voice-pass):**

- **GitHub confirm**: *"GitHub's connected. I can pull issues, look at PRs, and reference your code now. Want me to look at what's open on your main repo to start?"*
- **Calendar confirm**: *"Calendar's connected. I can check availability and reference what's scheduled. Want me to take a look at today?"*
- **Notion confirm**: *"Notion's connected — I can see the workspaces you granted. Want to point me at a doc to start with?"*

**Anti-pattern**: Don't surface internal token IDs, scope strings, or "successfully configured" status-message voice. The confirm voice names what changes FOR the user, not what changed in the system.

### Step 5 — Connection state surface (ongoing)

**When the user lands here**: They navigated from `/settings/integrations` overview, from a per-integration page link, or from Piper referring back to integration state. This is the **ongoing connection-state surface** for each connected integration.

**Form**: Per-integration page (existing `templates/settings_github.html`, `settings_calendar.html`, `settings_notion.html`; needs voice-pass + state-machine wire-up).

**State machine** (per Architect Round 1 input + Lead Dev build-cost lens):

| State | UI label (draft; Comms voice-pass) | Available actions |
|---|---|---|
| `connected` | *"Connected"* | Disconnect; Test connection |
| `connecting` | *"Setting up..."* | (No actions during transient state) |
| `degraded` | *"Connected, but having trouble reaching {provider}"* | Test connection; Disconnect |
| `failed` | *"Connection failed — last tried {time}"* | Reconnect; Disconnect; See what happened |
| `re-auth-required` | *"Connection expired — needs to refresh"* | Reconnect; Disconnect |
| `not_configured` | *"Not connected yet"* | Connect (jumps to Step 1) |

**Per-integration page layout** (consistent across all 3):

```
{Integration name} integration
────────────────────────────────
State: {state label}
What this lets me do: {capability-claim explicit list}
What this does NOT do: {non-capability explicit list}

[Actions: state-appropriate buttons]
[Last connected: {time}]
[Audit log: see what I've done with this connection → links to /transparency Surface 7]
```

**Voice principles applied**: capability-claim explicit + offer-first (action buttons frame as choices) + Surface 7 coordination via transparency link.

---

## OAuth + scope explanation UX

The **scope explanation in user terms** is the highest-leverage voice work in Surface 4. Per Comms Round 1, the failure mode is operator-legibility leak: showing the user `read:user` and `write:issues` without translation.

### Scope translation table (canonical for 1.0; Comms voice-pass)

**GitHub scopes**:

| OAuth scope | Plain-language label | What the user is granting |
|---|---|---|
| `repo` | "Read your repos" | "So I can find the right ones when you mention them" |
| `repo` (write portion) | "Write issues" | "Only used when you explicitly ask me to file one" |
| `read:user` | "Read your profile" | "Used to know whose repos to look at" |
| `read:org` | "See your organizations" | "Used to find org repos you have access to" |

**Calendar scopes** (Google Calendar):

| OAuth scope | Plain-language label | What the user is granting |
|---|---|---|
| `calendar.readonly` | "Read your calendars" | "So I can check availability" |
| `calendar.events.readonly` | "Read your events" | "So I can reference what's scheduled when you ask" |

**Notion scopes** (workspace-scoped, not capability-scoped):

| Notion permission | Plain-language label | What the user is granting |
|---|---|---|
| Workspace read | "Read pages and databases in this workspace" | "So I can pull from your docs when you reference them" |

### Scope-pickup rule (canonical for downstream design)

When a new OAuth scope is requested in a wizard (now or post-1.0), the canonical pattern is:

1. **Scope identifier internal** — the OAuth scope string lives in `integration_config_service.py` only
2. **Plain-language label** — what the user sees in the consent surface (Step 2)
3. **"What this lets me do" sentence** — the user's understanding of why this scope is being requested
4. **"What this does NOT do" sentence** (if scope is broader than the capability claim) — explicit constraint, even if technically the scope allows more

The third + fourth sentences are the Pattern-064 prevention discipline at the consent surface.

---

## Connection state UX (ongoing surfaces)

### `/settings/integrations` overview (existing, needs voice-pass)

**Current state**: `templates/integrations.html` with status dots (`healthy`/`degraded`/`failed`/`unknown`/`not_configured`). Voice register currently dev-default.

**Voice-pass target** (drafts; Comms):

**Header**: *"Integrations Piper can reach"*

**Per-integration card layout**:

```
{provider name + icon}
{state label in plain language}
{one-line capability summary}

[Connect] | [Manage] | [Disconnect]
```

**Empty state** (user has no integrations connected):

> *"No integrations connected yet. I can work with most things you ask me about without integrations — they just let me pull live data from the places you already use."*

**Voice principles applied**: factual + always-useful (no integrations isn't a failure state) + offer-first (Connect button is invitation, not requirement).

### Degraded-state surfacing (Surface 7 coordination)

When an integration enters `degraded` or `failed` state mid-session, Surface 7 banner/toast pattern applies. From Surface 4's side, the per-integration page surfaces the current state with context.

**Voice continuity**: Surface 4 connection-state language + Surface 7 degraded-mode language stay aligned. The same `degraded` integration shouldn't be described differently on the per-integration page vs. in a Surface 7 banner.

### Disconnect flow

**Voice register**: Confirmation step naming what disconnect means. Reversibility named.

**Drafts (Comms voice-pass):**

- **Pre-disconnect confirmation**: *"Disconnect GitHub? I'll stop pulling from your repos. The conversations we already had with GitHub context stay where they are — I just won't reach back to GitHub going forward. You can reconnect anytime."*
- **Post-disconnect toast**: *"Disconnected GitHub. I'll stop pulling from your repos. You can reconnect anytime from the integrations page."*

**Anti-pattern**: Don't make disconnect feel like a destructive operation. It's not destroying anything; it's revoking access. The voice should reflect that.

---

## Cross-client integration state (EC-1 + EC-2 + EC-5)

Per PDR-005 v0.5 §experience fill-in EC-2 (capability claim consistency) + EC-5 (context-coordination continuity): integration state lives in the server domain layer, not in the client. When a user connects GitHub from MCP/Claude Desktop and then arrives on a (post-1.0) Slack client, GitHub is still connected — same capability, same scope, same server-side connection state.

### What this surfaces for 1.0

Surface 4 today carries the **cross-client invariance** implicitly: server-side state, not client-side state. The user doesn't need to reconnect GitHub on each client.

What surfaces explicitly:
- The per-integration page shows the same state regardless of which client surfaced the request
- Disconnect on any client disconnects everywhere (the integration access is server-scoped, not client-scoped)
- Per-client integration variation is NOT a 1.0 commitment — if post-1.0 surfaces a need (e.g., "I want GitHub connected only on this client"), that's a separate ADR + UX design

### Voice register for cross-client moments

When a user arrives on a new client and sees that integrations carry over (per Surface 6 welcome-back variant):

> *"GitHub and Calendar are connected from when we set them up on Claude Desktop — same access here. Notion is still set up too. Want me to use any of them for what we're starting with?"*

This is Surface 6 voice referencing Surface 4 state; voice continuity required.

---

## Coordination with adjacent surfaces

### Surface 6 (First-run / welcome-back)

The `/setup` first-run wizard (existing `templates/setup.html`) is where new users encounter Surface 4 integrations in the bundled setup flow. Coordination:

- `/setup` walks user through Surface 6 first-meeting greeting → offers (Surface 4 Step 1) for one or more integrations → consent (Surface 4 Step 2) per integration
- Voice register: first-run register (per Surface 6 template-driven voice) folds into Surface 4 offer register at the integration step
- Cross-client first-meeting variant ("welcome back") names already-connected integrations (per EC-2 capability claim consistency)

Voice continuity: Surface 4 offer prose + Surface 6 first-run prose stay aligned in register.

### Surface 7 (Error / degraded / audit-read)

Surface 4 events flow into the audit envelope:
- Connect event captured with `host_id` field
- Disconnect event captured with `host_id` field
- Re-auth events captured
- Integration tool-call results captured per Surface 7's audit-envelope read surface

Coordination:
- Per-integration page links to `/transparency` filtered to that integration's events
- Surface 7 toast/banner pattern surfaces integration degraded state in-session
- Voice continuity across Surface 4 connection-state language + Surface 7 degraded-mode language

### Surface 2 (Privacy controls)

Integration tool calls within a private conversation respect the privacy commitment — the integration call happens, but the result + reasoning don't consolidate into working memory layer. Coordination:

- Surface 4 per-integration page doesn't need a privacy variant (integration state is per-user, not per-conversation)
- The privacy commitment applies to the integration's tool-call results within the conversation, not to the integration connection itself
- This nuance can be surfaced on the per-integration page if user-research signal post-1.0 indicates confusion

Voice continuity: Surface 2 + Surface 4 voice register stay aligned (offer-first cluster siblings).

### Composing surfaces (existing)

Composing surfaces are where the user encounters integration capability in practice. Surface 4 is the connection layer; composing surfaces are where the connection is exercised. Voice continuity matters because:

- Composing surfaces that gracefully degrade when integrations are unreachable should match Surface 4's connection-state language
- Capability claims in composing surfaces ("I can pull from GitHub") must match Surface 4 consent-surface claims (EC-2)

---

## Decision rules for downstream design

When extending Surface 4 (new integrations post-1.0, new scopes, new state-machine states), apply these rules in order:

1. **Capability-claim truthful at the consent surface always**. What the wizard says Piper will do with the access must match what the integration actually does (Pattern-064 prevention at the consent layer).
2. **Scope translation in user terms always**. OAuth scope strings live internal-only; the user sees plain-language labels + capability framings + non-capability framings.
3. **Offer-first activation at the integration entry-point**. Integration is never the default state imposed; user decides whether and when to connect.
4. **No alarm-pulse on permissions**. Permissions are the user's deliberate grant, not warnings to be defended against.
5. **Reversibility named at every state change**. Connect names disconnect; disconnect names reconnect.
6. **Cross-client invariance preserved**. Integration state lives in server domain layer; same state on every client (per EC-2). Per-client variation is post-1.0 and requires separate ADR.
7. **Surface the audit-envelope coupling honestly**. Per-integration page links to `/transparency` filtered to that integration's events. Don't hide this.
8. **Disconnect is not destructive**. The voice register treats disconnect as access revocation, not data deletion.

---

## Scope boundaries

This MUX doc commits to user-experience shape for Surface 4. It does NOT commit to:

- **Specific button colors, layout pixels, icon shapes** — implementation-time decisions per existing design-system conventions
- **Backend OAuth flow handlers or `integration_config_service` schema** — Lead Dev Phase 2.2 Surface 4 build handles this
- **Slack integration UX** — explicitly deferred per Round 2 ratification; if/when Slack returns to 1.0 scope, follows this same template
- **Cross-integration aggregation views** — each integration manages its own state; cross-integration is post-1.0
- **Per-host integration semantics** — `host_id` schema commitment in PDR-005 v0.5 mechanism set #4 enables future migration; semantic decision deferred to follow-up ADR
- **Automated token rotation UX** — basic re-auth-required state surfaced; full automated rotation post-1.0
- **Encryption / data-at-rest claims** — not in 1.0; if surfaced later, the architectural commitment must precede the voice claim
- **Voice prose polish** — Comms voice-pass per ratified CXO→Comms→CXO→iterate pattern

---

## Cross-references

- **PDR-005 v0.5** (canonical reference for product commitments): `dev/active/PDR-005-bring-your-own-chat-draft-v0.5-2026-05-19.md`
- **PDR-005 §experience fill-in** (EC-1/EC-2/EC-4/EC-5 framings this doc operationalizes): absorbed into v0.5; original at `mailboxes/ppm/read/memo-cxo-to-ppm-cc-arch-comms-lead-pa-ceo-exec-pdr-005-consequences-for-experience-fill-in-2026-05-18.md`
- **MUX/UI Round 2 synthesis** (Surface 4 paired-deliverable shape; integration pick + locked decisions): `mailboxes/cxo/sent/mux-ui-gap-cxo-round-2-synthesis-2026-05-15.md`
- **PPM Surface 4 unblocked signal**: `mailboxes/cxo/read/memo-ppm-to-lead-cc-cxo-arch-comms-pa-ceo-exec-surface-4-build-unblocked-pdr-005-v0.4-2026-05-18.md`
- **Surface 2 MUX doc v0.1** (offer-first cluster sibling; voice continuity reference): `docs/internal/design/mux/surface-2-privacy-per-conversation-controls.md`
- **Surface 7 MUX doc v0.1** (offer-first cluster sibling; voice continuity reference; audit-envelope coupling): `docs/internal/design/mux/surface-7-error-degraded-audit-read-states.md`
- **PDR-004** (P1 colleague-not-system, P2 offer-first, P4 LLM-floor; canonical voice authorities): `docs/internal/product/pdrs/pdr-004-experience-philosophy.md`
- **Comms Round 1 input** (voice signals for Surface 4; "highest-narrative-arc opportunity"): `mailboxes/cxo/read/mux-ui-gap-comms-input-2026-05-15.md`
- **Existing integration substrate**:
  - GitHub: `services/integrations/github/` (3,516 LOC; `production_client.py`, `repo_resolver.py`, `issue_analyzer.py`)
  - Calendar: `services/integrations/calendar/` (1,946 LOC; #790 trust-gated calendar shipped May 5)
  - Notion: `services/integrations/notion/` (1,092 LOC; #304 NOTION-ACTIVATE closed)
  - Shared: `web/api/routes/settings_integrations.py:323` (Slack OAuth start; pattern for others)
  - Config service: `integration_config_service.py` (token storage)
  - UI substrate: `templates/integrations.html` (overview), `templates/settings_{github,calendar,notion,slack}.html` (per-integration), `templates/setup.html` (first-run wizard `#390`)
- **#1075 route-prefix migration** (CLOSED May 16): Surface 4 callback URL stability dependency RESOLVED
- **#1018 audit_transparency Phase 2**: integration connect/disconnect events captured in audit envelope
- **ADR-051 RequestContext** (host_id flows through; #1015 Phase 4): `docs/internal/architecture/current/adrs/adr-051-request-context.md`
- **Calendar-offer policy** (voice borrowing source for offer-first-with-stakes register; canonical surface): TBD path; per Comms Round 1

---

## Status and handoff

**This is the CXO first pass.** Per PM-ratified coordination pattern (May 18):

1. ✅ **Step 1 — CXO first pass**: this document
2. ⏳ **Step 2 — Comms voice-pass**: tone refinement, voice-guide editorial moves, flagging opacity / load-bearing words / superlatives. Particularly important here per Comms Round 1: *"highest-narrative-arc opportunity"* + *"highest-risk-of-dev-default-voice"* — Comms voice-pass on Surface 4 has the largest gap between "what dev default produces" and "what the surface needs"
3. ⏳ **Step 3 — CXO review**: scope/structure preservation check; verify trust-extension framing preserved through tone refinement
4. ⏳ **Step 4 — Iterate Steps 2–3 until aligned** (typically 1 cycle, possibly 2)

Comms picks up at Step 2 when bandwidth lands. No external deadline; PM directive is "best available pace, steady forward progress."

**Voice continuity note for Comms**: Surface 4 + Surface 2 + Surface 7 are the three full MUX docs in the offer-first cluster. All three v0.1 drafts now awaiting voice-pass. Voice register continuity across all three matters; Comms voice-pass on the cluster can coordinate.

**Highest-leverage voice work in Surface 4** (per Comms Round 1):
- The Step 2 consent-surface prose for each of GitHub/Calendar/Notion (scope translation in user terms; capability-claim explicit; non-capability explicit)
- The Step 1 offer prose for each integration (trust-extension framing in 1-3 sentences)
- The state-machine labels on the per-integration page (plain-language state names that don't sound like dev-utility status messages)

— CXO, 2026-05-20 (v0.1 first-pass draft; Comms handoff pending)
