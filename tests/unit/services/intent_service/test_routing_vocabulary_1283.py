"""#1283 — routing-vocabulary reachability lint (Arch-ratified 2026-07-08, ADR-077).

The AC-4 ruling: SSOT = ACTION_REGISTRY canonicals; every canonical must be REACHABLE,
where reachability is the 4-surface predicate —

    rail (get_action_workflows) ∪ pre_classifier emissions ∪ floor-internal dispatch
    ∪ intentional-floor-allowlist

A canonical reachable through ANY surface is fine; reachable through NONE = the mode-2
structural gap this lint exists to catch (``productivity_query`` shipped that way and the
2026-07-08 live probe found it). The pre_classifier surface is DERIVED from source (its
two emission idioms below), not hand-listed — pre_classifier pairs every action with a
real category, so its emissions land in real handlers by construction. Floor-internal
names it doesn't cover go in FLOOR_ALLOWLIST with a file:line justification; that list
starts EMPTY (the derivation covered everything) and may only shrink or carry evidence.

History: v1 of this file used a 19-entry hand-maintained KNOWN_OFF_RAIL ledger; the
derived pre_classifier surface covered all 19, so the ledger was retired (2026-07-09).
The LLM-behavioral half of enforcement stays out of CI on cost grounds —
scripts/routing_probe_1283.py runs it against the frozen corpus
(tests/fixtures/routing_corpus_1283.yaml, Arch-ratified 2026-07-08).
"""

import re
from pathlib import Path

import yaml

from services.intent_service.action_registry import ACTION_REGISTRY
from services.intent_service.workflow_dispatcher import get_action_workflows
from services.intent_service.workflow_entries import register_default_workflows

_ROOT = Path(__file__).parents[4]
CORPUS = _ROOT / "tests" / "fixtures" / "routing_corpus_1283.yaml"
PRE_CLASSIFIER = _ROOT / "services" / "intent_service" / "pre_classifier.py"

# Floor/context-assembler-handled canonicals NOT covered by the rail or the derived
# pre_classifier surface. Every entry needs a file:line justification comment.
# Empty as of 2026-07-09 — pre_classifier's derivation covers all former ledger entries.
FLOOR_ALLOWLIST: dict = {}


def _rail() -> set:
    register_default_workflows()
    return set(get_action_workflows().keys())


def _pre_classifier_surface() -> set:
    """Derive the actions pre_classifier can emit, from its two source idioms:
    ``action="name"`` kwargs and ``(PATTERNS, IntentCategory.X, "name")`` tuples.
    If the file's idiom changes, names drop out of this set and the reachability
    test FAILS LOUDLY — the safe failure direction (update the extractor here)."""
    src = PRE_CLASSIFIER.read_text()
    kw = set(re.findall(r'action="([a-z_]+)"', src))
    tup = set(re.findall(r'IntentCategory\.\w+,\s*"([a-z_]+)"', src))
    return kw | tup


class TestRoutingVocabularyReachability:
    def test_every_registry_canonical_is_reachable(self):
        canon = {action for (_cat, action) in ACTION_REGISTRY}
        reachable = _rail() | _pre_classifier_surface() | set(FLOOR_ALLOWLIST)
        gaps = canon - reachable
        assert not gaps, (
            f"Registry canonicals reachable through NO dispatch surface: {sorted(gaps)}. "
            "Register on the rail (workflow_entries.py), emit from pre_classifier with a "
            "category pairing, or — if genuinely floor-internal-handled — add to "
            "FLOOR_ALLOWLIST with a file:line justification. An unaccounted canonical is "
            "the productivity_query hole the 2026-07-08 probe found live (mode 2)."
        )

    def test_floor_allowlist_carries_no_freeloaders(self):
        # Ratchet: an allowlist entry that became rail- or pre_classifier-reachable
        # must be removed in the same commit (the list only shrinks).
        stale = set(FLOOR_ALLOWLIST) & (_rail() | _pre_classifier_surface())
        assert not stale, f"FLOOR_ALLOWLIST entries now otherwise reachable: {sorted(stale)}"

    def test_pre_classifier_derivation_is_alive(self):
        # Canary for the extractor: pre_classifier emits a substantial vocabulary today
        # (30 names, 2026-07-09). If this collapses, the idiom changed — fix the
        # derivation in _pre_classifier_surface, don't allowlist around it.
        surface = _pre_classifier_surface()
        assert len(surface) >= 20, (
            f"pre_classifier surface derivation returned only {len(surface)} names — "
            "its emission idiom likely changed; update _pre_classifier_surface()."
        )

    def test_prompt_examples_teach_known_vocabulary(self):
        """(a) of the AC-4 ruling: the classification prompt's few-shot examples ARE the
        LLM's emission vocabulary — an example teaching an unknown action name is mode-1
        drift at the source (the probe traced get_current_status/get_priorities/... to
        exactly these lines). Action-routed examples must be registry/rail/pre_classifier
        known; category-routed teaching names are explicitly allowlisted (their rows route
        by CATEGORY — the probe verified each passes — so the action string is
        informational, but it still may not drift silently)."""
        from services.intent_service.prompts import INTENT_CLASSIFICATION_PROMPT

        CATEGORY_TEACHING = {
            # probe run-1 verified each of these routes correctly by category:
            "get_role",  # IDENTITY (probe row 8 PASS)
            "provide_guidance",  # GUIDANCE (row 9)
            "create_ticket",  # EXECUTION (row 10)
            "generate_summary",  # SYNTHESIS (row 12)
            "clarification_needed",  # CONVERSATION (row 28, corpus-ratified)
            "get_time_info",  # QUERY general-fact teaching example
            "get_information",  # QUERY general-knowledge teaching example
            "specific_action_name",  # the format placeholder, not a name
        }
        taught = set(re.findall(r'"action":\s*"([a-z_]+)"', INTENT_CLASSIFICATION_PROMPT))
        known = (
            {a for (_c, a) in ACTION_REGISTRY}
            | _rail()
            | _pre_classifier_surface()
            | CATEGORY_TEACHING
        )
        drift = taught - known
        assert not drift, (
            f"Prompt examples teach action names unknown to every vocabulary: {sorted(drift)}. "
            "Use the ACTION_REGISTRY canonical (see the provenance note above the examples "
            "in prompts.py); if genuinely category-routed teaching, allowlist it HERE with "
            "the probe evidence."
        )

    def test_corpus_action_expectations_exist_somewhere(self):
        corpus = yaml.safe_load(CORPUS.read_text())["corpus"]
        known = (
            {a for (_c, a) in ACTION_REGISTRY} | _rail() | _pre_classifier_surface()
        )
        bad = [
            (row["phrase"], row["expected"])
            for row in corpus
            if row["expected"].startswith("action:")
            and row["expected"].split(":", 1)[1] not in known
        ]
        assert not bad, (
            f"Corpus rows expect actions unknown to every vocabulary: {bad}. "
            "The corpus is the Arch-ratified contract (2026-07-08) — recalibrate "
            "against action_registry.py canonicals, don't invent names."
        )


class TestNormalizationShim:
    """#1283 AC-4 (b): the conservative near-miss shim — additive to aliases, exact
    post-strip matches only, pass-through otherwise (never a fuzzy guess)."""

    def _shim(self):
        from services.intent_service.workflow_dispatcher import normalize_action

        register_default_workflows()
        return normalize_action

    def test_known_rail_key_passes_through_untouched(self):
        n = self._shim()
        assert n("show_standup") == "show_standup"
        assert n("stale_prs_query") == "stale_prs_query"

    def test_unknown_variant_with_strippable_prefix_maps_to_rail_key(self):
        n = self._shim()
        # get_stale_prs is NOT a rail key; stale_prs IS (alias) — exact post-strip match
        assert n("get_stale_prs") == "stale_prs"
        assert n("fetch_stale_prs") == "stale_prs"

    def test_no_exact_match_passes_through(self):
        n = self._shim()
        # run-2's live variant: strips to pull_requests, which is no rail key → unchanged
        assert n("get_pull_requests") == "get_pull_requests"
        assert n("totally_unknown_thing") == "totally_unknown_thing"

    def test_empty_and_none_safe(self):
        n = self._shim()
        assert n("") == ""
