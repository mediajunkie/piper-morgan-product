# Privacy Policy — Piper Morgan

> ⛔ **CORRECTED 2026-08-02 — READ THIS BEFORE USING THIS DRAFT.**
> **A privacy policy URL already exists and is live: `https://pipermorgan.ai/privacy` returns HTTP 200.**
> My 7/31 statement that *"no public privacy policy page exists"* was **wrong**. I inferred it from the
> absence of a policy doc in this repo and never checked the live site — a `curl` would have settled it.
> **That is the fifth instance this fortnight of asserting a fact I could have checked in seconds**, and
> the most wasteful, because I drafted a whole document on top of it.
>
> ⚠️ **But do not swing the other way either — here is exactly what is and isn't established:**
> - ✅ `/privacy` returns **200**, title *"Privacy Policy - Piper Morgan"*.
> - ✅ **Server-rendered visible text is 29 characters.** Strip scripts and tags and the page contains its
>   title and nothing else. My first pass counted *"data" ×23 / "collect" ×11* — **those matches were in
>   the JavaScript bundle, not policy prose.** I nearly reported that as "it's substantive."
> - ❓ **Unknown**: whether it renders a real policy client-side in a browser. I cannot execute JS.
>
> 🔴 **Why the JS point is the actionable part, not pedantry**: Anthropic's rule is that *"missing or
> incomplete privacy policies result in immediate rejection,"* and directory review — human or
> automated — may fetch without JS. **A policy that requires JavaScript to appear can read as absent to
> the thing that matters.** Ten seconds in a browser settles it; I can't.
>
> **So this document's status changes**: not a replacement for a missing policy, but a **gap-checklist to
> audit the live one against.** The five 🔍 markers below are the questions to ask of whatever is
> actually published.

> ⚠️ **DRAFT — NOT FOR PUBLICATION AS-IS. PM review required.**
> **Why it exists**: both the Claude plugin directory and OpenAI's MCP submission require a public
> HTTPS privacy policy, and *"missing or incomplete privacy policies result in immediate rejection"*
> (Anthropic docs, verbatim). This is directory-blocking for both targets.
> **How it was written**: grounded in the actual code, not a template. Every factual claim below was
> checked against `services/`. **Items marked 🔍 could not be verified and must be confirmed or cut
> before publishing** — a privacy policy that promises behavior the system doesn't implement is worse
> than having none, because it converts a gap into a misrepresentation.
> **Publish to**: `https://pipermorgan.ai/privacy` (the website repo is not checked out on Amber —
> `~/Development/piper-morgan-website` does not exist here, so publication needs that repo).
> **Drafted by PA, 2026-07-29.**

---

**Last updated:** [DATE ON PUBLICATION]

Piper Morgan is an AI product-management assistant operated by Design in Product (Christian Crumlish).
This policy explains what data Piper Morgan handles, who it is shared with, and what control you have
over it. It covers the hosted service at `pipermorgan.ai` and the Piper Morgan plugin and MCP connector.

## What we collect

**Account information.** Your email address and authentication credentials, used to identify you and
secure your account.

**Conversation content.** The messages you exchange with Piper Morgan, and the documents, tickets, and
notes you provide or ask it to work with. This is stored so that Piper retains context across sessions —
persistence is a core function of the product, not an incidental byproduct.

**Connected-service data.** When you connect a third-party service, Piper Morgan accesses data from it
on your behalf. Currently supported: **GitHub, Notion, Slack, Google Calendar**, and local Git
repositories. Piper reads the data needed to perform the tasks you ask of it, and writes only where you
have directed it to (for example, filing an issue you asked it to file).

**Working state.** Piper Morgan derives and stores working state about how you work — inferred
preferences (such as communication style and level of technical detail), project context, and summaries
of prior work. This is what allows it to behave like a colleague rather than a fresh assistant each
session. This derivation is **rule-based, not model-inferred**.

**Operational data.** Logs and diagnostics necessary to run and debug the service.

## What we do NOT do

- **We do not sell your data.**
- **We do not use your content to train our own models.** Piper Morgan does not train models.
- **We do not use your data for advertising.**

## Who your data is shared with (sub-processors)

**Large language model providers.** To generate responses, your conversation content and relevant
context are sent to a third-party model provider. Depending on configuration, this may be
**Anthropic, OpenAI, or Google**. Their handling of that data is governed by their own terms.

**Hosting and infrastructure.** The service runs on **Fly.io**, with data stored in PostgreSQL, Redis,
and a vector database used for search and retrieval.

**Services you explicitly connect.** Data flows to and from GitHub, Notion, Slack, and Google Calendar
only for accounts you have connected and only as needed for the actions you request.

🔍 *Confirm this list is complete and name the specific provider(s) actually in production before
publishing — an incomplete sub-processor list is a compliance exposure, not just an omission.*

## Credentials and access tokens

OAuth tokens and API keys for connected services are stored in the operating-system keychain, not in
plaintext application storage.

⛔ **CORRECTED 2026-08-04 — the previous wording was FALSE for GitHub and must not be published.**
It read: *"When you disconnect a service, Piper Morgan revokes access at the provider, not merely
locally. For GitHub, Slack, and Google Calendar, disconnection performs a provider-side OAuth
revocation."* **Verified per-connector rather than in aggregate:**

| connector | provider-side revoke? | what actually happens |
|---|---|---|
| **Slack** | ✅ **yes** | `SlackOAuthHandler.revoke_workspace_access(user_id)` before the local clear |
| **Google Calendar** | ✅ **yes** | `GoogleCalendarOAuthHandler().revoke_token(refresh_token)` (the #542 fix) |
| **GitHub** | ❌ **NO** | keychain PAT + env + config-cache deleted, binding → `UNBOUND`, and `ConnectorGrantStore().delete(session, …)` — **a local DB row, not a GitHub API call** |

🔴 **Why this one is the dangerous direction**: a user told their GitHub access was revoked
provider-side **will not go revoke it**, and a live token keeps working. Overstating *permanence* on a
soft delete costs a user an unnecessary worry; overstating *revocation* costs them an active credential
they think is dead. **A privacy policy must not make the second error.**

**Honest replacement text** — do not restore the aggregate sentence:

> When you disconnect Slack or Google Calendar, Piper Morgan revokes the authorization at the provider
> and deletes the stored credential. When you disconnect GitHub, we delete the stored credential and
> end the connection on our side; **the authorization may remain listed in your GitHub settings until
> you remove it there.**

*(Last clause adopted from HOST's amended string — Comms is right that it's the best-written of the
three, and it's the only one carrying a user action.)*

⚠️ **Same defect, separate artifact, already corrected**: `dev/active/delete-copy-map-2026-08-03.md`
claimed LLM **API keys** are "revoked at the provider." Also false — `delete_user_key` is keychain + DB
only, and no provider revocation is structurally possible. **Two instances, two code paths, one root
cause: I read the word `revoke` in a docstring where it named a local operation and carried it
outward.**

## Your control over your data

**Disconnecting a service** stops all further access to it and revokes the credential as described above.

✅ **Data deletion and export — ANSWERED FROM THE CODE 2026-08-03. These were never PM questions and I
should not have deferred them.**

⚠️ **"Delete" in this product means SOFT delete, and a policy must not say otherwise.**

| capability | reality | source |
|---|---|---|
| **Account deletion** | ❌ **Does not exist.** No account-level deletion path anywhere. | searched `services/`, `web/api/routes/` |
| **Conversation deletion** | ⚠️ **SOFT** — a lifecycle transition, `ACTIVE/ARCHIVED → DELETED (terminal, no return)`. The record is marked, not removed. | `web/api/routes/conversations.py:716` |
| **Insight deletion** | ⚠️ **SOFT** — sets `is_deleted=True`; the row remains. Reset-all is `soft_delete_all`. | `repositories.py:2328,2350` |
| **Connector credentials** | ✅ **HARD, and better than most** — provider-side OAuth revocation *plus* keychain deletion. | `services/connectors/disconnect.py` |
| **Data export** | ⚠️ **Exists but narrow** — `GET /controls/export` returns **learning settings + learned patterns only.** Not conversations, not profile, not connector data. | `web/api/routes/learning.py:1320` |

🔴 **The load-bearing consequence**: a sentence like *"you can delete your data"* would be a
**misrepresentation** — the honest phrasing is that deletion **marks records as deleted and stops them
being served**, that **credentials are genuinely destroyed and revoked**, and that **account deletion is
by request** (with the contact address below) **because no self-service path exists.**

That is exactly the *"converts a gap into a misrepresentation"* risk this draft warns about — and I would
have shipped it as a question to PM rather than an answer, which would have put the burden of a code
audit on the person least placed to do it.

🔍 **Retention.** *No retention policy was found in the code. Either state the real practice ("retained
until you delete your account") or define one. Do not state a period we don't enforce.*

## Alpha and beta software

Piper Morgan is pre-release software. Do not rely on it as the sole repository of information you cannot
afford to lose, and do not entrust it with mission-critical decisions without independent verification.
We aim to protect your data but cannot offer production-grade guarantees at this stage.

## Security

Access to user data is scoped per user. Credentials are stored in the OS keychain. Transport is over
HTTPS.

✅ **Verified, keep as written.** Credentials are in the OS keychain (`keychain_service.py`); access is
owner-scoped (ADR-079); transport is HTTPS. **Do not add encryption-at-rest, audit-logging, penetration
testing or SOC 2** — none has a verified basis, and unsupported security claims are the highest-risk
sentences in a privacy policy.

## Children

Piper Morgan is not directed to children under 13 and we do not knowingly collect their data.

## Changes to this policy

We will update this page when practices change, and revise the "Last updated" date above.

## Contact

Questions, deletion requests, or privacy concerns: **[CONTACT EMAIL — PM to supply]**

---

### Reviewer checklist before publishing

- [ ] Resolve every 🔍 marker — each is an unverified claim, not a wording choice
- [ ] Confirm the sub-processor list is complete and name the production LLM provider(s)
- [ ] State the true deletion/export capability, including "not yet available, email us"
- [ ] State a retention practice that matches reality
- [ ] Supply a contact email
- [ ] PM review — this is a legal commitment, not documentation
- [ ] Publish at a stable HTTPS URL and reference it in both directory submissions
