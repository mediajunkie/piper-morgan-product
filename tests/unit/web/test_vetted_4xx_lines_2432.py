"""Issue 2432, steps 2 to 4: every 4xx line the CXO kept or reworded, word for word.

Sources: the CXO's read (issue comment 7144095698), her addendum (mail 01M87NVGEW) and the
step 1 lines she passed (issue comment of 2026-11-24 recording 6ff8197d9a); the password
rules behind a picker (Arch's note 01M87HVCTY).

LAYER: the constants themselves; an ``ast`` read that each is the ``detail`` of a
``UserFacingHTTPException`` in its own module (so it is marked); the app's REAL handler on a
small app for "reaches the client as written"; the change-password and reset routes called
through that handler; the admin gate as a dependency of a small route.
DENOMINATOR: every marked 4xx constant under ``web/`` and ``services/`` (the table below,
checked against an ``ast`` count of marked 4xx constants), the six computed constants,
the seven password rule codes and the not-offered family.
NOT COVERED: any rendered page. Nothing here was put on a screen.
"""

import ast
import importlib
import re
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import pytest
from fastapi import Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient

from services.api.errors import UserFacingHTTPException

ROOT = Path(__file__).resolve().parents[3]
CXO = "CXO comment 7144095698"
ADDENDUM = "CXO mail 01M87NVGEW"
STEP1 = "step 1 lines, CXO passed (mails 01M87HSM8A, 01M87K06YA, 01M87KM3VZ)"
EARLIER = "constant worded before 2432, kept as written"

# (module, constant, exact words, source)
TABLE = [
    ("services.api.transparency", "ADMIN_ACCOUNT_NEEDED_LINE", "This needs an admin account.", CXO),
    (
        "services.auth.auth_middleware",
        "ADMIN_ACCOUNT_NEEDED_FOR_CONFIG_LINE",
        "This changes app-wide configuration, so it needs an admin account. "
        "Nothing was changed.",
        CXO,
    ),
    (
        "services.auth.auth_middleware",
        "OPERATIONS_READERS_ONLY_LINE",
        "This page is for operations readers.",
        CXO,
    ),
    (
        "web.api.routes.admin_ops",
        "UNKNOWN_FLAG_DETAIL",
        "That is not a flag this page can set. Nothing was changed.",
        ADDENDUM,
    ),
    (
        "web.api.routes.admin_test_preferences",
        "ONLY_A_LISTED_TEST_ACCOUNT_LINE",
        "Only a listed test account can be reset.",
        CXO,
    ),
    (
        "web.api.routes.admin_test_preferences",
        "PREFERENCE_CANT_BE_RESET_LINE",
        "That preference can't be reset here.",
        CXO,
    ),
    (
        "web.api.routes.api_keys",
        "NOT_AN_LLM_PROVIDER",
        "This page is for AI provider keys only. Connected services like GitHub, "
        "Google Calendar and Notion are managed in Settings → Integrations.",
        ADDENDUM,
    ),
    (
        "web.api.routes.api_keys",
        "PROVIDER_NOT_USED_YET",
        "Piper doesn't use Google (Gemini) keys yet. Anthropic and OpenAI keys work.",
        ADDENDUM,
    ),
    (
        "web.api.routes.api_keys",
        "KEY_COULD_NOT_BE_SAVED_MESSAGE",
        "That key couldn't be saved. Check the provider and the key, then try again.",
        STEP1,
    ),
    (
        "web.api.routes.api_keys",
        "KEY_COULD_NOT_BE_REPLACED_MESSAGE",
        "That key couldn't be replaced. Check the provider and the key, then try again.",
        STEP1,
    ),
    ("web.api.routes.artifacts", "NOTHING_TO_SAVE_LINE", "There's nothing to save yet.", CXO),
    ("web.api.routes.artifacts", "TITLE_NEEDED_LINE", "Give it a title first.", CXO),
    (
        "web.api.routes.auth",
        "NEW_PASSWORDS_DONT_MATCH_LINE",
        "The new passwords don't match.",
        CXO,
    ),
    (
        "services.auth.password_validator",
        "PASSWORD_CANT_BE_USED_LINE",
        "That password can't be used. Choose a different one.",
        "CXO's fallback for the password branch (her log 11:51; Arch 01M87HVCTY)",
    ),
    (
        "web.api.routes.auth",
        "RESET_CODE_NOT_VALID_LINE",
        "That reset code isn't valid or has expired. Ask for a new one.",
        CXO,
    ),
    (
        "web.api.routes.auth",
        "PASSWORD_COULD_NOT_BE_CHANGED_MESSAGE",
        "Your password couldn't be changed just now. "
        "Try again in a moment; if it keeps failing, tell us.",
        STEP1,
    ),
    ("web.api.routes.conversations", "TITLE_NEEDED_LINE", "Give it a title first.", CXO),
    (
        "web.api.routes.conversations",
        "TITLE_TOO_LONG_LINE",
        "Titles can be up to 100 characters.",
        CXO,
    ),
    (
        "web.api.routes.conversations",
        "STATE_NOT_RECOGNISED_LINE",
        "That isn't a state I recognise. Choose active or archived.",
        CXO,
    ),
    (
        "web.api.routes.conversations",
        "CANT_BE_ARCHIVED_LINE",
        "That conversation can't be archived right now.",
        CXO,
    ),
    (
        "web.api.routes.conversations",
        "CANT_BE_REACTIVATED_LINE",
        "That conversation can't be reactivated right now.",
        CXO,
    ),
    (
        "web.api.routes.conversations",
        "ALREADY_DELETED_LINE",
        "That conversation has already been deleted.",
        CXO,
    ),
    (
        "web.api.routes.documents",
        "USER_KEY_REQUIRED_DETAIL",
        "This needs an OpenAI or Anthropic API key of your own. "
        "Add one in Settings → LLM API Keys, then try again. Nothing was charged.",
        ADDENDUM,
    ),
    (
        "web.api.routes.documents",
        "SEARCH_KEY_REQUIRED_DETAIL",
        "Document search needs an OpenAI API key of your own. "
        "Add one in Settings → LLM API Keys, then try again. Nothing was charged.",
        CXO,
    ),
    (
        "web.api.routes.documents",
        "TOO_FEW_TO_COMPARE_LINE",
        "Pick at least two documents to compare.",
        CXO,
    ),
    (
        "web.api.routes.documents",
        "TOO_MANY_TO_COMPARE_LINE",
        "You can compare up to five documents at a time.",
        CXO,
    ),
    ("web.api.routes.feedback", "FEEDBACK_NEEDED_LINE", "Write your feedback first.", CXO),
    ("web.api.routes.files", "CHOOSE_A_FILE_LINE", "Choose a file first.", CXO),
    ("web.api.routes.files", "CHOOSE_AT_LEAST_ONE_FILE_LINE", "Choose at least one file.", CXO),
    (
        "web.api.routes.files",
        "TOO_MANY_TO_DOWNLOAD_LINE",
        "You can download up to 50 files at a time.",
        CXO,
    ),
    ("web.api.routes.files", "CANT_DOWNLOAD_FILE_LINE", "You can't download that file.", CXO),
    ("web.api.routes.files", "CANT_VIEW_FILE_LINE", "You can't view that file.", CXO),
    (
        "web.api.routes.files",
        "FILE_NO_LONGER_AVAILABLE_LINE",
        "This file is no longer available. Please upload it again.",
        CXO,
    ),
    ("web.api.routes.knowledge_graph", "NODE_NAME_NEEDED_LINE", "Give it a name first.", CXO),
    ("web.api.routes.knowledge_graph", "NODE_TYPE_NEEDED_LINE", "Choose a type first.", CXO),
    (
        "web.api.routes.knowledge_graph",
        "EDGE_TYPE_NEEDED_LINE",
        "Choose a type for the connection first.",
        CXO,
    ),
    ("web.api.routes.lists", "LIST_NAME_NEEDED_LINE", "Give the list a name first.", CXO),
    ("web.api.routes.lists", "ITEM_TEXT_NEEDED_LINE", "Write the item first.", CXO),
    (
        "web.api.routes.preferences",
        "PREFERENCE_NOT_APPLIED_LINE",
        "I couldn't apply that preference.",
        CXO,
    ),
    (
        "web.api.routes.preferences",
        "TIME_ZONE_NOT_RECOGNISED_MESSAGE",
        "That isn't a time zone I recognise. Use a name like America/Los_Angeles.",
        STEP1,
    ),
    ("web.api.routes.projects", "PROJECT_NAME_NEEDED_LINE", "Give the project a name first.", CXO),
    (
        "web.api.routes.projects",
        "ONLY_OWNER_CAN_SHARE_LINE",
        "Only the project's owner can share it.",
        CXO,
    ),
    ("web.api.routes.projects", "NOTHING_TO_CHANGE_LINE", "There's nothing to change.", CXO),
    (
        "web.api.routes.projects",
        "INTEGRATION_SETTINGS_NOT_VALID_LINE",
        "That integration's settings aren't valid. Check them and try again.",
        CXO,
    ),
    (
        "web.api.routes.projects",
        "INTEGRATION_ALREADY_ADDED_LINE",
        "That integration is already added to this project.",
        CXO,
    ),
    (
        "web.api.routes.projects",
        "ONLY_OWNER_CAN_REMOVE_ACCESS_LINE",
        "Only the project's owner can remove someone's access, "
        "and that person has to be shared on the project.",
        ADDENDUM,
    ),
    (
        "web.api.routes.projects",
        "ONLY_OWNER_CAN_CHANGE_ROLE_LINE",
        "Only the project's owner can change someone's role, "
        "and that person has to be shared on the project.",
        ADDENDUM,
    ),
    (
        "web.api.routes.repositories",
        "OWNER_REPO_FORMAT_LINE",
        "Write the repository as owner/repo.",
        CXO,
    ),
    (
        "web.api.routes.repositories",
        "ALREADY_REGISTERED_LINE",
        "That repository is already registered.",
        CXO,
    ),
    (
        "web.api.routes.repositories",
        "ALREADY_LINKED_LINE",
        "That repository is already linked to this project.",
        CXO,
    ),
    ("web.api.routes.settings_integrations", "ENTER_CLIENT_ID_LINE", "Enter the client ID.", CXO),
    (
        "web.api.routes.settings_integrations",
        "ENTER_CLIENT_SECRET_LINE",
        "Enter the client secret.",
        CXO,
    ),
    (
        "web.api.routes.settings_integrations",
        "SLACK_REPLIES_OFF_LINE",
        "Slack replies are turned off in this release, so your token wasn't saved.",
        CXO,
    ),
    (
        "web.api.routes.settings_integrations",
        "SLACK_APP_TOKEN_SHAPE_LINE",
        "That doesn't look like an app-level token. They start with 'xapp-'. "
        "Check you copied the right one from Basic Information → App-Level Tokens.",
        CXO,
    ),
    (
        "web.api.routes.settings_integrations",
        "NOTION_KEY_DIDNT_WORK_LINE",
        "That Notion API key didn't work. Check it and try again.",
        CXO,
    ),
    (
        "web.api.routes.settings_integrations",
        "GITHUB_TOKEN_DIDNT_WORK_LINE",
        "That GitHub token didn't work. Check it and try again.",
        CXO,
    ),
    (
        "web.api.routes.settings_integrations",
        "CALENDAR_NOT_CONNECTED_LINE",
        "Google Calendar isn't connected yet. Connect it first, then refresh the list.",
        CXO,
    ),
    (
        "web.api.routes.settings_integrations",
        "CALENDAR_NEEDS_RECONNECT_LINE",
        "Google Calendar needs reconnecting. Reconnect it, then refresh the list.",
        CXO,
    ),
    (
        "web.api.routes.settings_integrations",
        "GITHUB_TOKEN_SHAPE_REFUSAL",
        'That doesn\'t look like a GitHub personal access token. They start with "ghp_" or '
        '"github_pat_".',
        CXO,
    ),
    (
        "web.api.routes.settings_integrations",
        "GITHUB_TOKEN_APP_CONNECTED_REFUSAL",
        "This account is connected through the Piper GitHub app, so it doesn't take a "
        "personal token.",
        CXO,
    ),
    (
        "web.api.routes.setup",
        "SETUP_ALREADY_COMPLETE_LINE",
        "Setup is already complete on this server. Sign in and manage "
        "credentials and projects from Settings → Integrations instead.",
        CXO,
    ),
    (
        "web.api.routes.setup",
        "SIGNED_IN_ACCOUNT_ONLY_LINE",
        "This setup step applies to the signed-in account only.",
        CXO,
    ),
    (
        "web.api.routes.setup",
        "INVITE_CODE_NOT_VALID_LINE",
        "That invite code isn't valid or has already been used.",
        CXO,
    ),
    (
        "web.api.routes.setup",
        "EMAIL_OR_USERNAME_IN_USE_LINE",
        "That email or username is already in use.",
        ADDENDUM,
    ),
    ("web.api.routes.setup", "PROJECT_NAME_NEEDED_LINE", "Give the project a name first.", CXO),
    (
        "web.api.routes.setup",
        "GITHUB_OWNER_REPO_LINE",
        "Write the GitHub repository as owner/repo.",
        CXO,
    ),
    ("web.api.routes.todos", "TODO_TITLE_NEEDED_LINE", "Give the todo a title first.", CXO),
    (
        "web.api.routes.todos",
        "DUE_DATE_NOT_READABLE_LINE",
        "I couldn't read that due date. Use a date like 2026-12-01.",
        CXO,
    ),
    (
        "web.api.routes.work_items",
        "WORK_ITEM_TITLE_NEEDED_LINE",
        "Give the work item a title first.",
        CXO,
    ),
]

# Computed once at import from a source of truth (CXO's "{LIST}" lines, Arch's item 3).
# If a source list changes, the sentence changes and this pin fails until it is read again.
COMPUTED = [
    (
        "web.api.routes.artifacts",
        "DOWNLOAD_FORMAT_NOT_RECOGNISED_LINE",
        "I can't download it in that format. Choose one of: md, txt.",
    ),
    (
        "web.api.routes.knowledge_graph",
        "NODE_TYPE_NOT_RECOGNISED_LINE",
        "That isn't a node type I recognise. Choose one of: CONCEPT, DOCUMENT, PERSON, "
        "ORGANIZATION, TECHNOLOGY, PROCESS, METRIC, EVENT, RELATIONSHIP, CUSTOM.",
    ),
    (
        "web.api.routes.knowledge_graph",
        "EDGE_TYPE_NOT_RECOGNISED_LINE",
        "That isn't an edge type I recognise. Choose one of: REFERENCES, DEPENDS_ON, "
        "IMPLEMENTS, MEASURES, INVOLVES, TRIGGERS, ENHANCES, REPLACES, SUPPORTS, BECAUSE, "
        "ENABLES, REQUIRES, PREVENTS, LEADS_TO, BEFORE, DURING, AFTER, CUSTOM.",
    ),
    (
        "web.api.exceptions",
        "ROLE_NOT_RECOGNISED_LINE",
        "That isn't a role I recognise. Choose one of: viewer, editor, admin.",
    ),
    (
        "web.api.routes.projects",
        "INTEGRATION_TYPE_NOT_RECOGNISED_LINE",
        "That isn't an integration type I recognise. Choose one of: github, jira, linear, slack.",
    ),
    (
        "web.api.routes.repositories",
        "PROVIDER_NOT_RECOGNISED_LINE",
        "That isn't a repository provider I recognise. Choose one of: bitbucket, github, gitlab.",
    ),
    ("web.api.routes.files", "FILE_TOO_LARGE_LINE", "That file is too large. The limit is 10 MB."),
    (
        "web.api.routes.files",
        "FILE_KIND_NOT_USABLE_LINE",
        "I can't use that kind of file. Allowed: .docx, .json, .md, .pdf, .txt.",
    ),
    (
        "services.integrations.integration_status_service",
        "GITHUB_NOT_OFFERED_LINE",
        "GitHub isn't available in this beta yet.",
    ),
    (
        "services.integrations.integration_status_service",
        "SLACK_NOT_OFFERED_LINE",
        "Slack isn't available in this beta yet.",
    ),
    (
        "services.integrations.integration_status_service",
        "CALENDAR_NOT_OFFERED_LINE",
        "Google Calendar isn't available in this beta yet.",
    ),
    (
        "services.integrations.integration_status_service",
        "NOTION_NOT_OFFERED_LINE",
        "Notion isn't available in this beta yet.",
    ),
    (
        "services.auth.password_validator",
        "PASSWORD_TOO_SHORT_LINE",
        "Your password needs at least 8 characters.",
    ),
]

# Used through an import: the module that raises with it, when not the one defining it.
RAISED_IN = {
    ("services.auth.password_validator", "PASSWORD_CANT_BE_USED_LINE"): ["web/api/routes/auth.py"],
    ("web.api.exceptions", "ROLE_NOT_RECOGNISED_LINE"): [
        "web/api/routes/lists.py",
        "web/api/routes/todos.py",
        "web/api/routes/projects.py",
    ],
}


def _marked_constant_details(rel_path):
    """UPPER_CASE names used as the ``detail`` of a ``UserFacingHTTPException`` in a file."""
    tree = ast.parse((ROOT / rel_path).read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "UserFacingHTTPException"
        ):
            detail = {k.arg: k.value for k in node.keywords}.get("detail")
            if isinstance(detail, ast.Name):
                names.add(detail.id)
    return names


def _path_of(module):
    return module.replace(".", "/") + ".py"


def _through_the_handler(exc):
    from web.app import app as real_app

    app = FastAPI()
    app.add_exception_handler(HTTPException, real_app.exception_handlers[HTTPException])

    @app.get("/call")
    async def _call():
        raise exc

    return TestClient(app).get("/call")


class TestEveryKeptOrRewordedLine:
    @pytest.mark.parametrize("module, name, words, source", TABLE)
    def test_the_constant_is_the_words(self, module, name, words, source):
        assert getattr(importlib.import_module(module), name) == words

    @pytest.mark.parametrize("module, name, words, source", TABLE)
    def test_it_is_raised_marked(self, module, name, words, source):
        for path in RAISED_IN.get((module, name), [_path_of(module)]):
            assert name in _marked_constant_details(path), f"{name} is not marked in {path}"

    @pytest.mark.parametrize("module, name, words, source", TABLE)
    def test_a_marked_raise_reaches_the_client_as_written(self, module, name, words, source):
        reply = _through_the_handler(UserFacingHTTPException(status_code=400, detail=words))
        assert reply.json() == {"message": words, "detail": words}

    def test_the_table_covers_every_marked_4xx_constant(self):
        """Every UPPER_CASE detail of a marked 4xx call is in TABLE or COMPUTED (or is a
        5xx line, which this issue does not touch)."""
        from tests.unit.web.test_status_lines_2432 import _marked_4xx_calls

        known = {name for _, name, *_ in TABLE} | {name for _, name, _ in COMPUTED}
        seen = set()
        for _path, _func, call in _marked_4xx_calls():
            detail = {k.arg: k.value for k in call.keywords}["detail"]
            if isinstance(detail, ast.Name):
                seen.add(detail.id)
        assert seen - known == set()
        # 75 distinct names (TITLE_NEEDED_LINE and PROJECT_NAME_NEEDED_LINE live in two
        # modules each).
        assert len(seen) == 75


class TestTheComputedLines:
    @pytest.mark.parametrize("module, name, words", COMPUTED)
    def test_the_sentence(self, module, name, words):
        assert getattr(importlib.import_module(module), name) == words

    @pytest.mark.parametrize("module, name, words", COMPUTED)
    def test_it_reaches_the_client_as_written(self, module, name, words):
        line = getattr(importlib.import_module(module), name)
        reply = _through_the_handler(UserFacingHTTPException(status_code=400, detail=line))
        assert reply.json()["message"] == words

    def test_the_share_routes_check_against_the_same_roles(self):
        from services.domain.models import ShareRole
        from web.api.exceptions import SHARE_ROLES

        assert SHARE_ROLES == tuple(r.value for r in ShareRole)
        for path in ("lists", "todos", "projects"):
            src = (ROOT / f"web/api/routes/{path}.py").read_text(encoding="utf-8")
            assert '["viewer", "editor", "admin"]' not in src
            assert "valid_roles = SHARE_ROLES" in src


class TestThePasswordRules:
    CODES = {
        "empty": "Your password can't be empty.",
        "too_short": "Your password needs at least 8 characters.",
        "no_uppercase": "Your password needs an uppercase letter.",
        "no_lowercase": "Your password needs a lowercase letter.",
        "no_digit": "Your password needs a number.",
        "no_special": "Your password needs a special character, such as ! @ # $ % ^ & * ( ).",
        "mismatch": "The passwords don't match.",
    }
    FALLBACK = "That password can't be used. Choose a different one."

    @pytest.mark.parametrize("code, line", sorted(CODES.items()))
    def test_each_code_maps_to_its_constant(self, code, line):
        from services.auth.password_validator import password_rule_line

        assert password_rule_line(code) == line

    @pytest.mark.parametrize("code", ["unknown", "", None, "Password cannot be empty"])
    def test_an_unknown_code_has_no_line_and_the_fallback_is_named(self, code):
        from services.auth import password_validator

        assert password_validator.password_rule_line(code) is None
        assert password_validator.PASSWORD_CANT_BE_USED_LINE == self.FALLBACK

    @pytest.mark.parametrize(
        "password, code",
        [
            ("", "empty"),
            ("Ab1!", "too_short"),
            ("abcdefg1!", "no_uppercase"),
            ("ABCDEFG1!", "no_lowercase"),
            ("Abcdefgh!", "no_digit"),
            ("Abcdefg12", "no_special"),
            ("Abcdefg1!", None),
        ],
    )
    def test_failed_rule_names_the_first_rule_broken(self, password, code):
        from services.auth.password_validator import PasswordValidator

        assert PasswordValidator.failed_rule(password) == code

    def test_validate_keeps_its_shape_and_words(self):
        from services.auth.password_validator import PasswordValidator

        assert PasswordValidator.validate("Abcdefg1!") == (True, None)
        assert PasswordValidator.validate("Ab1!") == (
            False,
            "Password must be at least 8 characters",
        )
        assert PasswordValidator.validate("Abcdefg12") == (
            False,
            "Password must contain at least one special character (!@#$%^&*())",
        )
        assert PasswordValidator.validate_match("a", "b") == (False, "Passwords do not match")

    @pytest.mark.parametrize(
        "password, line",
        [
            ("Ab1!", "Your password needs at least 8 characters."),
            ("abcdefg1!", "Your password needs an uppercase letter."),
            ("Abcdefgh!", "Your password needs a number."),
            ("Abcdefg12", "Your password needs a special character, such as ! @ # $ % ^ & * ( )."),
        ],
    )
    def test_the_change_route_answers_the_rules_line(self, password, line):
        from services.auth.models import PasswordChangeRequest
        from services.auth.password_validator import PasswordValidator
        from web.api.routes import auth

        user = SimpleNamespace(sub="u-2432", user_id=UUID("00000000-0000-0000-0000-000000002432"))
        data = PasswordChangeRequest.model_construct(
            current_password="Made-up-Old-Passw0rd!",
            new_password=password,
            new_password_confirm=password,
        )

        async def call():
            with patch.object(auth.db, "_initialized", True, create=True):
                return await auth.change_password(
                    request=MagicMock(),
                    data=data,
                    current_user=user,
                    credentials=SimpleNamespace(credentials="made-up-token"),
                    jwt_service=MagicMock(),
                )

        from web.app import app as real_app

        app = FastAPI()
        app.add_exception_handler(HTTPException, real_app.exception_handlers[HTTPException])

        @app.get("/call")
        async def _call():
            return await call()

        reply = TestClient(app).get("/call")
        assert reply.status_code == 400
        assert reply.json() == {"message": line, "detail": line}
        validator_words = PasswordValidator.validate(password)[1]
        assert validator_words and validator_words not in reply.text
        assert "Password must" not in reply.text

    def test_the_change_route_answers_the_mismatch_line(self):
        from services.auth.models import PasswordChangeRequest
        from web.api.routes import auth

        data = PasswordChangeRequest.model_construct(
            current_password="x", new_password="Abcdefg1!", new_password_confirm="Abcdefg1?"
        )

        async def call():
            with patch.object(auth.db, "_initialized", True, create=True):
                return await auth.change_password(
                    request=MagicMock(),
                    data=data,
                    current_user=SimpleNamespace(sub="u", user_id=UUID(int=1)),
                    credentials=SimpleNamespace(credentials="t"),
                    jwt_service=MagicMock(),
                )

        from web.app import app as real_app

        app = FastAPI()
        app.add_exception_handler(HTTPException, real_app.exception_handlers[HTTPException])

        @app.get("/call")
        async def _call():
            return await call()

        reply = TestClient(app).get("/call")
        assert reply.json()["message"] == "The new passwords don't match."

    def test_both_routes_pick_through_the_picker_and_never_send_the_validators_words(self):
        src = (ROOT / "web/api/routes/auth.py").read_text(encoding="utf-8")
        assert "PasswordValidator.validate(" not in src
        assert src.count("PasswordValidator.failed_rule(data.new_password)") == 2
        assert src.count("detail=password_rule_line(rule)") == 2
        assert src.count("detail=PASSWORD_CANT_BE_USED_LINE") == 2

    def test_an_unknown_code_answers_the_fallback_through_the_route(self):
        from services.auth.models import PasswordChangeRequest
        from web.api.routes import auth

        data = PasswordChangeRequest.model_construct(
            current_password="x", new_password="Abcdefg1!", new_password_confirm="Abcdefg1!"
        )

        async def call():
            with (
                patch.object(auth.db, "_initialized", True, create=True),
                patch.object(
                    auth.PasswordValidator, "failed_rule", MagicMock(return_value="new_rule")
                ),
            ):
                return await auth.change_password(
                    request=MagicMock(),
                    data=data,
                    current_user=SimpleNamespace(sub="u", user_id=UUID(int=1)),
                    credentials=SimpleNamespace(credentials="t"),
                    jwt_service=MagicMock(),
                )

        from web.app import app as real_app

        app = FastAPI()
        app.add_exception_handler(HTTPException, real_app.exception_handlers[HTTPException])

        @app.get("/call")
        async def _call():
            return await call()

        reply = TestClient(app).get("/call")
        assert reply.status_code == 400
        assert reply.json()["message"] == self.FALLBACK


class TestTheNotOfferedFamily:
    @pytest.mark.parametrize(
        "name, line",
        [
            ("github", "GitHub isn't available in this beta yet."),
            ("slack", "Slack isn't available in this beta yet."),
            ("calendar", "Google Calendar isn't available in this beta yet."),
            ("notion", "Notion isn't available in this beta yet."),
        ],
    )
    def test_each_named_refusal_reaches_the_client_as_ruled(self, name, line):
        from services.integrations import integration_status_service as svc

        assert svc.not_offered_line(name) == svc.not_offered_message(name) == line
        with patch.object(svc, "connector_offered", return_value=False):
            with pytest.raises(HTTPException) as exc:
                svc.refuse_unless_offered(name)
        raised = exc.value
        assert getattr(raised, "user_facing", False) is True
        reply = _through_the_handler(raised)
        assert reply.status_code == 409
        assert reply.json() == {"message": line, "detail": line}

    def test_a_name_with_no_line_answers_the_409_status_line(self):
        from services.integrations import integration_status_service as svc

        assert svc.not_offered_line("zoom") is None
        with patch.object(svc, "connector_offered", return_value=False):
            with pytest.raises(HTTPException) as exc:
                svc.refuse_unless_offered("zoom")
        assert not getattr(exc.value, "user_facing", False)
        reply = _through_the_handler(exc.value)
        assert reply.json()["message"] == "That conflicts with something that is already there."


class TestTheUnmarkedSites:
    """The sites the CXO sent to the status line stay plain ``HTTPException`` (comment
    7144095698, "Take the status line (D)", the missing-scopes 403 and the unknown-name
    not-offered fallback)."""

    UNMARKED = [
        ("services/api/transparency.py", "Not authorized to access this session's audit data"),
        ("web/api/routes/files.py", "Not authorized"),
        ("web/api/routes/lists.py", "user_id is required"),
        ("web/api/routes/todos.py", "user_id is required"),
    ]

    @pytest.mark.parametrize("path, words", UNMARKED)
    def test_the_raise_is_plain(self, path, words):
        tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
        hits = [
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id.endswith("HTTPException")
            and any(
                k.arg == "detail" and isinstance(k.value, ast.Constant) and k.value.value == words
                for k in node.keywords
            )
        ]
        assert hits == ["HTTPException"]

    def test_the_missing_scopes_403_is_plain_and_answers_the_status_line(self):
        from services.auth.auth_middleware import require_scopes

        checker = require_scopes(["admin", "secret-scope"])
        with pytest.raises(HTTPException) as exc:
            checker(SimpleNamespace(scopes=["user"]))
        assert not getattr(exc.value, "user_facing", False)
        reply = _through_the_handler(exc.value)
        assert reply.json()["message"] == "You don't have permission to do that."
        assert "secret-scope" not in reply.text


class TestTheAdminRefusalPrecedesAnyWrite:
    """CXO: "Nothing was changed." stays only with a test that the refusal comes first.
    ``require_admin`` is a dependency, so the route body never runs when it refuses."""

    def test_the_route_body_never_runs(self):
        from services.auth import auth_middleware
        from services.auth.auth_middleware import get_current_user, require_admin
        from web.app import app as real_app

        writes = []
        app = FastAPI()
        app.add_exception_handler(HTTPException, real_app.exception_handlers[HTTPException])

        @app.post("/write")
        async def _write(_user=Depends(require_admin)):
            writes.append("written")
            return {"ok": True}

        app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
            user_id=UUID(int=7), sub="u"
        )
        with patch.object(auth_middleware, "_user_is_admin", AsyncMock(return_value=False)):
            reply = TestClient(app).post("/write")
        assert reply.status_code == 403
        assert reply.json()["message"] == (
            "This changes app-wide configuration, so it needs an admin account. "
            "Nothing was changed."
        )
        assert writes == []


def test_no_marked_line_carries_a_code_word_the_cxo_named():
    """CXO's rule for every kept or reworded line: no ``user_id``, ``full_name``,
    ``ISO format`` or ``ACTIVE state``."""
    for module, name, words, _source in TABLE:
        for code_word in ("user_id", "full_name", "ISO format", "ACTIVE state"):
            assert code_word not in words, f"{module}.{name}"
    assert all(re.search(r"[.!?]$", words) for _m, _n, words, _s in TABLE)
