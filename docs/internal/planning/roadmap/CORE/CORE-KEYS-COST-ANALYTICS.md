# CORE-KEYS-COST-ANALYTICS: API Cost Tracking & Usage Analytics

## Context

Users need visibility into their API usage costs across different providers to budget effectively and optimize spending. Currently, costs are invisible until provider bills arrive.

**Parent Issue**: #228 (API Key Management)

---

## Problem Statement

**Current State**:
- Users don't know how much they're spending on API calls
- No visibility into which features/conversations cost the most
- Surprise bills from OpenAI/Anthropic at month-end
- No way to set budgets or spending alerts
- No comparison across providers

**User Pain Points**:
- "I got a $200 OpenAI bill and don't know why"
- "Which provider is more cost-effective for my usage?"
- "How can I reduce my API costs?"
- "Is this conversation going to be expensive?"
- "Can I set a monthly budget?"

---

## Proposed Solution

### 1. Usage Tracking
```python
class APIUsageTracker:
    """Track API usage per request"""

    async def log_api_call(
        self,
        user_id: str,
        provider: str,
        model: str,
        request_data: dict,
        response_data: dict,
        cost: float = None
    ):
        """Log API call with cost estimation"""

        usage = APIUsageLog(
            user_id=user_id,
            provider=provider,
            model=model,

            # Token counts
            prompt_tokens=response_data.get("usage", {}).get("prompt_tokens", 0),
            completion_tokens=response_data.get("usage", {}).get("completion_tokens", 0),
            total_tokens=response_data.get("usage", {}).get("total_tokens", 0),

            # Cost estimation
            estimated_cost=cost or self._estimate_cost(provider, model, response_data),

            # Context
            conversation_id=request_data.get("conversation_id"),
            feature=request_data.get("feature"),  # chat, research, code, etc.

            # Timestamp
            created_at=datetime.utcnow()
        )

        await self._store_usage(usage)
        await self._check_budget_alerts(user_id)
```

### 2. Cost Estimation
```python
class CostEstimator:
    """Estimate API costs based on usage"""

    # Pricing as of October 2025 (update regularly!)
    PRICING = {
        "openai": {
            "gpt-4": {
                "prompt": 0.03,      # per 1K tokens
                "completion": 0.06   # per 1K tokens
            },
            "gpt-4-turbo": {
                "prompt": 0.01,
                "completion": 0.03
            },
            "gpt-3.5-turbo": {
                "prompt": 0.0015,
                "completion": 0.002
            }
        },
        "anthropic": {
            "claude-3-opus": {
                "prompt": 0.015,
                "completion": 0.075
            },
            "claude-3-sonnet": {
                "prompt": 0.003,
                "completion": 0.015
            },
            "claude-3-haiku": {
                "prompt": 0.00025,
                "completion": 0.00125
            }
        }
    }

    def estimate_cost(
        self,
        provider: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int
    ) -> float:
        """Estimate cost for API call"""

        pricing = self.PRICING.get(provider, {}).get(model)
        if not pricing:
            return 0.0  # Unknown model

        prompt_cost = (prompt_tokens / 1000) * pricing["prompt"]
        completion_cost = (completion_tokens / 1000) * pricing["completion"]

        return round(prompt_cost + completion_cost, 4)
```

### 3. Budget Management
```python
class BudgetManager:
    """Manage user budgets and alerts"""

    async def set_budget(
        self,
        user_id: str,
        budget_type: str,  # daily, weekly, monthly
        amount: float,
        provider: str = None  # Optional: budget per provider
    ):
        """Set spending budget"""
        budget = Budget(
            user_id=user_id,
            budget_type=budget_type,
            amount=amount,
            provider=provider,
            alert_thresholds=[0.5, 0.75, 0.9, 1.0]  # 50%, 75%, 90%, 100%
        )
        await self._store_budget(budget)

    async def check_budget(
        self,
        user_id: str,
        budget_type: str
    ) -> BudgetStatus:
        """Check current budget usage"""
        budget = await self._get_budget(user_id, budget_type)
        usage = await self._get_usage(user_id, budget.period)

        percentage = (usage.total_cost / budget.amount) * 100

        return BudgetStatus(
            budget_amount=budget.amount,
            current_spending=usage.total_cost,
            percentage=percentage,
            alerts_triggered=self._check_thresholds(percentage, budget.alert_thresholds)
        )
```

### 4. Analytics Dashboard
```python
class UsageAnalytics:
    """Analyze API usage patterns"""

    async def get_usage_summary(
        self,
        user_id: str,
        period: str = "month"  # day, week, month, year
    ) -> UsageSummary:
        """Get usage summary for period"""

        logs = await self._get_usage_logs(user_id, period)

        return UsageSummary(
            total_cost=sum(log.estimated_cost for log in logs),
            total_requests=len(logs),
            total_tokens=sum(log.total_tokens for log in logs),

            # By provider
            by_provider=self._group_by(logs, "provider"),

            # By model
            by_model=self._group_by(logs, "model"),

            # By feature
            by_feature=self._group_by(logs, "feature"),

            # By conversation
            top_conversations=self._top_n(logs, "conversation_id", n=10),

            # Trends
            daily_costs=self._daily_breakdown(logs),

            # Cost efficiency
            cost_per_token=self._calculate_cost_per_token(logs),

            # Recommendations
            recommendations=self._generate_recommendations(logs)
        )
```

---

## Implementation Phases

### Phase 1: Usage Logging (3 hours)
- Create usage log database table
- Add logging to all LLM API calls
- Token counting
- Timestamp tracking

### Phase 2: Cost Estimation (4 hours)
- Provider pricing database
- Cost calculation logic
- Real-time cost display
- Historical cost accuracy

### Phase 3: Budget Management (4 hours)
- Budget configuration
- Alert thresholds
- Alert notifications
- Budget enforcement (optional)

### Phase 4: Analytics Dashboard (6 hours)
- Usage summaries
- Cost breakdowns
- Trend analysis
- Recommendations
- Export capabilities

### Phase 5: UI Integration (5 hours)
- Cost indicators in chat
- Budget widgets
- Usage dashboards
- Alerts/notifications

---

## Acceptance Criteria

### Core Functionality
- [ ] Log all API calls with token counts
- [ ] Estimate costs per call (±5% accuracy)
- [ ] Track spending per provider/model/feature
- [ ] Support daily/weekly/monthly budgets
- [ ] Send alerts at threshold levels

### User Experience
- [ ] Real-time cost display (per message)
- [ ] Clear budget status indicators
- [ ] Easy budget configuration
- [ ] Helpful cost optimization tips
- [ ] Export usage data (CSV/JSON)

### Accuracy
- [ ] Cost estimates within 5% of actual
- [ ] Pricing updates monthly
- [ ] Token counts match provider counts
- [ ] No missed API calls

### Performance
- [ ] Logging doesn't slow down API calls (<10ms overhead)
- [ ] Dashboard loads in <2 seconds
- [ ] Supports millions of usage logs
- [ ] Efficient queries for analytics

---

## Technical Design

### Database Schema
```sql
CREATE TABLE api_usage_logs (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    provider VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,

    -- Token usage
    prompt_tokens INTEGER NOT NULL,
    completion_tokens INTEGER NOT NULL,
    total_tokens INTEGER NOT NULL,

    -- Cost
    estimated_cost DECIMAL(10, 4) NOT NULL,

    -- Context
    conversation_id UUID,
    feature VARCHAR(50),  -- chat, research, code, etc.

    -- Timestamp
    created_at TIMESTAMP NOT NULL,

    -- Indexes
    INDEX idx_user_date (user_id, created_at),
    INDEX idx_provider (provider),
    INDEX idx_conversation (conversation_id)
);

CREATE TABLE user_budgets (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    budget_type VARCHAR(20) NOT NULL,  -- daily, weekly, monthly
    amount DECIMAL(10, 2) NOT NULL,
    provider VARCHAR(50),  -- NULL = all providers
    alert_thresholds DECIMAL(5, 2)[],  -- [0.5, 0.75, 0.9, 1.0]
    created_at TIMESTAMP NOT NULL,
    UNIQUE (user_id, budget_type, provider)
);

CREATE TABLE budget_alerts (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    budget_id UUID REFERENCES user_budgets(id),
    threshold DECIMAL(5, 2),  -- 0.75 = 75%
    triggered_at TIMESTAMP NOT NULL
);
```

### Cost Display Integration
```python
# In chat interface
async def send_message(message: str):
    # Call LLM
    response = await llm_service.generate(message)

    # Log usage
    await usage_tracker.log_api_call(
        user_id=current_user.id,
        provider="openai",
        model="gpt-4",
        request_data={"conversation_id": conversation.id},
        response_data=response
    )

    # Display with cost
    return {
        "message": response.text,
        "metadata": {
            "cost": response.cost,  # $0.0234
            "tokens": response.tokens,  # 782
            "model": "gpt-4"
        }
    }
```

---

## Example User Flows

### Flow 1: Real-Time Cost Display
```
User: "Write a comprehensive guide to machine learning"

Piper: [Response text...]

---
Cost: $0.12 | Tokens: 4,234 | Model: GPT-4
Today's spending: $2.34 / $10 daily budget (23%)
```

### Flow 2: Budget Alert
```
╔══════════════════════════════════════════════════════╗
║  ⚠️  BUDGET ALERT                                    ║
║                                                      ║
║  You've used 75% of your daily budget ($7.50/$10)   ║
║                                                      ║
║  Top expenses today:                                 ║
║  • Research feature: $3.45 (46%)                     ║
║  • Chat: $2.78 (37%)                                 ║
║  • Code generation: $1.27 (17%)                      ║
║                                                      ║
║  Tips to reduce costs:                               ║
║  → Use GPT-3.5 for simple queries (-80% cost)        ║
║  → Enable response caching (-30% cost)               ║
║                                                      ║
║  [Manage Budget]  [Dismiss]                          ║
╚══════════════════════════════════════════════════════╝
```

### Flow 3: Usage Dashboard
```bash
$ piper usage summary --month current

API Usage Summary (October 2025)

Total Cost: $234.56
Total Requests: 1,234
Total Tokens: 1.2M

By Provider:
┌───────────┬────────┬──────────┬────────┐
│ Provider  │ Cost   │ Requests │ Tokens │
├───────────┼────────┼──────────┼────────┤
│ OpenAI    │ $156.23│ 789      │ 780K   │
│ Anthropic │ $78.33 │ 445      │ 420K   │
└───────────┴────────┴──────────┴────────┘

By Model:
┌─────────────────┬────────┬──────────┐
│ Model           │ Cost   │ % of Total│
├─────────────────┼────────┼──────────┤
│ gpt-4           │ $89.12 │ 38%      │
│ claude-3-opus   │ $78.33 │ 33%      │
│ gpt-4-turbo     │ $45.67 │ 19%      │
│ gpt-3.5-turbo   │ $21.44 │ 9%       │
└─────────────────┴────────┴──────────┘

By Feature:
┌──────────────┬────────┬──────────┐
│ Feature      │ Cost   │ % of Total│
├──────────────┼────────┼──────────┤
│ Chat         │ $123.45│ 53%      │
│ Research     │ $67.89 │ 29%      │
│ Code Gen     │ $43.22 │ 18%      │
└──────────────┴────────┴──────────┘

Top 5 Most Expensive Conversations:
1. "ML System Design" - $12.34
2. "Code Review Project" - $8.90
3. "Research Report" - $7.56
4. "Architecture Planning" - $6.78
5. "Documentation Writing" - $5.43

Cost Optimization Tips:
✓ You're using GPT-3.5 for 15% of requests (great!)
→ Could save $45/month by using GPT-3.5 for more simple queries
→ Could save $23/month by enabling response caching
→ Could save $12/month by switching to Claude Haiku for code tasks

Monthly Trend:
Sept: $198.23
Oct:  $234.56 (+18%)
Projected Nov: $276.78
```

### Flow 4: Budget Configuration
```bash
$ piper budget set --daily 10 --weekly 50 --monthly 150

Budgets configured:
✓ Daily: $10
✓ Weekly: $50
✓ Monthly: $150

Alert thresholds:
- 50% ($5/$25/$75)
- 75% ($7.50/$37.50/$112.50)
- 90% ($9/$45/$135)
- 100% (limit reached)

Notifications will be sent via:
- In-app (always)
- Email (optional): user@example.com
- Slack (optional): @user
```

---

## Success Metrics

### User Awareness
- **Target**: 90% of users know their monthly spending
- **Measure**: User survey
- **Success**: >90% can accurately estimate costs

### Cost Optimization
- **Target**: 25% reduction in average per-user costs
- **Measure**: Before/after cost tracking
- **Success**: Users optimize based on visibility

### Budget Compliance
- **Target**: 85% of users stay within budget
- **Measure**: Users with budgets set
- **Success**: >85% don't exceed budgets

### Feature Adoption
- **Target**: 60% of users set budgets
- **Measure**: Users with active budgets
- **Success**: >60% adoption within 90 days

---

## Dependencies

**Required**:
- ✅ #228: API Key Management (key usage foundation)
- ✅ LLM service integration (token counting)
- ❌ Usage tracking infrastructure (new)
- ❌ Analytics database (new)

**Optional**:
- #249: Audit logging (usage audit trail)
- Email service (budget alert emails)
- Slack integration (budget alert DMs)

---

## Pricing Considerations

### Provider Pricing Updates
**Challenge**: Provider pricing changes frequently

**Solution**:
```python
class PricingUpdater:
    """Keep pricing data current"""

    async def update_pricing(self):
        """Fetch latest pricing from providers"""
        # Scrape OpenAI pricing page
        # Scrape Anthropic pricing page
        # Update database
        # Log changes

    # Run daily via cron
```

### Pricing Data Source
- OpenAI: https://openai.com/pricing
- Anthropic: https://www.anthropic.com/pricing
- Manual updates initially
- Automated scraping later
- User-submitted corrections

---

## Time Estimate

**Total**: 22 hours (~3 days)

**Breakdown**:
- Usage logging: 3 hours
- Cost estimation: 4 hours
- Budget management: 4 hours
- Analytics dashboard: 6 hours
- UI integration: 5 hours

---

## Priority

**Priority**: Medium (valuable feature, not critical)
**Milestone**: Beta (post-Alpha)
**Sprint**: A8 or later

**Rationale**: Valuable for user budgeting but not critical for Alpha. Add after core features complete. Users can track costs manually via provider dashboards initially.

---

## Related Issues

- #228: API Key Management (parent - provides foundation)
- #249: Audit Logging (usage should be logged)
- #218: Alpha Onboarding (usage tracking in setup)
- Future: Response caching (cost optimization)

**Epic**: CORE-USERS (Multi-user & Security)
**Labels**: enhancement, analytics, component: analytics, priority: medium
