"""#1678 — PiperConfigLoader._format_system_prompt() drift/render pins.

`_format_system_prompt()` used to extract exactly six hardcoded section
names ("User Context", "Current Focus (Q4 2025)", "Project Portfolio",
"Standing Priorities", "Calendar Patterns", "Knowledge Sources") — a set
that predates the current `config/PIPER.md` v3.0.0 layout (#923) and
doesn't match ANY of its real section headers ("System Identity", "Default
Personality Traits", "System Capabilities", ...). The effective system
prompt was two hardcoded lines + a hardcoded BEHAVIOR GUIDELINES block; the
entire curated file was silently dropped.

The fix renders every section the parsed config ACTUALLY has, in file
order, rather than matching against a fixed name list — so the file and
the renderer cannot drift apart the way they did here. This suite pins:
  1. every real PIPER.md section reaches the prompt (the drift pin);
  2. the exact rendered shape for a small controlled config (the render
     pin);
  3. the renderer still serves `personalization_service.py`'s directly-
     supplied dicts (NEUTRAL_DEFAULT_CONTEXT and a DB-stored principal
     context) with byte-identical output to the pre-fix hardcoded path —
     the "one formatter, two callers" contract #1678 preserves;
  4. an arbitrary custom section name (standing in for a real
     PIPER.user.md, which ADR-075 D3 says is served as a plain FALLBACK
     file, never merged with PIPER.md) renders through the same generic
     path, not a hardcoded allowlist;
  5. honest-empty behavior on a missing/unparseable file — never a crash.
"""

from __future__ import annotations

import re
from pathlib import Path

from services.configuration.piper_config_loader import PiperConfigLoader, piper_config_loader

# Every section config/PIPER.md v3.0.0 actually has, as of #1678 — used only
# to pin that the drift test's file-derived section set isn't vacuous (the
# TRUE assertion is "every section the file parses reaches the prompt",
# not a re-hardcoding of this list as the source of truth).
_MIN_EXPECTED_PIPER_MD_SECTION_COUNT = 8


def test_drift_pin_every_piper_md_section_reaches_the_prompt():
    """Every section `config/PIPER.md` actually parses to must appear in the
    rendered prompt. Fails if the file gains a section the renderer drops —
    the exact failure mode #1678 fixes (the file and the renderer silently
    drifting apart)."""
    loader = PiperConfigLoader(config_path="config/PIPER.md")
    config = loader.load_config()

    assert config, "config/PIPER.md failed to parse — cannot pin drift against nothing"
    assert len(config) >= _MIN_EXPECTED_PIPER_MD_SECTION_COUNT, (
        f"config/PIPER.md parsed only {len(config)} section(s) — expected at least "
        f"{_MIN_EXPECTED_PIPER_MD_SECTION_COUNT}. Either the file changed shape or "
        "parsing regressed; update this pin deliberately if the former."
    )

    prompt = loader._format_system_prompt(config)
    rendered_headers = set(re.findall(r"^## (.+)$", prompt, re.MULTILINE))

    missing = []
    for section_name, content in config.items():
        if not content or not content.strip():
            continue
        expected_header = loader._clean_section_header(section_name)
        if expected_header not in rendered_headers:
            missing.append(section_name)

    assert not missing, (
        f"Section(s) parsed from config/PIPER.md but missing from the rendered "
        f"prompt: {missing}. This is exactly the #1678 bug — content the file "
        f"has silently failing to reach the LLM."
    )


def test_non_regression_prompt_is_not_the_two_line_stub():
    """Pre-fix, `get_system_prompt()` returned a 439-char stub (two header
    lines + hardcoded BEHAVIOR GUIDELINES only) because none of the six
    hardcoded section names matched the real file. Pin that the live prompt
    is now substantially larger and carries real file content."""
    piper_config_loader.clear_cache()
    prompt = piper_config_loader.get_system_prompt()

    assert len(prompt) > 1000, (
        f"System prompt is only {len(prompt)} chars — close to the pre-fix "
        f"439-char stub. config/PIPER.md content is likely not reaching the "
        f"prompt again."
    )
    # Real PIPER.md content (System Capabilities section), not just the
    # hardcoded scaffold lines.
    assert "GitHub Integration" in prompt
    assert "## BEHAVIOR GUIDELINES" in prompt


def test_render_pin_exact_prompt_shape():
    """Exact rendered shape for a small controlled config: scaffold lines,
    one `## HEADER` + content + blank-line block per section in file order,
    then the BEHAVIOR GUIDELINES block."""
    loader = PiperConfigLoader(config_path="config/PIPER.md")
    config = {
        "🤖 First Section": "First content.",
        "Second Section": "Second content.",
    }

    prompt = loader._format_system_prompt(config)

    expected = (
        "You are Piper Morgan, an intelligent product management assistant.\n"
        "Use the following context to provide personalized, context-aware assistance:\n"
        "\n"
        "## FIRST SECTION\n"
        "First content.\n"
        "\n"
        "## SECOND SECTION\n"
        "Second content.\n"
        "\n"
        "## BEHAVIOR GUIDELINES\n"
        "- Be direct and efficiency-focused\n"
        "- Provide evidence-based responses\n"
        "- Reference specific projects, priorities, and context\n"
        "- Maintain professional but personable tone\n"
        "- Suggest next steps when appropriate\n"
        "- Use the user's name (if known) and refer to specific projects\n"
    )
    assert prompt == expected


def test_render_pin_empty_config_still_carries_behavior_guidelines():
    """Guidance must never be lost, even with a config that has no sections
    at all (e.g. an unparseable file degrading to `{}`, if that ever
    happened — the honest-empty path uses `_get_default_config()` instead,
    but the formatter itself must be safe against an empty dict too)."""
    loader = PiperConfigLoader(config_path="config/PIPER.md")
    prompt = loader._format_system_prompt({})

    assert "## BEHAVIOR GUIDELINES" in prompt
    assert "You are Piper Morgan" in prompt


def test_neutral_default_context_render_is_byte_identical_to_legacy_output():
    """`personalization_service.NEUTRAL_DEFAULT_CONTEXT` is keyed with the
    SAME two names ("User Context", "Standing Priorities") the pre-#1678
    hardcoded formatter special-cased — its comment says so explicitly
    ("SAME section names PiperConfigLoader._format_system_prompt() already
    parses"). The generic renderer must keep producing byte-identical
    output for this exact dict, or every seeded neutral-default persona's
    system prompt silently changes shape."""
    from services.configuration.personalization_service import NEUTRAL_DEFAULT_CONTEXT

    loader = PiperConfigLoader(config_path="config/PIPER.md")
    prompt = loader._format_system_prompt(NEUTRAL_DEFAULT_CONTEXT)

    expected = (
        "You are Piper Morgan, an intelligent product management assistant.\n"
        "Use the following context to provide personalized, context-aware assistance:\n"
        "\n"
        "## USER CONTEXT\n"
        f"{NEUTRAL_DEFAULT_CONTEXT['User Context']}\n"
        "\n"
        "## STANDING PRIORITIES\n"
        f"{NEUTRAL_DEFAULT_CONTEXT['Standing Priorities']}\n"
        "\n"
        "## BEHAVIOR GUIDELINES\n"
        "- Be direct and efficiency-focused\n"
        "- Provide evidence-based responses\n"
        "- Reference specific projects, priorities, and context\n"
        "- Maintain professional but personable tone\n"
        "- Suggest next steps when appropriate\n"
        "- Use the user's name (if known) and refer to specific projects\n"
    )
    assert prompt == expected


def test_db_stored_principal_context_renders_any_section_name():
    """A real per-principal `PersonalizationContext.context` row (ADR-075
    D2) can carry arbitrary section names a customized profile chose — not
    just the two NEUTRAL_DEFAULT_CONTEXT keys. The generic renderer must
    not silently drop a section just because its name isn't one of the
    legacy six (the exact #1678 bug, reproduced here at the DB-row-dict
    call site instead of the file call site)."""
    loader = PiperConfigLoader(config_path="config/PIPER.md")
    custom_context = {"Custom Working Style": "Prefers terse, bulleted answers."}

    prompt = loader._format_system_prompt(custom_context)

    assert "## CUSTOM WORKING STYLE" in prompt
    assert "Prefers terse, bulleted answers." in prompt


def test_overlay_fallback_pin_arbitrary_section_reaches_prompt(tmp_path: Path):
    """ADR-075 D3: a personal `PIPER.user.md` is served as a FALLBACK file
    (whichever file the loader is pointed at wins, whole — never a merge of
    both). Whatever real section names that file has, the same generic
    renderer must carry them through — not a hardcoded allowlist tuned to
    PIPER.md's current headers. Uses a section name that matches neither
    PIPER.md's real headers nor the legacy six-name list, standing in for a
    personal PIPER.user.md's own custom content."""
    user_config = tmp_path / "PIPER.user.md"
    user_config.write_text(
        "# PIPER.user.md\n\n"
        "## 👤 **My Personal Working Notes**\n\n"
        "Prefers async updates over meetings.\n"
    )

    loader = PiperConfigLoader(config_path=str(user_config))
    prompt = loader.get_system_prompt()

    assert "## MY PERSONAL WORKING NOTES" in prompt
    assert "Prefers async updates over meetings." in prompt


def test_missing_file_degrades_honestly_never_crashes(tmp_path: Path):
    """Absent config file → the documented default config/prompt, not a
    crash and not a silent empty string. `__init__` mkdir's the parent
    (existing loader behavior), so this uses a writable tmp_path rather
    than an unwritable absolute root path."""
    missing_config = tmp_path / "missing" / "PIPER.md"
    loader = PiperConfigLoader(config_path=str(missing_config))
    prompt = loader.get_system_prompt()

    assert prompt
    assert "You are Piper Morgan" in prompt


def test_unparseable_file_degrades_honestly_never_crashes(tmp_path: Path):
    """A config_path that exists but can't be read as a file (here: a
    directory) must degrade to the default config, never raise out of
    `get_system_prompt()`."""
    directory_as_config = tmp_path / "PIPER.md"
    directory_as_config.mkdir()

    loader = PiperConfigLoader(config_path=str(directory_as_config))
    prompt = loader.get_system_prompt()

    assert prompt
    assert "You are Piper Morgan" in prompt
