"""
Seed UAT insights for the m1-test user — #1047 M2D-UAT smoke prep (2026-05-28).

Creates a spread of SurfaceableInsights at varied confidence + trust-stage so the
Insight Journal (#1031), pull-mode (#1030), and push-mode (#1032) surfaces render
populated states for PM's anniversary UAT.

Run: venv/bin/python dev/2026/05/28/seed-uat-insights-m1test.py
Idempotent-ish: re-running adds more rows (fine for UAT). Tagged context_tags
with 'uat-anniversary-2026-05-28' so they're identifiable / removable later.
"""

import asyncio
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT_ROOT))

from services.database.repositories import InsightRepository  # noqa: E402
from services.database.session_factory import AsyncSessionFactory  # noqa: E402
from services.mux.composting_models import ExtractedLearning, Insight  # noqa: E402
from services.mux.composting_pipeline import SurfaceableInsight  # noqa: E402

M1_TEST_USER_ID = "009afc8c-bbb0-4391-8265-1575c0812949"
UAT_TAG = "uat-anniversary-2026-05-28"

# (description, confidence, min_trust_stage, expression, topic_tags)
SEED = [
    (
        "You consistently schedule deep-work blocks in the afternoon and keep "
        "mornings for standups and coordination.",
        0.88, 1,
        "I've noticed you protect your afternoons for focused work — mornings are "
        "where you do the coordinating.",
        ["work-rhythm", "scheduling"],
    ),
    (
        "You prefer terse status updates over long narrative reports when reviewing "
        "sprint progress.",
        0.82, 1,
        "When you check sprint progress, you seem to want the headline fast — less "
        "narrative, more signal.",
        ["communication-style", "reporting"],
    ),
    (
        "You tend to batch GitHub issue triage into a single focused pass rather "
        "than handling issues one at a time as they arrive.",
        0.64, 1,
        "It looks like you like to batch issue triage into one sitting rather than "
        "picking them off ad hoc.",
        ["workflow", "github"],
    ),
    (
        "You may be more receptive to proactive suggestions early in the week than "
        "on Fridays.",
        0.41, 3,
        "Tentatively — you might welcome proactive nudges more on Mondays than "
        "Fridays. Still a weak signal.",
        ["receptivity", "timing"],
    ),
    (
        "You value honest 'I don't know yet' responses over confident guesses when "
        "Piper lacks data.",
        0.79, 1,
        "You've signaled you'd rather I say 'I don't have that yet' than guess — "
        "honesty over false confidence.",
        ["trust", "honesty"],
    ),
]


async def main() -> None:
    created = 0
    async with AsyncSessionFactory.session_scope() as session:
        repo = InsightRepository(session)
        for i, (desc, conf, stage, expr, tags) in enumerate(SEED):
            learning = ExtractedLearning(
                source_objects=[f"uat-source-{i}"],
                insight=Insight(description=desc, confidence=conf, surprisingness=0.3),
                confidence=conf,
                topic_tags=tags,
                expression=expr,
                requires_attention=False,
            )
            si = SurfaceableInsight(
                object_id=f"uat-object-{i}",
                user_id=M1_TEST_USER_ID,
                learning=learning,
                min_trust_stage=stage,
                context_tags=tags + [UAT_TAG],
            )
            await repo.add(si)
            created += 1
        # session_scope() does NOT auto-commit (despite its docstring) — flush
        # alone rolls back on close. Explicit commit required.
        await session.commit()
    print(f"Seeded {created} insights for m1-test ({M1_TEST_USER_ID}), tag={UAT_TAG}")


if __name__ == "__main__":
    asyncio.run(main())
