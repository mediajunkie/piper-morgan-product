# Release Notes - v0.8.5.1

**Release Date**: January 31, 2026
**Type**: Patch Release (Bug Fixes)

---

## Summary

Fast-follow patch release addressing 14 alpha testing bugs discovered during post-MUX testing. All issues verified fixed and closed.

---

## Bug Fixes

### Authentication & Session (P0-P1)

| Issue | Title | Fix |
|-------|-------|-----|
| #723 | Logout not working | Cookie deletion on all logout paths |
| #724 | LLM API keys mismatch | User-scoped credential storage/retrieval |
| #730 | Username shows email prefix | Added username to JWT claims |
| #731 | Conversations not persisting | Auto-create conversation on first message |

### Portfolio & Projects (P0)

| Issue | Title | Fix |
|-------|-------|-----|
| #728 | Portfolio onboarding never saves | Multiple fixes: persistence, constraints, routing |
| #733 | Projects not saving during onboarding | Root cause fixes via #736, #737 |
| #736 | Projects unique constraint global | Migration: per-user uniqueness |
| #737 | Portfolio "yes" routes to small talk | Session creation in status handler |

### Navigation & UI (P2-P3)

| Issue | Title | Fix |
|-------|-------|-----|
| #720 | Race condition on first load | Log level change shows startup complete |
| #721 | Setup wizard missing stylesheet | tokens.css inclusion |
| #722 | First-time user routed to login | Auto-redirect to setup |
| #726 | Sidebar not showing current chat | last_activity_at update on turn |
| #727 | Text input triggers autofill | autocomplete="off" attribute |
| #729 | History button does nothing | HistorySidebar mount (via #735) |
| #732 | History trust-gated wrong level | Lowered from stage 2 to 1 |
| #735 | History sidebar never mounted | Full mount with API integration |

### Duplicate Closed

| Issue | Title | Resolution |
|-------|-------|------------|
| #725 | Chat refresh messages | Duplicate of #583 (fix intact) |

---

## Database Migrations

**New migration required**:
```bash
alembic upgrade head
```

Migration `3c85fd899ece_fix_projects_unique_constraint_736.py`:
- Changes `projects.name` constraint from global to per-user `(owner_id, name)`

---

## Files Modified

### Core Services
- `services/auth/jwt_service.py` - Username in JWT claims (#730)
- `services/auth/auth_middleware.py` - Request context injection (#734)
- `services/database/repositories.py` - last_activity_at update (#726)
- `services/intent_service/canonical_handlers.py` - Onboarding session fix (#737)
- `services/process/adapters.py` - captured_projects context (#728)
- `services/integrations/integration_config_service.py` - User-scoped config (#734)

### Web Routes
- `web/api/routes/auth.py` - Cookie deletion (#723)
- `web/api/routes/intent.py` - Auto-create conversation (#731)
- `web/api/routes/ui.py` - First-time user routing (#722)
- `web/api/routes/setup.py` - User context (#724)

### Templates
- `templates/home.html` - History sidebar mount (#735)
- `templates/setup.html` - tokens.css (#721)
- `templates/components/navigation.html` - Trust gate (#732)
- `templates/components/chat-inline.html` - autocomplete (#727)

### Infrastructure
- `main.py` - Log level for startup (#720)
- `alembic/versions/3c85fd899ece_...` - Migration (#736)

---

## Testing

- **Unit tests**: 5268 passed, 24 skipped
- **Template tests**: 638 passed
- **Onboarding tests**: 191 passed
- **History sidebar tests**: 56 passed

---

## Upgrade Instructions

1. Pull latest code:
   ```bash
   git pull origin production
   ```

2. Run database migration:
   ```bash
   alembic upgrade head
   ```

3. Restart server:
   ```bash
   python main.py
   ```

---

## Known Issues

See [ALPHA_KNOWN_ISSUES.md](../BETA_KNOWN_ISSUES.md) for current known issues.

---

**Full Changelog**: [v0.8.5...v0.8.5.1](https://github.com/mediajunkie/piper-morgan-product/compare/v0.8.5...v0.8.5.1)
