# Mobile Skunkworks Briefing

**Document Type**: Project Briefing
**Audience**: CXO, Mobile Consultant, Vibe Code Agent, other roles as needed
**Last Updated**: January 23, 2026
**Status**: On Hold (Not Abandoned)

---

## Executive Summary

The Mobile 2.0 skunkworks is an exploratory project to understand how Piper Morgan should feel as a mobile experience. It is **not** building "mobile Piper" — it's validating gestural interaction patterns that embody our object model grammar.

**Core hypothesis**: Gestures should be semantic, not positional. Swiping right on a Task means "complete"; swiping right on a Decision means "approve." The gesture vocabulary maps to entity types, not screen regions.

**Current state**: Code complete, tactile validation blocked by a bug (intent callbacks not firing). Native iOS build works; cards animate; intents don't trigger.

---

## Foundational Philosophy

These principles were established in the Dec 1, 2025 exploration session and should guide all mobile work:

### "The User is Mobile"

> "There is no mobile UX. There is a holistic UX with mobile touchpoints to ease the service journey and do jobs that need to be done."

**Implication**: Don't design "mobile Piper" as a separate product. Design for mobile users within a unified Piper experience.

### Front-End / Back-End Split

- **Phone**: Quick decisions, approvals, triage, capture
- **Laptop**: Context synthesis, complex work, deep execution
- **Piper**: Bridges the handoff between devices

Mobile isn't a smaller desktop. It's a different *role* in a cross-device workflow.

### Moment-Optimized, Not Feature-Portable

Don't shrink desktop features to fit a phone. Design for the unique moments mobile enables:

| Moment Type | Example | Mobile Job |
|-------------|---------|------------|
| Pre-meeting | 2 min before calendar event | Quick briefing |
| Post-meeting | 5 min after event ends | Capture action items |
| Interstitial | Waiting in line, between meetings | Triage, approvals |
| Transitional | Commute, walking | Debrief, processing |

### Entity-Based Gesture Grammar

Gestures map to the **entity model**, not arbitrary UI conventions:

| Entity | Swipe Right | Swipe Left | Swipe Up | Long Press |
|--------|-------------|------------|----------|------------|
| Task | Complete | Defer | Escalate | Show actions |
| Decision | Approve | Decline | Needs info | Show context |
| Person | Message | Snooze | — | Show relationships |
| Project | Dashboard | Archive | Add milestone | Show timeline |
| Blocker | Resolved | Escalate | — | Show blocked items |

This aligns with the MUX grammar: "Entities experience Moments in Places." The gesture is the embodied expression of interacting with an Entity.

### Lazy Object Instantiation (CloudOn Pattern)

> "Objects don't exist until attended to. Touch creates ontology."

Rather than pre-defining all possible objects, let the user's attention define what's "a thing." This came from CloudOn's work on document editing (US Patent 9886189) and transfers naturally to PM entities.

### Notification Ethics

> "Avoid the nag economy. Actionable, self-resolving, respectful of attention."

- **Actionable**: Not "something happened" but "here's a decision you can make"
- **Self-resolving**: Piper proposes action, user confirms, done
- **Respectful**: Trust earned through restraint, not engagement optimization

### Trust Gradient on Mobile

Trust manifests differently on mobile:

| Trust Stage | Mobile Behavior |
|-------------|-----------------|
| Stage 1 (New) | Notification-driven, pull interface only |
| Stage 2 (Building) | Proactive suggestions via notification |
| Stage 3 (Established) | Background sync, prepared briefings |
| Stage 4 (Trusted) | "I noticed you check X every morning..." |

**Key insight**: On mobile, trust is earned through *respect for attention*, not just *competence*. Interruptions feel more personal.

---

## Technical Implementation

### Stack

- **Framework**: Expo (React Native) with TypeScript
- **Gestures**: `react-native-gesture-handler` + `react-native-reanimated`
- **Haptics**: `expo-haptics`
- **Build path**: Native via Xcode (`npx expo run:ios`)

### Project Location

```
skunkworks/mobile/piper-mobile-poc/
├── src/
│   ├── entities/       # Entity types & mock data
│   ├── gestures/       # Entity-specific gesture→intent mappings
│   ├── components/     # EntityCard, IntentToast
│   ├── screens/        # GestureLabScreen (main playground)
│   └── theme/          # Dark theme, typography
```

### Current State (as of Jan 23, 2026)

*(This table is frozen, not silently stale — project Status is "On Hold" per the top of this
doc, so the Jan 23 snapshot reflects where it stopped, not where it currently stands. Noted
2026-08-11 during weekly-docs-audit #1583/#1585 since the bare "Current State" heading could
otherwise read as live.)*

| Component | Status |
|-----------|--------|
| Conceptual framework | ✓ Complete |
| Code implementation | ✓ Complete |
| Native build (Xcode) | ✓ Working |
| Visual feedback | ✓ Cards animate with gestures |
| Haptic feedback | ⏳ Untested (requires intent firing) |
| Intent callbacks | ✗ Bug — gestures don't trigger intents |
| Tactile validation | ⏳ Blocked by intent bug |

### Known Bug

**Symptom**: Cards animate when swiped (visual feedback works), but intent callbacks never fire.

**Likely cause**: Disconnect between gesture handler and intent callback. The `onEnd` handler either isn't detecting threshold crossings or isn't calling the callback.

**Debugging path**:
1. Review `EntityCard.tsx` (gesture handlers)
2. Review `GestureLabScreen.tsx` (intent state management)
3. Check: threshold comparison logic, `runOnJS` calls to escape worklet, callback prop connection

**Estimated fix**: 1-2 hours focused debugging

---

## Key Documents

| Document | Location | Purpose |
|----------|----------|---------|
| Original exploration | `2025-12-01-1815-mobile-opus-log.md` | Foundational philosophy |
| CXO feedback session | `2025-12-02-1651-cxo-opus-log.md` | UX guidance integration |
| PoC scaffold | `piper-mobile-poc-expo-scaffold.md` | Technical specification |
| One-shot prompt | `claude-code-one-shot-prompt.md` | Vibe coding brief |
| Implementation log | `2025-12-05-1030-vibe-code-opus-log.md` | Build details |
| Troubleshooting log | `2025-12-07-0703-vibe-code-opus-log.md` | Expo Go issues |
| Jan 3 status memo | `memo-cxo-mobile-poc-status.md` | Current state assessment |

---

## Relationship to Production Strategy

### ADR-042: Progressive Enhancement

The mobile skunkworks does **not** replace ADR-042. The production mobile strategy remains:

1. **Responsive Web** (current) — Mobile-friendly web UI
2. **PWA** (trigger: >20% mobile traffic for 3+ months)
3. **Native** (trigger: >30% mobile traffic for 6+ months + explicit requests)

The skunkworks is *informing* future native work, not building it now.

### Grammar Alignment

The entity-gesture mapping aligns with MUX grammar:
- **Entities**: The nouns you touch (Task, Decision, Person, Project, Blocker)
- **Moments**: The bounded time contexts mobile serves (pre-meeting, post-meeting, interstitial)
- **Places**: Mobile adds physical place awareness to virtual place awareness

When/if native mobile is built, the gesture grammar should feel like a natural extension of the desktop experience, not a different product.

---

## Questions to Answer (When Validation Possible)

The PoC was designed to answer:

1. **Does entity-based gesture mapping feel intuitive or confusing?**
2. **Can users learn the gesture vocabulary quickly?**
3. **Does haptic feedback create a satisfying sense of "commitment"?**
4. **Which gestures feel natural vs. forced?**
5. **Where does the mock fall short of real usage?**

---

## Next Steps

1. **Debug intent callback bug** (1-2 hours, requires Mobile Consultant or Vibe Code Agent)
2. **Tactile validation** (PM hands-on testing with working prototype)
3. **Capture learnings** (document what feels right/wrong)
4. **Feed insights to Track A** (design discovery)

The project moves at skunkworks pace — no urgency, but not abandoned.

---

## Contact Points

| Role | Responsibility |
|------|----------------|
| **PM (xian)** | Project sponsor, tactile testing |
| **CXO** | Design guidance, UX philosophy |
| **Mobile Consultant** | Technical planning, architecture |
| **Vibe Code Agent** | Implementation, debugging |

---

*Briefing compiled: January 23, 2026*
*For: Piper Morgan Mobile 2.0 Skunkworks*
