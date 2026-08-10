/**
 * #1581 [SECURITY] — stored-XSS regression for templates/files.html.
 * Same class and same harness pattern as #1578 (todos-page-xss.test.js).
 *
 * LAYER (named honestly): RUNTIME DOM, via jsdom. The page builds its cards in
 * an inline <script> template literal; this suite extracts that script from
 * the template source, evaluates it, and renders HOSTILE files into a real
 * jsdom container. It proves the escaping works when executed — element
 * injection, ATTRIBUTE injection (the page's old DOM-based escapeHtml did not
 * escape quotes, so value=""/aria-label sites were quote-breakable), onclick
 * contents — not merely that the source text contains escape calls (that
 * source-level half lives in
 * tests/unit/templates/test_files_xss_escaping_1581.py).
 *
 * What it still is NOT: a browser E2E through the live app (no server, no
 * upload round-trip). fetch/Dialog/ToastMessages are stubbed.
 */

const fs = require('fs');
const path = require('path');

const TEMPLATE = path.join(__dirname, '../../../templates/files.html');

// A payload that breaks out of: HTML text, double-quoted attributes, and
// single-quoted JS strings — all three contexts the page interpolates into.
const HOSTILE = '<img src=x onerror="window.__pwned = true">\'";--</script>';

// Quote-first payload for attribute contexts: with quote-less escaping it
// closes the attribute and plants a REAL onerror attribute on the element.
const HOSTILE_ATTR = '" onerror="window.__pwned = true" data-x="';

function loadFilesPage() {
  const html = fs.readFileSync(TEMPLATE, 'utf8');
  const inline = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)]
    .map((m) => m[1])
    .join('\n');
  expect(inline).toContain('function renderFiles');
  const wrapped = `
    ${inline}
    return {
      renderFiles,
      applyFileFilter,
      editTags,
      renameArtifact,
      previewFile,
      showPreviewModal,
      closePreviewModal,
      escapeHtml: typeof escapeHtml !== 'undefined' ? escapeHtml : undefined,
      escapeAttr: typeof escapeAttr !== 'undefined' ? escapeAttr : undefined,
    };
  `;
  // eslint-disable-next-line no-new-func
  return new Function(wrapped)();
}

const tick = () => new Promise((r) => setTimeout(r, 0));

describe('files.html render path — stored XSS (#1581)', () => {
  let page;

  beforeEach(() => {
    document.body.innerHTML = '<div id="files-container" class="files-grid"></div>';
    window.currentUser = { user_id: 'u1', username: 'xian', is_admin: false };
    delete window.__pwned;
    delete window._allFiles;
    global.ToastMessages = {
      success: jest.fn(),
      error: jest.fn(),
      info: jest.fn(),
    };
    global.Dialog = { show: jest.fn(), confirm: jest.fn(), close: jest.fn() };
    page = loadFilesPage();
  });

  afterEach(() => {
    delete global.ToastMessages;
    delete global.Dialog;
    delete window.currentUser;
    delete window._allFiles;
    page.closePreviewModal();
  });

  const container = () => document.getElementById('files-container');

  const file = (overrides = {}) => ({
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

  test('escapeHtml() neutralizes the payload INCLUDING quotes (the old DOM-based helper left quotes raw)', () => {
    expect(page.escapeHtml).toBeDefined();
    const div = document.createElement('div');
    div.innerHTML = page.escapeHtml(HOSTILE);
    expect(div.children).toHaveLength(0); // no elements were created
    expect(div.textContent).toBe(HOSTILE); // and the text survives verbatim
    // quote coverage — this is what the DOM-based helper failed at
    expect(page.escapeHtml('a"b\'c')).toBe('a&quot;b&#39;c');
    expect(page.escapeAttr).toBeDefined();
  });

  test('a hostile filename renders as inert text — no element injection, no handler', () => {
    page.renderFiles([file({ filename: HOSTILE })]);
    expect(container().querySelectorAll('img, script')).toHaveLength(0);
    expect(window.__pwned).toBeUndefined();
    // the user still SEES their exact filename (escaping, not stripping)
    expect(container().querySelector('.file-title').textContent).toContain(
      '<img src=x onerror='
    );
  });

  test('a quote-breaking filename cannot plant attributes via the checkbox aria-label', () => {
    page.renderFiles([file({ filename: HOSTILE_ATTR })]);
    // attribute injection: quote-less escaping lets the payload close the
    // aria-label and add a real onerror= attribute to the <input>
    expect(container().querySelector('[onerror]')).toBeNull();
    expect(window.__pwned).toBeUndefined();
    // attribute value round-trips (getAttribute returns the decoded string)
    const cb = container().querySelector('.file-select');
    expect(cb.getAttribute('aria-label')).toBe(
      `Select ${HOSTILE_ATTR} for bulk download`
    );
  });

  test('hostile owner_id on a shared row is inert', () => {
    page.renderFiles([file({ owner_id: HOSTILE })]); // not currentUser -> indicator renders
    expect(container().querySelectorAll('img, script')).toHaveLength(0);
    expect(window.__pwned).toBeUndefined();
    expect(container().querySelector('.resource-owner').textContent).toContain(
      '<img src=x'
    );
  });

  test('hostile content_type / kind / file_id are inert (text + attr + onclick contexts)', () => {
    page.renderFiles([
      file({
        content_type: HOSTILE,
        kind: HOSTILE_ATTR,
        file_id: '"><img src=x onerror="window.__pwned = true">',
      }),
    ]);
    expect(container().querySelectorAll('img, script')).toHaveLength(0);
    expect(container().querySelector('[onerror]')).toBeNull();
    expect(window.__pwned).toBeUndefined();
  });

  test('hostile tags render as inert chips', () => {
    page.renderFiles([file({ tags: [HOSTILE, 'benign'] })]);
    expect(container().querySelectorAll('img, script')).toHaveLength(0);
    const chips = container().querySelectorAll('.tag-chip');
    expect(chips).toHaveLength(2);
    expect(chips[0].textContent).toBe(HOSTILE);
  });

  test('Rename button onclick carries only the id — never the filename (JS-string context is unprotectable by HTML escaping)', () => {
    page.renderFiles([file({ kind: 'artifact', filename: HOSTILE })]);
    const btn = [...container().querySelectorAll('.btn-icon')].find(
      (b) => b.getAttribute('title') === 'Rename'
    );
    expect(btn).toBeTruthy();
    const onclick = btn.getAttribute('onclick');
    expect(onclick).toContain('f1');
    expect(onclick).not.toContain('<img');
    expect(onclick).not.toContain('__pwned');
  });

  test('renameArtifact(id) resolves the filename from state and the dialog input round-trips it inert', () => {
    const hostileName = `${HOSTILE_ATTR}.md`;
    window._allFiles = [file({ kind: 'artifact', filename: hostileName })];
    page.renameArtifact('f1');
    expect(global.Dialog.show).toHaveBeenCalledTimes(1);
    const config = global.Dialog.show.mock.calls[0][0];
    // Dialog form content is an innerHTML sink (dialog.js:84) — render it the
    // way Dialog does and prove the value attribute holds, inert and intact
    const div = document.createElement('div');
    div.innerHTML = config.content;
    const input = div.querySelector('#rename-title-input');
    expect(input).toBeTruthy();
    expect(input.value).toBe(HOSTILE_ATTR); // .md stripped, payload verbatim
    expect(input.getAttribute('onerror')).toBeNull();
    expect(div.querySelectorAll('img, script')).toHaveLength(0);
    expect(window.__pwned).toBeUndefined();
  });

  test('editTags dialog input round-trips hostile tags inert', () => {
    window._allFiles = [file({ tags: [HOSTILE_ATTR, 'benign'] })];
    page.editTags('f1', 'file');
    expect(global.Dialog.show).toHaveBeenCalledTimes(1);
    const config = global.Dialog.show.mock.calls[0][0];
    const div = document.createElement('div');
    div.innerHTML = config.content;
    const input = div.querySelector('#tagsInput');
    expect(input).toBeTruthy();
    expect(input.value).toBe(`${HOSTILE_ATTR}, benign`);
    expect(input.getAttribute('onerror')).toBeNull();
    expect(div.querySelectorAll('img, script')).toHaveLength(0);
  });

  test('hostile preview filename and content render inert in the preview modal', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        previewable: true,
        truncated: false,
        filename: HOSTILE,
        content: HOSTILE,
      }),
    });
    page.previewFile('f1', 'file');
    await tick();
    const overlay = document.getElementById('file-preview-overlay');
    expect(overlay).toBeTruthy();
    expect(overlay.querySelectorAll('img, script')).toHaveLength(0);
    expect(window.__pwned).toBeUndefined();
    expect(overlay.querySelector('.file-preview-title').textContent).toBe(HOSTILE);
    expect(overlay.querySelector('.file-preview-content').textContent).toBe(HOSTILE);
  });
});
