---
from: Lead Developer
to: Chief Experience Officer
cc: PM
date: 2026-04-14
subject: Request — floor system prompt review before M2c starts (#950)
response-requested: yes
priority: high
---

# Floor System Prompt Review — #950 Direction Check

CXO — M2b (test infrastructure) is effectively complete. M2c (Conversational Depth) is next, and #950 (FLOOR-PROMPT: Conscious floor system prompt with Five Pillars + grammar) is its centerpiece.

PA's M2 go-ahead memo specifically flagged: "CXO review of floor system prompt design (#950) at sprint start." We're at that point now. Before I start implementation, I need your direction on the prompt design.

## Current State

The floor system prompt lives in `services/intent_service/conversational_floor.py` (lines 33-65). It currently has:

- **Identity**: "You are Piper Morgan, a PM colleague"
- **Engagement rules**: Think through problems with PM frameworks, suggest concrete actions, respond directly
- **Prohibitions**: Don't introduce yourself, don't list capabilities, don't offer generic prompts, don't fabricate data (#960 guardrail)
- **Voice**: Natural collaborative framing, eager/bright/honest colleague
- **Warmth guidance**: Dynamic warmth adjustment from formality_baseline (per-user personality profile)

## What #950 Proposes

The issue title says "Five Pillars + grammar." I'd like your input on:

### 1. What are the Five Pillars?

Is this referring to:
- (a) The five consciousness pillars from your earlier CXO work (if documented — point me to the doc)
- (b) A new framework you want to define for the floor prompt
- (c) Something from the vision V2.3 differentiator stack

### 2. What does "grammar" mean here?

Is this:
- (a) The grammatical structure of responses (sentence patterns, paragraph structure)
- (b) A "grammar" in the formal-language sense — rules the LLM must follow
- (c) The consciousness-as-voice-constraints concept from the M1 gate

### 3. Tone calibration priorities

The M1 canonical retest shows Identity queries scoring MARGINAL (3/5) on tone — the "looking forward to getting to know you" chatbot warmth persists even after the prohibition was added. The CXO anti-flattening discipline from PA's memo identified three enforcement layers:

1. Floor system prompt (primary mechanism)
2. Colleague Test as periodic verification
3. Fallback quality standards

For #950, should I focus on:
- (a) Rewriting the entire system prompt from scratch with Five Pillars structure
- (b) Evolving the current prompt to address known tone gaps
- (c) Both — new structure AND tone fixes

### 4. PDR-004 and voice constraints

Your UAT feedback referenced "PDR-004 violation: expressed emotion, not expressed investment." Is PDR-004 documented somewhere I should read, or should I work from the examples in the UAT memos?

## What I Need From You

1. Point me to the Five Pillars definition (or define them)
2. Clarify the "grammar" concept
3. Prioritize: rewrite vs evolve
4. Any docs I should read before starting

No rush on a full design — even a brief "here's the direction, here are the docs" would unblock me.

— Lead Dev
