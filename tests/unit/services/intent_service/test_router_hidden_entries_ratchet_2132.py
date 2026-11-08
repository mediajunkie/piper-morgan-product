"""#2132 option (b), Arch condition 3: router-hidden rail entries are a ratchet, ceiling 2.

Ceiling 1 (compare_documents, 10-23); raised to 2 by Arch's ruling 2026-11-07 20:26 for
analyze_repository (#2270), and to 3 by his 2026-11-08 07:53 for
change_remembered_preference (#955), with the same named exit. **3 is the last raise**
(Arch 07:53): a fourth hidden entry needs #2149 to move, or the live-set route.

A ``router_visible=False`` entry is reachable only through the legacy classifier.
That is a bounded exception with a named exit (#2149, catalog size), never a
second routing surface. The ceiling only goes DOWN (when #2149 lets compare onto
the router); raising it needs Arch's ruling.

A hidden entry's legacy landing must survive EVERY legacy-side override:
``router_none_stands`` today (#2112; it sent compare to the floor on alpha
a54540c0a8 until 90f0000588), and any override added later. A new override
must exempt router-hidden landings, or the hidden entry closes nothing.
"""

from services.intent_service.workflow_dispatcher import get_action_workflows
from services.intent_service.workflow_entries import register_default_workflows

# Arch 2026-11-07 20:26 (#2270): raised to 2 for analyze_repository, the same exit
# (#2149); its landing pin is test_analyze_repository_2270.py's router-none test.
# Arch 2026-11-08 07:53 (#955): raised to 3, the last raise; landing pin in
# test_change_remembered_preference_955.py.
ROUTER_HIDDEN_CEILING = 3
EXPECTED_ROUTER_HIDDEN = {
    "compare_documents",
    "analyze_repository",
    "change_remembered_preference",
}


def test_router_hidden_entries_are_ratcheted():
    register_default_workflows()
    entries: dict = {}
    for k, e in get_action_workflows().items():
        entries.setdefault(id(e), (k, e))  # an entry is named by its first key
    hidden = {k for k, e in entries.values() if not e.router_visible}
    assert len(hidden) <= ROUTER_HIDDEN_CEILING, sorted(hidden)
    assert hidden == EXPECTED_ROUTER_HIDDEN


def test_the_classifier_example_teaches_compare_documents():
    from services.intent_service.prompts import INTENT_CLASSIFICATION_PROMPT

    assert (
        '"compare these two documents" → {{"category": "analysis", "action": "compare_documents"'
        in INTENT_CLASSIFICATION_PROMPT
    )
