/**
 * Dialog primitive tests — F1 #1170 (design-floor component)
 *
 * Tests web/static/js/dialog.js — the generalized, self-contained Dialog.open()
 * primitive + alert/prompt/promise-confirm wrappers (CXO-confirmed API), plus
 * back-compat for the legacy #confirmation-dialog (show/onConfirm) path.
 *
 * Behavioral (jsdom): asserts real DOM + promise resolution, not file content.
 */

const tick = () => new Promise((r) => setTimeout(r, 0));
const overlay = () => document.querySelector('.confirmation-dialog');

describe('Dialog primitive (F1 #1170)', () => {
  beforeEach(() => {
    global.loadScript('dialog.js');
  });

  // --- Dialog.open: structure -------------------------------------------------
  describe('Dialog.open() structure', () => {
    test('creates an accessible self-contained overlay in the body', () => {
      Dialog.open({ title: 'My Title', body: 'My body', actions: [{ label: 'OK', style: 'primary' }] });
      const el = overlay();
      expect(el).toBeTruthy();
      expect(el.classList.contains('active')).toBe(true);
      expect(el.getAttribute('role')).toBe('alertdialog');
      expect(el.getAttribute('aria-modal')).toBe('true');
      // aria-labelledby / describedby wired to the rendered title/body ids
      const titleId = el.getAttribute('aria-labelledby');
      const bodyId = el.getAttribute('aria-describedby');
      expect(el.querySelector(`#${titleId}`).textContent).toBe('My Title');
      expect(el.querySelector(`#${bodyId}`).textContent).toBe('My body');
    });

    test('renders actions with the right style classes and labels', () => {
      Dialog.open({
        title: 'T',
        actions: [
          { label: 'Cancel', style: 'ghost' },
          { label: 'Delete', style: 'danger' },
          { label: 'Save', style: 'primary' },
        ],
      });
      const btns = overlay().querySelectorAll('.confirmation-dialog-actions button');
      expect(btns).toHaveLength(3);
      expect(btns[0].className).toContain('btn-ghost');
      expect(btns[0].textContent).toBe('Cancel');
      expect(btns[1].className).toContain('btn-danger');
      expect(btns[2].className).toContain('btn-primary');
    });

    test('danger:false (default) tags neutral; danger:true does not', () => {
      Dialog.open({ title: 'A', danger: false, actions: [{ label: 'OK', style: 'primary' }] });
      expect(overlay().querySelector('.confirmation-dialog-content').classList.contains('dialog-neutral')).toBe(true);
      document.body.innerHTML = '';
      Dialog.open({ title: 'B', danger: true, actions: [{ label: 'OK', style: 'danger' }] });
      expect(overlay().querySelector('.confirmation-dialog-content').classList.contains('dialog-neutral')).toBe(false);
    });

    test('renders an optional icon', () => {
      Dialog.open({ title: 'T', icon: '⚠️', actions: [{ label: 'OK', style: 'primary' }] });
      expect(overlay().querySelector('.confirmation-dialog-icon').textContent).toBe('⚠️');
    });

    test('accepts an HTMLElement body (forms)', () => {
      const input = document.createElement('input');
      input.id = 'custom-field';
      Dialog.open({ title: 'T', body: input, actions: [{ label: 'OK', style: 'primary' }] });
      expect(overlay().querySelector('#custom-field')).toBeTruthy();
    });
  });

  // --- Dialog.open: behavior --------------------------------------------------
  describe('Dialog.open() behavior', () => {
    test('action onClick fires, then the dialog closes', async () => {
      const onClick = jest.fn();
      Dialog.open({ title: 'T', actions: [{ label: 'OK', style: 'primary', onClick }] });
      overlay().querySelector('button.btn-primary').click();
      await tick();
      expect(onClick).toHaveBeenCalledTimes(1);
      expect(overlay()).toBeFalsy(); // removed from the DOM
    });

    test('onClick returning false KEEPS the dialog open (validation)', async () => {
      Dialog.open({ title: 'T', actions: [{ label: 'OK', style: 'primary', onClick: () => false }] });
      overlay().querySelector('button.btn-primary').click();
      await tick();
      expect(overlay()).toBeTruthy(); // still open
    });

    test('closeHandle.close() programmatically removes the dialog', () => {
      const handle = Dialog.open({ title: 'T', actions: [{ label: 'OK', style: 'primary' }] });
      expect(overlay()).toBeTruthy();
      handle.close();
      expect(overlay()).toBeFalsy();
    });

    test('ESC closes a dismissible dialog and fires onDismiss', () => {
      const onDismiss = jest.fn();
      Dialog.open({ title: 'T', onDismiss, actions: [{ label: 'OK', style: 'primary' }] });
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
      expect(overlay()).toBeFalsy();
      expect(onDismiss).toHaveBeenCalledTimes(1);
    });

    test('ESC does NOT close when dismissible:false', () => {
      Dialog.open({ title: 'T', dismissible: false, actions: [{ label: 'OK', style: 'primary' }] });
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
      expect(overlay()).toBeTruthy();
    });

    test('backdrop click dismisses a dismissible dialog', () => {
      Dialog.open({ title: 'T', actions: [{ label: 'OK', style: 'primary' }] });
      const el = overlay();
      // mousedown whose target IS the overlay (the backdrop), not the content
      const evt = new MouseEvent('mousedown', { bubbles: true });
      Object.defineProperty(evt, 'target', { value: el });
      el.dispatchEvent(evt);
      expect(overlay()).toBeFalsy();
    });

    test('onDismiss does NOT fire when closed via an action', async () => {
      const onDismiss = jest.fn();
      Dialog.open({ title: 'T', onDismiss, actions: [{ label: 'OK', style: 'primary', onClick: () => {} }] });
      overlay().querySelector('button.btn-primary').click();
      await tick();
      expect(onDismiss).not.toHaveBeenCalled();
    });

    test('restores focus to the previously-focused element on close', () => {
      const trigger = document.createElement('button');
      document.body.appendChild(trigger);
      trigger.focus();
      expect(document.activeElement).toBe(trigger);
      const handle = Dialog.open({ title: 'T', actions: [{ label: 'OK', style: 'primary' }] });
      handle.close();
      expect(document.activeElement).toBe(trigger);
    });
  });

  // --- Dialog.alert -----------------------------------------------------------
  describe('Dialog.alert()', () => {
    test('renders a single OK button and resolves when acknowledged', async () => {
      const p = Dialog.alert({ title: 'Done', body: 'Saved' });
      const btns = overlay().querySelectorAll('.confirmation-dialog-actions button');
      expect(btns).toHaveLength(1);
      btns[0].click();
      await expect(p).resolves.toBeUndefined();
      expect(overlay()).toBeFalsy();
    });

    test('resolves when dismissed (ESC)', async () => {
      const p = Dialog.alert({ title: 'Done', message: 'Saved' });
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
      await expect(p).resolves.toBeUndefined();
    });
  });

  // --- Dialog.prompt ----------------------------------------------------------
  describe('Dialog.prompt()', () => {
    test('resolves the input value on confirm', async () => {
      const p = Dialog.prompt({ title: 'Rename', value: 'old' });
      const el = overlay();
      const input = el.querySelector('input');
      expect(input.value).toBe('old');
      input.value = 'new name';
      el.querySelector('button.btn-primary').click();
      await expect(p).resolves.toBe('new name');
    });

    test('resolves null on cancel', async () => {
      const p = Dialog.prompt({ title: 'Rename' });
      overlay().querySelector('button.btn-ghost').click();
      await expect(p).resolves.toBeNull();
    });

    test('resolves null on dismiss (ESC)', async () => {
      const p = Dialog.prompt({ title: 'Rename' });
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
      await expect(p).resolves.toBeNull();
    });

    test('validate() gates confirm: shows inline error + keeps open until valid', async () => {
      const p = Dialog.prompt({
        title: 'Rename',
        validate: (v) => (v.trim().length > 0 ? true : 'Name required'),
      });
      const el = overlay();
      const input = el.querySelector('input');
      const okBtn = el.querySelector('button.btn-primary');

      okBtn.click(); // empty → invalid
      await tick();
      expect(overlay()).toBeTruthy(); // still open
      expect(el.querySelector('.dialog-error').textContent).toBe('Name required');

      input.value = 'valid';
      okBtn.click();
      await expect(p).resolves.toBe('valid');
    });
  });

  // --- Dialog.confirm (promise branch) ---------------------------------------
  describe('Dialog.confirm() promise style', () => {
    test('resolves true on confirm', async () => {
      const p = Dialog.confirm({ title: 'Delete?', message: 'Sure?' });
      overlay().querySelector('button.btn-danger').click();
      await expect(p).resolves.toBe(true);
    });

    test('resolves false on cancel', async () => {
      const p = Dialog.confirm({ title: 'Delete?', message: 'Sure?' });
      overlay().querySelector('button.btn-ghost').click();
      await expect(p).resolves.toBe(false);
    });

    test('resolves false on dismiss (ESC)', async () => {
      const p = Dialog.confirm({ title: 'Delete?', message: 'Sure?' });
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
      await expect(p).resolves.toBe(false);
    });

    test('defaults to danger styling + ⚠️ icon', () => {
      Dialog.confirm({ title: 'Delete?', message: 'Sure?' });
      const el = overlay();
      expect(el.querySelector('.confirmation-dialog-icon').textContent).toBe('⚠️');
      expect(el.querySelector('button.btn-danger')).toBeTruthy();
      expect(el.querySelector('.confirmation-dialog-content').classList.contains('dialog-neutral')).toBe(false);
    });

    test('danger:false uses neutral + primary confirm', () => {
      Dialog.confirm({ title: 'Proceed?', message: 'ok', danger: false });
      const el = overlay();
      expect(el.querySelector('button.btn-primary')).toBeTruthy();
      expect(el.querySelector('.confirmation-dialog-content').classList.contains('dialog-neutral')).toBe(true);
    });
  });

  // --- back-compat: legacy callback / show() path ----------------------------
  describe('back-compat (legacy #confirmation-dialog path)', () => {
    test('confirm({onConfirm}) does NOT hit the self-contained open() path', () => {
      // No #confirmation-dialog partial present → legacy show() returns early,
      // and crucially the new promise/open() path is NOT triggered.
      Dialog.confirm({ title: 'T', message: 'M', onConfirm: jest.fn() });
      expect(overlay()).toBeFalsy();
    });

    test('confirm({onConfirm}) activates the legacy partial when present', () => {
      // Inject a minimal legacy partial
      document.body.innerHTML = `
        <div id="confirmation-dialog" class="confirmation-dialog" aria-hidden="true">
          <div class="confirmation-dialog-content">
            <div class="confirmation-dialog-icon"></div>
            <h2 class="confirmation-dialog-title"></h2>
            <div class="confirmation-dialog-message"></div>
            <div class="confirmation-dialog-actions">
              <button onclick="Dialog.cancel()"></button>
              <button id="dialog-confirm-btn" onclick="Dialog._doConfirm()"></button>
            </div>
          </div>
        </div>`;
      Dialog.confirm({ title: 'Remove?', message: 'gone', onConfirm: jest.fn() });
      const legacy = document.getElementById('confirmation-dialog');
      expect(legacy.classList.contains('active')).toBe(true);
      expect(legacy.querySelector('.confirmation-dialog-title').textContent).toBe('Remove?');
    });
  });
});
