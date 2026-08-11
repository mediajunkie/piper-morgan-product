# CLI Commands User Guide

**Complete command-line interface reference for Piper Morgan**
**Updated**: August 24, 2025
**Status**: Production-Ready CLI Documentation

Master Piper Morgan's powerful command-line interface for lightning-fast issue management, intelligent project analysis, and seamless workflow automation.

---

## 🚀 Quick Start

### New to Piper CLI?

Jump right in with these essential commands:

```bash
# Get project health overview
python main.py issues status

# Intelligent issue triage
python main.py issues triage

# Morning standup with context
python main.py standup
```

---

## 📋 Complete Command Reference

### Issue Intelligence Commands

Transform your issue management with AI-powered analysis and intelligent prioritization.

#### `piper issues status`

**Purpose**: Get comprehensive project health overview with actionable insights

**Usage**:

```bash
python main.py issues status [--project PROJECT_NAME]
```

**What you get**:

- ✅ **Current Status**: Open/closed issue counts with completion rates
- ✅ **Recent Activity**: Last 7 days of issue activity
- ✅ **Performance Insights**: Resolution patterns and velocity metrics
- ✅ **Actionable Recommendations**: Next steps based on your data

**Example Output**:

```
============================================================
  📊 Issue Status Overview
============================================================

📋 Current Status
----------------------------------------
ℹ️  Open Issues: 12
ℹ️  Closed Issues: 85
ℹ️  Total Issues: 97
ℹ️  Completion Rate: 87.6%

✅ High completion rate - excellent issue management!

📋 Recent Activity (Last 7 Days)
----------------------------------------
ℹ️  New Issues: 3
ℹ️  Resolved Issues: 8

🟢 Closed #127: PM-121 Canonical Query Integration
🟢 Closed #125: Weekly Docs Audit
🟡 Open #128: PM-122 FTUX Wizard Implementation

💡 Recommendations
----------------------------------------
✅ High recent resolution rate - excellent progress!
  • Maintain current momentum
  • Document successful patterns
```

#### `piper issues triage`

**Purpose**: AI-powered issue prioritization with intelligent analysis

**Usage**:

```bash
python main.py issues triage [--project PROJECT_NAME] [--limit NUMBER]
```

**What you get**:

- 🔥 **Smart Prioritization**: AI-driven priority scoring (High/Medium/Low)
- 📊 **Triage Analysis**: Detailed reasoning for each priority assignment
- ⚡ **Action Items**: Immediate next steps for high-priority issues
- 🧠 **Learning Integration**: System learns from your triage decisions

**Example Output**:

```
============================================================
  🔍 Issue Triage & Prioritization
============================================================

📋 Analyzing 10 Open Issues
----------------------------------------

📋 🚨 High Priority Issues
----------------------------------------
#128: PM-122 FTUX Wizard Implementation
   🚨 High priority: PM-122 FTUX Wizard Implementation - Requires immediate attention
   Assignee: mediajunkie

📋 ⚡ Medium Priority Issues
----------------------------------------
#120: PM-120 Persistent Context Database Integration
   ⚡ Medium priority: PM-120 Persistent Context Database Integration - Plan for next sprint

📋 Triage Summary & Action Items
----------------------------------------
✅ High Priority: 1 issues
ℹ️  Medium Priority: 2 issues
ℹ️  Low Priority: 7 issues

📋 🚨 Immediate Actions Required
----------------------------------------
• Review high-priority issues within 24 hours
• Assign team members to critical issues
• Update stakeholders on blocker status
```

**Options**:

- `--project`: Filter to specific project repository
- `--limit`: Maximum number of issues to analyze (default: 10)

#### `piper issues patterns`

**Purpose**: Discover patterns and insights across your issue management

**Usage**:

```bash
python main.py issues patterns [--feature FEATURE_NAME]
```

**What you get**:

- 🔍 **Pattern Discovery**: Learned patterns from your workflow
- 📈 **Confidence Scores**: How reliable each pattern is (0.0-1.0)
- 🔄 **Cross-Feature Learning**: Patterns shared between issues and standups
- 💡 **Actionable Insights**: Recommendations based on discovered patterns

**Example Output**:

```
============================================================
  🔍 Issue Pattern Discovery
============================================================

📋 Patterns from All Features
----------------------------------------
ℹ️  No patterns discovered yet

📋 🚀 Getting Started
----------------------------------------
• Run 'piper issues triage' to start learning
• Use 'piper standup' to build Morning Standup patterns
• Patterns will appear here as you use the system

📋 Pattern Discovery Summary
----------------------------------------
✅ Total Patterns: 0
ℹ️  Pattern Types: 0

💡 Pattern-Based Recommendations
----------------------------------------
ℹ️  Cross-Feature Learning Opportunities:
  • Look for patterns that could be shared between features
  • Identify common workflows for standardization
  • Consider creating shared pattern libraries
```

**Options**:

- `--feature`: Focus on specific feature patterns (`issue_intelligence`, `morning_standup`)

### Morning Standup Commands

Enhanced with Issue Intelligence integration for comprehensive daily standup context.

#### `piper standup`

**Purpose**: Intelligent morning standup with issue context and priority awareness

**Usage**:

```bash
python main.py standup
```

**What you get**:

- 📋 **Daily Focus**: Your top priorities for today
- 🔄 **Issue Context**: Recent issue activity relevant to your work
- ⚡ **Smart Recommendations**: AI-driven suggestions based on patterns
- 🧠 **Learning Integration**: Improves over time with your usage patterns

---

## 🛠 Advanced Usage

### Command Combinations

**Daily Workflow Pattern**:

```bash
# Start your day with comprehensive context
python main.py standup

# Check project health
python main.py issues status

# Triage new issues when needed
python main.py issues triage --limit 5

# Discover patterns weekly
python main.py issues patterns
```

### Project-Specific Workflows

**Focus on specific repository**:

```bash
# All commands support project filtering
python main.py issues status --project "mediajunkie/piper-morgan-product"
python main.py issues triage --project "myorg/myrepo" --limit 20
```

### Integration with Learning System

The CLI includes an advanced learning system that:

- ✅ **Learns from Usage**: Every triage decision improves future recommendations
- ✅ **Cross-Feature Patterns**: Issue patterns enhance standup context
- ✅ **Confidence Tracking**: Pattern reliability scores help you trust recommendations
- ✅ **Usage Analytics**: Track which patterns work best for your workflow

---

## 📊 Understanding Output

### Priority Levels

**🚨 High Priority** (Red):

- Contains keywords: urgent, critical, blocker, security, production
- Requires immediate attention (within 24 hours)
- Usually impacts users or blocks other work

**⚡ Medium Priority** (Yellow):

- Contains keywords: important, enhancement, performance
- Plan for next sprint or iteration
- Improves system but not immediately critical

**📝 Low Priority** (Blue):

- General improvements, documentation, nice-to-have features
- Review quarterly or batch with similar work
- Good for learning or filling gaps

### Learning Confidence Scores

**🟢 High Confidence (0.8-1.0)**:

- Pattern ready for production use
- Based on significant usage data
- Can be trusted for automated decisions

**🟡 Medium Confidence (0.4-0.7)**:

- Pattern shows promise but needs more validation
- Monitor and provide feedback
- Use with human oversight

**🔴 Low Confidence (0.0-0.4)**:

- Experimental pattern, use with caution
- Needs more data to become reliable
- Good for exploration and testing

---

## 🔧 Troubleshooting

### Common Issues

**❌ "No issues found"**:

- Check GitHub token configuration
- Verify repository access permissions
- Try specifying project with `--project` flag

**❌ "API rate limit exceeded"**:

- Wait for rate limit reset (usually 1 hour)
- Use `--limit` to reduce API calls
- Check GitHub API usage in your account

**❌ "Learning loop not available"**:

- This is normal on first use
- Patterns develop after using triage commands
- Run `piper issues triage` a few times to build data

**❌ "Permission denied"**:

- Ensure GitHub token has repository access
- Check GITHUB_TOKEN environment variable
- Verify repository name spelling

### Getting Help

```bash
# Get help for any command
python main.py issues --help
python main.py issues triage --help
python main.py standup --help

# Check system status
python main.py issues status
```

### Performance Tips

**Faster Commands**:

- Use `--limit 5` for quick triage checks
- Focus on specific projects with `--project`
- Run `patterns` command weekly, not daily

**Better Results**:

- Use triage command regularly to build learning data
- Provide specific project context when possible
- Review and adjust priority classifications for better learning

---

## 🔗 Related Documentation

### User Guides

- [Getting Started with Conversational AI](./getting-started-conversational-ai.md) - Natural language interaction
- [Understanding References](./understanding-anaphoric-references.md) - "that issue" patterns
- [Conversation Memory Guide](./conversation-memory-guide.md) - Context preservation

### Technical Resources

- [Issue Intelligence Feature Documentation](../features/issue-intelligence.md) - Complete feature reference
- [Canonical Queries Architecture](../../../internal/architecture/canonical-queries-architecture.md) - Technical architecture
- [CLI Development Guide](../../../internal/development/tools/CLI_STANDUP_IMPLEMENTATION.md) - For developers

### Integration Guides

- [GitHub Integration Setup](../../../internal/operations/production/github-integration-setup.md) - Configuration guide
- [Multi-Agent Coordination](../../../internal/development/methodology-core/MULTI_AGENT_INTEGRATION_GUIDE.md) - Advanced workflows

---

## 🎯 Success Indicators

### Personal Productivity

You're successfully using Piper CLI when:

- ✅ Daily standup takes <2 minutes with full context
- ✅ Issue triage decisions feel confident and consistent
- ✅ Priority classifications match your intuitive assessment
- ✅ Patterns emerge that reflect your actual workflow
- ✅ Context switches between projects feel seamless

### Team Adoption

Your team is getting value when:

- ✅ Issue resolution velocity increases measurably
- ✅ Priority discussions decrease (clear AI-driven consensus)
- ✅ New team members onboard faster with pattern guidance
- ✅ Cross-project pattern sharing improves consistency
- ✅ Morning standups are data-driven and actionable

---

## 🚀 Quick Reference

### Daily Commands

```bash
python main.py standup                    # Start your day
python main.py issues status             # Project health check
```

### Weekly Commands

```bash
python main.py issues triage             # Priority review
python main.py issues patterns           # Pattern insights
```

### Project-Specific

```bash
python main.py issues status --project "repo-name"
python main.py issues triage --project "repo-name" --limit 10
```

### Learning & Analytics

```bash
python main.py issues patterns                          # All patterns
python main.py issues patterns --feature issue_intelligence  # Specific feature
```

---

## 📝 Notion Integration CLI

Transform your Notion workspace management with powerful command-line tools for knowledge management and content creation.

### `notion status`

**Purpose**: Check Notion integration status and configuration

**Usage**:

```bash
python cli/commands/notion.py status
```

**What you get**:

- ✅ **Connection Status**: API key configuration and workspace access
- 📊 **Workspace Info**: Workspace name and base URL
- 🔑 **Authentication**: API key status and permissions
- 🌐 **API Status**: Notion API connectivity verification

**Example Output**:

```
✅ Connected to Notion workspace
📊 Workspace: Piper Morgan Development
🔑 API Key: Configured
🌐 Base URL: https://api.notion.com/v1
```

### `notion pages`

**Purpose**: List pages in your Notion workspace with metadata

**Usage**:

```bash
python cli/commands/notion.py pages
```

**What you get**:

- 📚 **Page Listing**: Up to 20 pages with titles, IDs, and URLs
- 🔍 **Metadata**: Page properties and access information
- 📱 **Direct Links**: Clickable URLs for immediate access
- 📊 **Workspace Overview**: Complete content inventory

**Example Output**:

```
Found 15 pages:
1. Project Requirements
   ID: abc12345...
   URL: https://notion.so/abc12345

2. Q4 Planning
   ID: def67890...
   URL: https://notion.so/def67890
```

### `notion search`

**Purpose**: Search across your entire Notion workspace

**Usage**:

```bash
python cli/commands/notion.py search --query "search term"
```

**What you get**:

- 🔍 **Full-Text Search**: Comprehensive content discovery
- 📊 **Relevant Results**: AI-powered search relevance
- 🏷️ **Content Types**: Pages, databases, and blocks
- ⚡ **Fast Results**: Optimized search performance

**Example Output**:

```
Search results for "project requirements":
• Project Requirements Document (Page)
• Q4 Planning Database (Database)
• Technical Specifications (Page)
```

### `notion create`

**Purpose**: Create new Notion pages with smart parent selection

**Usage**:

```bash
# Create with automatic parent selection
python cli/commands/notion.py create "Page Title"

# Create with specific parent
python cli/commands/notion.py create "Page Title" --parent-id "parent-page-id"
```

**What you get**:

- ✨ **Smart Creation**: Automatic parent page selection
- 🔗 **Hierarchy Management**: Proper page organization
- 📝 **Rich Content**: Full Notion page capabilities
- ✅ **Success Feedback**: Page details and direct links

**Example Output**:

```
✅ Page created successfully!
Title: Q4 2025 Planning
ID: xyz98765
URL: https://notion.so/xyz98765
```

### `notion test`

**Purpose**: Test Notion API connection and permissions

**Usage**:

```bash
python cli/commands/notion.py test
```

**What you get**:

- 🔗 **Connection Test**: Live API connectivity verification
- 🔐 **Permission Check**: Workspace access validation
- ⚡ **Performance**: Response time measurement
- 🛠️ **Troubleshooting**: Clear error messages if issues

---

### `publish`

**Purpose**: Publish markdown content to Notion with proper URL feedback and error handling

**Usage**:

```bash
# Publish markdown file to Notion
python cli/commands/publish.py publish README.md --to notion --location parent-page-id

# Publish with explicit format (default: markdown)
python cli/commands/publish.py publish docs/guide.md --to notion --location parent-id --format markdown
```

**What you get**:

- ✅ **Success Confirmation**: Clear publication status
- 🔗 **Direct URL**: Clickable link to published Notion page
- ⚠️ **Conversion Notes**: Warnings for unsupported markdown features
- 🛠️ **Error Guidance**: Actionable options when parent locations are invalid

**Example Output**:

```bash
📤 Publishing README.md to notion...
✅ Published successfully!
📄 Page ID: 25e11704-d8bf-8107-917c-cadf0cc9ac5a
🔗 URL: https://www.notion.so/README-25e11704d8bf8107917ccadf0cc9ac5a
⚠️ Conversion notes:
  - Complex table converted to simple format
  - Code blocks preserved with syntax highlighting
```

**Error Handling Example**:

```bash
📤 Publishing test.md to notion...
❌ Cannot create page under parent 'invalid-id': Parent page not found
Options:
  1. Use 'piper notion pages' to see available parents
  2. Specify different parent with --location
  3. Check parent page permissions in Notion
```

**Requirements**:
- Valid NOTION_API_KEY in .env file
- Parent page must be shared with your Notion integration
- Markdown file must exist and be readable

---

## 🔗 Related Documentation

### User Guides

- [Getting Started with Conversational AI](./getting-started-conversational-ai.md) - Natural language interaction
- [Understanding References](./understanding-anaphoric-references.md) - "that issue" patterns
- [Conversation Memory Guide](./conversation-memory-guide.md) - Context preservation

---

**Ready to transform your workflow?**

**[🚀 Start with Morning Standup](../../../internal/development/tools/MORNING_STANDUP_MVP_GUIDE.md)**

**[📊 Master Issue Intelligence](../features/issue-intelligence.md)**

**[🔄 Understand the Learning System](../../../internal/architecture/canonical-queries-architecture.md)**

---

**Last Updated**: August 28, 2025
**Version**: Issue Intelligence v1.0 + Notion CLI v1.0 Complete
**Status**: Production-Ready CLI Documentation with Notion Integration
