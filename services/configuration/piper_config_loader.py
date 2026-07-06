"""
PiperConfigLoader - Loads and manages PIPER.md configuration for conversation context

This service provides:
- PIPER.md markdown parsing and conversion to system prompt format
- Hot-reload capability for configuration changes
- Caching for performance
- Integration with conversation initialization
"""

import os
import re
import time
from pathlib import Path
from typing import Dict, Optional, Tuple

import structlog
import yaml

logger = structlog.get_logger()


class PiperConfigLoader:
    """
    Loads and manages PIPER.md configuration for enhanced conversation context

    Features:
    - Markdown parsing and system prompt conversion
    - Hot-reload capability
    - Performance caching
    - Error handling and fallbacks
    """

    def __init__(self, config_path: str = None):
        # Auto-detect user config with fallback to default
        if config_path is None:
            user_config = Path("config/PIPER.user.md")
            default_config = Path("config/PIPER.md")
            if user_config.exists():
                config_path = str(user_config)
                logger.debug("Using user configuration", path=config_path)
            else:
                config_path = str(default_config)
                logger.debug("Using default configuration (no user config found)", path=config_path)

        self.config_path = Path(config_path)
        self.last_modified = 0  # File modification time
        self.cache_time = 0  # When config was cached (GREAT-4C Phase 3)
        self.cached_config = None
        self.cached_system_prompt = None
        self.cache_ttl = 300  # 5 minutes

        # Cache metrics (GREAT-4C Phase 3)
        self.cache_hits = 0
        self.cache_misses = 0

        # Ensure config directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info("PiperConfigLoader initialized", config_path=str(self.config_path))

    def load_config(self) -> Optional[Dict[str, str]]:
        """
        Load PIPER.md configuration and parse into structured format

        Returns:
            Dictionary with parsed configuration sections
        """
        try:
            if not self.config_path.exists():
                logger.warning(
                    "PIPER.md not found, using default configuration", path=str(self.config_path)
                )
                return self._get_default_config()

            # Check if cache is valid
            current_mtime = self.config_path.stat().st_mtime
            current_time = time.time()

            cache_valid = (
                self.cached_config is not None
                and current_mtime <= self.last_modified  # File hasn't been modified
                and (current_time - self.cache_time) < self.cache_ttl  # Within TTL
            )

            if cache_valid:
                self.cache_hits += 1  # GREAT-4C Phase 3: Track cache hit
                logger.debug("Using cached PIPER.md configuration", cache_hits=self.cache_hits)
                return self.cached_config

            # Cache miss - need to read from disk
            self.cache_misses += 1  # GREAT-4C Phase 3: Track cache miss
            logger.debug("Cache miss - loading PIPER.md from disk", cache_misses=self.cache_misses)

            # Parse the markdown file
            config = self._parse_piper_md()
            if config:
                self.cached_config = config
                self.last_modified = current_mtime  # File modification time
                self.cache_time = current_time  # When we cached it
                logger.info("PIPER.md configuration loaded successfully", sections=len(config))
                return config
            else:
                logger.warning("Failed to parse PIPER.md, using default configuration")
                return self._get_default_config()

        except Exception as e:
            logger.error("Error loading PIPER.md configuration", error=str(e))
            return self._get_default_config()

    def get_system_prompt(self) -> str:
        """
        Convert PIPER.md configuration to system prompt format

        Returns:
            Formatted system prompt string
        """
        config = self.load_config()
        if not config:
            return self._get_default_system_prompt()

        try:
            system_prompt = self._format_system_prompt(config)
            self.cached_system_prompt = system_prompt
            return system_prompt
        except Exception as e:
            logger.error("Error formatting system prompt", error=str(e))
            return self._get_default_system_prompt()

    def _parse_piper_md(self) -> Optional[Dict[str, str]]:
        """
        Parse PIPER.md markdown file into structured configuration

        Returns:
            Dictionary with section names as keys and content as values
        """
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse markdown sections
            sections = {}
            current_section = None
            current_content = []

            in_code_block = False
            for original_line in content.split("\n"):
                # Preserve indentation in code blocks, strip elsewhere
                if original_line.strip().startswith("```"):
                    in_code_block = not in_code_block
                    line = original_line.strip()
                elif in_code_block:
                    line = original_line  # Preserve indentation in code blocks
                else:
                    line = original_line.strip()

                # Check for section headers (## or ###)
                if line.startswith("## "):
                    # Save previous section
                    if current_section and current_content:
                        sections[current_section] = "\n".join(current_content).strip()

                    # Start new section
                    current_section = line[3:].strip().replace("*", "").replace("**", "")
                    current_content = []

                elif line.startswith("### "):
                    # Subsection - append to current section
                    if current_section:
                        current_content.append(line)

                elif current_section:
                    # Content for current section
                    current_content.append(line)

            # Save last section
            if current_section and current_content:
                sections[current_section] = "\n".join(current_content).strip()

            return sections

        except Exception as e:
            logger.error("Error parsing PIPER.md", error=str(e))
            return None

    def _format_system_prompt(self, config: Dict[str, str]) -> str:
        """
        Format configuration into system prompt

        Args:
            config: Parsed configuration dictionary

        Returns:
            Formatted system prompt string
        """
        # Issue #909: User name comes from authenticated user, not hardcoded
        prompt_parts = [
            "You are Piper Morgan, an intelligent product management assistant.",
            "Use the following context to provide personalized, context-aware assistance:",
            "",
        ]

        # Add user context
        if "User Context" in config:
            prompt_parts.extend(["## USER CONTEXT", config["User Context"], ""])

        # Add current focus
        if "Current Focus (Q4 2025)" in config:
            prompt_parts.extend(["## CURRENT FOCUS", config["Current Focus (Q4 2025)"], ""])

        # Add project portfolio
        if "Project Portfolio" in config:
            prompt_parts.extend(["## PROJECT PORTFOLIO", config["Project Portfolio"], ""])

        # Add standing priorities
        if "Standing Priorities" in config:
            prompt_parts.extend(["## STANDING PRIORITIES", config["Standing Priorities"], ""])

        # Add calendar patterns
        if "Calendar Patterns" in config:
            prompt_parts.extend(["## CALENDAR PATTERNS", config["Calendar Patterns"], ""])

        # Add knowledge sources
        if "Knowledge Sources" in config:
            prompt_parts.extend(["## KNOWLEDGE SOURCES", config["Knowledge Sources"], ""])

        # Add personality and behavior guidelines
        prompt_parts.extend(
            [
                "## BEHAVIOR GUIDELINES",
                "- Be direct and efficiency-focused",
                "- Provide evidence-based responses",
                "- Reference specific projects, priorities, and context",
                "- Maintain professional but personable tone",
                "- Suggest next steps when appropriate",
                "- Use the user's name (if known) and refer to specific projects",
                "",
            ]
        )

        return "\n".join(prompt_parts)

    def _get_default_config(self) -> Dict[str, str]:
        """
        Get default configuration when PIPER.md is not available

        Returns:
            Default configuration dictionary
        """
        return {
            "User Context": "The user is a product practitioner. Learn about them through conversation.",
            "Current Focus": "MCP implementation and UX enhancement",
            "Project Portfolio": "Piper Morgan (primary), OneJob, Content Creation",
            "Standing Priorities": "Enhanced conversational context, MCP deployment, pattern validation",
            "Calendar Patterns": "Daily standup at 6 AM PT, development focus blocks",
            "Knowledge Sources": "Pattern index, architecture guides, session logs",
        }

    def _get_default_system_prompt(self) -> str:
        """
        Get default system prompt when configuration is not available

        Returns:
            Default system prompt string
        """
        # Issue #909: No hardcoded user name — learn from conversation
        return """You are Piper Morgan, an intelligent product management assistant.

## USER CONTEXT
The user is a product practitioner. Learn about them through conversation.

## CURRENT FOCUS
MCP implementation and UX enhancement.

## PROJECT PORTFOLIO
Piper Morgan (primary), OneJob, Content Creation.

## STANDING PRIORITIES
Enhanced conversational context, MCP deployment, pattern validation.

## BEHAVIOR GUIDELINES
- Be direct and efficiency-focused
- Provide evidence-based responses
- Reference specific projects and priorities
- Maintain professional but personable tone"""

    def is_config_modified(self) -> bool:
        """
        Check if PIPER.md has been modified since last load

        Returns:
            True if file has been modified
        """
        if not self.config_path.exists():
            return False

        current_mtime = self.config_path.stat().st_mtime
        return current_mtime > self.last_modified

    def reload_if_modified(self) -> bool:
        """
        Reload configuration if file has been modified

        Returns:
            True if configuration was reloaded
        """
        if self.is_config_modified():
            logger.info("PIPER.md modified, reloading configuration")
            self.cached_config = None
            self.cached_system_prompt = None
            return True
        return False

    def get_config_summary(self) -> Dict[str, any]:
        """
        Get configuration summary for monitoring

        Returns:
            Configuration status and metadata
        """
        return {
            "config_path": str(self.config_path),
            "exists": self.config_path.exists(),
            "last_modified": self.last_modified,
            "cached": self.cached_config is not None,
            "cache_age": time.time() - self.last_modified if self.last_modified else 0,
            "sections_count": len(self.cached_config) if self.cached_config else 0,
        }

    def load_pm_identity_config(self) -> Optional[str]:
        """
        Load the configured-PM username from PIPER.user.md (#1260, ADR-071 D7 prerequisite).

        Server-owned config (ADR-066 D7), replacing the hardcoded `username == 'xian'`
        literal that used to live in resolve_pm_owner_id. Single-tenant shape today
        (one username); ADR-071 D7 names the evolution to a multi-tenant principal
        when tenant_id lands — same seam, same config surface, different resolution.

        Returns:
            The configured PM's username, or None if no "PM Identity" section is
            present (graceful — callers fall through to their own None-handling,
            same as an absent env override).
        """
        try:
            config = self.load_config()
            if not config:
                return None

            pm_identity_section = None
            for section_name, content in config.items():
                if "pm identity" in section_name.lower():
                    pm_identity_section = content
                    break

            if not pm_identity_section:
                return None

            yaml_match = re.search(r"```yaml\s*(.*?)\s*```", pm_identity_section, re.DOTALL)
            if not yaml_match:
                return None

            pm_identity_data = yaml.safe_load(yaml_match.group(1).strip())
            if not pm_identity_data or "pm_identity" not in pm_identity_data:
                return None

            username = pm_identity_data["pm_identity"].get("username")
            return username if isinstance(username, str) and username else None

        except Exception as e:
            logger.error("Error loading PM identity configuration", error=str(e))
            return None

    def load_github_config(self):
        """
        Load GitHub configuration from PIPER.user.md

        Extracts YAML configuration from GitHub Integration section.
        Falls back to defaults if no configuration found.

        Returns:
            GitHubConfiguration instance with user settings or defaults
        """
        try:
            # Load the markdown configuration
            config = self.load_config()
            if not config:
                from services.config.github_config import GitHubConfiguration

                logger.debug("No PIPER.md config found, using GitHub defaults")
                return GitHubConfiguration.create_default()

            # Look for GitHub Integration section
            github_section_content = None
            for section_name, content in config.items():
                if "github" in section_name.lower() and "integration" in section_name.lower():
                    github_section_content = content
                    break

            if not github_section_content:
                from services.config.github_config import GitHubConfiguration

                logger.debug("No GitHub Integration section found, using defaults")
                return GitHubConfiguration.create_default()

            # Extract YAML from markdown code blocks (more robust)
            yaml_match = re.search(r"```yaml.*?```", github_section_content, re.DOTALL)
            if not yaml_match:
                from services.config.github_config import GitHubConfiguration

                logger.debug("No YAML configuration found in GitHub section, using defaults")
                return GitHubConfiguration.create_default()

            # Extract YAML content by removing markdown markers
            full_yaml_block = yaml_match.group(0)
            yaml_content = full_yaml_block.replace("```yaml", "").replace("```", "").strip()
            github_config_data = yaml.safe_load(yaml_content)

            if not github_config_data or "github" not in github_config_data:
                from services.config.github_config import GitHubConfiguration

                logger.debug("No github section in YAML, using defaults")
                return GitHubConfiguration.create_default()

            github_section = github_config_data["github"]
            if not isinstance(github_section, dict):
                from services.config.github_config import GitHubConfiguration

                logger.debug("GitHub section is not a dictionary, using defaults")
                return GitHubConfiguration.create_default()

            pm_numbers = github_section.get("pm_numbers", {})
            if not isinstance(pm_numbers, dict):
                pm_numbers = {}

            # Create GitHubConfiguration from user settings
            from services.config.github_config import GitHubConfiguration

            github_config = GitHubConfiguration(
                # Issue #1042: removed hardcoded "mediajunkie/piper-morgan-product"
                # / "mediajunkie" defaults. Empty defaults; runtime resolution
                # via repo_resolver fills in per-call.
                default_repository=github_section.get("default_repository", ""),
                owner=github_section.get("owner", ""),
                pm_prefix=pm_numbers.get("prefix", "PM-"),
                pm_start=pm_numbers.get("start_number", 1),
                pm_padding=pm_numbers.get("padding", 3),
                api_base=github_section.get("api_base", "https://api.github.com"),
                default_labels=github_section.get("default_labels", ["enhancement"]),
            )

            logger.info(
                "GitHub configuration loaded from PIPER.user.md",
                repository=github_config.default_repository,
                pm_format=github_config.format_pm_number(1),
            )

            return github_config

        except Exception as e:
            from services.config.github_config import GitHubConfiguration

            logger.error("Error loading GitHub configuration, using defaults", error=str(e))
            return GitHubConfiguration.create_default()

    def load_standup_config(self) -> Dict[str, any]:
        """
        Load standup configuration from PIPER.user.md

        Returns:
            Dictionary with standup configuration settings
        """
        try:
            config = self.load_config()
            if not config:
                logger.warning("No configuration loaded, using default standup settings")
                return self._get_default_standup_config()

            # Look for standup section
            standup_section = None
            for section_name, section_content in config.items():
                if "standup" in section_name.lower() or "morning" in section_name.lower():
                    standup_section = section_content
                    break

            if not standup_section:
                logger.debug("No standup configuration found, using defaults")
                return self._get_default_standup_config()

            # Extract YAML content from standup section
            yaml_match = re.search(r"```yaml\s*(.*?)\s*```", standup_section, re.DOTALL)
            if not yaml_match:
                logger.debug("No YAML configuration found in standup section, using defaults")
                return self._get_default_standup_config()

            # Parse YAML content
            yaml_content = yaml_match.group(1).strip()
            standup_config_data = yaml.safe_load(yaml_content)

            if not standup_config_data or "standup" not in standup_config_data:
                logger.debug("No standup section in YAML, using defaults")
                return self._get_default_standup_config()

            standup_section = standup_config_data["standup"]
            if not isinstance(standup_section, dict):
                logger.debug("Standup section is not a dictionary, using defaults")
                return self._get_default_standup_config()

            # Build configuration with defaults
            standup_config = {
                "questions": standup_section.get(
                    "questions",
                    [
                        "What's your name and role?",
                        "What day is it?",
                        "What should I focus on today?",
                        "What am I working on?",
                        "What's my top priority?",
                    ],
                ),
                "timing": standup_section.get(
                    "timing",
                    {
                        "preferred_time": "06:00",
                        "timezone": "America/Los_Angeles",
                        "duration_target": "3 seconds",
                        "time_range_hours": 2,
                    },
                ),
                "integrations": standup_section.get(
                    "integrations",
                    {
                        "github": True,
                        "calendar": True,
                        "issue_intelligence": True,
                        "document_memory": True,
                    },
                ),
                "user_identity": standup_section.get(
                    "user_identity",
                    {
                        "user_id": "default",
                        "display_name": "User",
                        "role": "Team Member",
                        "context": "working on projects",
                    },
                ),
                "content": standup_section.get(
                    "content",
                    {
                        "include_github_activity": True,
                        "include_calendar_events": True,
                        "include_issue_updates": True,
                        "include_document_insights": True,
                        "fallback_priorities": [
                            "Enhanced conversational context",
                            "MCP deployment",
                            "Pattern validation",
                        ],
                    },
                ),
            }

            logger.info(
                "Standup configuration loaded from PIPER.user.md",
                questions_count=len(standup_config["questions"]),
                user_id=standup_config["user_identity"]["user_id"],
            )

            return standup_config

        except Exception as e:
            logger.error("Error loading standup configuration, using defaults", error=str(e))
            return self._get_default_standup_config()

    def _get_default_standup_config(self) -> Dict[str, any]:
        """Get default standup configuration when user config is not available"""
        return {
            "questions": [
                "What's your name and role?",
                "What day is it?",
                "What should I focus on today?",
                "What am I working on?",
                "What's my top priority?",
            ],
            "timing": {
                "preferred_time": "06:00",
                "timezone": "America/Los_Angeles",
                "duration_target": "3 seconds",
                "time_range_hours": 2,
            },
            "integrations": {
                "github": True,
                "calendar": True,
                "issue_intelligence": True,
                "document_memory": True,
            },
            "user_identity": {
                "user_id": "default",
                "display_name": "User",
                "role": "Team Member",
                "context": "working on projects",
            },
            "content": {
                "include_github_activity": True,
                "include_calendar_events": True,
                "include_issue_updates": True,
                "include_document_insights": True,
                "fallback_priorities": [
                    "Enhanced conversational context",
                    "MCP deployment",
                    "Pattern validation",
                ],
            },
        }

    def get_cache_metrics(self) -> Dict[str, any]:
        """
        Get cache performance metrics.

        Returns:
            Dictionary with cache hits, misses, hit rate, and cache status

        Added in GREAT-4C Phase 3 for cache monitoring.
        """
        total = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total * 100) if total > 0 else 0

        # Check if cache is currently populated
        cache_populated = self.cached_config is not None

        # Calculate cache age (time since config was cached)
        cache_age_seconds = time.time() - self.cache_time if self.cache_time > 0 else None

        return {
            "hits": self.cache_hits,
            "misses": self.cache_misses,
            "total_requests": total,
            "hit_rate_percent": round(hit_rate, 2),
            "cache_populated": cache_populated,
            "cache_age_seconds": (
                round(cache_age_seconds, 2) if cache_age_seconds is not None else None
            ),
            "ttl_seconds": self.cache_ttl,
            "config_path": str(self.config_path),
        }

    def clear_cache(self) -> None:
        """
        Clear cached configuration and reset metrics.

        Forces next load_config() call to read from disk.

        Added in GREAT-4C Phase 3 for cache management.
        """
        self.cached_config = None
        self.cached_system_prompt = None
        self.last_modified = 0
        self.cache_time = 0
        self.cache_hits = 0
        self.cache_misses = 0
        logger.info("Cache cleared for PiperConfigLoader")


# Global instance for easy access
piper_config_loader = PiperConfigLoader()
