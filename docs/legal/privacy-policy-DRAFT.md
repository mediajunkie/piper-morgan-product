# Privacy Policy — Piper Morgan

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

**When you disconnect a service, Piper Morgan revokes access at the provider, not merely locally.** For
GitHub, Slack, and Google Calendar, disconnection performs a provider-side OAuth revocation *and*
deletes the stored credential. *(Verified in `services/connectors/disconnect.py`.)*

## Your control over your data

**Disconnecting a service** stops all further access to it and revokes the credential as described above.

🔍 **Data deletion and export.** *Before publishing, state plainly what a user can actually do today:*
- *Is there a working account-deletion path that removes conversation history and derived state?*
- *Is there a data-export path?*
- *If either does not exist, say so and give a contact address for manual requests, rather than implying
  a self-service capability that isn't built. This is the single most likely place for this document to
  over-promise.*

🔍 **Retention.** *No retention policy was found in the code. Either state the real practice ("retained
until you delete your account") or define one. Do not state a period we don't enforce.*

## Alpha and beta software

Piper Morgan is pre-release software. Do not rely on it as the sole repository of information you cannot
afford to lose, and do not entrust it with mission-critical decisions without independent verification.
We aim to protect your data but cannot offer production-grade guarantees at this stage.

## Security

Access to user data is scoped per user. Credentials are stored in the OS keychain. Transport is over
HTTPS.

🔍 *Do not add stronger security claims (encryption at rest, audit logging, penetration testing, SOC 2)
without a specific verified basis. Unsupported security claims are the highest-risk sentences in a
privacy policy.*

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
