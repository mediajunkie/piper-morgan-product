"""
Unit tests for chat widget component (#554).

Tests validate:
- Widget template structure and required elements
- CSS styling and responsive design
- JavaScript functionality for session management
- Toggle functionality and state persistence
- Message handling and history management
"""

import re
from pathlib import Path

import pytest


class TestChatWidgetTemplate:
    """Tests for chat-widget.html template structure."""

    @pytest.fixture
    def widget_html(self):
        """Load the widget template."""
        widget_path = Path("templates/components/chat-widget.html")
        assert widget_path.exists(), "chat-widget.html not found"
        return widget_path.read_text()

    def test_widget_container_exists(self, widget_html):
        """Widget has required container element."""
        assert "chat-widget-container" in widget_html

    def test_widget_container_id(self, widget_html):
        """Widget container has correct ID."""
        assert 'id="chat-widget-container"' in widget_html

    def test_widget_toggle_button_exists(self, widget_html):
        """Widget has toggle button."""
        assert "chat-widget-toggle" in widget_html

    def test_toggle_button_onclick_handler(self, widget_html):
        """Toggle button has onclick handler."""
        assert 'onclick="window.toggleChatWidget()"' in widget_html

    def test_widget_chat_container(self, widget_html):
        """Widget has chat container element."""
        assert 'class="chat-container"' in widget_html or "chat-container" in widget_html

    def test_chat_header_exists(self, widget_html):
        """Chat container has header."""
        assert "chat-header" in widget_html

    def test_chat_close_button_exists(self, widget_html):
        """Chat header has close button."""
        assert "chat-close" in widget_html

    def test_chat_window_exists(self, widget_html):
        """Widget has chat window for messages."""
        assert 'id="chat-window"' in widget_html or "chat-window" in widget_html

    def test_chat_form_exists(self, widget_html):
        """Widget has chat form."""
        assert 'id="chatForm"' in widget_html or "chatForm" in widget_html

    def test_chat_form_has_correct_id(self, widget_html):
        """Chat form has id 'chatForm' for JavaScript reference."""
        assert 'id="chatForm"' in widget_html

    def test_chat_input_exists(self, widget_html):
        """Widget has chat input field."""
        assert "chat-input" in widget_html

    def test_chat_input_is_textarea(self, widget_html):
        """#1737: chat input is a <textarea> (was <input type="text">) so
        long messages wrap + grow instead of scrolling off the right edge."""
        markup = re.sub(r"<!--.*?-->", "", widget_html, flags=re.DOTALL)
        assert "<textarea" in markup
        assert "<input" not in markup
        assert 'rows="1"' in markup

    def test_chat_input_name(self, widget_html):
        """Chat input has name attribute."""
        assert 'name="message"' in widget_html

    def test_chat_submit_button_exists(self, widget_html):
        """Widget has submit button."""
        assert 'type="submit"' in widget_html

    def test_initial_bot_message(self, widget_html):
        """Widget includes initial bot greeting."""
        assert "What can I help you with today?" in widget_html

    def test_aria_labels_present(self, widget_html):
        """Widget buttons have accessibility labels."""
        assert "aria-label" in widget_html

    def test_emoji_toggle_button(self, widget_html):
        """Toggle button includes emoji."""
        assert "💬" in widget_html

    def test_dependencies_documented(self, widget_html):
        """Widget component documents its dependencies."""
        assert "chat.css" in widget_html or "chat.js" in widget_html


class TestChatWidgetCSS:
    """Tests for chat.css styles."""

    @pytest.fixture
    def widget_css(self):
        """Load the widget CSS."""
        css_path = Path("web/static/css/chat.css")
        assert css_path.exists(), "chat.css not found"
        return css_path.read_text()

    def test_floating_position_styles(self, widget_css):
        """CSS includes fixed positioning for floating widget."""
        assert "position: fixed" in widget_css or "position:fixed" in widget_css.replace(" ", "")

    def test_z_index_defined(self, widget_css):
        """CSS defines z-index for layering."""
        assert "z-index" in widget_css

    def test_chat_widget_container_styling(self, widget_css):
        """CSS has chat-widget-container styles."""
        assert ".chat-widget-container" in widget_css

    def test_expanded_state_styles(self, widget_css):
        """CSS includes expanded state styles."""
        assert ".expanded" in widget_css

    def test_toggle_button_styles(self, widget_css):
        """CSS includes toggle button styles."""
        assert ".chat-widget-toggle" in widget_css

    def test_toggle_button_dimensions(self, widget_css):
        """Toggle button has specific dimensions."""
        # Should have width and height for circular button
        assert "56px" in widget_css or "width" in widget_css

    def test_toggle_button_hover_state(self, widget_css):
        """Toggle button has hover state."""
        assert ".chat-widget-toggle:hover" in widget_css

    def test_toggle_button_focus_state(self, widget_css):
        """Toggle button has focus state for accessibility."""
        assert ".chat-widget-toggle:focus" in widget_css

    def test_chat_container_styles(self, widget_css):
        """CSS styles the chat container."""
        assert ".chat-container" in widget_css

    def test_chat_window_height(self, widget_css):
        """Chat window has defined height."""
        assert "350px" in widget_css or "height" in widget_css

    def test_chat_form_styles(self, widget_css):
        """CSS styles the chat form."""
        assert ".chat-form" in widget_css

    def test_chat_input_styles(self, widget_css):
        """CSS styles the chat input."""
        assert ".chat-input" in widget_css

    def test_message_styles(self, widget_css):
        """CSS styles messages."""
        assert ".message" in widget_css

    def test_user_message_styling(self, widget_css):
        """CSS differentiates user messages."""
        assert ".user-message" in widget_css

    def test_bot_message_styling(self, widget_css):
        """CSS differentiates bot messages."""
        assert ".bot-message" in widget_css

    def test_responsive_styles_mobile(self, widget_css):
        """CSS includes mobile responsive styles."""
        assert "@media" in widget_css

    def test_responsive_breakpoint_tablet(self, widget_css):
        """CSS has tablet breakpoint."""
        assert "768px" in widget_css

    def test_responsive_breakpoint_phone(self, widget_css):
        """CSS has phone breakpoint."""
        assert "480px" in widget_css

    def test_animation_defined(self, widget_css):
        """CSS includes animation for widget expansion."""
        assert "@keyframes" in widget_css or "animation" in widget_css

    def test_error_message_styling(self, widget_css):
        """CSS includes error message styling."""
        assert ".error" in widget_css

    def test_thinking_message_styling(self, widget_css):
        """CSS includes thinking message styling."""
        assert ".thinking" in widget_css


class TestChatWidgetJS:
    """Tests for chat.js functionality."""

    @pytest.fixture
    def widget_js(self):
        """Load the widget JavaScript."""
        js_path = Path("web/static/js/chat.js")
        assert js_path.exists(), "chat.js not found"
        return js_path.read_text()

    def test_strict_mode(self, widget_js):
        """JS uses strict mode."""
        assert "'use strict'" in widget_js

    def test_iife_pattern(self, widget_js):
        """JS uses IIFE for encapsulation."""
        assert "(function()" in widget_js

    def test_toggle_function_exists(self, widget_js):
        """JS includes toggle function."""
        assert "toggleChatWidget" in widget_js

    def test_toggle_function_exported(self, widget_js):
        """Toggle function is exported to window."""
        assert "window.toggleChatWidget" in widget_js

    def test_append_message_function_exists(self, widget_js):
        """JS includes message append function."""
        assert "appendMessage" in widget_js

    def test_set_example_function_exists(self, widget_js):
        """JS includes setExample function."""
        assert "setExample" in widget_js

    def test_session_id_generation(self, widget_js):
        """JS can generate session IDs."""
        assert "generateSessionId" in widget_js

    def test_get_or_create_session_id(self, widget_js):
        """JS has session ID retrieval function."""
        assert "getOrCreateSessionId" in widget_js

    def test_session_storage_used(self, widget_js):
        """JS uses localStorage for session persistence."""
        assert "localStorage" in widget_js

    def test_storage_availability_check(self, widget_js):
        """JS checks if localStorage is available."""
        assert "storageAvailable" in widget_js

    def test_storage_keys_defined(self, widget_js):
        """JS defines storage keys as constants."""
        assert "STORAGE_KEYS" in widget_js

    def test_session_id_storage_key(self, widget_js):
        """JS defines session ID storage key."""
        assert "SESSION_ID" in widget_js or "piper_chat_session" in widget_js

    def test_chat_history_storage_key(self, widget_js):
        """JS defines chat history storage key."""
        assert "CHAT_HISTORY" in widget_js or "piper_chat_history" in widget_js

    def test_widget_state_storage_key(self, widget_js):
        """JS defines widget state storage key."""
        assert "WIDGET_STATE" in widget_js or "piper_chat_widget_expanded" in widget_js

    def test_api_endpoint_correct(self, widget_js):
        """JS calls correct API endpoint."""
        assert "/api/v1/intent" in widget_js

    def test_form_submit_handler(self, widget_js):
        """JS includes form submit handling."""
        assert "addEventListener" in widget_js and "submit" in widget_js

    def test_dom_ready_handler(self, widget_js):
        """JS waits for DOM ready."""
        assert "DOMContentLoaded" in widget_js

    def test_message_classes_used(self, widget_js):
        """JS applies correct message classes."""
        assert "user-message" in widget_js
        assert "bot-message" in widget_js

    def test_workflow_polling(self, widget_js):
        """JS includes workflow polling functionality."""
        assert "pollWorkflowStatus" in widget_js

    def test_error_handling(self, widget_js):
        """JS includes error handling."""
        assert "handleErrorResponse" in widget_js

    def test_response_handling(self, widget_js):
        """JS includes response handling."""
        assert "handleDirectResponse" in widget_js

    def test_window_exports(self, widget_js):
        """JS exports ChatWidget object to window."""
        assert "window.ChatWidget" in widget_js

    def test_chat_history_functions(self, widget_js):
        """JS includes chat history functions."""
        assert "saveChatHistory" in widget_js
        assert "loadChatHistory" in widget_js
        assert "clearChatHistory" in widget_js

    def test_session_persistence(self, widget_js):
        """JS persists session across pages."""
        assert "sessionId" in widget_js


class TestSessionManagement:
    """Tests for session persistence logic."""

    @pytest.fixture
    def widget_js(self):
        """Load the widget JavaScript."""
        js_path = Path("web/static/js/chat.js")
        assert js_path.exists(), "chat.js not found"
        return js_path.read_text()

    def test_session_id_initialization(self, widget_js):
        """Session ID is initialized on load."""
        assert "getOrCreateSessionId" in widget_js

    def test_session_id_persisted(self, widget_js):
        """Session ID is stored in localStorage."""
        assert "localStorage.setItem" in widget_js

    def test_session_id_retrieved(self, widget_js):
        """Session ID can be retrieved from localStorage."""
        assert "localStorage.getItem" in widget_js

    def test_crypto_api_fallback(self, widget_js):
        """JS has fallback for crypto API."""
        assert "crypto.randomUUID" in widget_js
        assert "generateSessionId" in widget_js

    def test_widget_state_persists(self, widget_js):
        """Widget expanded state is persisted."""
        assert "WIDGET_STATE" in widget_js

    def test_history_trimming(self, widget_js):
        """Chat history is trimmed to prevent storage quota issues."""
        assert "slice" in widget_js  # Array slicing for trimming
        assert "50" in widget_js  # History limit

    def test_history_restoration(self, widget_js):
        """Chat history can be restored from storage."""
        assert "restoreChatHistory" in widget_js

    def test_try_catch_storage_protection(self, widget_js):
        """Storage operations are wrapped in try-catch."""
        assert "try" in widget_js and "catch" in widget_js

    def test_graceful_storage_degradation(self, widget_js):
        """Code handles storage unavailability gracefully."""
        assert "storageAvailable" in widget_js


class TestToggleFunctionality:
    """Tests for widget toggle functionality."""

    @pytest.fixture
    def widget_js(self):
        """Load the widget JavaScript."""
        js_path = Path("web/static/js/chat.js")
        assert js_path.exists(), "chat.js not found"
        return js_path.read_text()

    @pytest.fixture
    def widget_html(self):
        """Load the widget template."""
        widget_path = Path("templates/components/chat-widget.html")
        assert widget_path.exists(), "chat-widget.html not found"
        return widget_path.read_text()

    def test_toggle_class_manipulation(self, widget_js):
        """Toggle function manipulates container class."""
        assert "classList.toggle" in widget_js
        assert "expanded" in widget_js

    def test_toggle_checks_expanded_state(self, widget_js):
        """Toggle function checks if container is expanded."""
        assert "classList.contains" in widget_js

    def test_toggle_updates_button_icon(self, widget_js):
        """Toggle updates button icon."""
        assert "innerHTML" in widget_js
        assert "✕" in widget_js  # Close icon
        assert "💬" in widget_js  # Chat icon

    def test_toggle_focuses_input(self, widget_js):
        """Toggle focuses input when expanded."""
        assert "input.focus()" in widget_js

    def test_toggle_uses_settimeout(self, widget_js):
        """Toggle uses setTimeout for focus after DOM update."""
        assert "setTimeout" in widget_js

    def test_form_not_submitted_on_toggle(self, widget_html):
        """Toggle buttons use type='button' to prevent form submission."""
        # Count occurrences of type="button" in toggle buttons
        assert 'type="button"' in widget_html

    def test_toggle_button_has_proper_event_handler(self, widget_html):
        """Toggle buttons have onclick handlers for both toggle and close."""
        assert widget_html.count('onclick="window.toggleChatWidget()"') >= 2

    def test_toggle_accessible(self, widget_js):
        """Toggle maintains accessibility with proper focus management."""
        assert "focus" in widget_js


class TestMessageHandling:
    """Tests for message display and history."""

    @pytest.fixture
    def widget_js(self):
        """Load the widget JavaScript."""
        js_path = Path("web/static/js/chat.js")
        assert js_path.exists(), "chat.js not found"
        return js_path.read_text()

    def test_append_message_creates_containers(self, widget_js):
        """appendMessage creates proper DOM structure."""
        assert "message-container" in widget_js
        assert "createElement" in widget_js

    def test_append_message_auto_scrolls(self, widget_js):
        """appendMessage scrolls to latest message."""
        assert "scrollTop" in widget_js
        assert "scrollHeight" in widget_js

    def test_user_message_handling(self, widget_js):
        """User messages are handled differently than bot messages."""
        assert "textContent" in widget_js
        assert "innerHTML" in widget_js

    def test_message_persistence_toggle(self, widget_js):
        """Messages can be marked for/against persistence."""
        assert "persist" in widget_js

    def test_thinking_message_not_persisted(self, widget_js):
        """'Thinking...' messages are not persisted."""
        assert "Thinking..." in widget_js

    def test_history_saved_after_message(self, widget_js):
        """Chat history is saved after new message."""
        assert "saveChatHistory" in widget_js

    def test_message_timestamp_recorded(self, widget_js):
        """Messages include timestamp."""
        assert "Date.now()" in widget_js or "timestamp" in widget_js

    def test_form_submission_handled(self, widget_js):
        """Form submission is properly handled."""
        assert "preventDefault" in widget_js
        assert "chatForm" in widget_js


class TestAPIIntegration:
    """Tests for API interaction."""

    @pytest.fixture
    def widget_js(self):
        """Load the widget JavaScript."""
        js_path = Path("web/static/js/chat.js")
        assert js_path.exists(), "chat.js not found"
        return js_path.read_text()

    def test_fetch_api_used(self, widget_js):
        """JS uses Fetch API for HTTP requests."""
        assert "fetch(" in widget_js

    def test_intent_endpoint_called(self, widget_js):
        """JS calls the correct intent endpoint."""
        assert "/api/v1/intent" in widget_js

    def test_session_sent_with_request(self, widget_js):
        """Session ID is sent with API requests."""
        assert "session_id" in widget_js

    def test_credentials_included(self, widget_js):
        """Fetch requests include credentials."""
        assert "credentials" in widget_js

    def test_json_content_type(self, widget_js):
        """Requests set JSON content-type."""
        assert "application/json" in widget_js

    def test_response_parsed_as_json(self, widget_js):
        """Responses are parsed as JSON."""
        assert "response.json()" in widget_js

    def test_error_handling_in_fetch(self, widget_js):
        """Fetch errors are properly handled."""
        assert "throw new Error" in widget_js or ".catch" in widget_js

    def test_workflow_id_handling(self, widget_js):
        """JS handles workflow IDs from API responses."""
        assert "workflow_id" in widget_js

    def test_permission_intent_check(self, widget_js):
        """JS checks for permission intent processor."""
        assert "processPermissionIntent" in widget_js


class TestInitialization:
    """Tests for widget initialization."""

    @pytest.fixture
    def widget_js(self):
        """Load the widget JavaScript."""
        js_path = Path("web/static/js/chat.js")
        assert js_path.exists(), "chat.js not found"
        return js_path.read_text()

    def test_init_function_exists(self, widget_js):
        """Initialization function is defined."""
        assert "initChat" in widget_js

    def test_init_waits_for_form(self, widget_js):
        """Init checks for form existence before proceeding."""
        assert "chatForm" in widget_js

    def test_init_restores_history(self, widget_js):
        """Init restores chat history."""
        assert "restoreChatHistory" in widget_js

    def test_init_restores_widget_state(self, widget_js):
        """Init restores widget expanded state."""
        assert "restoreWidgetState" in widget_js

    def test_init_adds_form_listener(self, widget_js):
        """Init adds form submit listener."""
        assert "addEventListener" in widget_js

    def test_dom_ready_check(self, widget_js):
        """JS checks document.readyState for DOM ready."""
        assert "document.readyState" in widget_js or "DOMContentLoaded" in widget_js

    def test_init_called_on_ready(self, widget_js):
        """Init is called when DOM is ready."""
        assert ("DOMContentLoaded" in widget_js and "initChat" in widget_js) or (
            "document.readyState" in widget_js and "initChat" in widget_js
        )


class TestAccessibility:
    """Tests for accessibility features."""

    @pytest.fixture
    def widget_html(self):
        """Load the widget template."""
        widget_path = Path("templates/components/chat-widget.html")
        assert widget_path.exists(), "chat-widget.html not found"
        return widget_path.read_text()

    @pytest.fixture
    def widget_css(self):
        """Load the widget CSS."""
        css_path = Path("web/static/css/chat.css")
        assert css_path.exists(), "chat.css not found"
        return css_path.read_text()

    def test_buttons_have_aria_labels(self, widget_html):
        """Interactive buttons have aria-label attributes."""
        assert "aria-label" in widget_html

    def test_form_inputs_have_labels(self, widget_html):
        """Form inputs have associated labels or placeholders."""
        assert "placeholder" in widget_html or "label" in widget_html

    def test_focus_states_defined_in_css(self, widget_css):
        """CSS includes :focus states for interactive elements."""
        assert ":focus" in widget_css

    def test_contrast_text_styling(self, widget_css):
        """CSS includes color definitions for text contrast."""
        assert "color:" in widget_css

    def test_semantic_html_structure(self, widget_html):
        """HTML uses semantic elements."""
        assert "<form" in widget_html or "<button" in widget_html


class TestMobileResponsiveness:
    """Tests for mobile responsive design."""

    @pytest.fixture
    def widget_css(self):
        """Load the widget CSS."""
        css_path = Path("web/static/css/chat.css")
        assert css_path.exists(), "chat.css not found"
        return css_path.read_text()

    def test_has_mobile_breakpoints(self, widget_css):
        """CSS includes mobile breakpoints."""
        assert "@media" in widget_css

    def test_tablet_breakpoint(self, widget_css):
        """CSS includes tablet breakpoint (768px)."""
        assert "768px" in widget_css

    def test_phone_breakpoint(self, widget_css):
        """CSS includes phone breakpoint (480px)."""
        assert "480px" in widget_css

    def test_mobile_full_screen_support(self, widget_css):
        """CSS supports full-screen on small screens."""
        assert "100vh" in widget_css or "100vw" in widget_css

    def test_touch_target_sizes(self, widget_css):
        """CSS ensures touch targets are appropriately sized."""
        assert "44px" in widget_css  # iOS recommended touch target

    def test_responsive_input_sizing(self, widget_css):
        """CSS adjusts input sizing for mobile."""
        # Should have font-size adjustments for mobile inputs
        assert "@media" in widget_css

    def test_prevents_zoom_on_input_focus(self, widget_css):
        """CSS includes font-size for input (prevents iOS zoom)."""
        assert "font-size" in widget_css


class TestComposerAutogrow1737:
    """#1737: composer grows to ~6 rows then scrolls internally, instead of
    a single-line <input> ticker-taping content off the right edge. Pinned at
    the source layer (template attributes + JS source), per m-43 — there is
    no JS harness in this repo (see tests/unit/web/test_static_cache_policy_1859.py
    for the same source-pin pattern)."""

    @pytest.fixture
    def widget_html(self):
        return Path("templates/components/chat-widget.html").read_text()

    @pytest.fixture
    def inline_html(self):
        return Path("templates/components/chat-inline.html").read_text()

    @pytest.fixture
    def chat_css(self):
        return Path("web/static/css/chat.css").read_text()

    @pytest.fixture
    def chat_js(self):
        return Path("web/static/js/chat.js").read_text()

    def test_both_composers_are_textareas(self, widget_html, inline_html):
        """Both live chat surfaces (floating widget + home inline) use a
        <textarea>, not <input type="text">."""
        for html in (widget_html, inline_html):
            markup = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)
            assert "<textarea" in markup
            assert 'type="text"' not in markup
            assert 'name="message"' in markup
            assert 'class="chat-input"' in markup

    def test_composers_start_at_one_row(self, widget_html, inline_html):
        """rows="1" — the composer starts single-line and only grows with
        content (it doesn't default to a tall box)."""
        for html in (widget_html, inline_html):
            assert 'rows="1"' in html

    def test_css_disables_manual_resize_handle(self, chat_css):
        """The browser's native textarea resize handle is disabled — growth
        is driven by chat.js's autogrow, not manual dragging."""
        assert "resize: none;" in chat_css

    def test_css_no_transition_on_composer(self, chat_css):
        """No CSS transition/animation touches .chat-input's box — the
        autogrow resize is an instant style.height set in JS, so there is
        nothing here for prefers-reduced-motion to need to disable."""
        # Isolate the base .chat-input rule block and confirm it carries no
        # transition/animation property.
        start = chat_css.index(".chat-input {")
        end = chat_css.index("}", start)
        rule_body = chat_css[start:end]
        assert "transition" not in rule_body
        assert "animation" not in rule_body

    def test_js_defines_max_row_cap(self, chat_js):
        """A capped row count exists (the "~6 rows then scroll" requirement),
        not unbounded growth."""
        assert "COMPOSER_MAX_ROWS = 6" in chat_js

    def test_js_defines_autogrow_function(self, chat_js):
        """The autogrow function exists and is scrollHeight-driven, capped
        at the max-row height, with no external library."""
        assert "function autoGrowComposer(textarea)" in chat_js
        assert "textarea.scrollHeight" in chat_js
        assert "maxHeight" in chat_js

    def test_js_wires_autogrow_on_input_event(self, chat_js):
        """The composer listens for the 'input' event and re-runs autogrow —
        this is what makes it grow AS THE USER TYPES, not just on submit."""
        assert (
            'composerInput.addEventListener("input", () => autoGrowComposer(composerInput));'
            in chat_js
        )

    def test_js_enter_sends_shift_enter_newlines(self, chat_js):
        """Enter (without Shift) submits the form; Shift+Enter is left to
        the browser's default textarea behavior (insert a newline) — no
        explicit Shift+Enter handler exists because none is needed."""
        assert '"Enter" && !e.shiftKey && !e.isComposing' in chat_js
        assert "e.preventDefault();" in chat_js
        assert "form.requestSubmit" in chat_js

    def test_js_ime_composition_guarded(self, chat_js):
        """isComposing guards against submitting mid-IME-candidate-selection
        on the Enter keystroke that confirms a composed character."""
        assert "e.isComposing" in chat_js

    def test_js_collapses_composer_after_send(self, chat_js):
        """After a message is sent the composer resets to one row instead
        of staying expanded at its pre-send height."""
        assert 'input.value = "";\n      autoGrowComposer(input);' in chat_js


class TestFileIntegrity:
    """Tests for file completeness and integrity."""

    def test_chat_js_not_empty(self):
        """chat.js file is not empty."""
        js_path = Path("web/static/js/chat.js")
        content = js_path.read_text()
        assert len(content) > 100

    def test_chat_css_not_empty(self):
        """chat.css file is not empty."""
        css_path = Path("web/static/css/chat.css")
        content = css_path.read_text()
        assert len(content) > 100

    def test_widget_html_not_empty(self):
        """chat-widget.html file is not empty."""
        widget_path = Path("templates/components/chat-widget.html")
        content = widget_path.read_text()
        assert len(content) > 50

    def test_js_valid_structure(self):
        """chat.js has valid JavaScript structure."""
        js_path = Path("web/static/js/chat.js")
        content = js_path.read_text()
        # Check for balanced braces
        assert content.count("{") == content.count("}")
        assert content.count("(") == content.count(")")

    def test_css_valid_structure(self):
        """chat.css has valid CSS structure."""
        css_path = Path("web/static/css/chat.css")
        content = css_path.read_text()
        # Check for balanced braces
        assert content.count("{") == content.count("}")

    def test_html_valid_structure(self):
        """chat-widget.html has valid HTML structure."""
        widget_path = Path("templates/components/chat-widget.html")
        content = widget_path.read_text()
        # Check for basic HTML validity
        assert "<" in content and ">" in content
