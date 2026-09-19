---
type: methodology
title: Multi-Agent Coordinator Quick Start Guide
valid_from: "2025-09-21"
last_updated: "2025-09-21"
---

# Multi-Agent Coordinator Quick Start Guide

**Purpose**: Get Multi-Agent coordination working in 5 minutes
**Target**: Immediate operational deployment for development teams
**Status**: Ready for Production Use

## 🚀 **5-Minute Quick Start**

### **Step 1: Deploy Multi-Agent Coordinator (2 minutes)**

```bash
# Make sure you're in the project root
cd /path/to/piper-morgan

# Run the deployment script
./../../scripts/deploy_multi_agent_coordinator.sh
```

**What This Does**:

- ✅ Creates integration modules
- ✅ Updates orchestration engine
- ✅ Adds API endpoints
- ✅ Sets up performance monitoring
- ✅ Runs validation tests

### **Step 2: Start Your Application (1 minute)**

```bash
# Start the main application
python main.py

# Or if using a different method
python -m uvicorn main:app --host 0.0.0.0 --port 8001
```

### **Step 3: Test Multi-Agent Coordination (2 minutes)**

```bash
# Test 1: Health Check
curl "http://localhost:8001/api/orchestration/multi-agent/health"

# Test 2: Trigger Coordination
curl -X POST "http://localhost:8001/api/orchestration/multi-agent" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Build a complete user preference API with testing",
    "category": "EXECUTION",
    "action": "build_user_preference_api"
  }'

# Test 3: Check Performance Metrics
curl "http://localhost:8001/api/orchestration/multi-agent/metrics"
```

## 🎯 **What You Get Immediately**

### **1. Multi-Agent Coordination API**

- **Endpoint**: `POST /api/orchestration/multi-agent`
- **Purpose**: Trigger coordination for complex tasks
- **Response**: Workflow ID and task breakdown

### **2. Health Monitoring**

- **Endpoint**: `GET /api/orchestration/multi-agent/health`
- **Purpose**: Check coordination system health
- **Response**: Status, response time, target met

### **3. Performance Metrics**

- **Endpoint**: `GET /api/orchestration/multi-agent/metrics`
- **Purpose**: Track coordination performance over time
- **Response**: Historical data, success rates, averages

## 🔧 **How to Use in Your Workflow**

### **Scenario 1: Complex Feature Development**

```python
# Instead of doing everything yourself, trigger multi-agent coordination
import requests

def build_complex_feature():
    response = requests.post(
        "http://localhost:8001/api/orchestration/multi-agent",
        json={
            "message": "Build a complete user preference management system",
            "category": "EXECUTION",
            "action": "build_user_preference_system",
            "context": {
                "complexity": "high",
                "domains": ["backend", "frontend", "testing", "documentation"]
            }
        }
    )

    if response.status_code == 200:
        result = response.json()
        workflow_id = result["workflow_id"]
        print(f"Multi-agent coordination initiated! Workflow ID: {workflow_id}")
        return workflow_id
    else:
        print("Failed to initiate coordination")
        return None
```

### **Scenario 2: Session-Based Coordination**

```python
# In your conversation/session handling
async def handle_complex_request(session_context, user_message):
    # Check if this requires multi-agent coordination
    if _requires_multi_agent(user_message):
        intent = Intent(
            category="EXECUTION",
            action="handle_complex_request",
            original_message=user_message
        )

        # Trigger coordination
        workflow = await session_integration.trigger_multi_agent_coordination(
            session_context, intent
        )

        return f"Multi-agent coordination started! Workflow ID: {workflow['workflow_id']}"
    else:
        # Handle with single agent
        return await handle_simple_request(user_message)
```

### **Scenario 3: Automated Testing**

```python
# In your test suite
async def test_multi_agent_coordination():
    """Test that coordination meets performance targets"""

    start_time = time.time()

    response = await client.post(
        "/api/orchestration/multi-agent",
        json={
            "message": "Test coordination performance",
            "action": "test_performance"
        }
    )

    duration_ms = int((time.time() - start_time) * 1000)

    assert response.status_code == 200
    assert duration_ms < 1000, f"Coordination took {duration_ms}ms, target is <1000ms"

    result = response.json()
    assert "workflow_id" in result
    assert result["status"] == "initiated"
```

## 📊 **Performance Expectations**

### **Response Time Targets**

- **Coordination Trigger**: <1000ms ✅
- **Health Check**: <2000ms ✅
- **Workflow Creation**: <1500ms ✅

### **Success Rates**

- **API Endpoints**: 100% ✅
- **Workflow Creation**: >80% ✅
- **Integration Health**: 100% ✅

## 🔍 **Monitoring & Debugging**

### **Real-Time Health Check**

```bash
# Check system health
curl "http://localhost:8001/api/orchestration/multi-agent/health"

# Expected response:
{
  "status": "healthy",
  "response_time_ms": 150,
  "target_met": true,
  "last_check": "2025-08-20T23:48:00.123456"
}
```

### **Performance Metrics**

```bash
# Get comprehensive metrics
curl "http://localhost:8001/api/orchestration/multi-agent/metrics"

# Expected response:
{
  "total_checks": 25,
  "healthy_checks": 24,
  "health_rate": 0.96,
  "average_response_time_ms": 180,
  "performance_target_met_rate": 0.92,
  "last_check": "2025-08-20T23:48:00.123456"
}
```

### **Validation Script**

```bash
# Run comprehensive validation
./../../scripts/validate_multi_agent_operation.sh

# This will test all endpoints and generate a report
```

## 🚨 **Troubleshooting**

### **Common Issues & Solutions**

#### **Issue 1: "Service not running on port 8001"**

```bash
# Solution: Start the main application
python main.py
```

#### **Issue 2: "Import errors in integration modules"**

```bash
# Solution: Re-run deployment script
./../../scripts/deploy_multi_agent_coordinator.sh
```

#### **Issue 3: "Performance targets not met"**

```bash
# Check system resources
top
free -h

# Check coordination logs
tail -f logs/orchestration.log
```

#### **Issue 4: "API endpoints return 404"**

```bash
# Check if API routes are registered
grep -r "router.include_router" main.py

# Verify endpoint registration
curl -v "http://localhost:8001/api/orchestration/multi-agent/health"
```

## 📚 **Next Steps After Quick Start**

### **1. Team Training (30 minutes)**

- Review `docs/development/HOW_TO_USE_MULTI_AGENT.md`
- Practice with coordination templates
- Understand agent strengths and assignments

### **2. Workflow Integration (1 hour)**

- Integrate coordination into existing workflows
- Add coordination triggers to complex tasks
- Set up automated coordination for high-complexity requests

### **3. Performance Optimization (2 hours)**

- Monitor metrics over time
- Identify bottlenecks
- Optimize coordination algorithms

### **4. Advanced Features (4 hours)**

- Custom coordination patterns
- Agent-specific task handlers
- GitHub integration for coordination tracking

## 🎉 **Success Indicators**

### **Immediate Success (5 minutes)**

- ✅ Deployment script runs without errors
- ✅ Application starts successfully
- ✅ Health check returns "healthy"
- ✅ Coordination trigger creates workflow

### **Short-term Success (1 hour)**

- ✅ Team can trigger coordination manually
- ✅ Performance targets consistently met
- ✅ Workflows execute successfully
- ✅ Integration with existing systems working

### **Long-term Success (1 week)**

- ✅ Multi-agent coordination is part of daily workflow
- ✅ Performance metrics show improvement
- ✅ Team productivity increased
- ✅ Complex tasks completed faster

## 📞 **Support & Resources**

### **Documentation**

- **Integration Guide**: `docs/./MULTI_AGENT_INTEGRATION_GUIDE.md`
- **Usage Guide**: `docs/development/HOW_TO_USE_MULTI_AGENT.md`
- **Templates**: `docs/development/multi-agent-templates.md`

### **Scripts**

- **Deployment**: `./../../scripts/deploy_multi_agent_coordinator.sh`
- **Validation**: `./../../scripts/validate_multi_agent_operation.sh`

### **API Endpoints**

- **Base URL**: `http://localhost:8001`
- **Coordination**: `/api/orchestration/multi-agent`
- **Health**: `/api/orchestration/multi-agent/health`
- **Metrics**: `/api/orchestration/multi-agent/metrics`

---

**Status**: Ready for immediate deployment and use
**Next**: Run the deployment script and start coordinating! 🚀
