"""
Configuration regression tests.

#1452 terminal-triage (2026-07-23): this file originally held 11 tests, 10 of
which were mock-theatre — each `patch()`ed PiperConfigLoader itself and then
asserted against its own MagicMock (Pattern-045: the test cannot detect any
regression in the thing it names, because the subject is replaced). The 7 that
were on the burn-down backlog were the ones where the REAL class leaked
through import order and collided with a superseded contract (pre-emoji
section keys, `validate_config`/`get_cached_config`/`reload_config` methods
that never survived the loader's evolution). Real loader coverage lives in
tests/performance/test_config_performance.py and
tests/integration/test_multi_user_configuration.py (20 live tests, green).

Kept: the one genuinely-real test — the PM-123 CLI regression run below
exercises the actual click commands end-to-end.
"""

import click.testing


class TestConfigurationRegression:
    """Real regression coverage retained from the original suite."""

    def test_pm123_backwards_compatibility_maintained(self):
        """Test that PM-123 CLI functionality is maintained."""
        from cli.commands.issues import issues

        runner = click.testing.CliRunner()

        # Test all PM-123 commands still work
        commands_to_test = [
            ["--help"],
            ["create", "--help"],
            ["verify", "--help"],
            ["sync", "--help"],
            ["create", "--title", "Regression test", "--dry-run"],
            ["verify"],
            ["sync", "--dry-run"],
        ]

        for cmd in commands_to_test:
            result = runner.invoke(issues, cmd)
            # Commands should not fail due to configuration changes
            assert result.exit_code == 0, f"Command {cmd} failed: {result.output}"
