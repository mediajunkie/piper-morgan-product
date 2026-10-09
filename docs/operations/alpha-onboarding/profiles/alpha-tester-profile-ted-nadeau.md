# Alpha Tester Profile: Ted Nadeau

> *"Your process is more formal than any of the other ones... despite you potentially having less coding experience."*
> — Ted Nadeau, Dec 2025

## Tester Summary

| Field | Value |
|-------|-------|
| **Name** | Ted Nadeau |
| **Role** | Architectural Advisor + Windows Alpha Tester |
| **Company** | Dot Line Inc. |
| **Relationship** | 44-year friendship (Princeton 1982, roommates sophomore year) |
| **Testing Environment** | Windows 11, VS Code → Cursor |
| **Onboarding Status** | 95% complete - blocked on account creation |
| **Communication Cadence** | Weekly calls (Wednesdays), async email threads |
| **First Contact** | Pre-project (lifelong friend and collaborator) |

---

## Background & Context

### The Friendship
Ted and xian met freshman year at Princeton (1982) and were roommates sophomore year. That's **44 years of collaboration history**. Ted describes their dynamic as "yes-but" (his style) versus xian's "yes-and" approach. They've always looked for projects to work on together, with varying success over the years. AI-assisted coding has brought their professional worlds closer than ever before.

### Professional Profile
Ted is a brilliant computer scientist with deep background in cognitive science and philosophy. He has European and Japanese heritage and possibly studied overseas. His career includes work at Prudential and extensive experience in software architecture. He currently runs Dot Line Inc. and describes himself as primarily a technical architect who thinks in systems, layers, and taxonomies.

### Why He's Involved
Ted isn't just testing Piper Morgan—he's intellectually invested in the problem space. He's simultaneously:
1. **Advising** on architecture and methodology
2. **Building** his own parallel exploration (MultiChat)
3. **Testing** the Windows alpha experience
4. **Potentially** becoming the first external OSS contributor

---

## Architectural Contributions

Ted's fingerprints are throughout the Piper Morgan architecture:

### ADRs Authored/Influenced
| ADR | Title | Ted's Contribution |
|-----|-------|-------------------|
| **ADR-046** | Moment.type Agent Architecture | Designed the core pattern, corrected naming to avoid W3C collision |
| **ADR-050** | Conversation-as-Graph Model | Based entirely on Ted's MultiChat PRD |

### Patterns Influenced
| Pattern | Ted's Input |
|---------|-------------|
| **Pattern-039** | Feature Prioritization Scorecard - implements Ted's cost/benefit model |
| **Pattern-040** | Integration Swappability - Ted's "many-to-one-to-many" insight |

### Key Architectural Insights (from transcripts)

**On bot team architecture** (Dec 2):
> "There's a front end that you interact with. There's a middleware... The backend team is interacting with all the various different services."

**On role separation** (Dec 2):
> "You don't want to need to keep any state in your head... Partitioning out the sub elements of yourself is really what part of doing."

**On terminology** (Dec 2):
- Proposed "micro formats" → evolved to "Moment types" through collaboration
- Added PDR and PRD to the glossary
- Suggested xian needs a PM bot role, not just architect

**On agent communication** (Dec 2):
> "The meta question is how do bots best communicate? Is it through files... messaging infrastructure... API based?"

---

## MultiChat: Ted's Parallel Exploration

Ted has been building his own proof-of-concept for multi-party AI conversations. This isn't competition—it's symbiotic exploration.

### What He Built
- **Stack**: React/Next.js in Google Anti-Gravity (Firebase IDE)
- **Repository**: `Ted-Nadeau/multichat` (forked to `external/ted-multichat/` in PM repo)
- **PRD**: 80KB comprehensive document

### Key Features Demonstrated (Jan 14)
1. **Timeline view** - Flattened chronological chat
2. **Thread view** - Nested, indented conversations
3. **Whisper feature** - AI suggestions visible only to one participant
4. **Declaration of Independence scenario** - Jefferson, Franklin, Adams collaborating
5. **Configuration screens** - Agent/conversation settings

### xian's Assessment (Jan 14)
> "I think it is a product in and of itself, as opposed to a feature of Piper Morgan... there's a Venn diagram intersection. The Piper Morgan use case is like a release partner for your MVP."

### Integration Path
- Won't merge Next.js code directly (different stack)
- POC serves as reference implementation
- Ted's PRD becomes spec for future Python/FastAPI version
- Tracked in PDR-101 (Multi-Entity Conversation)

---

## Windows Testing Experience

Ted is the **only Windows alpha tester**. His E1-E30 bug report is the most comprehensive onboarding documentation we have.

### Environment
- Windows 11
- Started in VS Code, transitioned to Cursor
- PowerShell terminal
- Docker Desktop with WSL/Ubuntu

### Onboarding Timeline
| Date | Progress |
|------|----------|
| Dec 2 | Fork/branch confusion, first sync attempts |
| Jan 21 | Homework to try alpha again |
| Jan 28 | Cursor setup, label/issue exploration |
| Feb 4 | Full setup attempt, hit venv errors |
| Feb 6 | E1-E30 comprehensive bug report |

### Current Status (Feb 6)
- ✅ Docker running (7 containers)
- ✅ Reached http://127.0.0.1:8001/setup
- ❌ Account creation failed at Step 3
- **Blocked by**: Likely database migration issues (features table)

### Key Bugs Discovered
1. **uvloop incompatibility** - Doesn't support Windows (needs PEP 508 marker)
2. **CRLF line endings** - Break Docker container startup
3. **localhost vs 127.0.0.1** - Windows networking quirk
4. **Migration chain** - `features` table doesn't exist
5. **Schema drift** - 6 mismatches between models and database

*(Full issue list extracted separately: `ted-nadeau-windows-issues-2026-02-07.md`)*

---

## Communication Style: "Ted-ese"

Working with Ted requires understanding his distinctive communication patterns.

### Characteristics
1. **Taxonomizes everything** - why-atoms, why-molecules, reaction decks, gesture palettes
2. **Defense-in-depth thinking** - Always recommends layering solutions, never choosing just one
3. **Artifact hunger** - Frustrated when chat doesn't produce reusable objects
4. **Convergence anxiety** - Frequently asks "Am I diverging?"
5. **Graph thinking** - Everything is nodes, links, relationships
6. **Process formalism** - Wants to understand "the right way" before improvising
7. **Granular reactions** - Invented literal "reaction deck" (cards to hold up in meetings)

### Vocabulary
| Ted Says | He Means |
|----------|----------|
| "Micro formats" | Structured moment types (he proposed this term) |
| "Synectics" | Problem-solving methodology using diverse perspectives and metaphor |
| "Defense-in-depth" | Layer multiple solutions, don't choose just one |
| "Yes-but" | His style (vs xian's "yes-and") |
| "Labor camp" | Humorous description of AI agent coordination |
| "Artifact hunger" | Wanting concrete deliverables from conversation |

### Meta-Awareness
Ted frequently observes his own communication challenges:
- *"I'm having positive conversation with ChatGPT but concerned this is 'chat' not artifacts"*
- *"Perhaps my unease is based upon notation itself (media is message)"*
- *"I think I'm erring in not working on clear artifact but that's my limitation"*

### How to Work With Ted
1. **Give him structure** - He thrives with templates, formats, explicit processes
2. **Expect taxonomy proposals** - He'll categorize and name things
3. **Validate convergence** - Periodically confirm alignment to reduce his anxiety
4. **Point to artifacts** - Show him concrete documents, not just conversation
5. **Accept the depth** - His emails are long because his thinking is thorough
6. **Use his frameworks** - When he invents something (why-molecules), use it back

---

## Why-Molecule Framework

One of Ted's most impressive contributions is a complete Intent Specification DSL he built with ChatGPT (Dec 27).

### Status Quo Atoms (SQ)
Problems he identified in PM tooling:
- SQ-1: Decision rationale scattered across tools
- SQ-2: Issue triage inconsistent, manual
- SQ-3: Must remember exact identifiers (cognitive load)
- SQ-4: Standup summaries manually compiled
- SQ-5: Context decays over time
- SQ-6: Tool fragmentation (GitHub/Slack/Notion/Calendar)

### Why Archetypes
- **Optimization**: Same outcome, fewer resources
- **Amplification**: Same actor, more power
- **Stabilization**: Reduce risk, improve sustainability
- **Transformation**: Previously impossible → possible

### Key Insight
> *"Requirements : what :: decisions : why"*

Ted wants "why-engineering" to be as rigorous as requirements engineering. This aligns perfectly with Piper Morgan's vision of capturing not just what happened, but why.

---

## Weekly Call Pattern

### Schedule
- **Day**: Wednesdays (flexible)
- **Duration**: ~1 hour
- **Format**: Screen share, live exploration, async follow-up

### Typical Agenda
1. Catch-up on email threads
2. GitHub/branch coordination
3. Ted demos his progress
4. xian screen-shares development workflow
5. Architectural discussion
6. Action items for next week

### Transcript Themes Over Time
| Date | Primary Focus |
|------|--------------|
| Dec 2 | Fork/branch setup, advisor mailbox, role architecture |
| Jan 14 | MultiChat demo, roadmap review, competitive analysis |
| Jan 21 | xian's workflow demo, skills/patterns discussion |
| Jan 28 | Personal roadmap, beads concept, version management |
| Feb 4 | Windows setup attempt, Cursor installation |

---

## Open Items & Action Tracking

### Ted's Current Commitments
| Item | Status | Notes |
|------|--------|-------|
| Complete Windows setup | Blocked | Needs account creation bug fix |
| Security review with Geoff Hager | In progress | Geoff responded Dec 25, status unclear |
| MultiChat integration planning | Future | Post-MVP roadmap item |
| Frank Ryle introduction | Scheduled | March meeting in Palo Alto |

### For the Team
| Item | Owner | Status |
|------|-------|--------|
| Fix E1-E30 Windows bugs | Lead Dev | Issues extracted |
| Debug account creation | Lead Dev | High priority |
| Create Contributing.md | Docs | Dead link discovered |
| Formalize Ted's glossary edits | Docs | In his fork |

### Ted's Suggestions to Implement
1. **PM bot role** - xian should have a product manager assistant, not just architect
2. **Skills formalization** - Harvest implicit skills from methodology
3. **Layered bot architecture** - Front-end, middleware, backend separation
4. **File locking for coordination** - Simpler than branch management for agents

---

## Quotes That Capture Ted

On xian's methodology:
> *"Your process is more formal than any of the other ones... despite you potentially having less coding experience. That's a compliment to your architecture of this approach."*

On his own process:
> *"I've never interacted with a team before where I can just say things in TED speak and they can get it, understand it, process it, move forward."*

On the project:
> *"When you become Fred Fiandaca, you know, and things are just sort of running... you're left with sort of emotional insights and smiling. I mean, that would be fine."*

On AI collaboration:
> *"I call it labor camp. And Sergeant Schultz is the one who sees nothing."*

---

## Network & Referrals

### Geoff Hager (Security)
- Certified AWS Solutions Architect Professional, Enterprise Architect
- Connected Dec 22, offered security review
- Went dark after Dec 25, resurfaced Feb 1 apologizing
- Ted actively re-engaging (Feb 4, 5, 7 emails with comprehensive onboarding guidance)
- **Current status**: Interested but not yet active - Ted doing heavy lifting
- "May be even more difficult than I to merge-in" (Ted's caveat)

### Frank Ryle (PM)
- Princeton friend, world-respected Project Manager
- Goldman Sachs background
- Consulting for Intuitive Surgical (da Vinci microsurgery platform)
- Meeting planned for March in Palo Alto

---

## Files & References

### In Repository
- `external/ted-multichat/` - Ted's POC repository
- `advisors/ted/` - Inbox/outbox for advisor communication
- Issue #002 - Advisor Mailbox (created for Ted)
- PDR-101 - Multi-Entity Conversation (based on Ted's PRD)

### Documents Ted Has Drafted (Feb 2026)
- **PR/FAQ for MultiChat** - Amazon-style press release format
- **"Piper Morgan by Analogy"** - Jira comparison framing doc (now `piper-morgan-by-analogy.md`)

### Extracted This Session
- `ted-nadeau-windows-issues-2026-02-07.md` - 14 GitHub issues from E1-E30

### Meeting Transcripts
- Dec 2, 2025 - Fork setup, role architecture
- Jan 14, 2026 - MultiChat demo
- Jan 21, 2026 - Workflow screen share
- Jan 28, 2026 - Roadmap discussion
- Feb 4, 2026 - Windows setup attempt

---

*Profile created: February 7, 2026*
*Last updated: February 7, 2026*
*Created by: HOSR*

---

## Status update — October 8, 2026 (HOST)

Re-invited to the hosted alpha on 2026-07-12 (the greeting carries no first name; the address matches his). No later usage status verified.

*Source: Themis's read of the PM Sent folder (greeting names, dates and snippets only, no codes), logged in HOST's 2026-10-08 session log. Earlier sections above are as of February 2026 and not re-verified.*
