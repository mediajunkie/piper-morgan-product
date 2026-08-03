"""#1466 — Slack-linking flow copy, in constants rather than code paths.

The division ratified 2026-08-03 (Lead memo / Arch ratification / CXO flow
spec): CXO owns the link-flow UX and copy; strings live HERE (the
decline/confirm tables), never inline in mechanism code, so copy is adjustable
without touching the mechanism.

Sources, verbatim where specified:
- CXO flow spec: dev/active/design-spec-slack-linking-flow-1466-2026-08-03.md
  §3a (unlinked decline — THE load-bearing string), §3b (confirmations, both
  sides), §3c (unlink).
- Arch ratification conditions 1+2 (rate-limit + already-linked declines are
  not in CXO's spec; written to CXO's §3a requirements table: say plainly what
  Piper knows/doesn't, never imply user error, carry the path, no apology
  cadence).

Formatting note: CXO's spec renders the decline link as a bold button-ish
link ("[**Link your account**]"). On the Slack surface that is mrkdwn:
``<url|label>``. The words are CXO's verbatim; only the link markup is
surface-adapted.
"""

# --- §3a — the unlinked decline (the actual first contact for this surface) ---

UNLINKED_DECLINE_PROSE = (
    "I don't know who you are on this Slack yet, so I can't get to your todos — "
    "they're tied to your Piper account and I've no way to tell which one is yours."
)

# {link_url}: deep link to the settings link section, carrying the caller's
# slack_user_id/team_id as opaque params (CXO §2 — a one-click path, not an
# instruction; post-login the section renders "Link this Slack account" with
# the code pre-minted).
UNLINKED_DECLINE_LINK_LINE = (
    "<{link_url}|Link your account> — takes about twenty seconds, "
    "and then `/standup` and your todos work here."
)


def unlinked_decline(link_url: str) -> str:
    """The full §3a decline: prose + the link as a link."""
    return UNLINKED_DECLINE_PROSE + "\n" + UNLINKED_DECLINE_LINK_LINE.format(link_url=link_url)


# --- §3b — confirmations (both sides say different things) ---

# In Slack, where the user just acted: names the next action (they're mid-flow).
LINKED_CONFIRMATION_SLACK = (
    "Linked — you're {slack_handle} here and {piper_account} in Piper. "
    "Try `/standup`, or ask me what's on your plate."
)

# In Piper settings, where they'll return later: a status line.
LINKED_CONFIRMATION_SETTINGS = "Slack linked — {slack_handle} in {workspace}. Unlink any time."

# --- §3c — unlink (states the consequence) ---

UNLINK_CONFIRMATION = (
    "Unlinked. Piper won't respond to you in {workspace} until you link again."
)

# --- Arch condition 2 — re-link of an already-linked identity: fail-closed,
# named honestly, with the unlink-first path carried. Never a silent no-op,
# never an owner overwrite. ---

ALREADY_LINKED_DECLINE = (
    "This Slack account is already linked to a Piper account, so this code can't "
    "move it. To relink it somewhere else, unlink first in Piper under "
    "Settings → Integrations → Slack, then redeem a fresh code."
)

# --- Arch condition 1 — bounded redemption attempts: fail-closed, honest ---

RATE_LIMITED_DECLINE = (
    "Too many link attempts from this Slack workspace just now, so I've stopped "
    "checking codes for a bit. Wait about ten minutes and try again."
)

# --- redemption misses (wrong/expired/spent code) ---

INVALID_CODE_DECLINE = (
    "That code didn't match an active link code — codes work once and expire "
    "after about ten minutes. Mint a fresh one here: <{link_url}|Link your account>."
)

# --- /link with no code supplied ---

LINK_USAGE_PROMPT = (
    "Send `/link` with the 6-digit code from your Piper settings — "
    "<{link_url}|mint one here>, then try `/link 123456` with your code."
)
