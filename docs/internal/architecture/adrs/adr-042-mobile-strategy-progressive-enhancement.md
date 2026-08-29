# ADR-042: Mobile Strategy - Progressive Enhancement

## Status

**Accepted** | Proposed | Deprecated | Superseded

## Context

Ted Nadeau asked: "Is the product mobile-enabled, e.g., with swipe gesture?"

This question raises strategic decisions about mobile support:

- **User expectations**: Modern users expect mobile access to productivity tools
- **Development cost**: Native mobile apps require 3-6 months (iOS + Android)
- **Maintenance burden**: Native apps require ongoing platform updates, app store submissions
- **Feature parity**: Mobile-first design may constrain desktop capabilities
- **Current usage**: Alpha users are technical PMs, primarily using desktop workflows
- **Competitive landscape**: GitHub, Jira, Linear all offer mobile apps (but secondary to web)

Traditional approaches to mobile:

1. **Mobile-first**: Build native apps from day one → High initial cost, unknown demand
2. **Desktop-only**: Ignore mobile → Limits adoption, poor tablet/phone UX
3. **Responsive web**: Make web app mobile-friendly → Quick win, but limited native features
4. **Progressive Web App (PWA)**: Installable web app → Native-like experience, one codebase

This ADR defines Piper's mobile strategy using **progressive enhancement**.

## Decision

**We will adopt a progressive enhancement mobile strategy**, implementing mobile support in phases based on validated user demand:

### Phase 1: Mobile-Optimized Web (P3 - Wait for Demand)

**When**: When analytics show >10% mobile traffic or users explicitly request mobile access

**What**:
- Responsive CSS for key workflows (issue creation, chat, notifications)
- Touch gesture handlers (swipe left/right for navigation, pull-to-refresh)
- Mobile-friendly UI components (larger touch targets, simplified navigation)
- Viewport optimization (meta tags, responsive breakpoints)

**Effort**: 1-2 weeks
**Benefit**: Works in mobile browsers without app installation
**Risk**: Low (CSS + touch handlers, no new infrastructure)

**Implementation**:
```css
/* Mobile breakpoints */
@media (max-width: 768px) {
  /* Simplified navigation, larger touch targets */
}

/* Touch gesture support */
.swipeable {
  touch-action: pan-x;
}
```

### Phase 2: Progressive Web App (PWA) (P4 - Future)

**When**: When Phase 1 shows sustained mobile usage (>20% traffic for 3+ months)

**What**:
- Service worker for offline support
- Web app manifest (installable on home screen)
- Push notifications (via web push API)
- Cache-first strategy for static assets
- Background sync for offline actions

**Effort**: 2-3 weeks
**Benefit**: Feels like native app, works offline, one codebase
**Risk**: Medium (service worker complexity, browser compatibility)

**Implementation**:
```json
// manifest.json
{
  "name": "Piper Morgan",
  "short_name": "Piper",
  "start_url": "/",
  "display": "standalone",
  "icons": [...]
}
```

### Phase 3: Native Mobile App (Only if Strong Demand)

**When**: When Phase 2 shows power-user demand for native features (camera integration, deep OS integration, offline-first workflows)

**What**:
- React Native app (iOS + Android)
- Native UI components
- Native push notifications
- Deep linking
- OS-level integrations (Share sheet, widgets)

**Effort**: 3-6 months
**Benefit**: Premium mobile experience, full native capabilities
**Risk**: High (two platforms, app store approvals, ongoing maintenance)

**Decision criteria**:
- >30% mobile traffic for 6+ months
- Explicit user requests for native features
- Competitive pressure (users choosing competitors for mobile app)
- Budget available for 2+ developers (iOS + Android)

### What We Will NOT Do

- ❌ **Build native apps preemptively** (high cost, unknown demand)
- ❌ **Mobile-first design** (constrains desktop power-user workflows)
- ❌ **Separate mobile backend** (one API serves all clients)
- ❌ **Feature parity requirements** (mobile can be subset of desktop)

## Consequences

### Positive

- **Cost efficiency**: Build mobile support incrementally, only when validated
- **One codebase**: Web + PWA share same React codebase
- **Low maintenance**: No app store submissions until Phase 3
- **Fast iteration**: Deploy mobile updates instantly (no app review delay)
- **Risk mitigation**: If mobile demand is low, we invested minimally
- **Desktop-first**: Don't compromise desktop UX for hypothetical mobile users

### Negative

- **Delayed mobile features**: Users requesting mobile may wait months
- **Competitive disadvantage**: If competitors have native apps and we don't
- **PWA limitations**: iOS PWA support weaker than Android (notifications, background sync)
- **User education**: "Why isn't there an app?" → Explain PWA benefits

### Neutral

- **Analytics requirement**: Need mobile traffic data to make Phase 1 decision
- **Gesture design**: Must design touch gestures carefully (swipe conflicts with browser back/forward)
- **Testing burden**: Must test on iOS Safari, Android Chrome, various screen sizes

## Implementation

### Phase 1 Trigger: Mobile Analytics

**Add mobile traffic tracking**:
```python
# web/api/middleware.py
from fastapi import Request
import user_agents

async def track_mobile_usage(request: Request):
    ua = user_agents.parse(request.headers.get("user-agent"))
    if ua.is_mobile:
        # Track mobile traffic
        analytics.increment("mobile_traffic")
```

**Decision criteria**:
- If mobile traffic > 10% for 2+ weeks → Start Phase 1
- If users explicitly request mobile support → Start Phase 1

### Phase 1 Implementation: Responsive Web

**Responsive CSS** (`web/static/styles/mobile.css`):
```css
/* Mobile breakpoints */
@media (max-width: 768px) {
  .sidebar { display: none; }
  .main-content { width: 100%; }
  button { min-height: 44px; } /* iOS touch target size */
}

/* Touch gestures */
.swipeable {
  touch-action: pan-x;
}
```

**Touch gesture handlers** (`web/static/js/gestures.js`):
```javascript
let touchStartX = 0;
let touchEndX = 0;

function handleGesture() {
  if (touchEndX < touchStartX - 50) {
    // Swipe left (next)
    navigateNext();
  }
  if (touchEndX > touchStartX + 50) {
    // Swipe right (back)
    navigateBack();
  }
}

document.addEventListener('touchstart', e => {
  touchStartX = e.changedTouches[0].screenX;
});

document.addEventListener('touchend', e => {
  touchEndX = e.changedTouches[0].screenX;
  handleGesture();
});
```

### Phase 2 Implementation: PWA

**Service worker** (`web/static/sw.js`):
```javascript
// Cache-first strategy
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
```

**Web app manifest** (`web/static/manifest.json`):
```json
{
  "name": "Piper Morgan",
  "short_name": "Piper",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#4a90e2",
  "icons": [
    {
      "src": "/static/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/static/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### Phase 3 Decision Criteria

**Proceed to native app if ALL of the following**:
- ✅ Mobile traffic > 30% for 6+ months (sustained demand)
- ✅ 5+ explicit user requests for native app features
- ✅ Competitive pressure (users choosing competitors for mobile app)
- ✅ Budget available ($200K+, 6 months, 2 developers)
- ✅ PWA limitations blocking core workflows

**Tech stack** (if Phase 3 proceeds):
- **React Native** (share logic with web React app)
- **Expo** (managed workflow, faster development)
- **Native modules**: Push notifications, deep linking, camera

## Rationale

### Why Progressive Enhancement?

**Cost efficiency**: Mobile apps are expensive to build and maintain. Progressive enhancement lets us validate demand before investing.

**One codebase**: Web → PWA requires minimal changes (service worker + manifest). Web → Native requires full rewrite.

**Fast iteration**: Web updates deploy instantly. Native apps require app store review (1-7 days).

**Desktop-first**: Piper's alpha users are technical PMs who work primarily on desktop. Don't compromise desktop UX for hypothetical mobile users.

### Why NOT Mobile-First?

**User research**: Alpha users are technical PMs using desktop workflows (GitHub, Jira, Notion, terminal). Mobile is secondary.

**Competitive analysis**:
- **GitHub**: Desktop-first, mobile app is simplified (notifications, issues, not full IDE)
- **Jira**: Desktop-first, mobile app is subset (view issues, not admin)
- **Linear**: Desktop-first, mobile app is minimal (notifications, quick actions)

**Power-user workflows**: PM tasks (issue creation, roadmap planning, document review) benefit from large screens, keyboards, multi-window workflows.

**Strategic focus**: Better to excel at desktop PM workflows than be mediocre at mobile.

### Why NOT Native Apps First?

**High cost, unknown demand**:
- Native apps: 3-6 months, $200K+ (iOS + Android)
- PWA: 2-3 weeks, $20K (one codebase)
- Responsive web: 1-2 weeks, $10K (CSS + touch handlers)

**Maintenance burden**:
- Native: App store submissions, platform updates, two codebases
- PWA: Deploy instantly, one codebase, no app store

**Risk**: If mobile demand is low, we wasted 6 months. If high, we can build later with validated requirements.

### Why PWA Before Native?

**PWA advantages**:
- ✅ One codebase (web + PWA share React components)
- ✅ Instant deployment (no app store review)
- ✅ Lower cost (2-3 weeks vs 3-6 months)
- ✅ Cross-platform (iOS, Android, desktop)

**PWA limitations** (trigger for Phase 3):
- ⚠️ iOS push notifications weaker than native
- ⚠️ No background sync on iOS
- ⚠️ Limited offline storage
- ⚠️ No OS-level integrations (Share sheet, widgets)

If PWA limitations block core workflows → Build native (Phase 3).

### Ted's Question: Swipe Gestures

**Answer**: Yes, mobile will support swipe gestures (Phase 1).

**Implementation**:
- Swipe left/right for navigation (issue list, chat history)
- Pull-to-refresh for updates
- Long-press for context menus

**Design principle**: Touch gestures should enhance (not replace) tap-based navigation. Users should be able to accomplish all tasks without gestures (accessibility).

## Related Decisions

### Complements

- **ADR-013**: MCP + Spatial Intelligence Integration → Mobile can use same MCP adapters
- **Pattern-007**: Graceful Degradation → Mobile gracefully degrades if offline (PWA cache)
- **Pattern-039**: Feature Prioritization Scorecard → Mobile scored 0.69 (P3 - Wait for demand)

### Supersedes

None. This is the first mobile strategy ADR.

### Related Future Decisions

- **ADR documenting Native App Tech Stack**: Planned if Phase 3 proceeds
- **ADR documenting Mobile-Specific Features**: Document camera, offline workflow capabilities when implemented

## Measurement

### Success Criteria

**Phase 1 (Mobile-Optimized Web)**:
- Mobile traffic > 10% → Proceed
- User requests mobile support → Proceed
- Mobile bounce rate < 50% (users stay on mobile)
- Mobile task completion > 70% (users can complete core workflows)

**Phase 2 (PWA)**:
- Mobile traffic > 20% for 3+ months → Proceed
- PWA installation rate > 10% of mobile users
- Offline usage > 5% of mobile sessions

**Phase 3 (Native App)**:
- Mobile traffic > 30% for 6+ months → Proceed
- 5+ explicit requests for native features
- Competitive pressure (users choosing competitors for mobile)

### Analytics to Track

```python
# Track mobile usage
analytics.increment("mobile_traffic")
analytics.increment("mobile_task_completion")
analytics.increment("pwa_installs")
analytics.increment("offline_usage")
```

## References

### Documentation

- **Research source**: `dev/2025/11/20/ted-nadeau-follow-up-research.md` (Section 4)
- **Ted's reply**: `dev/2025/11/20/ted-nadeau-follow-up-reply.md` (Section 4)
- **Cover note**: `dev/2025/11/20/chief-architect-cover-note-ted-research.md`

### External References

- **Progressive Web Apps**: https://web.dev/progressive-web-apps/
- **Mobile-first vs Desktop-first**: https://www.lukew.com/ff/entry.asp?933
- **PWA on iOS**: https://webkit.org/blog/8090/workers-at-your-service/
- **Touch gestures**: https://developer.mozilla.org/en-US/docs/Web/API/Touch_events

### Competitive Analysis

| Product | Mobile Strategy | Our Takeaway |
|---------|----------------|--------------|
| GitHub | Desktop-first, native mobile (simplified) | Mobile is secondary for dev tools |
| Jira | Desktop-first, native mobile (subset) | PM tools are desktop-heavy |
| Linear | Desktop-first, minimal mobile | Fast startups still prioritize desktop |
| Notion | Cross-platform from day one | Consumer product (different market) |
| Slack | Mobile-first | Chat is mobile-native (Piper is not) |

**Conclusion**: PM/dev tools are desktop-first. Mobile is valuable but secondary.

---

**Decision made**: November 20, 2025
**Author**: Code Agent (Research Session)
**Inspired by**: Ted Nadeau's mobile strategy question
**Status**: Accepted
**Reviewers**: Chief Architect (pending), PM (approved approach)
