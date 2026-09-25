"""
Personality Integration for Web Interface

Provides personality enhancement integration for web endpoints.
Handles PIPER.user.md parsing and personality profile management.
"""

import os
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from services.domain.user_preference_manager import UserPreferenceManager


@dataclass
class WebPersonalityConfig:
    """Web-friendly personality configuration"""

    warmth_level: float = 0.7  # 0.0-1.0
    confidence_style: str = "contextual"  # numeric/descriptive/contextual/hidden
    action_orientation: str = "high"  # high/medium/low
    technical_depth: str = "balanced"  # detailed/balanced/simplified

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON responses"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WebPersonalityConfig":
        """Create from dictionary data"""
        return cls(
            warmth_level=data.get("warmth_level", 0.7),
            confidence_style=data.get("confidence_style", "contextual"),
            action_orientation=data.get("action_orientation", "high"),
            technical_depth=data.get("technical_depth", "balanced"),
        )


class PiperConfigParser:
    """Parser for PIPER.user.md configuration files, with a per-user overlay.

    #1791: personality preferences are per-user via ``UserPreferenceManager``
    (``users.preferences["upm"]["personality_profile"]``, the #1574 store).
    ``config/PIPER.user.md`` (and the rest of ``config_paths``) is now the
    INSTANCE-WIDE DEFAULT ONLY — served to any user who has never saved a
    profile of their own, never a per-user home. It is NOT migrated into any
    user's row: the file was shared across every alpha tester before this
    change, so whoever "owns" any given value in it today is unknowable — a
    copy would silently hand one unlucky user's history to whichever user
    happens to save first. Every user starts from the default and re-answers
    once, the same precedent #1422's questionnaire already set for testers.

    A ``user_id`` that does not parse as a UUID (the CLI's literal
    ``"default"``, or any other non-principal caller) has no per-user row to
    address — it falls through to the same instance-wide file, which is what
    "default" already meant. This is not a special case; it's the same rule
    applied to a caller that isn't a real user.
    """

    def __init__(self):
        self.config_paths = [
            Path("config/PIPER.user.md"),
            Path("PIPER.user.md"),
            Path("config/PIPER.defaults.md"),
        ]
        self._preferences = UserPreferenceManager()

    @staticmethod
    def _as_uuid(user_id: Any) -> Optional[uuid.UUID]:
        """A real per-user row requires a real principal. Anything else (the
        CLI's default string, a stray non-UUID caller) has no row to read or
        write and falls through to the instance-wide file."""
        try:
            return uuid.UUID(str(user_id))
        except (ValueError, TypeError, AttributeError):
            return None

    async def load_personality_config(self, user_id: str = "default") -> WebPersonalityConfig:
        """Load personality configuration: the user's own saved profile if
        they have one, else the instance-wide default file."""
        config, _scope = await self.load_personality_config_scoped(user_id)
        return config

    async def load_personality_config_scoped(
        self, user_id: str = "default"
    ) -> "tuple[WebPersonalityConfig, str]":
        """Same as ``load_personality_config``, plus which store actually
        served the result — ``"user"`` (the caller's own saved row) or
        ``"instance"`` (the shared default file, either because there's no
        real per-user principal or because this user has never saved a
        profile of their own). Lets callers (the API routes) report an
        honest ``scope`` instead of a hardcoded literal.
        """
        personality_data: Optional[Dict[str, Any]] = None
        scope = "instance"
        uid = self._as_uuid(user_id)
        if uid is not None:
            personality_data = await self._preferences.get_personality(uid)
            if personality_data is not None:
                scope = "user"

        if personality_data is None:
            # No real principal, or a real principal with nothing saved yet:
            # instance-wide default.
            config_data = self._load_config_file()
            personality_data = config_data.get("personality", {})

        return WebPersonalityConfig.from_dict(personality_data), scope

    def write_scope_for(self, user_id: str = "default") -> str:
        """Which store a save for this ``user_id`` will land in — ``"user"``
        (their own row) or ``"instance"`` (the shared default file, for a
        non-UUID caller). No I/O; mirrors ``save_personality_config``'s own
        routing decision so callers (the PUT route) can report it."""
        return "user" if self._as_uuid(user_id) is not None else "instance"

    async def save_personality_config(
        self, config: WebPersonalityConfig, user_id: str = "default"
    ) -> bool:
        """Save personality configuration.

        A real per-user principal writes to their OWN row only — never the
        shared instance file, which is exactly the property that let #1734's
        admin gate come off the PUT route in this same change (a per-user
        write no longer has a global blast radius). A non-UUID caller (the
        CLI's "default") has no row and writes the instance-wide file, same
        as before #1791.
        """
        uid = self._as_uuid(user_id)
        if uid is not None:
            try:
                await self._preferences.set_personality(uid, config.to_dict())
                return True
            except Exception as e:
                print(f"Error saving personality config: {e}")
                return False

        try:
            config_data = self._load_config_file()
            config_data["personality"] = config.to_dict()
            return self._save_config_file(config_data)
        except Exception as e:
            print(f"Error saving personality config: {e}")
            return False

    def _load_config_file(self) -> Dict[str, Any]:
        """Load configuration from PIPER.user.md file"""
        for config_path in self.config_paths:
            if config_path.exists():
                try:
                    with open(config_path, "r") as f:
                        content = f.read()

                    # Extract YAML from markdown (look for yaml code blocks)
                    if "```yaml" in content:
                        yaml_start = content.find("```yaml") + 7
                        yaml_end = content.find("```", yaml_start)
                        yaml_content = content[yaml_start:yaml_end].strip()
                        return yaml.safe_load(yaml_content) or {}

                except Exception as e:
                    print(f"Error loading config from {config_path}: {e}")
                    continue

        # Return default configuration
        return {
            "personality": {
                "warmth_level": 0.7,
                "confidence_style": "contextual",
                "action_orientation": "high",
                "technical_depth": "balanced",
            }
        }

    def _save_config_file(self, config_data: Dict[str, Any]) -> bool:
        """Save configuration to PIPER.user.md file"""
        try:
            config_path = self.config_paths[0]  # Use primary config path

            # Ensure directory exists
            config_path.parent.mkdir(parents=True, exist_ok=True)

            # Create markdown content with YAML
            yaml_content = yaml.dump(config_data, default_flow_style=False, sort_keys=False)
            markdown_content = f"""# Piper Morgan User Configuration

```yaml
{yaml_content}```

## Personality Settings

- **warmth_level**: How friendly vs professional (0.0-1.0)
- **confidence_style**: How confidence is displayed (numeric/descriptive/contextual/hidden)
- **action_orientation**: How much guidance is provided (high/medium/low)
- **technical_depth**: Level of technical detail (detailed/balanced/simplified)

## Usage

This configuration is automatically loaded by Piper Morgan for personality enhancement.
"""

            with open(config_path, "w") as f:
                f.write(markdown_content)

            return True

        except Exception as e:
            print(f"Error saving config file: {e}")
            return False


class PersonalityResponseEnhancer:
    """Simple response enhancer for web interface"""

    def __init__(self):
        self.config_parser = PiperConfigParser()

    def enhance_response(
        self, response: str, config: WebPersonalityConfig, confidence: float = 0.5
    ) -> str:
        """Enhance response with personality based on configuration with graceful degradation"""

        # Graceful degradation: return original response if input is invalid
        if not response:
            import logging

            logging.getLogger(__name__).warning(
                "Empty response provided to personality enhancement"
            )
            return response or ""

        if response is None:
            import logging

            logging.getLogger(__name__).warning("None response provided to personality enhancement")
            return ""

        try:
            # Store original response for fallback
            original_response = response

            # Apply warmth level enhancement
            if config.warmth_level >= 0.8:
                response = self._add_warmth(response, "high")
            elif config.warmth_level >= 0.5:
                response = self._add_warmth(response, "medium")

            # Add confidence indicators
            if config.confidence_style != "hidden":
                confidence_text = self._format_confidence(confidence, config.confidence_style)
                if confidence_text:
                    response = f"{response} ({confidence_text})"

            # Add action orientation
            if config.action_orientation == "high":
                response = self._add_action_guidance(response)

            return response

        except Exception as e:
            # Graceful degradation: log error and return original response
            import logging

            logging.getLogger(__name__).warning(f"Personality enhancement failed: {e}")
            return original_response

    def _add_warmth(self, response: str, level: str) -> str:
        """Add warmth to response based on level"""
        warmth_starters = {
            "high": ["Perfect!", "Great!", "Excellent!", "Fantastic!"],
            "medium": ["Good!", "Nice!", "Well done!", "Solid!"],
        }

        # Simple warmth enhancement
        if response.startswith(("✅", "Task completed", "Analysis complete")):
            if level in warmth_starters:
                starter = warmth_starters[level][0]  # Use first option for consistency
                if response.startswith("✅"):
                    return response.replace("✅", f"✅ {starter}")
                else:
                    return f"{starter} {response}"

        return response

    def _format_confidence(self, confidence: float, style: str) -> str:
        """Format confidence indicator"""
        if style == "numeric":
            return f"{int(confidence * 100)}% confident"
        elif style == "descriptive":
            if confidence >= 0.8:
                return "high confidence"
            elif confidence >= 0.6:
                return "moderate confidence"
            else:
                return "limited visibility"
        elif style == "contextual":
            if confidence >= 0.8:
                return "based on recent patterns"
            elif confidence >= 0.6:
                return "from available data"
            else:
                return "with current information"
        return ""

    def _add_action_guidance(self, response: str) -> str:
        """Add action-oriented guidance"""
        if "completed successfully" in response.lower():
            return f"{response}—ready for the next step!"
        elif "analysis" in response.lower():
            return f"{response} Here's what I recommend:"
        elif "error" in response.lower():
            return f"{response} Let me try a different approach."

        return response


# Enhanced response examples for different personality levels
PERSONALITY_RESPONSE_EXAMPLES = {
    "warmth_0.3": {
        "success": "Task completed successfully.",
        "analysis": "Analysis complete. Results available.",
        "error": "Error encountered: Connection failed.",
    },
    "warmth_0.7": {
        "success": "Perfect! Your task is complete and ready for the next step.",
        "analysis": "I've analyzed this thoroughly—here's what I found:",
        "error": "I ran into a connection issue, but let me try a different approach.",
    },
    "warmth_1.0": {
        "success": "Fantastic! Everything's done and looking great—you're all set!",
        "analysis": "Great question! I've dug into this and have some exciting insights:",
        "error": "Oops, hit a small connection bump, but no worries—I've got a backup plan!",
    },
}
