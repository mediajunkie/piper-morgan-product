"""#1283 — routing-vocabulary ratchet (the no-LLM half of the behavioral corpus).

The 2026-07-08 probe proved the failure shapes this file freezes out:
- mode-2: a registry CANONICAL missing from its own handler's rail aliases
  (``productivity_query`` was, until the same-day fix);
- silent vocabulary drift: corpus rows or registry entries naming actions no
  dispatch surface knows.

The intent stack has FOUR dispatch surfaces (see
docs/internal/architecture/current/intent-routing-stack.md): pre_classifier →
LLM classifier → action rail → category/floor-internal handling. The rail is
the only one statically enumerable, so this ratchet works by explicit
accounting: every registry canonical must be ON the rail or in the
KNOWN_OFF_RAIL ledger below (floor/pre-classifier-surface handled). A new
canonical that lands in neither fails the build; migrating one onto the rail
means REMOVING it here in the same commit (ratchet direction: ledger only
shrinks). The LLM half of enforcement (running the corpus phrases through the
real classifier) stays out of CI on cost grounds — it lives in
scripts/routing_probe_1283.py, gated on Arch's corpus ratification.
"""

from pathlib import Path

import yaml

from services.intent_service.action_registry import ACTION_REGISTRY
from services.intent_service.workflow_dispatcher import get_action_workflows
from services.intent_service.workflow_entries import register_default_workflows

CORPUS = Path(__file__).parents[4] / "tests" / "fixtures" / "routing_corpus_1283.yaml"

# Registry canonicals deliberately NOT on the get_action_workflows rail —
# handled at the pre-classifier / category-handler / floor surfaces instead.
# Status per the 2026-07-08 probe + code trace where verified; the rest are
# accounted-pending-verification (Arch 4-surface accounting, #1283 AC-4).
KNOWN_OFF_RAIL = {
    # CONVERSATION floor handles these socially, pre-rail:
    "greeting",
    "farewell",
    "thanks",
    # probe-verified category/floor-surface handling:
    "get_identity",  # IDENTITY category (probe row PASSed via category)
    "get_current_time",  # TEMPORAL (probe PASS)
    "get_top_priority",  # PRIORITY (probe PASS)
    "get_project_status",  # STATUS (probe PASS; pre_classifier emits it too)
    "pull_insights",  # MEMORY — conversational_floor.py handles by name
    "write_stakeholder_update",  # floor, checked before document patterns (#1256)
    "manage_portfolio",  # PORTFOLIO via pre_classifier
    # accounted, not yet individually probe-verified:
    "analyze_blockers",
    "complete_todo",
    "explain_suggestion",
    "explain_trust",
    "get_capabilities",
    "get_contextual_guidance",
    "get_feature_info",
    "get_memory",
    "manage_repos",
}


def _rail() -> set:
    register_default_workflows()
    return set(get_action_workflows().keys())


class TestRoutingVocabularyRatchet:
    def test_every_registry_canonical_is_railed_or_accounted(self):
        canon = {action for (_cat, action) in ACTION_REGISTRY}
        unaccounted = canon - _rail() - KNOWN_OFF_RAIL
        assert not unaccounted, (
            f"Registry canonicals on NO known dispatch surface: {sorted(unaccounted)}. "
            "Either register the action on the rail (workflow_entries.py) or, if it is "
            "genuinely floor/pre-classifier-handled, add it to KNOWN_OFF_RAIL with a "
            "comment saying which surface handles it. Do not leave it unaccounted — "
            "that is exactly the productivity_query hole the #1283 probe found live."
        )

    def test_off_rail_ledger_only_shrinks(self):
        stale = KNOWN_OFF_RAIL & _rail()
        assert not stale, (
            f"Now ON the rail but still in KNOWN_OFF_RAIL: {sorted(stale)}. "
            "Remove them from the ledger in this same commit (ratchet discipline)."
        )

    def test_corpus_action_expectations_exist_somewhere(self):
        corpus = yaml.safe_load(CORPUS.read_text())["corpus"]
        known = {a for (_c, a) in ACTION_REGISTRY} | _rail()
        bad = [
            (row["phrase"], row["expected"])
            for row in corpus
            if row["expected"].startswith("action:")
            and row["expected"].split(":", 1)[1] not in known
        ]
        assert not bad, (
            f"Corpus rows expect actions unknown to registry AND rail: {bad}. "
            "The corpus drifted from the vocabulary — recalibrate against "
            "action_registry.py canonicals (see the probe-run-1 lesson: the draft "
            "corpus used aspirational names and produced 7 false FAILs)."
        )
