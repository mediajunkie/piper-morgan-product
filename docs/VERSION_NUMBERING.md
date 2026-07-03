# Piper Morgan Version Numbering Scheme

**Current Version**: 0.8.9.1 (Alpha — security patch, closed #1343; next: 0.9.0 beta at MVP)
**Last Updated**: July 2, 2026

---

## Overview

Piper Morgan uses semantic versioning with a three-tier system: **X.Y.Z**

Each tier has specific meaning that communicates the maturity and stage of the software.

---

## Version Tiers Explained

### First Digit (X): Major Stage
Indicates the fundamental maturity level of the product.

- **0** = Pre-MVP (experimental, alpha, beta)
- **1** = MVP (minimum viable product)
- **2+** = Post-MVP (major platform upgrades or fundamental changes)

**Examples**:
- `0.8.0` → Pre-MVP, alpha stage
- `1.0.0` → MVP release
- `2.0.0` → Major platform redesign or fundamental architecture change

---

### Second Digit (Y): Milestone
Within each major stage, marks significant feature milestones and capabilities.

**Pre-MVP Milestones** (0.Y.Z):
- **0.0** = Proof of concept to prototype
- **0.1** = New DDD (Domain-Driven Design) foundation
- **0.2** = GitHub integration, documentation, learning conversations
- **0.3** = MCP (Model Context Protocol) integration
- **0.4** = Spatial intelligence
- **0.5** = Ethical boundaries layer
- **0.6** = Plug-in architecture
- **0.7** = Great Refactor (system-wide architectural improvements)
- **0.8** = Alpha release (first external testers)
- **0.9** = Beta release (wider testing)

**MVP Milestones** (1.Y.Z):
- **1.0** = MVP release
- **1.1** = First feature addition post-MVP
- **1.2+** = Subsequent feature additions

---

### Third Digit (Z): Patch/Update
Within each milestone, marks incremental updates, bug fixes, and improvements.

**Release Types**:
- **X.Y.0** = Major milestone release (e.g., `0.8.0` = first alpha)
- **X.Y.1** = First update to milestone (e.g., `0.8.1` = first alpha update)
- **X.Y.2+** = Subsequent patches and updates

**Examples**:
- `0.8.0` → First alpha release
- `0.8.1` → First update to alpha testers
- `0.9.0` → First beta release
- `0.9.1` → First update to beta testers
- `1.0.0` → First MVP release
- `1.0.1` → Fast-follow bug fix

---

## Version History Timeline

### Early Development (May - August 2025)
- **0.0.1** (May 28, 2025) - Proof of concept
- **0.0.2** - First interactive prototype
- **0.0.x** - Various increasingly sophisticated iterations

### Foundation Era (August - September 2025)
- **0.1.0** - Real product foundation with DDD architecture
- **0.2.0** - GitHub integration, documentation system, learning conversations
- **0.3.0** - Model Context Protocol (MCP) integration
- **0.4.0** - Spatial intelligence capabilities
- **0.5.0** - Ethical boundaries layer activated
- **0.6.0** - Plug-in architecture implemented

### Maturation Era (September - October 2025)
- **0.7.0** - Great Refactor (system-wide improvements)
  - Sprint GREAT-1 through GREAT-6
  - Architecture consolidation
  - Pattern standardization
  - Performance optimization

### Alpha Era (October 2025 - Present)
- **0.8.0** (October 24, 2025) - First Alpha Release
- **0.8.1–0.8.6** - Alpha updates (Oct 2025 – May 2026)
- **0.8.7** (June 3, 2026) - M1 Foundation + M2 Conscious Floor stable cut for alpha
- **0.8.8** (June 19–20, 2026) - D1 close: Radar default home, F2 shell complete, BYOC credential layer, Conscious Floor, Files, Slack inbound, 252/252 regression
- **0.8.9** (June 22, 2026) - RECONNECT WS-1: DB-backed connector config + StandupAssembler; security: AES-256-GCM field encryption, encrypted secrets, per-user LLM key routing, auth hardening; Design D2: token system, mobile nav, Radar rename
- **0.8.9.1** (July 2, 2026) - Security patch: closed #1343 anonymous LLM-key billing exposure (Caddy edge-gate removal had dropped the perimeter that made the old server-key fallback safe) ← **CURRENT**

### Beta Era (Planned)
- **0.9.0** - Beta / MVP release (wider testing, more self-service, UUID bearer auth)
- **0.9.x** - Beta updates and refinements

### Production Era (Planned)
- **1.0.0** - MVP feature set polished for production release
- **1.0.x** - Post-MVP bug fixes and improvements
- **1.1.0+** - Feature additions

---

## How to Interpret Versions

### Reading a Version Number

**Example**: `0.8.1`
- **0** = Pre-MVP stage (still experimental)
- **8** = Alpha milestone (external testers)
- **1** = First update since alpha launch

**Meaning**: "This is the first update to alpha testers during the pre-MVP phase."

### What This Tells You

**If you see 0.x.x**:
- Software is pre-MVP
- Expect bugs, rough edges, incomplete features
- Breaking changes may occur between milestones
- Not for production use

**If you see 1.0.x**:
- Software has reached MVP
- Core functionality is stable
- Suitable for production use (with caveats)
- Breaking changes will be rare

**If you see 1.x.0** (where x > 0):
- New features added post-MVP
- May introduce new capabilities
- Backwards compatibility preserved where possible

---

## Alpha vs Beta vs MVP

### Alpha (0.8.x)
**Purpose**: Early testing with small group (2-5 testers)
- Guided setup process
- Close PM support
- Frequent bugs expected
- Rapid iteration based on feedback
- Focus: "Does this basically work?"

### Beta (0.9.x)
**Purpose**: Wider testing (10-20 testers)
- More self-service
- Documented known issues
- Fewer critical bugs
- Weekly updates
- Focus: "Is this reliable enough?"

### MVP (1.0.0)
**Purpose**: First production release
- All core features working
- Comprehensive documentation
- Stable enough for real work
- Regular update schedule
- Focus: "Is this useful?"

---

## Version Communication

### In Documentation
Always reference the current version:
```markdown
This guide is for Piper Morgan v0.8.0
```

### In Code
Check version programmatically:
```python
from services.config import VERSION
print(f"Piper Morgan {VERSION}")
```

### For Users
System status shows version:
```bash
python main.py status
# → Piper Morgan v0.8.0
```

---

## Frequently Asked Questions

### Why start at 0.8.0 for alpha?
The version number reflects the journey from proof-of-concept (0.0.1) through multiple major milestones (DDD, MCP, plugins, refactor) before reaching alpha testing readiness.

### When will we reach 1.0?
Version 1.0 (MVP) will be released when:
- Core features are stable
- Beta testing validates reliability
- Documentation is comprehensive
- System is production-ready (with caveats)

Estimated: Early 2026

### What happens after 1.0?
Post-MVP versions (1.1+) will add new features while maintaining backwards compatibility. Major architectural changes would trigger 2.0.

### Can I rely on 0.8.x for production work?
No. Alpha versions (0.8.x) are explicitly **not** for production use. See ALPHA_AGREEMENT.md for details.

---

## See Also

- `ALPHA_TESTING_GUIDE.md` - Setup instructions for v0.8.0
- `ALPHA_AGREEMENT.md` - Legal terms for alpha testing
- `ALPHA_KNOWN_ISSUES.md` - Current bugs and limitations
- `CHANGELOG.md` - Detailed changes between versions

---

_Last Updated: June 22, 2026_
_Applies To: Piper Morgan 0.8.0+_
