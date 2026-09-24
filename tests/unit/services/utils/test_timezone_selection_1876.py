"""#1876 — the shared timezone-SELECTION vocabulary (`timezone_choices`,
`resolve_timezone_token`) both the Settings page and the chat action build on.

LAYER (m-43): pure-function unit tests against the real `zoneinfo` tzdata
installed in this environment — no mocking of `available_timezones()`, so a
result here is a real claim about what the running interpreter's tzdata
actually contains. The one exception (`TestAmbiguousViaMonkeypatch`) is
explicit about substituting a synthetic zone set, because genuine same-city-
name collisions in the real IANA database are not guaranteed to exist across
tzdata versions — a test asserting on one would be tzdata-version-coupled.

DENOMINATOR: `timezone_choices()` (ordering + completeness) and
`resolve_timezone_token()` (exact IANA match, unambiguous bare-city match, no
match, ambiguous match, and normalization of spaces/hyphens/case). Does NOT
cover the chat handler's own candidate-EXTRACTION regex (see
test_set_timezone_chat_action_1876.py) or the route layer (see
test_preferences_timezone_1876.py) — this file is the shared resolver only.
"""

from __future__ import annotations

from zoneinfo import available_timezones

from services.utils.datetime_utils import resolve_timezone_token, timezone_choices


class TestTimezoneChoices:
    def test_returns_every_real_iana_zone(self):
        choices = timezone_choices()
        assert set(choices) == available_timezones()

    def test_no_duplicates(self):
        choices = timezone_choices()
        assert len(choices) == len(set(choices))

    def test_common_zones_come_first_and_in_declared_order(self):
        choices = timezone_choices()
        # UTC and the US majors must lead — the settings <select> shouldn't
        # make the common case scroll past ~350 names.
        head = choices[:5]
        assert head == [
            "UTC",
            "America/Los_Angeles",
            "America/Denver",
            "America/Chicago",
            "America/New_York",
        ]

    def test_remainder_is_sorted(self):
        choices = timezone_choices()
        common_count = len(
            [
                z
                for z in (
                    "UTC",
                    "America/Los_Angeles",
                    "America/Denver",
                    "America/Chicago",
                    "America/New_York",
                    "Europe/London",
                    "Europe/Paris",
                    "Europe/Helsinki",
                    "Asia/Tokyo",
                    "Asia/Shanghai",
                    "Australia/Sydney",
                )
                if z in available_timezones()
            ]
        )
        rest = choices[common_count:]
        assert rest == sorted(rest)


class TestResolveTimezoneTokenExactAndCity:
    def test_exact_iana_name_resolves_to_itself(self):
        zone, candidates = resolve_timezone_token("Europe/Helsinki")
        assert zone == "Europe/Helsinki"
        assert candidates == ["Europe/Helsinki"]

    def test_unambiguous_bare_city_resolves(self):
        # Helsinki has exactly one IANA zone with that city segment.
        zone, candidates = resolve_timezone_token("Helsinki")
        assert zone == "Europe/Helsinki"
        assert candidates == ["Europe/Helsinki"]

    def test_case_insensitive(self):
        zone, _ = resolve_timezone_token("helsinki")
        assert zone == "Europe/Helsinki"

    def test_spaces_normalize_to_underscores(self):
        zone, _ = resolve_timezone_token("Los Angeles")
        assert zone == "America/Los_Angeles"

    def test_hyphens_normalize_to_underscores(self):
        # Port-au-Prince is a real IANA city segment (America/Port-au-Prince);
        # confirm the resolver's hyphen normalization round-trips through it
        # rather than asserting on a fabricated example.
        assert "America/Port-au-Prince" in available_timezones()
        zone, _ = resolve_timezone_token("Port-au-Prince")
        assert zone == "America/Port-au-Prince"


class TestResolveTimezoneTokenHonestFailures:
    def test_no_match_returns_none_and_empty_candidates(self):
        zone, candidates = resolve_timezone_token("Nowheresville")
        assert zone is None
        assert candidates == []

    def test_empty_string_returns_none_and_empty(self):
        assert resolve_timezone_token("") == (None, [])

    def test_whitespace_only_returns_none_and_empty(self):
        assert resolve_timezone_token("   ") == (None, [])


class TestAmbiguousViaMonkeypatch:
    """A genuine tzdata city-name collision isn't guaranteed to exist (or stay
    stable) across tzdata versions, so the ambiguous-match behavior is proven
    against a SYNTHETIC zone set — stated explicitly as a substitution, not a
    claim about real tzdata."""

    def test_two_zones_sharing_a_city_segment_are_both_returned_unresolved(self, monkeypatch):
        import services.utils.datetime_utils as du

        fake_zones = frozenset(
            {"Region/Springfield", "OtherRegion/Springfield", "America/Los_Angeles"}
        )
        monkeypatch.setattr("zoneinfo.available_timezones", lambda: fake_zones)
        zone, candidates = du.resolve_timezone_token("Springfield")
        assert zone is None, "an ambiguous city must never be silently resolved"
        assert candidates == ["OtherRegion/Springfield", "Region/Springfield"]
