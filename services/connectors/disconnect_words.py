"""What a disconnect says, before and after, keyed by connector and leg (CXO and Arch, 2026-11-18).

CXO's rule (mail 01M7S2GFBP): a disconnect that leaves something valid at the provider says
so, before (the dialog) and after (the toast). Arch (01M7S2YPDA): the "stays valid"
sentences live in ONE map, keyed by connector and leg, like ``STALE_FACTS``; the dialog,
the single-card toast and the Disconnect All lines all read it. GitHub's leg comes from the
card's one resolver (ADR-070 B4), carried in the card payload; when the resolver can't name
one leg, the ``unknown`` entry is used, and every clause in it is true for all three legs
(Arch 01M7S3ZFGB, CXO 01M7S4FFKW and 01M7S4P271).

What stays, from ``services/connectors/disconnect.py``: the Piper GitHub app stays
installed (the grant is revoked, the installation is not); a personal GitHub token and a
Notion key are the person's own and are never revoked; Slack, Google and a classic GitHub
sign-in are revoked at the provider, so nothing stays unless that revoke fails.

Words are CXO's, verbatim. Nothing here is a code word the page shows.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

#: GitHub's legs as the card names them. ``app``: the Piper GitHub app's grant; ``oauth``:
#: a classic GitHub sign-in; ``token``: the person's own token; ``unknown``: the resolver
#: couldn't name one (a stale grant, a token covering for one, an unreadable credential).
GITHUB_LEGS = ("app", "oauth", "token", "unknown")

#: How a cleared card is named in Disconnect All's closing line: ``plain`` (it needs the
#: person to remove Piper there), ``may`` (it may, depending on the leg), or None.
PLAIN = "plain"
MAY = "may"


@dataclass(frozen=True)
class DisconnectWords:
    dialog: str  # the confirm dialog's message, under the title "Disconnect {name}?"
    cleared: str  # the toast after a cleared disconnect
    stays: bool  # something may stay valid at the provider: the cleared toast is a warning
    all_note: Optional[str]  # PLAIN, MAY or None, for Disconnect All's closing line


_REVOKES = (
    "I'll disconnect {name} and revoke Piper's access there. You can connect it again anytime."
)

DISCONNECT_WORDS: dict[tuple[str, Optional[str]], DisconnectWords] = {
    ("slack", None): DisconnectWords(
        dialog=_REVOKES.format(name="Slack"),
        cleared="Slack disconnected.",
        stays=False,
        all_note=None,
    ),
    ("calendar", None): DisconnectWords(
        dialog=_REVOKES.format(name="Google Calendar"),
        cleared="Google Calendar disconnected.",
        stays=False,
        all_note=None,
    ),
    ("notion", None): DisconnectWords(
        dialog=(
            "I'll delete the copy of your Notion key that Piper holds. The key stays valid in "
            "Notion until you remove the integration there. You can connect it again anytime."
        ),
        cleared=(
            "Notion disconnected. Your key stays valid in Notion until you remove the "
            "integration there."
        ),
        stays=True,
        all_note=PLAIN,
    ),
    ("github", "app"): DisconnectWords(
        dialog=(
            "I'll disconnect GitHub. The Piper GitHub app stays installed on your account until "
            "you remove it in GitHub's settings. You can connect it again anytime."
        ),
        cleared=(
            "GitHub disconnected. The Piper GitHub app stays installed until you remove it in "
            "GitHub's settings."
        ),
        stays=True,
        all_note=PLAIN,
    ),
    ("github", "token"): DisconnectWords(
        dialog=(
            "I'll delete the copy of your GitHub token that Piper holds. The token stays valid "
            "at GitHub until you delete it there. You can connect it again anytime."
        ),
        cleared="GitHub disconnected. Your token stays valid at GitHub until you delete it there.",
        stays=True,
        all_note=PLAIN,
    ),
    ("github", "oauth"): DisconnectWords(
        dialog=_REVOKES.format(name="GitHub"),
        cleared="GitHub disconnected.",
        stays=False,
        all_note=None,
    ),
    ("github", "unknown"): DisconnectWords(
        dialog=(
            "I'll disconnect GitHub. If you connected it with the Piper GitHub app or a "
            "personal token, that stays on at GitHub until you remove it in GitHub's settings. "
            "You can connect it again anytime."
        ),
        cleared=(
            "GitHub disconnected. If you connected it with the Piper GitHub app or a personal "
            "token, remove that in GitHub's settings too."
        ),
        stays=True,
        all_note=MAY,
    ),
}

#: Where a person removes Piper at each provider (CXO: "Google Calendar's settings" isn't a
#: place a person can find).
REMOVE_PLACE = {
    "Slack": "Slack's settings",
    "Google Calendar": "your Google account's settings",
    "GitHub": "GitHub's settings",
    "Notion": "Notion's settings",
}


def disconnect_words(connector: str, leg: Optional[str] = None) -> DisconnectWords:
    """The words for one card. GitHub with no leg, or a leg the map doesn't hold, is
    ``unknown``: never a guess (Arch)."""
    if connector == "github":
        return DISCONNECT_WORDS[("github", leg if leg in GITHUB_LEGS else "unknown")]
    return DISCONNECT_WORDS[(connector, None)]


def revoke_failed_line(service: str) -> str:
    """Piper's copies are gone but the provider-side revoke failed (CXO 10-25, place fixed
    11-18). Added to the success message, in warning style."""
    return (
        f"Piper no longer holds your access. I couldn't revoke it at {service}, so it stays "
        f"valid there until you remove Piper in {REMOVE_PLACE[service]}."
    )


def all_revoke_failed_line(service: str) -> str:
    """Disconnect All's line for a card whose revoke failed (CXO 01M7S2GFBP D)."""
    return (
        f"{service}: I couldn't revoke Piper's access, so it stays valid there until you "
        f"remove Piper in {REMOVE_PLACE[service]}."
    )


def all_incomplete_line(service: str) -> str:
    """Disconnect All's line for a card that didn't fully clear, or raised (CXO D)."""
    return (
        f"{service}: I couldn't fully disconnect it. A saved copy of your access may still be "
        "stored. Press Disconnect on its card to try again."
    )


def all_closing_line(notes: dict[str, str]) -> Optional[str]:
    """Disconnect All's closing line from the listed (or cleared) cards' ``all_note``,
    display name → PLAIN or MAY. Only GitHub can be MAY. None when nobody is named.

    CXO 01M7S2GFBP B/D and 01M7S4P271: known app or token legs and Notion get the plain
    line; an unknown GitHub leg gets the conditional one; a classic leg isn't named."""
    plain = [name for name, note in notes.items() if note == PLAIN]
    may = [name for name, note in notes.items() if note == MAY]
    if may:
        if plain:
            return (
                f"{' and '.join(plain)} also needs you to remove Piper in its settings, and "
                f"{may[0]} may too if you connected it with the app or a token."
            )
        return (
            f"{may[0]} may need you to remove Piper in its settings if you connected it with "
            "the app or a token."
        )
    if len(plain) == 1:
        return f"{plain[0]} also needs you to remove Piper in its settings."
    if plain:
        return f"{' and '.join(plain)} also need you to remove Piper in their own settings."
    return None


def all_closing_table() -> dict[str, str]:
    """Every closing line the page can need, keyed by the sorted ``name:note`` pairs joined
    with ``|`` (the page builds the same key). The page reads this table; it holds no words
    of its own."""
    candidates = {
        "GitHub": [None, PLAIN, MAY],
        "Notion": [None, PLAIN],
    }
    table: dict[str, str] = {}
    for github in candidates["GitHub"]:
        for notion in candidates["Notion"]:
            notes = {
                name: note
                for name, note in (("GitHub", github), ("Notion", notion))
                if note is not None
            }
            line = all_closing_line(notes)
            if line:
                table[closing_key(notes)] = line
    return table


def closing_key(notes: dict[str, str]) -> str:
    return "|".join(sorted(f"{name}:{note}" for name, note in notes.items()))


def page_all_words() -> dict:
    """What the Integrations page needs for Disconnect All and has no route reply for: the
    closing lines, and the incomplete line for a card whose request never answered."""
    return {"closing": all_closing_table(), "incomplete": all_incomplete_line("{service}")}
