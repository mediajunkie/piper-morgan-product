# Prompt for Cursor Agent: GREAT-4E Phase 2 - Interface Validation

## Context

Phase 1 complete: All 13 categories validated through direct service (13/117 tests, 11%)

**This is Phase 2**: Test all 13 categories through Web, Slack, and CLI interfaces (39 additional tests)

## Session Log

Continue: `dev/2025/10/06/2025-10-06-0752-prog-cursor-log.md`

## Mission

Implement tests for Web API, Slack, and CLI interfaces. Each interface must test all 13 intent categories.

---

## Phase 2: Interface Validation (39 Tests)

### Test Distribution

- Web API: 13 tests (test_web_interface.py)
- Slack: 13 tests (test_slack_interface.py)
- CLI: 13 tests (test_cli_interface.py)
- Total: 39 tests (bringing total to 52/117)

### Strategy

Each interface test should:
1. Send request through that interface's entry point
2. Verify intent classification happens
3. Verify handler executes
4. Verify no placeholder messages
5. Update coverage tracker

---

## Part 1: Web API Interface (13 Tests)

Update: `tests/intent/test_web_interface.py`

### Web API Entry Point

The web API is in `web/app.py`. Check for intent endpoints:

```bash
grep -n "intent\|/api" web/app.py | head -20
```

### Example Web Test Structure

```python
@pytest.mark.asyncio
async def test_temporal_web(self, intent_service):
    """WEB 1/13: TEMPORAL category."""
    from tests.intent.coverage_tracker import coverage
    import time

    # Simulate web API request
    # This will depend on how web/app.py exposes intent endpoint
    # Common patterns:
    # - POST /api/v1/intent
    # - POST /api/chat
    # - POST /process

    # Option A: If web app has test client
    from web.app import app
    client = app.test_client()

    response = client.post('/api/v1/intent', json={
        'message': 'What\'s on my calendar today?',
        'user_id': 'test_user',
        'session_id': 'test_session'
    })

    assert response.status_code == 200
    data = response.get_json()

    # Verify no placeholder in response
    if 'message' in data:
        self.assert_no_placeholder(data['message'])

    # Update coverage
    coverage.categories_tested.add("TEMPORAL")
    coverage.interfaces_tested.add("web")
    coverage.interface_tests_passed += 1

    print(f"✓ WEB/TEMPORAL")
```

### Implementation Notes

**Before implementing all 13 tests**, investigate the web API structure:

```python
# At top of test file, add investigation code:
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Check web app structure
from web import app
print("Available routes:")
for rule in app.url_map.iter_rules():
    print(f"  {rule.endpoint}: {rule.rule}")
```

Once you understand the API structure, implement all 13 tests following the pattern.

---

## Part 2: Slack Interface (13 Tests)

Update: `tests/intent/test_slack_interface.py`

### Slack Integration Entry Point

Slack integration is in `services/integrations/slack/`. Check for message handling:

```bash
grep -rn "def.*message\|async def.*process" services/integrations/slack/ | head -10
```

### Example Slack Test Structure

```python
@pytest.mark.asyncio
async def test_temporal_slack(self, intent_service):
    """SLACK 1/13: TEMPORAL category."""
    from tests.intent.coverage_tracker import coverage

    # Simulate Slack message event
    # Common pattern: Slack sends events to webhook

    # Option A: Direct service call
    from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

    router = SlackIntegrationRouter()

    # Simulate Slack event
    slack_event = {
        'type': 'message',
        'text': 'What\'s on my calendar today?',
        'user': 'U12345',
        'channel': 'C12345',
        'ts': '1234567890.123456'
    }

    result = await router.handle_message(slack_event)

    # Verify no placeholder
    if hasattr(result, 'message'):
        self.assert_no_placeholder(result.message)

    # Update coverage
    coverage.categories_tested.add("TEMPORAL")
    coverage.interfaces_tested.add("slack")
    coverage.interface_tests_passed += 1

    print(f"✓ SLACK/TEMPORAL")
```

### Implementation Notes

**Before implementing**, investigate Slack integration:

```python
# Check Slack router structure
from services.integrations.slack import slack_integration_router
import inspect

print("Slack router methods:")
for name, method in inspect.getmembers(slack_integration_router.SlackIntegrationRouter):
    if not name.startswith('_'):
        print(f"  {name}")
```

---

## Part 3: CLI Interface (13 Tests)

Update: `tests/intent/test_cli_interface.py`

### CLI Entry Point

CLI is in `cli/` directory. Check for command handling:

```bash
ls -la cli/commands/
grep -rn "def.*command\|click.command" cli/ | head -10
```

### Example CLI Test Structure

```python
@pytest.mark.asyncio
async def test_temporal_cli(self, intent_service):
    """CLI 1/13: TEMPORAL category."""
    from tests.intent.coverage_tracker import coverage

    # Simulate CLI command
    # Common patterns:
    # - Click commands
    # - ArgParse commands
    # - Direct function calls

    # Option A: If using Click
    from click.testing import CliRunner
    from cli.commands import main  # or whatever the main CLI is

    runner = CliRunner()
    result = runner.invoke(main, ['ask', 'What\'s on my calendar today?'])

    assert result.exit_code == 0

    # Verify no placeholder in output
    self.assert_no_placeholder(result.output)

    # Update coverage
    coverage.categories_tested.add("TEMPORAL")
    coverage.interfaces_tested.add("cli")
    coverage.interface_tests_passed += 1

    print(f"✓ CLI/TEMPORAL")
```

### Implementation Notes

**Before implementing**, investigate CLI structure:

```bash
# Check CLI structure
ls -la cli/
ls -la cli/commands/
cat cli/__init__.py | head -20
```

---

## Special Handling: Interface Not Found

If any interface doesn't exist or isn't accessible:

```python
@pytest.mark.skip(reason="CLI interface not implemented yet")
@pytest.mark.asyncio
async def test_temporal_cli(self, intent_service):
    """CLI 1/13: TEMPORAL category - SKIPPED."""
    pass
```

Update the gameplan to reflect reality:
- If CLI doesn't exist: Skip all 13 CLI tests, adjust total to 39 tests
- Document in session log which interfaces were skipped

---

## Coverage Report After Phase 2

Add at end of EACH interface test file:

```python
@pytest.mark.asyncio
async def test_zzz_coverage_report(self):
    """Generate coverage report after interface tests."""
    from tests.intent.coverage_tracker import coverage

    print("\n" + "=" * 80)
    print(coverage.report())
    print("=" * 80)
```

---

## Running the Tests

```bash
# Run each interface separately
pytest tests/intent/test_web_interface.py -v
pytest tests/intent/test_slack_interface.py -v
pytest tests/intent/test_cli_interface.py -v

# Or all at once
pytest tests/intent/test_*_interface.py -v

# Should show:
# test_web_interface.py: 14 passed (13 tests + coverage report)
# test_slack_interface.py: 14 passed
# test_cli_interface.py: 14 passed (or 13 skipped if N/A)
#
# Total: 52/52 interface tests (or adjusted if CLI N/A)
```

---

## Success Criteria

- [ ] Web API: 13/13 tests implemented and passing
- [ ] Slack: 13/13 tests implemented and passing
- [ ] CLI: 13/13 tests implemented (passing or skipped with reason)
- [ ] Coverage report shows 4/4 interfaces (or 3/4 if CLI N/A)
- [ ] Total: 52/52 interface tests (or adjusted)
- [ ] No placeholder messages anywhere
- [ ] Session log updated with actual interface coverage

---

## Critical Notes

- Investigate each interface BEFORE writing all 13 tests
- If interface doesn't exist, skip with clear documentation
- Each test must update coverage tracker
- Stop if any implemented interface fails tests
- Document actual vs planned coverage

---

**Effort**: Large (~1.5-2 hours for 39 tests across 3 interfaces)
**Priority**: HIGH (validates all entry points)
**Deliverables**: 39 interface tests + updated coverage report
