# Link Maintenance Guide

**Last Updated**: October 1, 2025
**Owner**: DevOps Team
**Related**: `.github/workflows/link-checker.yml`, `.github/workflows/weekly-docs-audit.yml`

---

## Overview

This guide describes the automated and manual processes for maintaining links in Piper Morgan documentation to prevent link rot and ensure documentation reliability.

## Automated Link Checking

### CI Workflow

Our documentation uses **Lychee**, a fast Rust-based link checker that runs automatically via GitHub Actions.

**Workflow File**: `.github/workflows/link-checker.yml`

**Triggers**:
- Push to `main` or `develop` branches (docs changes)
- Pull requests targeting `main` (docs changes)
- Weekly schedule: Sundays at 2 AM UTC
- Manual dispatch via GitHub Actions UI

**What It Checks**:
- All markdown files in `docs/**/*.md`
- All root-level markdown files (`*.md`)
- Internal relative links (`.md` files)
- External HTTP/HTTPS links

**Exclusions**:
- Localhost URLs (`127.0.0.1`, `localhost`)
- Private network addresses
- Social media sites (LinkedIn, Twitter, Facebook, Instagram)
- Email addresses (mailto:)

### Reading Link Check Results

**In GitHub Actions**:
1. Navigate to Actions tab → Link Checker workflow
2. View job summary for high-level results
3. Download `link-checker-results` artifact for detailed report
4. Check workflow logs for verbose output

**In Pull Requests**:
- Link checker automatically comments on PRs with results
- Shows broken links found in changed files
- Blocks merge if critical links are broken (configurable)

**Artifact Storage**:
- Results stored for 30 days
- Downloadable from workflow run page
- Includes `link-checker-results.md` and `lychee.log`

## Manual Link Checking

### Weekly Audit Process

Part of the FLY-AUDIT workflow (Mondays at 9 AM PT):

```bash
# Manual link check command
/agent Check for broken links in docs/**/*.md
```

**When to Check Manually**:
- Before major documentation releases
- After bulk documentation updates
- When investigating reported broken links
- When adding new external dependencies

### Local Testing

**Option 1: Using lychee (recommended)**
```bash
# Install lychee
brew install lychee  # macOS
# or
cargo install lychee  # via Rust

# Check all docs
lychee "docs/**/*.md" "*.md" --verbose

# Quick check (internal links only)
lychee "docs/**/*.md" "*.md" --offline

# Check specific file
lychee docs/troubleshooting.md
```

**Option 2: Using markdown-link-check**
```bash
# Install
npm install -g markdown-link-check

# Check single file
markdown-link-check docs/troubleshooting.md

# Check all markdown files
find docs -name "*.md" -exec markdown-link-check {} \;
```

## Common Issues and Fixes

### Issue 1: Broken Internal Links

**Symptom**:
```
❌ docs/guide.md → docs/reference/api.md [404 Not Found]
```

**Diagnosis**:
```bash
# Verify file exists
ls -la docs/reference/api.md

# Search for the file
find docs -name "api.md"
```

**Solutions**:
1. File moved → Update link to new location
2. File deleted → Remove link or link to alternative
3. Typo in path → Fix the link path
4. Wrong relative path → Check from link's directory

**Fix Example**:
```markdown
# Before (broken)
[API Reference](reference/api.md)

# After (fixed)
API Reference *(proposed; doc TBD)*
```

### Issue 2: Broken External Links

**Symptom**:
```
❌ https://example.com/docs → [404 Not Found]
```

**Diagnosis**:
```bash
# Test the link
curl -I https://example.com/docs

# Check for redirects
curl -L -I https://example.com/docs
```

**Solutions**:
1. Permanent redirect (301/308) → Update to new URL
2. Temporary unavailable (5xx) → Wait and recheck
3. Dead link (404) → Find replacement or use Web Archive
4. SSL/certificate issues → Check domain validity

**Using Web Archive**:
```bash
# Find archived version
https://web.archive.org/web/*/https://example.com/docs
```

### Issue 3: False Positives

**Symptom**: Link works in browser but fails in checker

**Common Causes**:
- Rate limiting (429 errors)
- Bot detection / User-Agent blocking
- Requires authentication
- JavaScript-rendered content
- Geo-restrictions

**Solutions**:
```yaml
# Add to workflow exclusions
--exclude="problematic-domain.com"

# Or add to .lycheeignore
problematic-domain.com/*
```

### Issue 4: Link Anchors

**Symptom**: Anchor links (`#section`) fail validation

**Examples**:
```markdown
# Internal anchor
[Jump to section](#troubleshooting)

# External anchor
[FastAPI Docs](https://fastapi.tiangolo.com/tutorial/#first-steps)
```

**Lychee Behavior**:
- Internal anchors: Validated if `--check-anchors` enabled
- External anchors: Usually ignored (expensive to check)

**Fix**:
```bash
# Local anchor validation
lychee docs/file.md --check-anchors
```

## Maintenance Workflow

### 1. Detection

**Automated** (preferred):
- CI workflow fails on PR
- Weekly scheduled check creates alert
- GitHub Actions sends notification

**Manual**:
- User reports broken link
- Developer notices during work
- Weekly audit checklist

### 2. Triage

**Priority Levels**:
- **P0 Critical**: Homepage, README, getting started guides
- **P1 High**: Architecture docs, ADRs, API references
- **P2 Medium**: How-to guides, tutorials, examples
- **P3 Low**: Legacy docs, archived content, supplementary links

**Response Times**:
- P0: Fix within 24 hours
- P1: Fix within 1 week
- P2: Fix within 2 weeks
- P3: Fix on next docs cleanup sprint

### 3. Fix Implementation

**Branch Naming**:
```bash
git checkout -b docs/fix-broken-links-YYYYMMDD
```

**Commit Message Format**:
```
docs: Fix broken links in [section]

- Update [file]: [old link] → [new link]
- Remove dead link to [resource] (no longer available)
- Add Web Archive link for [historical reference]

Related: #[issue number]
```

**Testing**:
```bash
# Test locally before pushing
lychee "docs/**/*.md" --verbose

# Or test specific changed files
lychee docs/changed-file.md
```

### 4. Verification

**PR Checklist**:
- [ ] Link checker passes in CI
- [ ] No new broken links introduced
- [ ] Updated links actually work (manual browser check)
- [ ] Related documentation updated if needed
- [ ] Changelog updated for significant changes

**Post-Merge**:
- Monitor link checker results for 48 hours
- Verify in production documentation
- Update issue tracker

## Best Practices

### For Documentation Authors

**DO**:
- ✅ Use relative paths for internal links
- ✅ Test links before committing
- ✅ Prefer stable URLs (docs.example.com vs blog posts)
- ✅ Use version-specific links when appropriate
- ✅ Include link context in text (not just "click here")
- ✅ Archive important external content locally if possible

**DON'T**:
- ❌ Link to localhost URLs in committed docs
- ❌ Use absolute paths for internal docs
- ❌ Link to unstable/temporary URLs
- ❌ Forget to update links when moving files
- ❌ Link to private/authenticated resources
- ❌ Use URL shorteners (hide destination, can expire)

### Link Longevity Tips

**Internal Links**:
```markdown
# Good - Relative from current location
[Pattern Catalog](../internal/architecture/current/patterns/README.md)

# Avoid - Absolute paths (fragile to repo moves)
[Pattern Catalog](/docs/internal/architecture/current/patterns/README.md)
```

**External Links**:
```markdown
# Good - Official versioned docs
[FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

# Risky - Blog posts, temporary content
[Some Tutorial](https://randomblog.com/fastapi-guide)
```

**API Documentation**:
```markdown
# Good - Points to live API docs (localhost example docs)
See API documentation at http://localhost:8001/docs

# Better - Note that it's a local example
When running locally, see API docs at http://localhost:8001/docs
```

### Archive Important Content

For critical external resources:

1. **Save to docs**: Copy essential content to local docs
2. **Web Archive**: Submit to https://web.archive.org
3. **Git submodule**: For large external docs
4. **PDF export**: For one-time reference material

## Tools and Resources

### Lychee Link Checker
- **Website**: https://lychee.cli.rs/
- **GitHub**: https://github.com/lycheeverse/lychee
- **Action**: https://github.com/lycheeverse/lychee-action
- **Docs**: https://lychee.cli.rs/usage/cli/

### Markdown Link Check
- **GitHub**: https://github.com/tcort/markdown-link-check
- **NPM**: https://www.npmjs.com/package/markdown-link-check

### Web Archive
- **Wayback Machine**: https://web.archive.org/
- **Save Page**: https://web.archive.org/save/

### Browser Extensions
- **Check My Links** (Chrome): Validates links on web pages
- **Link Checker** (Firefox): Similar functionality

## Configuration Reference

### Lychee Configuration

**Command-line flags** (from `.github/workflows/link-checker.yml`):
```bash
--verbose              # Detailed output
--no-progress         # No progress bar (CI-friendly)
--exclude-loopback    # Skip localhost
--exclude-private     # Skip private IPs
--exclude-mail        # Skip mailto: links
--max-redirects=10    # Follow up to 10 redirects
--timeout=30          # 30-second timeout per link
--retry-wait-time=5   # Wait 5s between retries
--max-retries=3       # Retry failed links 3 times
--accept=200,204,301,302,307,308,429  # Accepted status codes
```

**Exclusion patterns** (can add to workflow):
```yaml
--exclude="domain.com"           # Exclude entire domain
--exclude="domain.com/path/*"    # Exclude path pattern
--exclude-file=.lycheeignore     # Use ignore file
```

### .lycheeignore File

Create `.lycheeignore` in repository root:
```
# Social media (already excluded in workflow)
linkedin.com/*
twitter.com/*

# Known false positives
example-site-with-bot-detection.com/*

# Development URLs
localhost/*
127.0.0.1/*

# Requires authentication
internal-wiki.company.com/*
```

## Metrics and Monitoring

### Key Metrics

Track in weekly audits:
- **Total links**: Count of all links in documentation
- **Broken links**: Number of 404/dead links
- **Link health rate**: (Working links / Total links) × 100
- **Mean time to fix**: Average time from detection to fix
- **Recurrence rate**: Links that break repeatedly

### Health Targets

- **Link health rate**: ≥ 95%
- **Broken links**: ≤ 5 total
- **P0 mean time to fix**: < 24 hours
- **Weekly check success rate**: 100%

### Reporting

**Weekly Report** (automated in FLY-AUDIT):
```markdown
## Link Health Report - [Date]

- Total links: [count]
- Broken links: [count] ([percentage]%)
- Links fixed this week: [count]
- New broken links: [count]
- Link health rate: [percentage]%

### Action Items
- [ ] Fix [file] - [link description]
- [ ] Update [section] external references
```

## Troubleshooting

### Workflow Fails but Links Work Locally

**Possible causes**:
1. CI has different network access
2. Rate limiting from many parallel checks
3. Different lychee version

**Debug**:
```bash
# Match CI lychee version
lychee --version

# Run with same flags as CI
lychee "docs/**/*.md" --verbose --exclude-loopback --exclude-private
```

### Too Many False Positives

**Solutions**:
1. Add exclusions to workflow
2. Create `.lycheeignore` file
3. Increase timeout/retries
4. Check for bot detection

### Link Checker Takes Too Long

**Optimizations**:
```yaml
# Check only changed files in PR
- name: Get changed files
  uses: tj-actions/changed-files@v40
  with:
    files: |
      **/*.md

# Pass only changed files to lychee
--paths="${{ steps.changed-files.outputs.all_changed_files }}"
```

### Need to Skip Validation

**Emergency bypass** (use sparingly):
```yaml
# In workflow, add condition
if: github.event_name != 'push' || contains(github.event.head_commit.message, '[skip-link-check]')
```

**Commit message**:
```
docs: Update content [skip-link-check]

Temporary bypass for known external service outage.
Will revalidate after service restoration.
```

## Support

### Getting Help

1. **Check workflow logs**: Detailed error messages in Actions
2. **Search issues**: Check if others hit same problem
3. **Create issue**: Use template "Documentation - Broken Links"
4. **Ask in Slack**: #documentation channel
5. **Weekly audit**: Discuss in Monday FLY-AUDIT issue

### Reporting Problems

**Issue template**:
```markdown
## Broken Link Report

**File**: docs/path/to/file.md
**Line**: [line number]
**Link**: [broken URL]
**Error**: [error message from lychee]

**Expected**: Link should point to [description]
**Actual**: Returns [404/timeout/etc]

**Context**: [why this link is important]
**Priority**: [P0/P1/P2/P3]

**Attempted fixes**: [what you tried]
```

---

## Appendix: Link Health Status

**Last Full Check**: October 1, 2025

### Current State (Post-GREAT-2E Phase 1)
- **Total links**: 1,173
- **Broken links**: 0 (3 fixed in troubleshooting.md)
- **Link health rate**: 100%
- **Files with links**: 175 of 540 docs (32%)

### Recent Changes
- **2025-10-01**: Fixed 3 broken links in troubleshooting.md
- **2025-10-01**: Implemented automated link checker workflow
- **2025-09-30**: All 41 ADRs verified current (updated within 7 days)

### Known Issues
- None currently

---

**Document Control**:
- Version: 1.0
- Created: October 1, 2025
- Last Review: October 1, 2025
- Next Review: October 8, 2025 (weekly)
- Owner: DevOps Team
- Approver: Technical Lead
