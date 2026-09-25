"""#1791 — PiperConfigParser + PersonalityResponseEnhancer at the unit layer,
below the HTTP routes (see test_personality_principal_from_session_1751.py and
test_personality_put_admin_gated_1734.py for the route-level pins, and
tests/unit/services/domain/test_personality_preference_persistence_1791.py for
the real-DB UserPreferenceManager pins).

DENOMINATOR: this file covers PiperConfigParser.load_personality_config /
save_personality_config / load_personality_config_scoped and
PersonalityResponseEnhancer.enhance_response's per-user behavior, directly —
two real-UUID users saving different profiles get their own back, a
never-saved user gets the instance default, and the ENHANCER actually
produces different output for two users with different warmth_level (not
just that the stored dict differs). A non-UUID caller (the CLI's literal
"default") still round-trips through the instance file, unchanged from
pre-#1791 behavior.

LAYER (m-43): no live Postgres required — UserPreferenceManager degrades to
in-memory-only for the life of one PiperConfigParser instance without a real
DB row (documented on the class itself; see test_preferences_timezone_1876.py
for the same reliance elsewhere), which is enough for a same-process
save-then-load round trip. File-system layer: PiperConfigParser resolves
config/PIPER.user.md relative to CWD, so each test chdirs into tmp_path.
"""

from __future__ import annotations

import uuid

import pytest

from web.personality_integration import (
    PersonalityResponseEnhancer,
    PiperConfigParser,
    WebPersonalityConfig,
)

pytestmark = pytest.mark.asyncio

SENTINEL_OVERLAY = """# Piper Morgan User Configuration

```yaml
personality:
  warmth_level: 0.31
  confidence_style: numeric
  action_orientation: low
  technical_depth: detailed
```
"""

USER_A = uuid.uuid4()
USER_B = uuid.uuid4()


@pytest.fixture
def overlay(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    overlay_path = config_dir / "PIPER.user.md"
    overlay_path.write_text(SENTINEL_OVERLAY)
    return overlay_path


@pytest.fixture
def parser(overlay):
    return PiperConfigParser()


class TestTwoUsersEachGetTheirOwnProfileBack:
    async def test_different_saved_profiles_round_trip_independently(self, parser):
        config_a = WebPersonalityConfig(
            warmth_level=0.95,
            confidence_style="descriptive",
            action_orientation="medium",
            technical_depth="simplified",
        )
        config_b = WebPersonalityConfig(
            warmth_level=0.05,
            confidence_style="numeric",
            action_orientation="high",
            technical_depth="detailed",
        )

        assert await parser.save_personality_config(config_a, str(USER_A))
        assert await parser.save_personality_config(config_b, str(USER_B))

        loaded_a = await parser.load_personality_config(str(USER_A))
        loaded_b = await parser.load_personality_config(str(USER_B))

        assert loaded_a.to_dict() == config_a.to_dict()
        assert loaded_b.to_dict() == config_b.to_dict()
        assert loaded_a.to_dict() != loaded_b.to_dict()

    async def test_scope_is_user_after_a_save_instance_before(self, parser):
        before, before_scope = await parser.load_personality_config_scoped(str(USER_A))
        assert before_scope == "instance"
        assert before.warmth_level == 0.31

        await parser.save_personality_config(WebPersonalityConfig(warmth_level=0.77), str(USER_A))
        after, after_scope = await parser.load_personality_config_scoped(str(USER_A))
        assert after_scope == "user"
        assert after.warmth_level == 0.77


class TestUserWithNoAnswersGetsTheInstanceDefault:
    async def test_never_saved_user_reads_the_default_file(self, parser):
        config = await parser.load_personality_config(str(uuid.uuid4()))
        assert config.warmth_level == 0.31
        assert config.confidence_style == "numeric"


class TestNonUuidCallerUsesTheInstanceFileUnchanged:
    async def test_default_string_still_reads_and_writes_the_file(self, parser, overlay):
        loaded = await parser.load_personality_config("default")
        assert loaded.warmth_level == 0.31

        new_config = WebPersonalityConfig(warmth_level=0.6)
        assert await parser.save_personality_config(new_config, "default")
        assert "0.6" in overlay.read_text(), "a non-UUID caller's save must still hit the file"

        # And it must NOT have created a per-user row that a real UUID could collide with.
        reloaded = await parser.load_personality_config("default")
        assert reloaded.warmth_level == 0.6


class TestEnhancerShapesRepliesPerUser:
    async def test_two_users_different_warmth_produce_different_enhanced_text(self, parser):
        enhancer = PersonalityResponseEnhancer()

        warm = WebPersonalityConfig(warmth_level=0.95, confidence_style="hidden")
        cool = WebPersonalityConfig(warmth_level=0.1, confidence_style="hidden")

        await parser.save_personality_config(warm, str(USER_A))
        await parser.save_personality_config(cool, str(USER_B))

        config_a = await parser.load_personality_config(str(USER_A))
        config_b = await parser.load_personality_config(str(USER_B))

        text = "Task completed successfully"
        enhanced_a = enhancer.enhance_response(text, config_a, confidence=0.9)
        enhanced_b = enhancer.enhance_response(text, config_b, confidence=0.9)

        assert enhanced_a != enhanced_b, (
            "the enhancer produced identical output for two users with different "
            "saved warmth_level — per-user personality is not actually shaping replies"
        )
        assert enhanced_a.startswith(
            "Perfect!"
        ), "high warmth_level (user A) should prepend a warm opener"
        assert not enhanced_b.startswith(
            "Perfect!"
        ), "low warmth_level (user B) should NOT get the high-warmth opener"
