#!/bin/bash
# Create missing __init__.py files in services/ subdirectories
# Created: 2025-11-04
# Issue: Test infrastructure failures due to missing __init__.py

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 Scanning for missing __init__.py files in services/..."
echo ""

# Directories that SHOULD have __init__.py (contain Python code)
DIRS=(
    "services/analysis"
    "services/analytics"
    "services/api/health"
    "services/debugging"
    "services/ethics"
    "services/health"
    "services/infrastructure/errors"
    "services/infrastructure/extractors"
    "services/infrastructure/logging"
    "services/infrastructure/monitoring"
    "services/integrations/mcp"
    "services/intelligence/spatial"
    "services/observability"
    "services/security"
    "services/session"
    "services/todo"
    "services/ui_messages"
    "services/utils"
)

CREATED_COUNT=0
EXISTED_COUNT=0

for dir in "${DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo -e "${YELLOW}⏭️  $dir does not exist (skipping)${NC}"
        continue
    fi

    if [ ! -f "$dir/__init__.py" ]; then
        MODULE_NAME=$(basename "$dir")
        echo "# ${MODULE_NAME} module" > "$dir/__init__.py"
        echo -e "${GREEN}✅ Created $dir/__init__.py${NC}"
        ((CREATED_COUNT++))
    else
        echo "⏭️  $dir/__init__.py already exists"
        ((EXISTED_COUNT++))
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ Complete: Created $CREATED_COUNT files, $EXISTED_COUNT already existed${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "  1. Review created files: git status"
echo "  2. Run tests: ./scripts/run_tests.sh fast"
echo "  3. Commit: git add services/*/__init__.py && git commit"
echo ""
