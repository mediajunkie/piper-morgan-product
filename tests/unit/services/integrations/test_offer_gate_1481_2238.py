"""CIO 2026-11-04 16:10, Arch 16:15 (rides #1551's unit as its own commit): an exposure-
bearing deferral carries a mechanical trigger on the thing that would expose it. Slack's
socket path binds every sender to the connector owner (#1481) and a global Notion env key
beats the user's own (#2238). Neither is a cross-user read while the connector is not
offered on beta, so the gate is the offer: this pin fails the moment ``slack`` or ``notion``
enters the beta offered set while its issue is open. Closing the issue is what unlocks the
edit here (the #1817 trigger shape).
"""

from __future__ import annotations

from services.integrations import integration_status_service as iss

# The connector whose offer is gated, and the open issue that gates it.
GATED_UNTIL_CLOSED = {
    "slack": 1481,  # socket-mode senders are bound to the connector owner
    "notion": 2238,  # a global Notion env key beats the user's own
}


class TestTheOfferIsTheGate:
    def test_the_beta_set_offers_neither_gated_connector(self):
        for name, issue in GATED_UNTIL_CLOSED.items():
            assert name not in iss.BETA_OFFERED_CONNECTORS, (
                f"{name} entered BETA_OFFERED_CONNECTORS while #{issue} is open: every beta "
                f"account would share the connector owner's data. Close #{issue} first, then "
                "remove its row from GATED_UNTIL_CLOSED in this pin."
            )

    def test_the_beta_host_offers_neither_even_with_staging_extras_defined(self, monkeypatch):
        """The staging-only extras (Notion for #2238's own check) must stay keyed on the
        staging app name, so alpha and beta never pick them up."""
        monkeypatch.setenv("FLY_APP_NAME", "piper-morgan")
        offered = iss.offered_connectors()
        for name in GATED_UNTIL_CLOSED:
            assert name not in offered

    def test_the_staging_extra_is_the_only_way_notion_appears(self, monkeypatch):
        monkeypatch.setenv("FLY_APP_NAME", iss.STAGING_APP_NAME)
        assert "notion" in iss.offered_connectors()
        assert "slack" not in iss.offered_connectors()
