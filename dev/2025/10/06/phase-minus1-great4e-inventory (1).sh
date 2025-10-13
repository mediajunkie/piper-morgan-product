#!/bin/bash
# GREAT-4E Phase -1: Complete Coverage Inventory
# Apply lessons from GREAT-4D - enumerate EVERYTHING before starting

echo "=== GREAT-4E Phase -1: Coverage Inventory ==="
echo "Date: $(date)"
echo ""

echo "1. VERIFY ALL 13 INTENT CATEGORIES EXIST:"
echo "-------------------------------------------"
grep "class IntentCategory" services/shared_types.py
echo ""
echo "Count categories:"
grep -o "^    [A-Z_]*" services/shared_types.py | wc -l
echo "(Must be 13)"
echo ""

echo "2. IDENTIFY ALL ENTRY POINT INTERFACES:"
echo "----------------------------------------"
echo "Web API:"
ls -la web/app.py 2>/dev/null && echo "  ✓ Web API exists" || echo "  ✗ Web API not found"
ls -la web/routes/ 2>/dev/null && echo "  ✓ Routes directory exists" || echo "  ✗ Routes not found"
echo ""

echo "Slack Integration:"
find services -name "*slack*" -type f 2>/dev/null | head -5
echo ""

echo "CLI:"
ls -la cli/ 2>/dev/null && echo "  ✓ CLI exists" || echo "  ✗ CLI not found"
ls -la main.py 2>/dev/null && echo "  ✓ main.py exists" || echo "  ✗ main.py not found"
echo ""

echo "Direct Service:"
ls -la services/intent/intent_service.py 2>/dev/null && echo "  ✓ IntentService exists" || echo "  ✗ IntentService not found"
echo ""

echo "3. COUNT EXISTING INTENT TESTS:"
echo "--------------------------------"
echo "Intent test files:"
find tests -name "*intent*" -type f 2>/dev/null | wc -l
echo ""
echo "Specific test files:"
find tests -name "*intent*" -type f 2>/dev/null
echo ""

echo "4. CHECK EXISTING DOCUMENTATION:"
echo "--------------------------------"
echo "Intent guides:"
ls -la docs/guides/intent*.md 2>/dev/null || echo "  No intent guides found"
echo ""

echo "ADR-032:"
ls -la docs/adrs/adr-032* 2>/dev/null || echo "  ADR-032 not found"
ls -la docs/architecture/adr-032* 2>/dev/null || echo "  ADR-032 not found (alt location)"
echo ""

echo "README intent section:"
grep -n "intent\|Intent" README.md 2>/dev/null | head -3 || echo "  No intent section found"
echo ""

echo "5. VERIFY HANDLER IMPLEMENTATION FOR ALL 13:"
echo "---------------------------------------------"
echo "Checking services/intent/intent_service.py for handlers:"
for category in TEMPORAL STATUS PRIORITY IDENTITY GUIDANCE EXECUTION ANALYSIS SYNTHESIS STRATEGY LEARNING UNKNOWN QUERY CONVERSATION; do
    handler_count=$(grep -c "_handle.*${category,,}" services/intent/intent_service.py 2>/dev/null || echo 0)
    if [ "$handler_count" -gt 0 ]; then
        echo "  ✓ $category: handler found"
    else
        echo "  ? $category: checking alternate pattern..."
        # Check for the category in routing
        alt_count=$(grep -c "IntentCategory.${category}" services/intent/intent_service.py 2>/dev/null || echo 0)
        if [ "$alt_count" -gt 0 ]; then
            echo "    ✓ $category: routing found"
        else
            echo "    ✗ $category: NO HANDLER OR ROUTING"
        fi
    fi
done
echo ""

echo "6. CREATE COVERAGE MATRIX:"
echo "--------------------------"
echo "Category      | Handler | Web | Slack | CLI | Direct | Test | Docs"
echo "------------- | ------- | --- | ----- | --- | ------ | ---- | ----"

for category in TEMPORAL STATUS PRIORITY IDENTITY GUIDANCE EXECUTION ANALYSIS SYNTHESIS STRATEGY LEARNING UNKNOWN QUERY CONVERSATION; do
    # Check handler
    handler="?"
    grep -q "_handle.*${category,,}\|IntentCategory.${category}" services/intent/intent_service.py 2>/dev/null && handler="✓"

    # Check tests
    test="?"
    grep -q "${category}" tests/intent/*.py 2>/dev/null && test="✓"

    printf "%-13s | %-7s | %-3s | %-5s | %-3s | %-6s | %-4s | %-4s\n" \
        "$category" "$handler" "?" "?" "?" "?" "$test" "?"
done
echo ""

echo "7. CALCULATE BASELINE COVERAGE:"
echo "--------------------------------"
echo "Categories with handlers: $(grep -c "_handle.*intent\|IntentCategory" services/intent/intent_service.py)/13"
echo "Interfaces identified: TBD (need PM confirmation)"
echo "Existing tests: $(find tests -name "*intent*" -type f 2>/dev/null | wc -l)"
echo "Existing docs: $(ls -1 docs/guides/intent*.md 2>/dev/null | wc -l)"
echo ""

echo "8. QUESTIONS FOR PM:"
echo "--------------------"
echo "1. Which interfaces actually exist and should be tested?"
echo "   - Web API: ?"
echo "   - Slack: ?"
echo "   - CLI: ?"
echo "   - Direct: ?"
echo ""
echo "2. Are all 13 categories required for validation?"
echo "   - Or can some be skipped/deferred?"
echo ""
echo "3. Load testing infrastructure available?"
echo "   - locust/k6/other tool?"
echo "   - Test environment accessible?"
echo ""
echo "4. CI/CD pipeline integration:"
echo "   - GitHub Actions? Jenkins? Other?"
echo "   - Access to configure?"
echo ""

echo "=== Phase -1 Complete ==="
echo "Review findings with PM before creating gameplan"
