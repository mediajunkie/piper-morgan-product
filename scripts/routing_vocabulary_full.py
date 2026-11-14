"""The full routing vocabulary: the importable sets plus the pre-classifier's names.

``services/intent_service/routing_vocabulary.py`` holds the sets a served process can
import. The pre-classifier's emitted action names are derived here from
``pre_classifier.py``'s SOURCE TEXT (its two emission idioms), which is right for a
test or a script and wrong for a served process (Arch, #2327, 2026-11-14). So this
lives in ``scripts/`` and nothing under ``services/`` imports it.

Readers: the 1283 reachability lint
(``tests/unit/services/intent_service/test_routing_vocabulary_1283.py``) and
``scripts/floored_action_tally.py``.

Concept: docs/internal/architecture/current/intent-routing-stack.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import FrozenSet, Optional, Set

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PRE_CLASSIFIER_SOURCE = ROOT / "services" / "intent_service" / "pre_classifier.py"


def pre_classifier_surface(source: Optional[Path] = None) -> Set[str]:
    """The actions pre_classifier can emit, from its two source idioms:
    ``action="name"`` kwargs and ``(PATTERNS, IntentCategory.X, "name")`` tuples.
    If the file's idiom changes, names drop out and the lint's canary fails loudly,
    the safe failure direction (update the extractor here)."""
    src = (source or PRE_CLASSIFIER_SOURCE).read_text()
    kwargs = set(re.findall(r'action="([a-z_]+)"', src))
    tuples = set(re.findall(r'IntentCategory\.\w+,\s*"([a-z_]+)"', src))
    return kwargs | tuples


def full_vocabulary() -> FrozenSet[str]:
    """Every action name some surface of the code knows."""
    from services.intent_service.routing_vocabulary import importable_vocabulary

    return frozenset(importable_vocabulary() | pre_classifier_surface())
