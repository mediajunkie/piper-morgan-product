# TODO Triage: 14 Untracked TODOs in Service Code

**From**: docs
**To**: lead
**Date**: 2026-04-02
**Re**: Quarterly maintenance finding (#938)
**Response-Requested**: no
**Priority**: low

---

During the Q2 quarterly maintenance sweep, I found 14 TODO comments in `services/` without associated issue numbers. These represent untracked work.

**Files affected:**

| File | TODO |
|------|------|
| `services/database/models.py:1845` | Re-enable after UniversalList migration |
| `services/intent_service/canonical_handlers.py:4455` | Replace with database-backed repository |
| `services/intent_service/llm_classifier_factory.py:55` | Wire BoundaryEnforcer |
| `services/analysis/document_analyzer.py:74` | Move key_points to top-level key_findings |
| `services/security/key_leak_detector.py:92` | Implement HIBP integration |
| `services/security/user_api_key_service.py:76` | Re-enable after alpha onboarding |
| `services/auth/user_service.py:116` | Use proper database storage in production |
| `services/learning/context_matcher.py:82` | Parse time specifications |
| `services/scheduler/standup_reminder_job.py:148` | Query UserPreferenceManager |

(Plus 5 references to `TODO_QUERY_PATTERNS` / `TODO_COMPLETE_PATTERNS` in `pre_classifier.py` which are variable names, not action items.)

**Ask**: When convenient, triage these — either file issues for the real ones or remove stale TODOs. Per project convention, discovered work should be tracked.

Also noted: 4 directories missing `__init__.py`:
- `services/integrations/demo/tests`
- `services/integrations/jira`
- `services/integrations/slack/tests`
- `services/orchestration-engine`
