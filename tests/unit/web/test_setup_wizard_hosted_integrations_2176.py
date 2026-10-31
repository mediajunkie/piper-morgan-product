"""#2176: the hosted wizard's step 2 shows no Slack or Google Calendar app-credential forms.

CXO (2026-10-25 17:43): a person in the hosted wizard is never the site's admin, and PM's
2026-10-01 ruling is that a non-admin never sees the app-credential card. On a hosted
instance step 2 renders one line in place of both blocks and keeps the Notion box;
self-host keeps the forms (the person running it is the admin). The status calls that
fell back to showing the forms on a failed read are not made on a hosted wizard.
"""

from __future__ import annotations

import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from services.integrations.integration_status_service import BETA_OFFERED_CONNECTORS

REPO_ROOT = Path(__file__).resolve().parents[3]
# #2237: Slack is outside the offered set, so the line no longer promises it.
LINE = "You can connect Google Calendar later, in Settings → Integrations."
FORM_IDS = (
    "slack-config-needed",
    "slack-client-id",
    "slack-client-secret",
    "save-slack-credentials-btn",
    "calendar-config-needed",
    "calendar-client-id",
    "calendar-client-secret",
    "save-calendar-credentials-btn",
)


def _render(hosted: bool) -> str:
    env = Environment(loader=FileSystemLoader(str(REPO_ROOT / "templates")))
    return env.get_template("setup.html").render(
        asset_v="t", hosted=hosted, offered_connectors=list(BETA_OFFERED_CONNECTORS)
    )


def _step2(html: str) -> str:
    start = html.index('id="step-2"')
    return html[start : html.index('id="step-3"', start)]


class TestHostedStep2:
    def test_no_app_credential_box(self):
        step2 = _step2(_render(True))
        for element_id in FORM_IDS:
            assert f'id="{element_id}"' not in step2, element_id
        assert "Client ID" not in step2
        assert "Client Secret" not in step2
        assert "Google Cloud Console" not in step2
        assert "api.slack.com/apps" not in step2

    def test_the_connect_later_line_is_present_once(self):
        assert _step2(_render(True)).count(LINE) == 1

    def test_notion_box_is_removed(self):
        # #2237 (CXO): Notion is outside the offered set; the step does not offer it.
        step2 = _step2(_render(True))
        assert 'id="notion-key"' not in step2
        assert "Notion" not in step2
        assert "Optional integrations" in step2


class TestSelfHostStep2:
    def test_forms_are_kept_and_the_line_is_absent(self):
        step2 = _step2(_render(False))
        for element_id in FORM_IDS:
            greyed = element_id.startswith(("slack", "save-slack"))  # #2237
            assert (f'id="{element_id}"' in step2) is not greyed, element_id
        assert LINE not in step2
        assert 'id="notion-key"' not in step2


class TestHostedWizardMakesNoStatusCall:
    def test_both_status_checks_run_only_when_not_hosted(self):
        js = (REPO_ROOT / "web/static/js/setup.js").read_text()
        for call in (
            "checkSlackCredentialsStatus().then",
            "checkCalendarCredentialsStatus().then",
            "checkSlackCallbackParams();",
            "checkCalendarCallbackParams();",
        ):
            assert js.count(call) == 1, call
            before = js[: js.index(call)]
            guard = before.rindex("if (!hosted) {")
            # the call sits inside that guard: no block close at the guard's indent between them
            assert not re.search(r"\n    \}\n", before[guard:]), call
        # `hosted` is declared before either guard uses it
        assert js.index("const hosted = document.body.dataset.hosted === 'true';") < js.index(
            "if (!hosted) {"
        )
