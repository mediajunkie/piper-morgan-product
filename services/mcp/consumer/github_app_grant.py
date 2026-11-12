"""#2342 (ADR-081 D3): the GitHub App grant record and the switch that turns App mode on.

**App mode** is keyed on configuration, never on the deploy (Arch 2026-11-12 06:51): it is
on only when BOTH ``GITHUB_APP_CLIENT_ID`` and ``GITHUB_APP_CLIENT_SECRET`` are present.
One alone is never a half-on mode; ``app_mode_config_warning`` names the missing one for
the startup log. With App mode off, connect, the resolver and the classic OAuth App behave
exactly as before this module existed.

**The grant record** is one value in the encrypted ``github_mcp_oauth`` row: the user
access token, its expiry, the refresh token, its expiry, and the marker
``minted_by: github_app``. One row, so a refresh rewrites both tokens in one write
(GitHub spends the refresh token it is given; ADR-081, refresh notes).

How a stored value is classified when read (Arch's condition on the record):

* does not start with ``{``: a **classic** grant, which is a bare token string and the
  only shape any writer has ever stored one in (``classify`` returns None);
* starts with ``{`` and is anything but a complete, marked record (it does not parse,
  it lost or mangled its marker, a token or an expiry is missing): a **read failure**
  (``GrantRecordDamaged``). Never classic, or a damaged App grant would be marked
  ``cutover``, its user told the wrong thing, and the cutover script would delete it
  (Arch 2026-11-12 06:51, corrected 07:24).

Neither token ever appears in a ``repr``, a log line or an exception message.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Optional, Tuple

MINTED_BY_APP = "github_app"

ENV_APP_CLIENT_ID = "GITHUB_APP_CLIENT_ID"
ENV_APP_CLIENT_SECRET = "GITHUB_APP_CLIENT_SECRET"
ENV_APP_SLUG = "GITHUB_APP_SLUG"

#: Refresh when the access token has less than this left (Arch accepted 5 minutes).
REFRESH_SKEW_SECONDS = 300

#: The ``connector_bindings.status_reason`` values. Only these two are ever written.
REASON_CUTOVER = "cutover"
REASON_REFRESH_REJECTED = "refresh_rejected"


class GrantRecordDamaged(Exception):
    """A stored value that claims to be an App grant record but can't be used as one.
    A read failure (#2151's contract), never a classic grant."""


def app_client() -> Tuple[str, str]:
    """The App's client ID and secret from the environment only (no keychain fallback)."""
    return (
        os.getenv(ENV_APP_CLIENT_ID, "").strip(),
        os.getenv(ENV_APP_CLIENT_SECRET, "").strip(),
    )


def app_mode() -> bool:
    """True only when both the App's client ID and its secret are configured."""
    client_id, client_secret = app_client()
    return bool(client_id and client_secret)


def app_mode_config_warning() -> Optional[str]:
    """The startup warning for a half-set configuration, or None. Names the missing
    variable, never a value."""
    client_id, client_secret = app_client()
    if bool(client_id) == bool(client_secret):
        return None
    missing = ENV_APP_CLIENT_SECRET if client_id else ENV_APP_CLIENT_ID
    present = ENV_APP_CLIENT_ID if client_id else ENV_APP_CLIENT_SECRET
    return (
        f"GitHub App mode is OFF: {present} is set but {missing} is not. "
        "Both are needed; the classic OAuth App keeps serving."
    )


def app_install_url() -> Optional[str]:
    """Where a person installs the App on repositories, or None when no slug is set."""
    slug = os.getenv(ENV_APP_SLUG, "").strip()
    return f"https://github.com/apps/{slug}/installations/new" if slug else None


@dataclass(frozen=True)
class GitHubAppGrant:
    """A user access token minted by the published GitHub App, with its refresh token.
    Expiries are Unix seconds."""

    access_token: str
    access_expires_at: int
    refresh_token: str
    refresh_expires_at: int

    def __repr__(self) -> str:  # never a token
        return (
            "GitHubAppGrant(access_expires_at="
            f"{self.access_expires_at}, refresh_expires_at={self.refresh_expires_at})"
        )

    def encode(self) -> str:
        return json.dumps(
            {
                "minted_by": MINTED_BY_APP,
                "access_token": self.access_token,
                "access_expires_at": int(self.access_expires_at),
                "refresh_token": self.refresh_token,
                "refresh_expires_at": int(self.refresh_expires_at),
            },
            separators=(",", ":"),
        )

    def access_expired(self, now: Optional[float] = None) -> bool:
        return (time.time() if now is None else now) >= self.access_expires_at

    def refresh_due(self, now: Optional[float] = None) -> bool:
        current = time.time() if now is None else now
        return current >= self.access_expires_at - REFRESH_SKEW_SECONDS


def looks_like_record(raw: Optional[str]) -> bool:
    """True when a stored value is shaped like a grant record (it starts with ``{``),
    whatever mode this process is in. Such a value must never be forwarded as a bearer:
    it holds the refresh token. ``classify`` then says whether it is usable."""
    return raw is not None and raw.strip().startswith("{")


def classify(raw: Optional[str]) -> Optional[GitHubAppGrant]:
    """The App grant a stored value holds, or None for a classic grant (a bare token
    string: anything that does not start with ``{``).

    Raises ``GrantRecordDamaged`` for a value that starts with ``{`` and is not a
    complete, marked, well-typed record.
    """
    if raw is None:
        return None
    text = raw.strip()
    if not text.startswith("{"):
        return None
    try:
        data = json.loads(text)
    except ValueError as e:
        raise GrantRecordDamaged("grant record is not valid JSON") from e
    if not isinstance(data, dict):
        raise GrantRecordDamaged("grant record is not a JSON object")
    if data.get("minted_by") != MINTED_BY_APP:
        # Arch 2026-11-12 07:24: a classic grant is a bare token string; no writer has
        # ever stored one as JSON. An object that lost or mangled its marker is damage.
        raise GrantRecordDamaged("grant record carries no App marker")
    access = data.get("access_token")
    refresh = data.get("refresh_token")
    access_exp = data.get("access_expires_at")
    refresh_exp = data.get("refresh_expires_at")
    if not (isinstance(access, str) and access and isinstance(refresh, str) and refresh):
        raise GrantRecordDamaged("App grant record is missing a token")
    if (
        not isinstance(access_exp, int)
        or isinstance(access_exp, bool)
        or not isinstance(refresh_exp, int)
        or isinstance(refresh_exp, bool)
    ):
        raise GrantRecordDamaged("App grant record is missing an expiry")
    return GitHubAppGrant(
        access_token=access,
        access_expires_at=access_exp,
        refresh_token=refresh,
        refresh_expires_at=refresh_exp,
    )
