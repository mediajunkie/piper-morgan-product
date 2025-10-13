"""
CLI Commands for Personality Configuration

Provides command-line interface for managing personality preferences.
Integrates with PIPER.user.md configuration system.
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from services.intent_service.canonical_handlers import CanonicalHandlers
from web.personality_integration import (
    PersonalityResponseEnhancer,
    PiperConfigParser,
    WebPersonalityConfig,
)


class PersonalityCLI:
    """CLI interface for personality configuration"""

    def __init__(self):
        self.config_parser = PiperConfigParser()
        self.enhancer = PersonalityResponseEnhancer()

    def print_colored(self, text: str, color: str = "reset", bold: bool = False) -> None:
        """Print colored text to terminal"""
        colors = {
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "purple": "\033[95m",
            "cyan": "\033[96m",
            "white": "\033[97m",
            "reset": "\033[0m",
        }

        style = "\033[1m" if bold else ""
        reset = colors["reset"]
        color_code = colors.get(color, colors["reset"])

        print(f"{style}{color_code}{text}{reset}")

    def show_current_config(self, user_id: str = "default") -> None:
        """Display current personality configuration"""
        try:
            config = self.config_parser.load_personality_config(user_id)

            self.print_colored("🎭 Current Personality Configuration", "cyan", bold=True)
            print()

            self.print_colored(f"User ID: {user_id}", "white")
            print()

            self.print_colored("Settings:", "yellow", bold=True)
            print(
                f"  Warmth Level:      {config.warmth_level:.1f} (0.0=professional, 1.0=friendly)"
            )
            print(f"  Confidence Style:  {config.confidence_style}")
            print(f"  Action Orientation: {config.action_orientation}")
            print(f"  Technical Depth:   {config.technical_depth}")
            print()

            # Show examples
            self.print_colored("Preview Examples:", "yellow", bold=True)
            examples = self._get_examples(config)
            for category, text in examples.items():
                print(f"  {category.capitalize()}: {text}")

        except Exception as e:
            self.print_colored(f"❌ Error loading configuration: {e}", "red")

    def update_config(
        self,
        user_id: str = "default",
        warmth: Optional[float] = None,
        confidence: Optional[str] = None,
        actions: Optional[str] = None,
        technical: Optional[str] = None,
    ) -> None:
        """Update personality configuration"""
        try:
            # Load current config
            config = self.config_parser.load_personality_config(user_id)

            # Update specified values
            if warmth is not None:
                if 0.0 <= warmth <= 1.0:
                    config.warmth_level = warmth
                else:
                    self.print_colored("❌ Warmth level must be between 0.0 and 1.0", "red")
                    return

            if confidence is not None:
                valid_styles = ["numeric", "descriptive", "contextual", "hidden"]
                if confidence in valid_styles:
                    config.confidence_style = confidence
                else:
                    self.print_colored(
                        f"❌ Confidence style must be one of: {', '.join(valid_styles)}", "red"
                    )
                    return

            if actions is not None:
                valid_actions = ["high", "medium", "low"]
                if actions in valid_actions:
                    config.action_orientation = actions
                else:
                    self.print_colored(
                        f"❌ Action orientation must be one of: {', '.join(valid_actions)}", "red"
                    )
                    return

            if technical is not None:
                valid_technical = ["detailed", "balanced", "simplified"]
                if technical in valid_technical:
                    config.technical_depth = technical
                else:
                    self.print_colored(
                        f"❌ Technical depth must be one of: {', '.join(valid_technical)}", "red"
                    )
                    return

            # Save updated config
            success = self.config_parser.save_personality_config(config, user_id)

            if success:
                self.print_colored("✅ Personality configuration updated successfully!", "green")
                print()
                self.show_current_config(user_id)
            else:
                self.print_colored("❌ Failed to save personality configuration", "red")

        except Exception as e:
            self.print_colored(f"❌ Error updating configuration: {e}", "red")

    def apply_preset(self, preset: str, user_id: str = "default") -> None:
        """Apply personality preset"""
        presets = {
            "professional": WebPersonalityConfig(
                warmth_level=0.3,
                confidence_style="numeric",
                action_orientation="medium",
                technical_depth="detailed",
            ),
            "friendly": WebPersonalityConfig(
                warmth_level=0.8,
                confidence_style="contextual",
                action_orientation="high",
                technical_depth="balanced",
            ),
            "technical": WebPersonalityConfig(
                warmth_level=0.4,
                confidence_style="descriptive",
                action_orientation="high",
                technical_depth="detailed",
            ),
            "casual": WebPersonalityConfig(
                warmth_level=1.0,
                confidence_style="hidden",
                action_orientation="medium",
                technical_depth="simplified",
            ),
        }

        if preset not in presets:
            self.print_colored(f"❌ Unknown preset: {preset}", "red")
            self.print_colored(f"Available presets: {', '.join(presets.keys())}", "yellow")
            return

        try:
            config = presets[preset]
            success = self.config_parser.save_personality_config(config, user_id)

            if success:
                self.print_colored(f"✅ Applied '{preset}' preset successfully!", "green")
                print()
                self.show_current_config(user_id)
            else:
                self.print_colored("❌ Failed to save preset configuration", "red")

        except Exception as e:
            self.print_colored(f"❌ Error applying preset: {e}", "red")

    def test_enhancement(
        self, text: str, user_id: str = "default", confidence: float = 0.8
    ) -> None:
        """Test personality enhancement on sample text"""
        try:
            config = self.config_parser.load_personality_config(user_id)
            enhanced = self.enhancer.enhance_response(text, config, confidence)

            self.print_colored("🧪 Personality Enhancement Test", "cyan", bold=True)
            print()
            self.print_colored("Original:", "yellow")
            print(f"  {text}")
            print()
            self.print_colored("Enhanced:", "green")
            print(f"  {enhanced}")
            print()
            self.print_colored("Settings Used:", "blue")
            print(f"  Warmth: {config.warmth_level:.1f}, Confidence: {config.confidence_style}")
            print(f"  Actions: {config.action_orientation}, Technical: {config.technical_depth}")

        except Exception as e:
            self.print_colored(f"❌ Error testing enhancement: {e}", "red")

    def _get_examples(self, config: WebPersonalityConfig) -> dict:
        """Get example responses for current configuration"""
        examples = {
            "success": "Task completed successfully",
            "analysis": "Analysis complete",
            "error": "Error encountered",
        }

        enhanced_examples = {}
        for category, text in examples.items():
            enhanced = self.enhancer.enhance_response(text, config, confidence=0.8)
            enhanced_examples[category] = enhanced

        return enhanced_examples


def main():
    """Main CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Piper Morgan Personality Configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python personality.py show                    # Show current settings
  python personality.py set --warmth 0.8       # Set warmth level
  python personality.py set --confidence contextual --actions high
  python personality.py preset friendly        # Apply friendly preset
  python personality.py test "Task completed"  # Test enhancement
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Show command
    show_parser = subparsers.add_parser("show", help="Show current personality configuration")
    show_parser.add_argument("--user", default="default", help="User ID (default: default)")

    # Set command
    set_parser = subparsers.add_parser("set", help="Update personality settings")
    set_parser.add_argument("--user", default="default", help="User ID (default: default)")
    set_parser.add_argument("--warmth", type=float, help="Warmth level (0.0-1.0)")
    set_parser.add_argument(
        "--confidence",
        choices=["numeric", "descriptive", "contextual", "hidden"],
        help="Confidence display style",
    )
    set_parser.add_argument(
        "--actions", choices=["high", "medium", "low"], help="Action orientation level"
    )
    set_parser.add_argument(
        "--technical",
        choices=["detailed", "balanced", "simplified"],
        help="Technical depth preference",
    )

    # Preset command
    preset_parser = subparsers.add_parser("preset", help="Apply personality preset")
    preset_parser.add_argument("--user", default="default", help="User ID (default: default)")
    preset_parser.add_argument(
        "name", choices=["professional", "friendly", "technical", "casual"], help="Preset name"
    )

    # Test command
    test_parser = subparsers.add_parser("test", help="Test personality enhancement")
    test_parser.add_argument("--user", default="default", help="User ID (default: default)")
    test_parser.add_argument(
        "--confidence", type=float, default=0.8, help="Confidence level (0.0-1.0)"
    )
    test_parser.add_argument("text", help="Text to enhance")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    cli = PersonalityCLI()

    if args.command == "show":
        cli.show_current_config(args.user)
    elif args.command == "set":
        cli.update_config(
            user_id=args.user,
            warmth=args.warmth,
            confidence=args.confidence,
            actions=args.actions,
            technical=args.technical,
        )
    elif args.command == "preset":
        cli.apply_preset(args.name, args.user)
    elif args.command == "test":
        cli.test_enhancement(args.text, args.user, args.confidence)


if __name__ == "__main__":
    main()
