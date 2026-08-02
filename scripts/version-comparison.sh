#!/bin/bash

echo "🔍 DETAILED VERSION COMPARISON REPORT"
echo "===================================="
echo ""

# Function to compare files
compare_file() {
    local file="$1"
    local current_file="$file"
    local recovered_file="COMPLETE-RECOVERY/$file"

    echo "📄 Comparing: $file"
    echo "----------------------------------------"

    if [[ -f "$current_file" && -f "$recovered_file" ]]; then
        current_lines=$(wc -l < "$current_file")
        recovered_lines=$(wc -l < "$recovered_file")

        echo "Current version: $current_lines lines"
        echo "Recovered version: $recovered_lines lines"

        # Show actual differences
        echo ""
        echo "🔄 Differences (current vs recovered):"
        diff -u "$current_file" "$recovered_file" | head -50
        echo ""

        if [[ $current_lines -gt $recovered_lines ]]; then
            echo "⚠️  Current version is LONGER - may contain newer changes"
        elif [[ $recovered_lines -gt $current_lines ]]; then
            echo "⚠️  Recovered version is LONGER - may contain lost content"
        else
            echo "✅ Same length - checking content differences"
        fi
    else
        echo "❌ One or both files missing"
    fi

    echo ""
    echo "=========================================="
    echo ""
}

# Compare critical files
echo "Comparing critical files that showed mismatches:"
echo ""

compare_file "CLAUDE.md"

echo "🎯 RECOMMENDATION:"
echo "1. Review the diff output above"
echo "2. Determine which version has the latest intended changes"
echo "3. Manually merge the best content from both versions"
echo "4. The recovered files represent your work AS OF the stash creation"
echo "5. Current files represent the state AFTER merge conflicts and resets"
