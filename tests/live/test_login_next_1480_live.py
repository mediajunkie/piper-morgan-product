"""#1597 backlog item / #1480 — Slack deep-link params through the login round trip.

WHAT THIS VERIFIES (m-43 — name the layer, precisely, because this item is
split across two layers):

  VERIFIED HERE (real-server HTTP layer):
  - The middleware half: an UNAUTHENTICATED browser-shaped GET of the #1466
    deep link gets a 302 to /login with the WHOLE path+query percent-encoded
    into a single `next` param. (The original defect: unencoded building
    split the query at '&' and slack_team_id leaked out of `next` as a stray
    /login param.)
  - The login_page half: an ALREADY-AUTHENTICATED visit to /login?next=…
    302s to the sanitized next target, not '/'.
  - The open-redirect guard, live: /login?next=https://evil.example with a
    real cookie must NOT bounce off-site.

  NOT VERIFIED HERE — UNRUNNABLE BY THIS HARNESS (and said so honestly):
  - The client half: web/static/js/auth.js safeNextUrl() reading `next` after
    a successful login POST, redirecting there, and re-attaching the
    #link-slack fragment. That is JavaScript executing in a browser; this
    harness drives HTTP and never executes JS. It is ALSO the exact line that
    carried the original bug, and its existing coverage is static source-text
    grepping — so the #1597 stated check ("log out, open the deep link, log
    in, confirm landing on the pre-minted link card") remains only PARTIALLY
    discharged. The browser half needs a chrome-driven or manual pass; see
    the explicitly-skipped test at the bottom, which exists so this gap is
    visible in every run rather than absorbed.

Issue: #1597 (item 3: #1480)
"""

from urllib.parse import parse_qs, quote, urlsplit

import httpx
import pytest

DEEP_LINK_PATH = "/settings/integrations/slack"
DEEP_LINK_QUERY = "slack_user_id=U1597LIVE&slack_team_id=T1597LIVE"
DEEP_LINK = f"{DEEP_LINK_PATH}?{DEEP_LINK_QUERY}"


@pytest.mark.live
class TestLoginNextLive:
    def test_unauthenticated_deep_link_visit_encodes_full_query_into_next(
        self, live_server
    ):
        """Logged-out browser hits the deep link → 302 /login?next=<one
        encoded param carrying BOTH slack ids>."""
        with httpx.Client(base_url=live_server.base_url, timeout=15.0) as anon:
            resp = anon.get(
                DEEP_LINK,
                headers={"accept": "text/html"},
                follow_redirects=False,
            )
        assert resp.status_code == 302, (
            f"Expected 302 redirect to /login for unauthenticated deep-link "
            f"visit, got {resp.status_code}: {resp.text[:300]}"
        )
        location = resp.headers.get("location", "")
        split = urlsplit(location)
        assert split.path == "/login", f"Redirect went to {location!r}, not /login"

        params = parse_qs(split.query)
        # THE original defect, asserted dead: slack_team_id must NOT appear
        # as its own /login param (that was the '&' split leak)...
        assert "slack_team_id" not in params, (
            f"#1480 FAILED LIVE: slack_team_id leaked out of `next` as a "
            f"stray /login param — Location: {location!r}"
        )
        # ...and `next` must decode to the complete original path+query.
        assert params.get("next") == [DEEP_LINK], (
            f"#1480 FAILED LIVE: next did not round-trip the full deep link. "
            f"Location: {location!r}, decoded next: {params.get('next')!r}"
        )
        print(f"\n#1480 live evidence (middleware half) — Location: {location}")

    def test_authenticated_login_visit_honors_next(self, turn_driver):
        """Already-authenticated GET /login?next=<deep link> → 302 to the
        deep link, not '/'. (The login_page half of the fix.)

        History: strict-xfail 2026-08-16 → fixed by #1640 (2026-08-18).
        The #1597 live run found this bounce structurally DEAD: /login sat
        in AuthMiddleware's exclude_paths, so the cookie was never parsed
        and request.state.user_id was never set. #1640 made /login
        OPTIONAL-auth (OPTIONAL_AUTH_UI_PATHS, same mechanism as "/"
        per #1399); the xfail flipped XPASS and the marker came off per
        its own instruction."""
        resp = turn_driver.get(
            f"/login?next={quote(DEEP_LINK, safe='')}",
            headers={"accept": "text/html"},
            follow_redirects=False,
        )
        assert resp.status_code == 302, (
            f"Expected authenticated /login?next=… to 302, got "
            f"{resp.status_code}: {resp.text[:300]}"
        )
        location = resp.headers.get("location", "")
        assert location == DEEP_LINK, (
            f"#1480 FAILED LIVE: authenticated /login bounce went to "
            f"{location!r}, expected {DEEP_LINK!r}"
        )
        print(f"\n#1480 live evidence (login_page half) — Location: {location}")

    def test_open_redirect_guard_live(self, turn_driver):
        """The guard, on the real server: an absolute-URL next must fall back
        to '/', never bounce off-site. Only observable through the
        already-authenticated bounce (live since #1640); the probe-skip
        stays as a regression guard — if the bounce ever goes dead again
        this SKIPS loudly rather than fake-passing (m-44)."""
        probe = turn_driver.get(
            f"/login?next={quote(DEEP_LINK, safe='')}",
            headers={"accept": "text/html"},
            follow_redirects=False,
        )
        if probe.status_code != 302:
            pytest.skip(
                "UNMEASURABLE LIVE: the authenticated /login bounce did not "
                f"fire (got HTTP {probe.status_code} for a benign next) — a "
                "REGRESSION of #1640, which made the bounce reachable. No "
                "server-side redirect exists through which to observe the "
                "open-redirect guard. (sanitize_next_path itself remains "
                "unit-covered.)"
            )
        for evil in ("https://evil.example/x", "//evil.example/x", "/\\evil"):
            resp = turn_driver.get(
                f"/login?next={quote(evil, safe='')}",
                headers={"accept": "text/html"},
                follow_redirects=False,
            )
            assert resp.status_code == 302
            location = resp.headers.get("location", "")
            assert location == "/", (
                f"Open-redirect guard FAILED LIVE for next={evil!r}: "
                f"Location {location!r}"
            )

    def test_browser_half_post_login_landing_UNRUNNABLE_here(self):
        """The #1597 stated check's decisive half. Kept as a permanent,
        loudly-skipped marker so no run of this suite reads as having
        verified it (m-44: a check that can't run must never read as passed)."""
        pytest.skip(
            "UNRUNNABLE-BY-THIS-HARNESS: the post-login landing (auth.js "
            "safeNextUrl() redirect + #link-slack fragment re-attach + the "
            "pre-minted link card render) is browser-executed JavaScript. "
            "This harness drives HTTP only. Needs a chrome-driven or manual "
            "pass: log out, open /settings/integrations/slack?slack_user_id="
            "X&slack_team_id=Y#link-slack, log in, confirm landing on the "
            "pre-minted link card rather than '/'."
        )
