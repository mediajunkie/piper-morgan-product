"""#2301 interim (Arch 11-06 11:26; CXO's line): "what's in my project?" reaches the
floor with project names and counts only, and the floor improvised around the gap
("just tell me directly", PA's Path B preview). Until the project-scoped read lands,
the STATUS gather carries a static capability fact and the floor says CXO's line.
REMOVE this file with the fact, in the commit that lands #2301's read.
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.intent_service.context_assembler import (
    PROJECT_CONTENTS_UNAVAILABLE,
    ContextAssembler,
)
from services.intent_service.conversational_floor import (
    PROJECT_CONTENTS_LINE,
    ConversationalFloor,
)


def test_the_line_is_cxos():
    assert PROJECT_CONTENTS_LINE == "I can see your projects' names, but not the tasks in them yet."


@pytest.mark.asyncio
async def test_the_status_gather_always_carries_the_fact():
    assembler = ContextAssembler()
    with patch.object(assembler, "_gather_calendar_context", AsyncMock(return_value={})):
        context = await assembler._gather_status_priority_context(user_id=None)
    assert context[PROJECT_CONTENTS_UNAVAILABLE] is True


def test_the_floor_states_the_line_only_when_the_fact_is_present():
    floor = ConversationalFloor.__new__(ConversationalFloor)
    with_fact = floor._format_domain_context({PROJECT_CONTENTS_UNAVAILABLE: True})
    without = floor._format_domain_context({})
    assert f'say exactly: "{PROJECT_CONTENTS_LINE}"' in with_fact
    assert PROJECT_CONTENTS_LINE not in without
