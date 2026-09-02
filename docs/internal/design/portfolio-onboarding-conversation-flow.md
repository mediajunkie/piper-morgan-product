# Portfolio Onboarding Conversation Flow

> **Status note (2026-09-02, Docs, #1585)**: **#561 is CLOSED** — this design shipped. Kept as the
> historical design record for the implemented flow, not as a live spec. Much newer FTUX work
> exists (the ratified first-contact criterion, 2026-08-15; the FTUX experience model,
> 2026-08-21) — check those first for anything about *current* onboarding design; this document
> predates both by seven months and was not re-verified against them.

**Issue**: #561 MUX-FTUX-CONVERSE
**Parent**: #490 FTUX-PORTFOLIO (Complete)
**Status**: Design Document — implemented, historical record
**Date**: 2026-01-24

---

## Overview

This document specifies the complete conversation flow for portfolio onboarding,
addressing design gaps identified during PM testing on 2026-01-10.

### Problems Addressed

1. **"Main project" wording confusion** - Current prompt "...or is that your main focus?" implies hierarchy that may not exist
2. **No GitHub linking** - Projects created with name/description only, no repo connection
3. **Incomplete state machine** - Edge cases and recovery paths not documented

---

## State Machine

```
                                    ┌─────────────────────────────────────────┐
                                    │                                         │
                                    ▼                                         │
┌──────────────┐   accept    ┌──────────────────┐   done/    ┌────────────┐   │
│              │────────────▶│                  │───decline──▶│            │   │
│  INITIATED   │             │ GATHERING_PROJECTS│            │ CONFIRMING │   │
│              │◀────────────│                  │◀──add more──│            │   │
└──────────────┘   (restart) └──────────────────┘             └────────────┘   │
       │                            │                               │          │
       │ decline                    │ add project                   │ confirm  │
       │                            ▼                               ▼          │
       │                     ┌──────────────────┐            ┌────────────┐    │
       │                     │  (optional new)  │            │            │    │
       │                     │ LINKING_GITHUB   │───────────▶│  COMPLETE  │    │
       │                     └──────────────────┘   skip/    └────────────┘    │
       │                                            done                       │
       │                                                                       │
       ▼                                                                       │
┌──────────────┐                                                               │
│   DECLINED   │───────────────────────────────────────────────────────────────┘
└──────────────┘   (user can restart later with "set up my projects")
```

### States

| State | Description | Entry Conditions |
|-------|-------------|------------------|
| `INITIATED` | Piper offered onboarding | User has no projects, greeted Piper |
| `GATHERING_PROJECTS` | Collecting project info | User accepted offer |
| `LINKING_GITHUB` | **NEW** Optional GitHub linking | Project captured, user interested |
| `CONFIRMING` | Reviewing before save | User indicated done adding |
| `COMPLETE` | Projects saved | User confirmed |
| `DECLINED` | User opted out | User declined at any point |

---

## Conversation Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           HAPPY PATH (Recommended)                           │
└─────────────────────────────────────────────────────────────────────────────┘

User: "Hi Piper"
                                        ┌─────────────────────────────────────┐
Piper: "Hello! I'm Piper Morgan, your   │ STATE: INITIATED                   │
       PM assistant. I'd love to learn  │ Theatrical framing: curiosity,     │
       about what you're working on.    │ not interrogation                   │
       Would you like to tell me about  └─────────────────────────────────────┘
       your projects?"

User: "Sure" / "Yes" / "OK"
                                        ┌─────────────────────────────────────┐
Piper: "Great! What's a project you're  │ STATE: GATHERING_PROJECTS           │
       focused on right now?"           │ Changed: "a project" not "the main  │
                                        │ project" - removes hierarchy        │
                                        └─────────────────────────────────────┘

User: "I'm building a fitness app called HealthTrack"
                                        ┌─────────────────────────────────────┐
Piper: "HealthTrack - got it! Is this   │ NEW: GitHub linking offer           │
       connected to a GitHub repo?      │ Optional, can skip                  │
       I can help track issues and PRs  └─────────────────────────────────────┘
       if you'd like to link it."

User: "Not yet" / "Skip for now"
                                        ┌─────────────────────────────────────┐
Piper: "No problem. Would you like to   │ Revised: No "main focus" implication│
       tell me about any other          │ Just asks about more projects       │
       projects, or is that all         └─────────────────────────────────────┘
       for now?"

User: "That's all for now"
                                        ┌─────────────────────────────────────┐
Piper: "Perfect. I have HealthTrack     │ STATE: CONFIRMING                   │
       noted. Should I save this to     │ Clear confirmation request          │
       your portfolio?"                 └─────────────────────────────────────┘

User: "Yes"
                                        ┌─────────────────────────────────────┐
Piper: "All set! I've added HealthTrack │ STATE: COMPLETE                     │
       to your portfolio. I'll help     │ Transition to normal conversation   │
       you stay on track. What would    └─────────────────────────────────────┘
       you like to focus on today?"
```

---

## Alternative Paths

### Path A: User Has Multiple Projects

```
User: "I have two projects"

Piper: "I'd love to hear about both! Let's start with one -
       what's a project you're working on?"

User: "HealthTrack, a fitness app"

Piper: "HealthTrack - got it! Is this connected to a GitHub repo?"

User: "Yes, it's at github.com/user/healthtrack"

Piper: "Perfect, I've linked that. What's your other project?"
       ▲
       └── Note: Piper remembers user said "two" and asks for the other

User: "DataViz, a data visualization library"

Piper: "DataViz - nice! GitHub repo for this one?"

User: "github.com/user/dataviz"

Piper: "Got it. Any other projects, or are those the two?"
       ▲
       └── References the "two" user mentioned, natural closure

User: "That's them"

Piper: "Perfect. I have HealthTrack and DataViz noted.
       Should I save these to your portfolio?"
```

### Path B: User Declines Initially, Returns Later

```
User: "Hi"

Piper: "Hello! I'd love to learn about what you're working on..."

User: "Not right now"

Piper: "No problem! Whenever you're ready, just say 'set up my
       projects' and we can do that. What can I help with today?"

... (later in conversation or new session) ...

User: "Set up my projects"

Piper: "Great! What's a project you're focused on right now?"
       ▲
       └── Resumes GATHERING_PROJECTS state
```

### Path C: User Adds Project During Confirmation

```
Piper: "I have HealthTrack noted. Should I save this?"

User: "Actually, I also have another project"

Piper: "Sure! What's the other project?"
       ▲
       └── Returns to GATHERING_PROJECTS

User: "MealPlanner"

Piper: "MealPlanner - got it! GitHub repo?"

User: "No"

Piper: "No problem. Any other projects?"

User: "That's all"

Piper: "Perfect. I have HealthTrack and MealPlanner noted.
       Should I save these to your portfolio?"
```

### Path D: User Provides GitHub URL Immediately

```
User: "I'm working on HealthTrack at github.com/user/healthtrack"

Piper: "HealthTrack - got it, and I've linked the GitHub repo!
       Would you like to tell me about any other projects?"
       ▲
       └── Skips explicit GitHub question since user provided URL
```

---

## Prompt Language Improvements

### Current vs. Improved

| Situation | Current | Improved | Rationale |
|-----------|---------|----------|-----------|
| First project ask | "What's the **main** project you're focused on?" | "What's **a** project you're focused on right now?" | Removes hierarchy assumption |
| More projects? | "...or is that your **main focus**?" | "Would you like to tell me about any other projects, or is that all for now?" | Neutral, no hierarchy |
| Multiple captured | "Should I save these?" | "I have [X] and [Y] noted. Should I save these to your portfolio?" | Confirms what was captured |
| Unclear input | "Just say 'yes' to confirm" | "You can say 'yes' to save, 'add more' for more projects, or 'start over' if something's wrong" | More options, clearer |

### Theatrical Framing (per MomentType.QUESTION patterns)

The onboarding flow should feel like:
- **Curiosity**, not interrogation
- **Invitation**, not requirement
- **Collaboration**, not data entry

**Good**: "I'd love to learn about what you're working on"
**Bad**: "Please enter your project information"

**Good**: "Is this connected to a GitHub repo? I can help track issues if you'd like"
**Bad**: "Enter GitHub URL (optional)"

---

## GitHub Linking Design

### When to Offer

| Trigger | Offer GitHub? | Rationale |
|---------|---------------|-----------|
| Project name captured | Yes | Natural point to ask |
| User provides URL in description | No (auto-detect) | Don't re-ask |
| User said "skip" for previous project | Still ask | Each project is independent |
| User seems in a hurry ("just add it") | Softer offer | "We can link GitHub later if you'd like" |

### GitHub URL Detection

```python
GITHUB_URL_PATTERN = r"github\.com/[\w-]+/[\w.-]+"
```

If detected in user message, auto-extract and confirm:
> "I noticed a GitHub link - I've connected that to HealthTrack!"

### Linking Flow

```
STATE: GATHERING_PROJECTS
  │
  ├─ Project info extracted
  │
  ▼
┌─────────────────────────────────────────┐
│ Check: Did user provide GitHub URL?     │
└─────────────────────────────────────────┘
  │                    │
  │ Yes                │ No
  ▼                    ▼
Auto-link,          Offer linking
confirm           ┌─────────────────┐
                  │ "Is this        │
                  │ connected to    │
                  │ GitHub?"        │
                  └─────────────────┘
                    │         │
                    │ Yes     │ No/Skip
                    ▼         ▼
              ┌─────────┐   Continue to
              │ Get URL │   "more projects?"
              └─────────┘
                    │
                    ▼
              Validate & link
                    │
                    ▼
              "more projects?"
```

---

## Edge Cases

### User Input Classification

| Input | Interpretation | Response |
|-------|----------------|----------|
| "no" | Decline/done | Context-dependent (INITIATED=decline, GATHERING=done) |
| "nope that's it" | Done adding | Transition to CONFIRMING |
| "yes" | Accept/confirm | Context-dependent |
| "yeah I have another one" | Add more | Stay in GATHERING |
| "wait, I made a mistake" | Error recovery | "No problem! What would you like to fix?" |
| "start over" | Reset | Clear and restart from INITIATED |
| "cancel" | Abort | Transition to DECLINED |
| [gibberish] | Unclear | Re-prompt with options |
| [long description] | Project info | Extract name, ask for clarification if needed |

### Error Recovery

```
User: "Actually that's wrong"

Piper: "No problem! Would you like to:
       - Change something about [last project]?
       - Remove [last project]?
       - Start over completely?"

User: "Remove HealthTrack"

Piper: "Done - I've removed HealthTrack. Would you like to
       add a different project, or continue with the others?"
```

---

## Implementation Notes

### New State Required

Add `LINKING_GITHUB` to `PortfolioOnboardingState`:

```python
class PortfolioOnboardingState(Enum):
    INITIATED = "initiated"
    GATHERING_PROJECTS = "gathering_projects"
    LINKING_GITHUB = "linking_github"  # NEW
    CONFIRMING = "confirming"
    COMPLETE = "complete"
    DECLINED = "declined"
```

### Handler Changes

1. After `_extract_project_info()`, check for GitHub URL
2. If no URL, offer linking before asking about more projects
3. Add `_handle_linking_github()` method
4. Update `_handle_gathering()` to route through linking

### Pattern Additions

```python
# GitHub URL patterns
GITHUB_URL_PATTERNS = [
    r"github\.com/([\w-]+)/([\w.-]+)",
    r"git@github\.com:([\w-]+)/([\w.-]+)",
]

# Skip linking patterns
SKIP_LINKING_PATTERNS = [
    r"\b(no|nope|skip|not yet|later|don't have one)\b",
]
```

---

## Acceptance Criteria Checklist

- [x] Document complete conversation state machine
- [x] Design improved "more projects?" prompt language
- [x] Design optional GitHub linking step
- [x] Create conversation flow diagram
- [x] Get PM approval on design before implementation

---

## Decision Points - APPROVED

### Decision 1: GitHub Linking State ✅

**Approved**: Add explicit `LINKING_GITHUB` state
- Clear state machine, easy to track

### Decision 2: Auto-Detection of GitHub URLs ✅

**Approved**: Auto-detect and confirm
- Less friction when user provides URL
- Confirmation prevents mis-detection issues

### Decision 3: When to Offer GitHub Linking ✅

**Approved**: After every project, softer language on subsequent
- Consistent experience
- "Want to link this one too?" for 2nd+ projects

---

*Document created: 2026-01-24*
*Author: Lead Developer session*
*PM approval: 2026-01-24 9:56 AM - All three decisions approved*
