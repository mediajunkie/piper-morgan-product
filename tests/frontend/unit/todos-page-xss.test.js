/**
 * #1578 [SECURITY] — stored-XSS regression for templates/todos.html.
 *
 * LAYER (named honestly): RUNTIME DOM, via jsdom. The page builds its rows in
 * an inline <script> template literal; this suite extracts that script from
 * the template source, evaluates it together with the real permissions.js,
 * and renders HOSTILE todos into a real jsdom container. It proves the
 * escaping works when executed — element injection, attribute round-trips,
 * onclick contents — not merely that the source text contains escape calls
 * (that source-level half lives in
 * tests/unit/templates/test_todos_xss_escaping_1578.py).
 *
 * What it still is NOT: a browser E2E through the live app (no server, no
 * shared-with-me route). fetch/Dialog/Toast are stubbed.
 */

const fs = require('fs');
const path = require('path');

const TEMPLATE = path.join(__dirname, '../../../templates/todos.html');
const PERMISSIONS = path.join(__dirname, '../../../web/static/js/permissions.js');

// A payload that breaks out of: HTML text, double-quoted attributes, and
// single-quoted JS strings — all three contexts the page interpolates into.
const HOSTILE = '<img src=x onerror="window.__pwned = true">\'";--</script>';

function loadTodosPage() {
  const html = fs.readFileSync(TEMPLATE, 'utf8');
  const inline = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)]
    .map((m) => m[1])
    .join('\n');
  expect(inline).toContain('function renderTodos');
  const permissions = fs.readFileSync(PERMISSIONS, 'utf8');
  const wrapped = `
    ${permissions}
    ${inline}
    return {
      renderTodos,
      editTodo,
      shareTodo,
      renderCurrentShares,
      escapeAttr: typeof escapeAttr !== 'undefined' ? escapeAttr : undefined,
      escapeHtml: typeof escapeHtml !== 'undefined' ? escapeHtml : undefined,
    };
  `;
  // eslint-disable-next-line no-new-func
  return new Function(wrapped)();
}

const tick = () => new Promise((r) => setTimeout(r, 0));

describe('todos.html render path — stored XSS (#1578)', () => {
  let page;

  beforeEach(() => {
    document.body.innerHTML = '<div id="todos-container"></div>';
    window.currentUser = { user_id: 'u1', username: 'xian', is_admin: false };
    delete window.__pwned;
    global.ToastMessages = {
      success: jest.fn(),
      error: jest.fn(),
      info: jest.fn(),
    };
    global.Dialog = { show: jest.fn(), confirm: jest.fn(), close: jest.fn() };
    page = loadTodosPage();
  });

  afterEach(() => {
    delete global.ToastMessages;
    delete global.Dialog;
    delete window.currentUser;
    delete window.LifecycleIndicator;
  });

  const container = () => document.getElementById('todos-container');

  test('escapeHtml() neutralizes the payload (DOM round-trip, not entity-string pinning)', () => {
    expect(page.escapeHtml).toBeDefined();
    const div = document.createElement('div');
    div.innerHTML = page.escapeHtml(HOSTILE);
    expect(div.children).toHaveLength(0); // no elements were created
    expect(div.textContent).toBe(HOSTILE); // and the text survives verbatim
  });

  test('a hostile shared title renders as inert text — no element injection, no handler', () => {
    page.renderTodos([
      { id: 't1', text: HOSTILE, owner_id: 'u1', status: 'pending', priority: 'high' },
    ]);
    expect(container().querySelectorAll('img, script')).toHaveLength(0);
    expect(window.__pwned).toBeUndefined();
    // the user still SEES their exact title (escaping, not stripping)
    expect(container().querySelector('.resource-title').textContent).toContain(
      '<img src=x onerror='
    );
  });

  test('edit mode round-trips a hostile title through the input unchanged and inert', () => {
    page.renderTodos([
      { id: 't1', text: HOSTILE, owner_id: 'u1', status: 'pending', priority: 'low' },
    ]);
    page.editTodo('t1');
    const input = document.getElementById('edit-title-input-t1');
    expect(input).toBeTruthy();
    expect(input.value).toBe(HOSTILE); // attribute-escaped, property-decoded
    expect(container().querySelectorAll('img, script')).toHaveLength(0);
    expect(window.__pwned).toBeUndefined();
  });

  test('hostile owner_username on a shared-with-me row is inert', () => {
    page.renderTodos([
      {
        id: 't2',
        text: 'benign',
        owner_id: 'attacker',
        owner_username: HOSTILE,
        shared_with: [{ user_id: 'u1', role: 'VIEWER' }],
        status: 'pending',
      },
    ]);
    expect(container().querySelectorAll('img, script')).toHaveLength(0);
    expect(container().querySelector('.shared-indicator').textContent).toContain(
      '<img src=x'
    );
  });

  test('hostile status / priority / lifecycle_state are inert (attr + text contexts)', () => {
    window.LifecycleIndicator = { getPhrase: (s) => `phase of ${s}` };
    const hostileStage = '"><img src=x onerror="window.__pwned = true">';
    page.renderTodos([
      {
        id: 't3',
        text: 'benign',
        owner_id: 'u1',
        status: HOSTILE,
        priority: hostileStage,
        lifecycle_state: hostileStage,
      },
    ]);
    expect(container().querySelectorAll('img, script')).toHaveLength(0);
    expect(window.__pwned).toBeUndefined();
    // attribute value round-trips (getAttribute returns the decoded string)
    expect(
      container()
        .querySelector('.lifecycle-indicator')
        .getAttribute('data-lifecycle-stage')
    ).toBe(hostileStage);
  });

  test('Share button onclick carries only the id — never the title (JS-string context is unprotectable by HTML escaping)', () => {
    page.renderTodos([
      { id: 't4', text: HOSTILE, owner_id: 'u1', status: 'pending' },
    ]);
    const btn = container().querySelector('.share-btn');
    expect(btn).toBeTruthy();
    const onclick = btn.getAttribute('onclick');
    expect(onclick).toContain('t4');
    expect(onclick).not.toContain('<img');
    expect(onclick).not.toContain('__pwned');
  });

  test('shareTodo(id) resolves the title from state and hands it to the textContent-sink Dialog title', async () => {
    page.renderTodos([
      { id: 't4', text: HOSTILE, owner_id: 'u1', status: 'pending' },
    ]);
    global.fetch.mockResolvedValueOnce({ ok: true, json: async () => [] });
    page.shareTodo('t4');
    await tick();
    expect(global.Dialog.show).toHaveBeenCalledTimes(1);
    const config = global.Dialog.show.mock.calls[0][0];
    // full title reaches the dialog (Dialog.show sets it via textContent —
    // pinned behaviorally in dialog.test.js), so no data loss from the fix
    expect(config.title).toBe(`Share ${HOSTILE}`);
  });

  test('hostile share.user_email in the share list is inert', () => {
    const html = page.renderCurrentShares(
      [{ user_id: 'u9', user_email: HOSTILE, role: 'VIEWER' }],
      'todos',
      't1'
    );
    const div = document.createElement('div');
    div.innerHTML = html;
    expect(div.querySelectorAll('img, script')).toHaveLength(0);
    expect(div.textContent).toContain('<img src=x');
  });
});
