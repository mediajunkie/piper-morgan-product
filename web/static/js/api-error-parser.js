/**
 * api-error-parser.js
 *
 * Shared helper for parsing FastAPI error response detail across integration
 * settings UIs. FastAPI returns two distinct shapes:
 *
 *   1. Validation errors (HTTP 422):
 *      { "detail": [ { "loc": [...], "msg": "...", "type": "..." }, ... ] }
 *
 *   2. Explicit HTTPException with string detail (HTTP 4xx/5xx):
 *      { "detail": "Invalid API key — Notion API returned 401" }
 *
 * Pre-fix code path was:
 *
 *      throw new Error(error.detail || 'Failed to save');
 *
 * When detail is the array shape, `new Error([...])` stringifies the array
 * to "[object Object]" and the toast shows that literal — hiding the real
 * error from the user AND masking actual backend bugs (#1080 verification
 * surfaced this; the Form() annotation bug at services/web/api/routes/
 * settings_integrations.py was hidden behind "[object Object]" toast text).
 *
 * Filed as #1119 FRONTEND-ERROR-RENDER.
 */

/**
 * Parse a FastAPI-shape error.detail into a human-readable string.
 *
 * @param {*} detail - The error.detail value from a parsed JSON response.
 *                     Can be a string (HTTPException), an array of validation
 *                     errors (422), an object, undefined, or null.
 * @param {string} fallback - Fallback message if detail is missing or unparseable.
 * @returns {string} Human-readable error message safe to display in a toast.
 */
function parseApiDetail(detail, fallback) {
  if (typeof detail === 'string' && detail.trim()) {
    return detail;
  }
  if (Array.isArray(detail)) {
    // FastAPI 422 structured detail — array of { loc, msg, type } objects
    const parts = detail.map((e) => {
      const loc = Array.isArray(e.loc) ? e.loc.filter(Boolean).join('.') : '';
      const msg = e.msg || 'invalid';
      return loc ? `${loc}: ${msg}` : msg;
    });
    if (parts.length > 0) {
      return `Validation error — ${parts.join('; ')}`;
    }
  }
  if (detail && typeof detail === 'object' && detail.msg) {
    return detail.msg;
  }
  return fallback || 'Request failed';
}
