# Audit: #969 against bug_report_alpha.md

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Bug Description | ✅ | Two clear bugs with error messages |
| Steps to Reproduce | ✅ | Canonical retest runner reproduces (Q41, Q60) |
| Expected Behavior | ✅ | "user-friendly messages on error, not raw stack-trace text" |
| Actual Behavior | ✅ | Error messages documented |
| Environment | ⚠️ | Missing explicit version — add v0.8.6 post-M1 |
| Screenshots/Logs | ✅ | Error messages from retest |
| Severity | ⚠️ | Not marked — Minor (2 queries out of 61, non-blocking) |
| Additional Context | ✅ | M0 vs M1 comparison, #943 relationship |

## Fixes Applied

1. Environment: v0.8.6, post-M1, fresh canonical-test account
2. Severity: Minor — 2 queries, not blocking M2a gate, but real backend bugs

## Audit Result

All items ✅ after fixes. These are small, well-scoped bugs. Proceeding directly to investigation + fix (no full gameplan needed — the scope is two error handlers).
