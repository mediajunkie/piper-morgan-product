# IAC Talk Review — What Needs Attention Before April 17

**Author**: PA
**Date**: April 8, 2026
**Status**: Assessment for xian — 9 days to conference

---

## Overall Assessment

The talk is strong. The structure (Problem → Insight → Architecture → Proof → Call) is clean, the memorable lines land, and the emotional arc builds well. Most of it doesn't need changes. Here's what does:

## Must Address

### 1. The 80.3% Claim (Slides 11-12)

This is the only empirical proof point in the talk. Where does this number come from? It should be:
- Traceable to a specific test/experiment
- Defensible if questioned (methodology, dataset, what was clustered, what "accuracy" means here)
- Current — if the architecture has changed since this was measured, note that

**Action**: Verify the source. If it's from the knowledge base clustering work, confirm the methodology is documented. If someone asks "how did you measure that?" in Q&A, xian needs a 30-second answer.

### 2. "Piper Morgan" Description Needs Updating

The talk says "I've been building an AI assistant called Piper Morgan." Since March, the product vision has evolved significantly:
- Floor-first routing (ADR-060) — Piper enhances an LLM, doesn't replace it
- "Bring Your Own Chat" — Piper is an MCP server, not a standalone app
- Consciousness as architecture — the Five Pillars aren't features, they're structural constraints

**Suggested tweak** (Slide 1 speaker notes): "I've been building something called Piper Morgan — a system that makes AI assistants into PM colleagues. Not another app — it enhances the AI tools you already use, through structure."

This is more accurate and more interesting to an IA audience — it's about structure enhancing existing systems, not building another product.

### 3. The "Colleague, Not Tool" Point Deserves a Beat

Section 3 mentions "Piper is designed to be a colleague, not a tool and not a friend" as the fourth principle but rushes through it. This is actually the most IA-relevant point — it's about designing the *nature of the relationship* through structure. Could get 30 more seconds:

"The way Piper speaks, what it offers to do, how it earns the right to be proactive — these aren't personality settings in a config file. They're structural constraints. The system literally cannot behave like a sycophantic assistant because that interaction pattern doesn't exist in the architecture. That's information architecture applied to AI personality."

## Worth Considering

### 4. The "Inhabited Spaces" Thread

Slide 6 introduces "new kinds of inhabitants" — non-human sapience in information spaces. This is powerful but could feel abstract without a concrete example. The Piper Morgan agent team (14 roles coordinating through mailboxes and session logs) is a live example of designed inhabited space with multiple AI inhabitants. If xian is comfortable sharing that detail, it would ground the abstract claim.

### 5. Slide Count

The outline says 17 slides but the speaker notes only cover 16. Verify the actual deck matches one or the other.

### 6. The PowerPoint

`dev/active/ethics-as-ia-draft.pptx` exists. Has it been updated since the March 1 outline? Does it need visual polish or is it presentation-ready?

## Don't Change

- The opening hook ("policy problem, not architecture problem") — strong
- The "road that doesn't go near the cliff" metaphor — memorable, clear
- The emotional arc toward "NEEDED" — earned and genuine
- The closing ("Not through policy. Through structure.") — lands perfectly
- The Q&A prompts — practical

## Preparation Checklist

- [ ] Verify 80.3% claim source and prepare 30-second methodology answer
- [ ] Update "what is Piper Morgan" description for current vision
- [ ] Review and finalize slide deck (match to outline)
- [ ] Rehearse at least once with timing checkpoints
- [ ] Prepare for likely Q&A: "How do you prevent the ethics layer from being bypassed?" and "What about open-source models without boundary enforcement?"

---

*9 days out. The content is 90% there. The remaining 10% is verification and polish.*
