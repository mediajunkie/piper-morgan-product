"""
AAXT: 5 Golden Multi-Turn Scenarios with LLM-as-Judge.

These scenarios test conversational QUALITY, not mechanics. Each scenario
runs a multi-turn conversation through the real app, then uses an LLM judge
to score the final exchange against the Colleague Test rubric.

Issue: #929 AAXT Golden Scenarios
Requires: AAXT_ENABLED=true + ANTHROPIC_API_KEY

Cost: ~$0.05-0.10 per scenario at Sonnet pricing. ~$0.50 for all 5.
Set AAXT_JUDGE_MODEL for cheaper models (e.g., gemini-1.5-flash).

Scenarios:
1. Context Retention — does Piper resolve pronouns across turns?
2. Task Lifecycle — can a user create-list-complete-verify a todo?
3. Mid-Flow Interruption — does Piper handle topic switches gracefully?
4. Cross-Domain Voice — is the personality consistent across domains?
5. Capability Honesty — does Piper avoid promising what it can't do?
"""

import json
import os

import pytest

JUDGE_MODEL = os.getenv("AAXT_JUDGE_MODEL", "claude-sonnet-4-20250514")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def converse(client, messages, session_id, auth):
    """Send a sequence of messages, return all responses."""
    responses = []
    for msg in messages:
        kwargs = {"json": {"message": msg, "session_id": session_id}}
        if auth:
            kwargs.update(auth)
        resp = await client.post("/api/v1/intent", **kwargs)
        assert resp.status_code == 200, f"HTTP {resp.status_code}: {resp.text[:200]}"
        data = resp.json()
        responses.append({"user": msg, "piper": data.get("message", ""), "intent": data.get("intent", {})})
    return responses


def judge_final_response(judge_client, scenario_name, conversation, criteria):
    """Score the final response in a conversation against specific criteria.

    Returns dict with: score (0-9), verdict (PASS/MARGINAL/FAIL), rationale.
    """
    # Format conversation for judge
    conv_text = "\n".join(
        f"User: {turn['user']}\nPiper: {turn['piper']}\n"
        for turn in conversation
    )

    prompt = f"""You are evaluating a multi-turn conversation between a user and Piper Morgan (a PM assistant).

SCENARIO: {scenario_name}

CONVERSATION:
{conv_text}

EVALUATION CRITERIA:
{criteria}

Score the FINAL Piper response using the Colleague Test rubric:
- Relevance (R, 0-3): Did Piper engage with what the user asked?
- Context (C, 0-3): Did Piper use conversation context correctly?
- Tone (T, 0-3): Does Piper sound like a colleague?

PASS: total >= 7, no dimension = 0
MARGINAL: total 5-6, no zeros
FAIL: total < 5 or any zero

Return ONLY valid JSON:
{{"relevance": <0-3>, "context": <0-3>, "tone": <0-3>, "total": <sum>, "verdict": "PASS"|"MARGINAL"|"FAIL", "rationale": "<one sentence>"}}"""

    msg = judge_client.messages.create(
        model=JUDGE_MODEL,
        max_tokens=300,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = msg.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```", 2)[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
    return json.loads(raw)


# ---------------------------------------------------------------------------
# Scenario 1: Context Retention
# ---------------------------------------------------------------------------


class TestContextRetention:
    """Does Piper resolve references across turns?

    User asks about a topic, then uses pronouns/references in follow-up.
    Piper should resolve 'that', 'it', 'the one I mentioned' correctly.
    """

    @pytest.mark.aaxt
    @pytest.mark.asyncio
    async def test_pronoun_resolution_across_turns(
        self, aaxt_client, aaxt_auth, judge_client
    ):
        """Ask about a topic, then reference it with 'that'."""
        conversation = await converse(
            aaxt_client,
            [
                "I need to plan a stakeholder presentation for next week",
                "Can you help me structure that?",
            ],
            "aaxt-context-1",
            aaxt_auth,
        )

        scores = judge_final_response(
            judge_client,
            "Context Retention — pronoun resolution",
            conversation,
            "Did Piper understand 'that' refers to the stakeholder presentation? "
            "Did the response help structure a presentation, not ask what 'that' is?",
        )

        assert scores["verdict"] in ("PASS", "MARGINAL"), (
            f"Context retention failed: {scores['verdict']} "
            f"(R={scores['relevance']} C={scores['context']} T={scores['tone']}). "
            f"Rationale: {scores.get('rationale')}"
        )


# ---------------------------------------------------------------------------
# Scenario 2: Task Lifecycle Simulation
# ---------------------------------------------------------------------------


class TestTaskLifecycle:
    """Can a user complete a full todo lifecycle in conversation?"""

    @pytest.mark.aaxt
    @pytest.mark.asyncio
    async def test_create_list_complete_verify(
        self, aaxt_client, aaxt_auth, judge_client
    ):
        """Full todo lifecycle: create → list → complete → verify."""
        conversation = await converse(
            aaxt_client,
            [
                "Add a todo: prepare quarterly review deck",
                "Show my todos",
                "Complete the quarterly review todo",
                "Show my todos",
            ],
            "aaxt-lifecycle-1",
            aaxt_auth,
        )

        scores = judge_final_response(
            judge_client,
            "Task Lifecycle — create/list/complete/verify",
            conversation,
            "Was the full lifecycle completed? After creating, listing, and completing "
            "the todo, does the final 'show my todos' reflect that the item is done "
            "(either removed from active list or marked complete)? "
            "Was the flow natural and efficient?",
        )

        assert scores["verdict"] in ("PASS", "MARGINAL"), (
            f"Task lifecycle failed: {scores['verdict']} "
            f"(R={scores['relevance']} C={scores['context']} T={scores['tone']}). "
            f"Rationale: {scores.get('rationale')}"
        )


# ---------------------------------------------------------------------------
# Scenario 3: Mid-Flow Interruption
# ---------------------------------------------------------------------------


class TestMidFlowInterruption:
    """Does Piper handle topic switches gracefully?"""

    @pytest.mark.aaxt
    @pytest.mark.asyncio
    async def test_topic_switch_and_return(
        self, aaxt_client, aaxt_auth, judge_client
    ):
        """Start one topic, switch to another, check recovery."""
        conversation = await converse(
            aaxt_client,
            [
                "Help me think through our product roadmap priorities",
                "Actually, quick question — what day is it?",
                "OK thanks, back to the roadmap — what framework would you suggest?",
            ],
            "aaxt-interruption-1",
            aaxt_auth,
        )

        scores = judge_final_response(
            judge_client,
            "Mid-Flow Interruption — topic switch and return",
            conversation,
            "After the interruption (date question), did Piper return to the "
            "roadmap discussion naturally? Did it pick up the thread and suggest "
            "a prioritization framework, or did it treat it as a fresh topic?",
        )

        assert scores["verdict"] in ("PASS", "MARGINAL"), (
            f"Interruption recovery failed: {scores['verdict']} "
            f"(R={scores['relevance']} C={scores['context']} T={scores['tone']}). "
            f"Rationale: {scores.get('rationale')}"
        )


# ---------------------------------------------------------------------------
# Scenario 4: Cross-Domain Voice
# ---------------------------------------------------------------------------


class TestCrossDomainVoice:
    """Is Piper's personality consistent across different domains?"""

    @pytest.mark.aaxt
    @pytest.mark.asyncio
    async def test_consistent_personality(
        self, aaxt_client, aaxt_auth, judge_client
    ):
        """Collect responses from 5 domains, judge personality consistency."""
        conversation = await converse(
            aaxt_client,
            [
                "Add a todo: review sprint retro notes",
                "What can you help me with?",
                "How should I prioritize my work this week?",
                "Thanks for the help!",
                "Tell me about yourself",
            ],
            "aaxt-voice-1",
            aaxt_auth,
        )

        # For cross-domain, we judge the full conversation, not just final response
        scores = judge_final_response(
            judge_client,
            "Cross-Domain Voice — personality consistency",
            conversation,
            "Look at ALL 5 responses across different domains (todo, capabilities, "
            "prioritization, farewell, identity). Is the personality consistent? "
            "Same warmth level, same professionalism, same 'colleague' feel? "
            "Or does the voice shift jarringly between domains? "
            "Score based on consistency, not individual response quality.",
        )

        assert scores["verdict"] in ("PASS", "MARGINAL"), (
            f"Voice consistency failed: {scores['verdict']} "
            f"(R={scores['relevance']} C={scores['context']} T={scores['tone']}). "
            f"Rationale: {scores.get('rationale')}"
        )


# ---------------------------------------------------------------------------
# Scenario 5: Capability Honesty
# ---------------------------------------------------------------------------


class TestCapabilityHonesty:
    """Does Piper avoid promising things it can't do?"""

    @pytest.mark.aaxt
    @pytest.mark.asyncio
    async def test_unregistered_capability_honesty(
        self, aaxt_client, aaxt_auth, judge_client
    ):
        """Ask for something Piper can't do. Should be honest, not promise."""
        conversation = await converse(
            aaxt_client,
            [
                "Can you set up a Jira integration for my team?",
                "What about connecting to our Confluence wiki?",
            ],
            "aaxt-honesty-1",
            aaxt_auth,
        )

        scores = judge_final_response(
            judge_client,
            "Capability Honesty — unregistered integrations",
            conversation,
            "Piper does NOT have Jira or Confluence integrations. Did Piper: "
            "(a) honestly acknowledge the limitation, "
            "(b) suggest alternatives it CAN do, "
            "(c) avoid falsely promising to set up Jira/Confluence? "
            "A good response is honest but helpful. A bad response promises things "
            "Piper can't deliver or gives vague 'I'll look into it' without substance.",
        )

        assert scores["verdict"] in ("PASS", "MARGINAL"), (
            f"Capability honesty failed: {scores['verdict']} "
            f"(R={scores['relevance']} C={scores['context']} T={scores['tone']}). "
            f"Rationale: {scores.get('rationale')}"
        )
