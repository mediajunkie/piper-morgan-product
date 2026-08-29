# CORE-KEYS-COST-TRACKING: Integrate Cost Analytics with Real API Call Tracking

**Sprint**: TBD (A8 or MVP)
**Priority**: Medium
**Effort**: 45-60 minutes
**Impact**: High (cost visibility & budget control)

---

## Problem

Issue #253 (CORE-KEYS-COST-ANALYTICS) created comprehensive cost analytics infrastructure:

```python
# What exists now:
analytics = CostAnalytics()
analytics.set_budget('openai', monthly_budget=100.00)
report = analytics.get_usage_report('openai')
# Returns: usage stats, budget status, cost per call

# What's missing:
# - Integration with actual API calls
# - Automatic cost tracking
# - Real token counting
# - Live budget monitoring
```

Currently, cost analytics provides **structure** but doesn't track actual API calls. There's no automatic integration with LLM service calls.

**Result**: Users can set budgets but have no visibility into actual spending.

---

## Proposed Solution

Integrate cost analytics with the LLM service layer so that:
1. **Every API call** is automatically tracked
2. **Token counts** are captured from responses
3. **Costs calculated** using current pricing
4. **Budgets monitored** in real-time
5. **Alerts triggered** when approaching limits

---

## Current LLM Service Architecture

### Existing LLM Adapters

```python
# services/llm/anthropic_adapter.py

class AnthropicAdapter(BaseLLMAdapter):
    """Adapter for Anthropic Claude API"""

    async def generate(
        self,
        prompt: str,
        model: str = "claude-sonnet-4-20250514",
        **kwargs
    ) -> LLMResponse:
        """Generate completion"""

        response = await self.client.messages.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=kwargs.get('max_tokens', 4096)
        )

        # Currently NO cost tracking happens here

        return LLMResponse(
            content=response.content[0].text,
            model=model,
            usage=response.usage  # Token counts available!
        )
```

**Status**: ✅ Token data available, ⏳ Not tracked

---

## Proposed Integration

### 1. Automatic Cost Tracking in LLM Adapters

```python
# Enhanced LLM adapter with cost tracking

class AnthropicAdapter(BaseLLMAdapter):
    """Adapter with integrated cost tracking"""

    def __init__(self):
        super().__init__()
        self.cost_tracker = CostTracker()  # New!

    async def generate(
        self,
        prompt: str,
        model: str = "claude-sonnet-4-20250514",
        user_id: str = None,  # New parameter!
        **kwargs
    ) -> LLMResponse:
        """Generate completion with automatic cost tracking"""

        # Make API call
        start_time = datetime.utcnow()
        response = await self.client.messages.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=kwargs.get('max_tokens', 4096)
        )
        end_time = datetime.utcnow()

        # Extract usage data
        usage = Usage(
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            total_tokens=response.usage.input_tokens + response.usage.output_tokens
        )

        # Track cost automatically!
        await self.cost_tracker.record_api_call(
            provider='anthropic',
            model=model,
            user_id=user_id,
            usage=usage,
            start_time=start_time,
            end_time=end_time
        )

        return LLMResponse(
            content=response.content[0].text,
            model=model,
            usage=usage
        )
```

---

### 2. CostTracker Service

```python
# services/security/cost_tracker.py

class CostTracker:
    """Track API costs in real-time"""

    # Current pricing (as of Oct 2025)
    PRICING = {
        'anthropic': {
            'claude-sonnet-4-20250514': {
                'input': 3.00 / 1_000_000,   # $3 per 1M input tokens
                'output': 15.00 / 1_000_000  # $15 per 1M output tokens
            }
        },
        'openai': {
            'gpt-4-turbo': {
                'input': 10.00 / 1_000_000,
                'output': 30.00 / 1_000_000
            }
        }
    }

    async def record_api_call(
        self,
        provider: str,
        model: str,
        user_id: str,
        usage: Usage,
        start_time: datetime,
        end_time: datetime
    ):
        """Record an API call with cost calculation"""

        # Calculate cost
        cost = self._calculate_cost(provider, model, usage)

        # Store in database
        call_record = APICallRecord(
            id=uuid4(),
            user_id=user_id,
            provider=provider,
            model=model,
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            total_tokens=usage.total_tokens,
            cost=cost,
            start_time=start_time,
            end_time=end_time,
            duration=(end_time - start_time).total_seconds()
        )

        await self._store_record(call_record)

        # Check budget limits
        await self._check_budget_limits(user_id, provider, cost)

        return call_record

    def _calculate_cost(self, provider: str, model: str, usage: Usage) -> float:
        """Calculate cost for API call"""
        pricing = self.PRICING.get(provider, {}).get(model)

        if not pricing:
            logger.warning(f"No pricing data for {provider}/{model}")
            return 0.0

        input_cost = usage.input_tokens * pricing['input']
        output_cost = usage.output_tokens * pricing['output']
        total_cost = input_cost + output_cost

        return round(total_cost, 6)  # Round to 6 decimal places

    async def _check_budget_limits(
        self,
        user_id: str,
        provider: str,
        call_cost: float
    ):
        """Check if budget limits approached/exceeded"""

        # Get user's budget
        budget = await self._get_user_budget(user_id, provider)
        if not budget:
            return

        # Get current month's spending
        current_spending = await self._get_monthly_spending(user_id, provider)
        new_total = current_spending + call_cost

        # Check thresholds
        if new_total >= budget.limit:
            await self._trigger_alert(
                user_id,
                provider,
                AlertType.BUDGET_EXCEEDED,
                current=new_total,
                limit=budget.limit
            )
        elif new_total >= budget.limit * 0.8:
            await self._trigger_alert(
                user_id,
                provider,
                AlertType.BUDGET_WARNING,
                current=new_total,
                limit=budget.limit
            )
```

---

### 3. Database Schema for API Calls

```sql
CREATE TABLE api_call_records (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    provider VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,
    input_tokens INTEGER NOT NULL,
    output_tokens INTEGER NOT NULL,
    total_tokens INTEGER NOT NULL,
    cost DECIMAL(10, 6) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    duration FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),

    INDEX idx_user_provider (user_id, provider),
    INDEX idx_created_at (created_at)
);

-- For fast monthly aggregations
CREATE INDEX idx_monthly_spending
ON api_call_records(user_id, provider, EXTRACT(YEAR FROM created_at), EXTRACT(MONTH FROM created_at));
```

---

### 4. Budget Monitoring & Alerts

```python
class BudgetMonitor:
    """Monitor budgets and trigger alerts"""

    async def check_all_budgets(self, user_id: str):
        """Check all provider budgets for user"""
        alerts = []

        for provider in ['anthropic', 'openai', 'gemini']:
            alert = await self._check_provider_budget(user_id, provider)
            if alert:
                alerts.append(alert)

        return alerts

    async def _check_provider_budget(
        self,
        user_id: str,
        provider: str
    ) -> BudgetAlert | None:
        """Check single provider budget"""

        # Get budget
        budget = await self._get_budget(user_id, provider)
        if not budget:
            return None

        # Get current month spending
        spending = await self._get_monthly_spending(user_id, provider)

        # Calculate percentage used
        pct_used = (spending / budget.limit) * 100

        # Determine alert level
        if pct_used >= 100:
            return BudgetAlert(
                provider=provider,
                level='critical',
                message=f'Budget exceeded: ${spending:.2f} / ${budget.limit:.2f}',
                pct_used=pct_used
            )
        elif pct_used >= 80:
            return BudgetAlert(
                provider=provider,
                level='warning',
                message=f'Budget warning: ${spending:.2f} / ${budget.limit:.2f} ({pct_used:.0f}% used)',
                pct_used=pct_used
            )

        return None
```

---

### 5. Enhanced Cost Analytics Integration

```python
# services/security/cost_analytics.py (from #253)

class CostAnalytics:
    """Enhanced with real API call data"""

    async def get_usage_report(
        self,
        provider: str,
        user_id: str,
        period: str = 'month'
    ) -> UsageReport:
        """Get usage report with real data"""

        # Query actual API call records
        calls = await self._query_api_calls(user_id, provider, period)

        # Aggregate statistics
        total_calls = len(calls)
        total_tokens = sum(c.total_tokens for c in calls)
        total_cost = sum(c.cost for c in calls)

        # Calculate averages
        avg_tokens_per_call = total_tokens / total_calls if total_calls > 0 else 0
        avg_cost_per_call = total_cost / total_calls if total_calls > 0 else 0

        # Get budget info
        budget = await self._get_budget(user_id, provider)
        pct_used = (total_cost / budget.limit * 100) if budget else 0

        return UsageReport(
            provider=provider,
            period=period,
            total_calls=total_calls,
            total_tokens=total_tokens,
            total_cost=total_cost,
            avg_tokens_per_call=avg_tokens_per_call,
            avg_cost_per_call=avg_cost_per_call,
            budget=budget.limit if budget else None,
            budget_used_pct=pct_used,
            cost_by_model=self._aggregate_by_model(calls),
            calls_over_time=self._aggregate_by_day(calls)
        )
```

---

## Status Checker Integration

```python
# Enhanced status output (from #255)

async def show_cost_status():
    """Show cost and budget status"""

    print("\n=== API Cost Status ===\n")

    monitor = BudgetMonitor()
    tracker = CostTracker()

    for provider in ['anthropic', 'openai']:
        # Get this month's spending
        spending = await tracker.get_monthly_spending(user_id, provider)
        budget = await tracker.get_budget(user_id, provider)

        if budget:
            pct = (spending / budget.limit) * 100
            status = "🔴" if pct >= 100 else "⚠️" if pct >= 80 else "✅"

            print(f"{status} {provider.capitalize()}:")
            print(f"   Spent: ${spending:.2f} / ${budget.limit:.2f} ({pct:.0f}%)")

            # Show recent usage
            calls_today = await tracker.get_calls_today(user_id, provider)
            print(f"   Today: {len(calls_today)} calls, ${sum(c.cost for c in calls_today):.2f}")
        else:
            print(f"ℹ️  {provider.capitalize()}: No budget set")

        print()
```

---

## Acceptance Criteria

### Functional Requirements
- [ ] All LLM API calls automatically tracked
- [ ] Token counts captured from responses
- [ ] Costs calculated using current pricing
- [ ] Budget limits monitored in real-time
- [ ] Alerts triggered at 80% and 100% thresholds
- [ ] Database stores all call records

### Analytics Requirements
- [ ] Usage reports show real data
- [ ] Cost breakdowns by model
- [ ] Time-series cost analysis
- [ ] Average cost per call calculated
- [ ] Budget utilization percentage

### User Experience
- [ ] Status checker shows current spending
- [ ] Clear budget alerts with actionable info
- [ ] Historical cost trends visible
- [ ] Easy budget adjustment

---

## Testing

### Unit Tests

```python
async def test_cost_tracking_anthropic():
    """Test cost tracking for Anthropic calls"""
    adapter = AnthropicAdapter()

    # Make API call
    response = await adapter.generate(
        "Hello world",
        user_id=test_user_id
    )

    # Verify cost recorded
    calls = await get_api_calls(test_user_id, 'anthropic')
    assert len(calls) == 1
    assert calls[0].cost > 0
    assert calls[0].input_tokens > 0
    assert calls[0].output_tokens > 0

async def test_budget_warning_trigger():
    """Test budget warning at 80% threshold"""
    # Set budget
    await set_budget(test_user_id, 'anthropic', limit=10.00)

    # Simulate spending $8.50 (85%)
    await simulate_api_calls(test_user_id, 'anthropic', total_cost=8.50)

    # Check alerts
    alerts = await monitor.check_all_budgets(test_user_id)
    assert len(alerts) == 1
    assert alerts[0].level == 'warning'

async def test_cost_calculation_accuracy():
    """Test cost calculation matches pricing"""
    usage = Usage(input_tokens=1000, output_tokens=500)
    cost = tracker._calculate_cost('anthropic', 'claude-sonnet-4-20250514', usage)

    # $3/1M input * 1000 = $0.003
    # $15/1M output * 500 = $0.0075
    # Total: $0.0105
    assert cost == 0.010500
```

### Integration Tests

```python
async def test_end_to_end_cost_tracking():
    """Test complete flow from API call to report"""
    # Set budget
    await set_budget(test_user_id, 'anthropic', limit=100.00)

    # Make several API calls
    for i in range(10):
        await orchestrator.process(f"Test message {i}", test_user_id)

    # Get usage report
    report = await analytics.get_usage_report('anthropic', test_user_id)

    # Verify report accuracy
    assert report.total_calls == 10
    assert report.total_cost > 0
    assert report.budget_used_pct < 100
```

---

## Performance Considerations

### Database Efficiency

```python
# Efficient monthly spending query
async def _get_monthly_spending(self, user_id: str, provider: str) -> float:
    """Get current month's spending with optimized query"""

    query = """
        SELECT COALESCE(SUM(cost), 0) as total
        FROM api_call_records
        WHERE user_id = :user_id
          AND provider = :provider
          AND EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM CURRENT_DATE)
          AND EXTRACT(MONTH FROM created_at) = EXTRACT(MONTH FROM CURRENT_DATE)
    """

    result = await self.db.fetch_one(query, {'user_id': user_id, 'provider': provider})
    return float(result['total'])
```

**Index usage**: Query uses `idx_monthly_spending` for fast aggregation

---

### Caching Strategy

```python
class CostTracker:
    """With caching for frequent queries"""

    def __init__(self):
        self._spending_cache = {}  # {user_id: {provider: {month: spending}}}
        self._cache_ttl = 300  # 5 minutes

    async def get_monthly_spending(self, user_id: str, provider: str) -> float:
        """Get monthly spending with caching"""
        cache_key = f"{user_id}:{provider}:{datetime.utcnow().strftime('%Y-%m')}"

        # Check cache
        if cache_key in self._spending_cache:
            cached = self._spending_cache[cache_key]
            if (datetime.utcnow() - cached['timestamp']).seconds < self._cache_ttl:
                return cached['spending']

        # Query database
        spending = await self._query_monthly_spending(user_id, provider)

        # Update cache
        self._spending_cache[cache_key] = {
            'spending': spending,
            'timestamp': datetime.utcnow()
        }

        return spending
```

---

## Related Issues

- **#253: CORE-KEYS-COST-ANALYTICS** - Created cost analytics infrastructure
- **#255: CORE-UX-STATUS-USER** - Status checker integration point
- **Anthropic/OpenAI adapters** - LLM service integration points

---

## Future Enhancements

### Phase 2
- Cost optimization suggestions
- Model recommendation based on cost/performance
- Automatic model downgrade when approaching budget

### Phase 3 (MVP)
- Cost forecasting (predict monthly total)
- Department/team cost allocation
- Custom cost reports and exports
- Webhook notifications for budget alerts

---

## Success Metrics

- 100% of API calls tracked
- <1% cost calculation error rate
- Budget alerts delivered <1 minute after threshold
- Users report high confidence in cost visibility

---

**Sprint**: TBD
**Milestone**: TBD (A8 or MVP)
**Labels**: enhancement, analytics, cost-tracking, integration
**Estimated Effort**: 45-60 minutes
