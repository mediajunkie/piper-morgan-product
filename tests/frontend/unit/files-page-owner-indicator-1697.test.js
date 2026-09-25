/**
 * #1697 — templates/files.html rendered "Uploaded by: " with nothing after
 * the colon for every uploaded file. Root cause: GET /api/v1/files/list's
 * file-kind (`kind: "file"`) projection carried no `owner_id` field, so
 * isOwner(file) (`file.owner_id === window.currentUser.user_id`) always
 * evaluated false for a caller's OWN files — the ownerIndicator branch fired
 * when it should never have, and `escapeHtml(undefined)` renders as ''.
 *
 * Two-layer fix:
 * - web/api/routes/files.py: file-kind entries now carry `owner_id`
 *   (mirroring the artifact-kind projection, which already carried it —
 *   82d8b56/#1165 — for the identical isOwner() reason). Since GET /list is
 *   owner-scoped, this makes isOwner() correctly evaluate true for every
 *   returned file, so the indicator naturally never renders.
 * - templates/files.html: ownerIndicator additionally requires
 *   `file.owner_id` truthy (not just `!isOwner(file)`), so even a future/
 *   defensive gap in the API contract can never reproduce a dangling label.
 *
 * LAYER (m-43, named honestly): RUNTIME DOM via jsdom — same harness pattern
 * as files-page-xss.test.js (#1581): the page's inline <script> is extracted
 * from the real template source and evaluated, then renderFiles() is called
 * with API-response-shaped objects and the actual DOM output is inspected.
 * This is the layer that answers "does the browser ever show a dangling
 * label" — a Jinja-source string pin (tests/unit/templates/
 * test_files_xss_escaping_1581.py) only proves the JS text is present, not
 * what it renders given real data.
 *
 * Denominator (m-44): covers the ownerIndicator branch of renderFiles() only
 * (kind: 'file' and kind: 'artifact' rows, owned and — for completeness —
 * the hypothetical not-owned case). Does not re-cover the rest of the XSS
 * escaping sweep already owned by files-page-xss.test.js.
 */

const fs = require('fs');
const path = require('path');

const TEMPLATE = path.join(__dirname, '../../../templates/files.html');
// #1582: escapeHtml/escapeAttr are no longer defined inline in files.html —
// they're consolidated into this shared asset (loaded shell-wide by
// layouts/app_shell.html). Prepend its real source into the evaluated
// wrapper so the extracted inline script's calls to escapeHtml/escapeAttr
// resolve exactly as they do in the browser.
const ESCAPE_JS = fs.readFileSync(
  path.join(__dirname, '../../../web/static/js/escape.js'),
  'utf8'
);

function loadFilesPage() {
  const html = fs.readFileSync(TEMPLATE, 'utf8');
  const inline = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)]
    .map((m) => m[1])
    .join('\n');
  expect(inline).toContain('function renderFiles');
  const wrapped = `
    ${ESCAPE_JS}
    ${inline}
    return { renderFiles };
  `;
  // eslint-disable-next-line no-new-func
  return new Function(wrapped)();
}

describe('files.html renderFiles() — owner indicator (#1697)', () => {
  let page;

  beforeEach(() => {
    document.body.innerHTML = '<div id="files-container" class="files-grid"></div>';
    window.currentUser = { user_id: 'u1', username: 'xian', is_admin: false };
    global.ToastMessages = { success: jest.fn(), error: jest.fn(), info: jest.fn() };
    global.Dialog = { show: jest.fn(), confirm: jest.fn(), close: jest.fn() };
    page = loadFilesPage();
  });

  afterEach(() => {
    delete global.ToastMessages;
    delete global.Dialog;
    delete window.currentUser;
    delete window._allFiles;
  });

  const container = () => document.getElementById('files-container');

  // Post-#1697 API shape: file-kind entries now carry owner_id, matching the
  // caller's own id (GET /list is owner-scoped — services/database via
  // web/api/routes/files.py::list_files WHERE owner_id == current_user.sub).
  const ownFile = (overrides = {}) => ({
    file_id: 'f1',
    filename: 'notes.md',
    kind: 'file',
    owner_id: 'u1',
    size: 1234,
    uploaded_at: '2026-08-10T12:00:00Z',
    content_type: 'text/markdown',
    tags: [],
    ...overrides,
  });

  test('an owned file-kind entry (post-fix API shape) never shows "Uploaded by:"', () => {
    page.renderFiles([ownFile()]);
    expect(container().querySelector('.resource-owner')).toBeNull();
    expect(container().textContent).not.toContain('Uploaded by');
  });

  test('an owned artifact-kind entry never shows "Uploaded by:" either (unchanged behavior)', () => {
    page.renderFiles([ownFile({ file_id: 'a1', kind: 'artifact' })]);
    expect(container().querySelector('.resource-owner')).toBeNull();
    expect(container().textContent).not.toContain('Uploaded by');
  });

  test('regression guard: a file-kind entry MISSING owner_id (the pre-fix API shape) still never dangles the label', () => {
    // Reproduces exactly what GET /list used to send for kind: 'file' before
    // #1697 — no owner_id key at all. Without the template-side guard this
    // used to render "Uploaded by: " with nothing after the colon.
    const preFixShape = ownFile();
    delete preFixShape.owner_id;
    page.renderFiles([preFixShape]);
    const indicator = container().querySelector('.resource-owner');
    expect(indicator).toBeNull();
    expect(container().textContent).not.toContain('Uploaded by');
  });

  test('a genuinely not-owned row (owner_id present, different from the caller) shows a FILLED label, never a bare one', () => {
    page.renderFiles([ownFile({ owner_id: 'someone-else' })]);
    const indicator = container().querySelector('.resource-owner');
    expect(indicator).not.toBeNull();
    expect(indicator.textContent).toContain('Uploaded by:');
    expect(indicator.textContent.trim()).not.toBe('Uploaded by:');
    expect(indicator.textContent).toContain('someone-else');
  });
});
