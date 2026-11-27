/**
 * #2455: the project page said "No work items for this project" right after
 * chat confirmed a todo added to that project. The page now shows the
 * project's open todos (Arch's rule and CXO's words, 2026-11-27).
 *
 * LAYER: RUNTIME DOM via jsdom, the harness files-page-owner-indicator-1697
 * uses: the page's inline <script> is taken from the real template (Jinja
 * comments stripped, as the server strips them), evaluated, and the DOM it
 * writes is read. Arch's two render tests are the first and the fourth here.
 *
 * Denominator: the Open todos section only. Not covered: the project card,
 * the Config tab, a real browser, the route (tests/unit/web/api/routes/
 * test_project_todos_route_2455.py).
 */

const fs = require('fs');
const path = require('path');

const TEMPLATE = path.join(__dirname, '../../../templates/project_detail.html');
const ESCAPE_JS = fs.readFileSync(
  path.join(__dirname, '../../../web/static/js/escape.js'),
  'utf8'
);

const NONE = 'No open todos in this project.';
const COULD_NOT_CHECK =
  "I couldn't check this project's todos just now. Reload the page to try again.";

function servedTemplate() {
  return fs.readFileSync(TEMPLATE, 'utf8').replace(/\{#[\s\S]*?#\}/g, '');
}

function loadPage() {
  const html = servedTemplate();
  const inline = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)]
    .map((m) => m[1])
    .join('\n')
    .replace('"{{ project_id }}"', '"p-1"');
  expect(inline).toContain('function renderProjectTodos');
  // The section's own markup, from the template, so a renamed id fails here.
  const section = html.match(/<div class="work-items-section" id="project-todos-section">[\s\S]*?<\/div>\s*<\/div>\s*<\/div>/);
  expect(section).not.toBeNull();
  document.body.innerHTML = section[0];
  const wrapped = `
    ${ESCAPE_JS}
    ${inline}
    return { loadProjectTodos, renderProjectTodos };
  `;
  // eslint-disable-next-line no-new-func
  return new Function(wrapped)();
}

function container() {
  return document.getElementById('project-todos-container');
}

function respond(status, body) {
  global.fetch = jest.fn().mockResolvedValue({
    status,
    ok: status >= 200 && status < 300,
    json: async () => body,
  });
}

describe('#2455 project page: Open todos', () => {
  let errorSpy;
  let setupFetch;
  beforeEach(() => {
    errorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    setupFetch = global.fetch; // setup.js's mock; it clears it before each test
  });
  afterEach(() => {
    errorSpy.mockRestore();
    global.fetch = setupFetch;
  });

  test('a project with one open todo shows the todo text', async () => {
    const page = loadPage();
    respond(200, {
      todos: [{ text: 'send the invites', repeat: 1, priority: null }],
      count: 1,
      cap_line: null,
    });
    await page.loadProjectTodos();
    expect(global.fetch).toHaveBeenCalledWith('/api/v1/projects/p-1/todos', {
      credentials: 'include',
    });
    const rows = [...container().querySelectorAll('li.project-todo')].map((li) => li.textContent);
    expect(rows).toEqual(['send the invites']);
    expect(container().textContent).not.toContain(NONE);
    expect(container().textContent).not.toContain(COULD_NOT_CHECK);
  });

  test('rows keep the order given, with repeats and the priority note', async () => {
    const page = loadPage();
    respond(200, {
      todos: [
        { text: 'call the caterer', repeat: 1, priority: 'urgent' },
        { text: 'review prs', repeat: 3, priority: 'high' },
        { text: 'book the venue', repeat: 1, priority: null },
      ],
      count: 3,
      cap_line: 'Showing the first 3 todos in Launch.',
    });
    await page.loadProjectTodos();
    const rows = [...container().querySelectorAll('li.project-todo')].map((li) => li.textContent);
    expect(rows).toEqual([
      'call the caterer (urgent)',
      'review prs (×3) (high)',
      'book the venue',
    ]);
    expect(container().querySelector('.project-todos-cap').textContent).toBe(
      'Showing the first 3 todos in Launch.'
    );
  });

  test('a read that succeeded and found none says so, in CXO\'s words', async () => {
    const page = loadPage();
    respond(200, { todos: [], count: 0, cap_line: null });
    await page.loadProjectTodos();
    expect(container().textContent.trim()).toBe(NONE);
  });

  test('a failed read shows the couldn\'t-check line, never "none" or a count', async () => {
    const page = loadPage();
    respond(500, { detail: 'whatever the server said' });
    await page.loadProjectTodos();
    expect(container().textContent.trim()).toBe(COULD_NOT_CHECK);
    expect(container().querySelectorAll('li').length).toBe(0);
  });

  test('a network failure shows the couldn\'t-check line', async () => {
    const page = loadPage();
    global.fetch = jest.fn().mockRejectedValue(new Error('offline'));
    await page.loadProjectTodos();
    expect(container().textContent.trim()).toBe(COULD_NOT_CHECK);
  });

  test('a 200 whose body has no todos list is a failed read, not "none"', async () => {
    const page = loadPage();
    respond(200, { detail: 'not the shape' });
    await page.loadProjectTodos();
    expect(container().textContent.trim()).toBe(COULD_NOT_CHECK);
  });

  test('a todo\'s text is escaped', async () => {
    const page = loadPage();
    respond(200, {
      todos: [{ text: '<img src=x onerror=alert(1)>', repeat: 1, priority: null }],
      count: 1,
      cap_line: null,
    });
    await page.loadProjectTodos();
    expect(container().querySelector('img')).toBeNull();
    expect(container().textContent).toContain('<img src=x onerror=alert(1)>');
  });

  test('a project that is not the person\'s (404) leaves the section silent', async () => {
    const page = loadPage();
    respond(404, {});
    await page.loadProjectTodos();
    expect(container().textContent.trim()).toBe('');
  });

  test('the served page has no Work Items section', () => {
    const html = servedTemplate();
    expect(html).not.toContain('Work Items');
    expect(html).not.toContain('No work items for this project');
  });
});
