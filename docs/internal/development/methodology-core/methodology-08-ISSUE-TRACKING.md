# Methodology 08: Issue Tracking Verification

**Status**: ✅ **PRODUCTION READY** - Systematic Protocol Established
**Created**: August 23, 2025
**Last Updated**: August 23, 2025

## 🎯 The Problem

**PM number reuse and fabrication causes tracking chaos**:
- Duplicate PM numbers across different issues
- Fabricated issue numbers that don't exist in GitHub
- Inconsistent tracking between GitHub, CSV, and backlog.md
- Loss of traceability and project history integrity

## 🛡️ The Protocol

### **CRITICAL RULES - NEVER VIOLATE**

1. **VERIFY existing PM numbers before creation**
2. **NEVER guess or fabricate issue numbers**
3. **CHECK GitHub, CSV, backlog alignment**
4. **CREATE sequential PM numbers only after verification**

## 🔍 Implementation Process

### **Step 1: GitHub Verification**
```bash
# Check all GitHub issues for PM numbers
gh issue list --state all --limit 100 | grep "PM-" | head -20

# Verify specific PM number exists
gh issue list --search "PM-XXX" --state all
```

### **Step 2: CSV File Verification**
```bash
# Check CSV file for current PM numbers
grep "PM-" docs/planning/pm-issues-status.csv

# Find highest PM number in CSV
grep "PM-" docs/planning/pm-issues-status.csv | sort -V | tail -5
```

### **Step 3: Backlog.md Verification**
```bash
# Check backlog.md for referenced PM numbers
grep "PM-" docs/planning/backlog.md

# Verify PM numbers mentioned in planning docs
grep -r "PM-" docs/planning/ --include="*.md"
```

### **Step 4: Sequential Number Assignment**
```bash
# Determine next valid PM number
# Example: If highest is PM-122, next is PM-123
# NEVER skip numbers or reuse existing ones
```

## 🚫 Anti-Patterns to Avoid

### **❌ NEVER DO THESE**
- **Fabricate PM numbers** without GitHub verification
- **Reuse existing PM numbers** for new issues
- **Skip sequential numbering** (PM-120, PM-125, PM-130)
- **Assume PM numbers exist** without checking
- **Create PM numbers** without cross-referencing all sources

### **✅ ALWAYS DO THESE**
- **Verify with GitHub first** - source of truth
- **Check CSV alignment** - local tracking
- **Verify backlog.md consistency** - planning alignment
- **Use next sequential number** after verification
- **Document verification process** in issue creation

## 🔧 Agent Requirements

### **Mandatory Protocol Compliance**
- **Must follow verification protocol** before any issue creation
- **Must cross-reference all tracking systems** (GitHub, CSV, backlog)
- **Must document issue creation rationale** with verification evidence
- **Must prevent duplicate PM numbers** through systematic checking

### **Verification Checklist**
- [ ] GitHub issues checked for existing PM numbers
- [ ] CSV file verified for current PM numbering
- [ ] Backlog.md checked for PM number references
- [ ] Next sequential number calculated and verified
- [ ] No conflicts detected across all sources

## 📊 Current State Verification

### **Last Verification**: August 23, 2025
**Status**: ✅ **VERIFIED** - No conflicts detected

**Current PM Numbers**:
- **Highest PM Number**: PM-122 (Issue #128)
- **Next Valid PM Number**: PM-123
- **GitHub Alignment**: ✅ Consistent
- **CSV Alignment**: ✅ Consistent
- **Backlog Alignment**: ✅ Consistent

## 🚀 Usage Examples

### **Creating New Issue with PM-123**
```bash
# 1. Verify current state
gh issue list --state all --limit 100 | grep "PM-" | tail -5

# 2. Check CSV for confirmation
grep "PM-" docs/planning/pm-issues-status.csv | sort -V | tail -3

# 3. Create issue with verified PM number
gh issue create --title "PM-123: [Issue Title]" --body "Description..."
```

### **Verifying Existing PM Number**
```bash
# Check if PM-120 exists and what it contains
gh issue list --search "PM-120" --state all

# Verify against CSV
grep "PM-120" docs/planning/pm-issues-status.csv
```

## 🔄 Integration Points

### **CLI Commands**
- `piper issues create` - Enforce verification protocol
- `piper issues verify` - Check PM number consistency
- `piper issues sync` - Synchronize all tracking systems

### **GitHub Actions**
- **Pre-commit hooks** - Verify PM number consistency
- **Issue creation validation** - Prevent duplicate PM numbers
- **Automated synchronization** - Keep all systems aligned

### **Agent Workflows**
- **Before issue creation** - Mandatory verification
- **During development** - Continuous consistency checking
- **After completion** - Update all tracking systems

## 📚 References

- **CLAUDE.md *(proposed; doc TBD)*** - Agent rules and requirements
- **[pm-issues-status.csv](../../planning/pm-issues-status.csv)** - Current PM number tracking
- **backlog.md *(proposed; doc TBD)*** - Planning and issue references
- **[GitHub Issues](https://github.com/mediajunkie/piper-morgan-product/issues)** - Source of truth

## 🎯 Success Metrics

- **Zero duplicate PM numbers** across all systems
- **100% verification compliance** before issue creation
- **Perfect alignment** between GitHub, CSV, and backlog
- **Systematic enforcement** of tracking protocol
- **Clear audit trail** for all PM number assignments

---

**Status**: ✅ **PROTOCOL ESTABLISHED** - Ready for systematic enforcement across all agent interactions.

**Next Action**: Implement `piper issue create` command with verification protocol enforcement.
