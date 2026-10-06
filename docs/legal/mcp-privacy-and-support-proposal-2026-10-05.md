# Proposal: privacy-policy MCP section + a support page

**Author**: PA, 2026-10-05, at PM's request. **Status**: proposal for PM's review. The voice pass goes to
Comms, and the website edit is Web's to make once PM approves. **Nothing here is live.**

Why now: every directory we plan to list in asks for a privacy-policy URL and a support contact. The
live `pipermorgan.ai/privacy` ("Last updated: May 2026") never mentions MCP, connectors, ChatGPT or
Claude, and `pipermorgan.ai/support` is a 404.

Every factual statement below was checked against the code on 2026-10-05; the source is noted in brackets.
**If the server changes, this copy must change with it.** (Same lockstep rule as the consent page.)

---

## A. New privacy-policy section (insert after "Data Sharing and Third Parties")

### Using Piper from ChatGPT, Claude and other AI assistants

You can connect Piper to an AI assistant you already use, such as ChatGPT or Claude, through Piper's
connector at `mcp.pipermorgan.ai` (built on the Model Context Protocol, "MCP"). Here is what that
connection does and doesn't do.

**What the assistant can read.** Only with your approval, given on a Piper sign-in page, and only
read-only:
- your Piper profile: organization, active projects and stated priorities;
- your colleague model: the things Piper has confirmed with you about how you work;
- your open GitHub issues, read through the GitHub account you connected to Piper.

The assistant **cannot change anything** in Piper through this connection, and it **cannot see
another person's data**. [The server exposes three read-only resources and one read-only tool; every
request is tied to the account that approved it; per-user isolation is tested (#1458).]

**Where your data goes.** When your assistant reads from Piper, that information goes to the assistant's
provider (for example OpenAI or Anthropic) as part of your conversation. From then on it's handled
under **that provider's** privacy terms, not ours. Piper does not run its own AI model on this
connection. [PDR-006: a pure tool server, no server-side LLM.]

**What Piper keeps about the connection.**
- A record of each connected assistant app: the name it registers with and its sign-in callback
  addresses. [`mcp_oauth_clients`: `client_name`, `redirect_uris`]
- Access credentials, **stored only as one-way hashes, never in readable form**. [`identity.py`:
  SHA-256 `hash_credential`] Access tokens expire after one hour; the longer-lived token that renews
  them expires after 30 days. [`oauth_provider.py`: `ACCESS_TOKEN_TTL`, `REFRESH_TOKEN_TTL`]
- When each connection was created and last used. [`last_used_at`]
- Standard technical request logs (time, address requested, result), kept for security and
  troubleshooting.

Piper **does not receive your conversations** with the assistant. It only receives the specific
requests your assistant makes to read the items listed above.

**Turning it off.** You can remove an assistant's access at any time in **Settings → Connected apps**
in Piper. It stops working immediately. Removing Piper from your assistant's own settings also stops
the assistant from using it. ⚠️ *Gate: publish this paragraph only after the Revoke fix (`87e8bc9c49`) is
live on alpha and has been seen working. Until then, omit the first sentence.*

---

## B. A support page: `pipermorgan.ai/support`

**Piper Morgan support**

**Contact**: `<SUPPORT ADDRESS — PM to choose>`. We read every message. During the beta, expect a reply
within <N> business days. *(PM: pick a real, monitored address. Directory reviewers and users will write
to it, so it must be watched.)*

**Connecting Piper to ChatGPT or Claude**
- Add a connector with the URL `https://mcp.pipermorgan.ai/mcp`.
- You'll be sent to Piper to sign in and approve read-only access.
- Then ask your assistant: "What does Piper know about me?"

**Something isn't working**
- *"No tools" or "action discovery failed"*: remove the connector and add it again, so your assistant
  picks up Piper's current tools.
- *The assistant says it has no access*: you may have revoked it, or it may have expired. Reconnect from
  your assistant.
- *Parts of the answer are empty*: that's honest, not broken. Piper only reports what it actually
  has, and a new account has little in its colleague model yet.

**Removing access**: Settings → Connected apps in Piper (see the gate above), or remove Piper from your
assistant.

**Privacy**: see [our privacy policy](/privacy).

---

## Decisions for PM
1. **The support address.** It's the one blocking choice.
2. Approve section A's facts (they're code-checked, but it's your policy), then route to Comms for voice
   and Web to publish. Bump the policy's "Last updated" date.
3. The "Turning it off" sentence waits for the Revoke fix to be live and seen working.
