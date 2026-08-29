# CORE-USERS-ONBOARD: Alpha User Onboarding Infrastructure

Alpha testing requires users to self-onboard with minimal friction. Currently, configuration is developer-focused with manual file editing. Alpha users need a guided setup experience.

**Strategic Context** (from usage models analysis):
- Piper Morgan supports **three usage models**: DIY Technical, Guided Alpha, Hosted SaaS
- Current model (DIY) works for technical users but blocks broader alpha testing
- 85% of multi-user infrastructure complete (User model, JWT, API keys, etc.)
- **Opportunity**: Support both DIY and Guided models in Alpha with minimal additional work

---

## Current State

### What Works Today (DIY Technical Users) ✅
```bash
git clone https://github.com/mediajunkie/piper-morgan
cp config/PIPER.user.md.example config/PIPER.user.md
# Edit API keys, GitHub tokens, etc.
docker-compose up
# Access at http://localhost:8001
```

**Status**: Fully functional for technical users

### What's Missing for Guided Alpha Users ❌
- Configuration requires manual editing of YAML/JSON files
- API keys scattered across different config files
- No first-run experience or validation
- No preference management UI
- No validation of user setup
- No troubleshooting guidance

---

## Scope

### Phase 1: Setup Wizard (CLI) - Priority 1
**First-run experience for new users:**

```bash
# One-command install
curl -sSL https://install.piper-morgan.com | bash

# Or manual clone + wizard
git clone https://github.com/mediajunkie/piper-morgan
cd piper-morgan
./piper-morgan setup

# Interactive wizard:
Welcome to Piper Morgan Alpha!

Let's get you set up (5 minutes):

1. System Check
   ✓ Docker installed
   ✓ Python 3.11+ available
   ✓ Port 8001 available

2. API Keys (Required)
   OpenAI API key: [____] ← Validates in real-time
   Status: ✓ Valid (gpt-4 access confirmed)

   Anthropic API key (optional): [____]
   Status: ✓ Valid (claude-3-opus access confirmed)

3. Integrations (Optional)
   GitHub token: [____] or [Skip]
   Notion key: [____] or [Skip]
   Slack token: [____] or [Skip]

4. Basic Preferences
   Default LLM: [1] Claude Opus  [2] GPT-4
   Response style: [1] Concise  [2] Balanced  [3] Detailed
   Auto-save conversations: [Y/n]

5. User Account
   Username: [____] (for multi-user support)
   Email: [____] (optional, for notifications)

Setup complete! 🎉
Starting Piper Morgan...
Access at: http://localhost:8001

First-time user? Try these commands:
  piper help        # Show available commands
  piper status      # Check system health
  piper config      # Manage preferences
```

**Key Features**:
- ✅ Real-time API key validation (calls provider APIs)
- ✅ Clear error messages with troubleshooting steps
- ✅ Optional integrations (skip if not needed)
- ✅ Sensible defaults (can start immediately)
- ✅ Progress indicators and success confirmation

### Phase 2: User Preferences System - Priority 2
```yaml
# Auto-generated: ~/.piper/preferences.yaml
user:
  name: "Alpha User"
  email: "user@example.com"
  username: "alpha_user_1"  # Used for keychain isolation

llm:
  default_model: "claude-3-opus-20240229"
  fallback_model: "gpt-4"
  temperature: 0.7
  max_tokens: 4000

behavior:
  response_style: "balanced"  # concise | balanced | detailed
  auto_save: true
  confirmation_required: ["delete", "publish", "rotate_key"]
  show_confidence_scores: false

integrations:
  github:
    enabled: true
    default_repo: "user/repo"
    token_stored: true  # In OS keychain
  notion:
    enabled: false
  slack:
    enabled: false

personality:
  warmth_level: 0.7
  confidence_style: "contextual"
  action_orientation: "medium"
  technical_depth: "balanced"
```

**Management Commands**:
```bash
piper config set llm.model claude-3-opus-20240229
piper config get llm.model
piper config list
piper config edit  # Opens in $EDITOR
piper config reset  # Reset to defaults
```

### Phase 3: Health Checks & Validation - Priority 1
```bash
piper status

System Status: ✓ Healthy

Database:
  ✓ PostgreSQL connected (port 5433)
  ✓ 84 users in database
  ✓ Migrations up to date

API Keys:
  ✓ OpenAI (gpt-4 access)
  ✓ Anthropic (claude-3-opus access)
  ✗ GitHub (token expired)  ← Clear actionable error

Integrations:
  ✓ GitHub (3 repos connected)
  ✓ Keychain access working
  ⚠ Notion (not configured)

Performance:
  ✓ Response time: 127ms (average)
  ✓ Memory usage: 2.3GB / 8GB
  ✓ Database pool: 3/10 connections

Recommendations:
  → Rotate GitHub token (expired 3 days ago)
  → Consider enabling Notion integration
  → System running optimally
```

### Phase 4: Documentation - Priority 1
- Alpha quickstart guide (video + written)
- Common issues FAQ with solutions
- Discord/Slack community setup
- Troubleshooting flowcharts
- Architecture overview for technical users

---

## Implementation Strategy

### Phase 1A: Minimal Setup Wizard (Week 1) - 8 hours
**Goal**: Get users from zero to first query in <5 minutes

```python
# New: scripts/setup_wizard.py
class SetupWizard:
    async def run_setup(self):
        # 1. System checks
        await self.check_docker()
        await self.check_python()
        await self.check_ports()

        # 2. API key collection
        openai_key = await self.prompt_api_key("OpenAI", required=True)
        await self.validate_api_key("openai", openai_key)  # Real validation!

        anthropic_key = await self.prompt_api_key("Anthropic", required=False)
        if anthropic_key:
            await self.validate_api_key("anthropic", anthropic_key)

        # 3. Store keys securely (uses Issue #228 infrastructure!)
        await self.store_api_key("openai", openai_key)
        if anthropic_key:
            await self.store_api_key("anthropic", anthropic_key)

        # 4. Create user account
        user = await self.create_user_account()

        # 5. Set preferences
        await self.configure_preferences()

        # 6. Start system
        await self.start_piper_morgan()
```

**Dependencies**:
- ✅ User model (Issue #228)
- ✅ UserAPIKeyService (Issue #228)
- ✅ KeychainService (Issue #228)
- ✅ JWT authentication (Issue #227)

**Leverage**: 85% infrastructure exists, just need UI layer!

### Phase 1B: Status & Health Checks (Week 1) - 4 hours
```python
# New: scripts/status_checker.py
class StatusChecker:
    async def check_system_health(self):
        # Database connectivity
        # API key validity
        # Integration status
        # Performance metrics
        # Actionable recommendations
```

### Phase 2: Preferences Management (Week 2) - 6 hours
```python
# Enhanced: services/preferences/preference_manager.py
class PreferenceManager:
    async def get_preference(self, user_id: str, key: str):
        # Read from ~/.piper/preferences.yaml

    async def set_preference(self, user_id: str, key: str, value: Any):
        # Update preferences.yaml
        # Validate value
        # Apply immediately
```

### Phase 3: Documentation (Week 2) - 6 hours
- Video walkthrough (10 minutes)
- Quickstart guide (written)
- FAQ (common issues + solutions)
- Troubleshooting flowchart
- Community Discord/Slack setup

---

## Technical Considerations

### Leverage Existing Infrastructure (85% Complete!) ✅
- **User Model**: Already exists (Issue #228)
- **API Key Storage**: KeychainService + UserAPIKeyService ready (Issue #228)
- **Validation**: Real API validation methods exist
- **Database**: PostgreSQL with migrations
- **Authentication**: JWT token system (Issue #227)

### New Components (15% Remaining)
- ❌ Setup wizard CLI (8 hours)
- ❌ Status checker (4 hours)
- ❌ Preferences management (6 hours)
- ❌ Documentation (6 hours)

**Total New Development**: 24 hours (~3 days)

### Architecture Integration
```
┌─────────────────────────────────────────────────────────┐
│              Setup Wizard (NEW)                          │
│         • System checks                                  │
│         • API key collection & validation                │
│         • User account creation                          │
│         • Preference configuration                       │
└───────────┬─────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────┐
│         Existing Infrastructure (85% COMPLETE)           │
│                                                          │
│  UserAPIKeyService → KeychainService → OS Keychain      │
│  User Model → PostgreSQL                                 │
│  JWT Authentication → Token Management                   │
│  LLM Services → Provider APIs                           │
└──────────────────────────────────────────────────────────┘
```

---

## Success Metrics

### Setup Time
- **Target**: <5 minutes from clone to first query
- **Measure**: Average time for 10 alpha users
- **Success**: 90%+ complete setup in <5 minutes

### Setup Completion Rate
- **Target**: >90% of users complete setup
- **Measure**: Users who start setup wizard and reach "Setup complete!"
- **Success**: <10% dropout rate

### Support Tickets
- **Target**: <10% of users need support during setup
- **Measure**: Support requests in Discord/Slack during first week
- **Success**: >80% self-service resolution

### User Satisfaction
- **Target**: >80% satisfied with setup experience
- **Measure**: Post-setup survey (1-5 star rating)
- **Success**: Average rating >4.0 stars

### Time to Value
- **Target**: First successful query within 10 minutes
- **Measure**: Time from setup start to first PM response
- **Success**: 90%+ achieve this

---

## Acceptance Criteria

### Phase 1A: Setup Wizard (Priority 1)
- [ ] One-command setup: `./piper-morgan setup`
- [ ] Real-time API key validation (calls provider APIs)
- [ ] Clear error messages with troubleshooting steps
- [ ] User account creation (username, email optional)
- [ ] Secure key storage (uses Issue #228 infrastructure)
- [ ] System starts automatically after setup
- [ ] Setup completion in <5 minutes for 90% of users

### Phase 1B: Health Checks (Priority 1)
- [ ] `piper status` command shows system health
- [ ] Database connectivity check
- [ ] API key validity check (for all configured providers)
- [ ] Integration status (GitHub, Notion, Slack)
- [ ] Performance metrics (response time, memory, connections)
- [ ] Actionable recommendations for issues

### Phase 2: Preferences (Priority 2)
- [ ] Preferences stored in `~/.piper/preferences.yaml`
- [ ] CLI commands: `piper config get/set/list/edit/reset`
- [ ] Validation of preference values
- [ ] Immediate application of changes
- [ ] Backward compatible with PIPER.user.md overrides

### Phase 3: Documentation (Priority 1)
- [ ] Video walkthrough (10 minutes)
- [ ] Quickstart guide (written, step-by-step)
- [ ] FAQ covering 90%+ of common issues
- [ ] Troubleshooting flowchart
- [ ] Community Discord/Slack setup guide
- [ ] Architecture overview for technical users

### Quality Gates
- [ ] Setup wizard tested on macOS, Linux, Windows
- [ ] All error paths have clear messages
- [ ] Rollback possible (return to manual config)
- [ ] No breaking changes to existing DIY workflow
- [ ] Complete test coverage for wizard logic

---

## Usage Models Strategy

### Support Three Models in Alpha

#### Model 1: DIY Technical (Keep Working) ✅
**Current workflow continues unchanged:**
```bash
git clone https://github.com/mediajunkie/piper-morgan
# Manual config editing
docker-compose up
```

**No changes needed** - already works perfectly

#### Model 2: Guided Alpha (New, This Issue) 🆕
**New wizard-based workflow:**
```bash
curl -sSL https://install.piper-morgan.com | bash
# Interactive setup wizard
./piper-morgan start
```

**Development needed** - this issue's scope

#### Model 3: Hosted SaaS (Future, Not Alpha) 🔮
**Future production workflow:**
```bash
# Visit https://piper.example.com
# Sign up, onboard, start using
```

**Out of scope** - requires significant infrastructure

### Alpha Testing Waves

#### Wave 1: Technical Early Adopters (Weeks 1-4)
- **Target**: 10-20 developers, DevOps, technical PMs
- **Approach**: Current DIY model
- **Onboarding**: Enhanced README + Discord
- **Success**: 80%+ setup within 30 min

#### Wave 2: Guided Technical Users (Weeks 5-8)
- **Target**: 20-30 less technical users (PMs, analysts)
- **Approach**: New setup wizard (this issue)
- **Onboarding**: Video walkthrough + wizard
- **Success**: 90%+ setup within 5 min

#### Wave 3: End-User Testing (Weeks 9-12)
- **Target**: 30-50 non-technical users
- **Approach**: Polished wizard + documentation
- **Onboarding**: Full onboarding experience
- **Success**: 95%+ setup within 5 min

---

## Cost Model Analysis

### Alpha Phase (No Infrastructure Costs!)
```
Infrastructure: $0 (users self-host locally)
Development: ~24 hours (setup wizard, docs)
Support: $200-500/month (Discord/Slack community management)
User LLM Costs: $10-50/month (users pay directly)

Total Cost per User: $10-50/month (user pays)
Developer Time: ~3 days one-time investment
```

### Benefits
- ✅ Zero hosting costs during alpha
- ✅ Users maintain privacy (local deployment)
- ✅ Users control their LLM costs
- ✅ Validates product-market fit before infrastructure investment
- ✅ Smooth path to future hosted/SaaS model

---

## Time Estimate

### Phase 1A: Setup Wizard (8 hours)
- System checks: 2 hours
- API key collection & validation: 3 hours
- User account creation: 1 hour
- Integration: 2 hours

### Phase 1B: Health Checks (4 hours)
- Status command: 2 hours
- Health checks: 2 hours

### Phase 2: Preferences (6 hours)
- Preference storage: 2 hours
- CLI commands: 2 hours
- Validation: 2 hours

### Phase 3: Documentation (6 hours)
- Video: 3 hours
- Written docs: 2 hours
- FAQ: 1 hour

**Total Estimated Time**: 24 hours (~3 days)

---

## Priority & Dependencies

**Priority**: High - Blocking broader alpha testing

**Dependencies**:
- ✅ #228: Multi-user API key management (COMPLETE!)
- ✅ #227: JWT authentication (COMPLETE!)
- ✅ #229: Production database (COMPLETE!)

**Enables**:
- Alpha Wave 2: Guided technical users
- Alpha Wave 3: End-user testing
- Future: Hosted/SaaS deployment

**Epic**: CORE-USERS (Multi-user & Security)
**Milestone**: Alpha
**Sprint**: A7 (Recommended)

---

## Future Enhancements (Post-Alpha)

### Beta Phase
- Web-based setup wizard (alternative to CLI)
- One-click Docker install
- Automated update system
- Remote diagnostics

### Production Phase
- Managed hosting option
- Team/organization support
- SSO integration (GitHub, Google)
- Enterprise onboarding flows

---

## Notes

**Philosophy**: Keep it simple - this is alpha, not production. Focus on the critical path: getting users from zero to first successful interaction quickly.

**Key Insight**: 85% of infrastructure already exists! This issue is primarily UI/UX layer over solid foundations.

**Strategy**: Support both DIY (technical) and Guided (less technical) models in Alpha. Validate product-market fit before investing in hosted infrastructure.

---

**Related Issues**:
- #228: API Key Management (COMPLETE - provides infrastructure!)
- #248: Conversational Personality Preferences (A7 or Piper Education)
- Future: SaaS deployment automation

**Labels**: enhancement, component: cli, component: ui, onboarding, alpha-blocking
