// G24 / F1 #1170: Dialog primitive (design-floor component)
// Global Dialog service. Two layers, coexisting:
//  • Legacy DOM-coupled path (show / confirm-callback / cancel / _doConfirm) —
//    renders into the #confirmation-dialog partial; preserved for back-compat.
//  • Self-contained primitive (open / alert / prompt + promise-confirm) — builds
//    its own DOM, so it works on ANY page (no partial include required). This is
//    the CXO-confirmed F1 API and the target for new code + native-dialog migration.
// Both reuse the token'd .confirmation-dialog* chrome (dialog.css). Provides
// focus trap, keyboard nav (Escape), return-focus, ARIA. Native browser
// confirm()/alert()/prompt() are retired in favor of these (native-dialog lint gate).
// WCAG 2.2 AA: focus management, keyboard accessible, ARIA attributes

const Dialog = {
  // State
  isOpen: false,
  confirmCallback: null,
  cancelCallback: null,
  focusedElementBeforeOpen: null,

  /**
   * Show confirmation dialog
   * @param {Object} config - Configuration object
   * @param {string} config.mode - Dialog mode: 'confirm' (default) or 'form' (Issue #462)
   * @param {string} config.title - Dialog title (e.g., "Delete Standup?")
   * @param {string} config.message - Warning message (text only)
   * @param {string} config.content - HTML content for form dialogs (Issue #462)
   * @param {string} config.confirmText - Button text (e.g., "Delete", "Reset", "Clear")
   * @param {string} config.cancelText - Cancel button text (default: "Cancel")
   * @param {Function} config.onConfirm - Callback when user confirms
   * @param {Function} config.onCancel - Callback when user cancels (optional)
   */
  show(config = {}) {
    const dialog = document.getElementById('confirmation-dialog');
    if (!dialog) return;

    // Determine mode: 'confirm' (default) for destructive actions, 'form' for create/edit
    // Issue #462: Mode controls icon visibility and button styling
    const mode = config.mode || 'confirm';

    // Update dialog text and buttons
    const title = dialog.querySelector('.confirmation-dialog-title');
    const message = dialog.querySelector('.confirmation-dialog-message');
    const confirmBtn = dialog.querySelector('#dialog-confirm-btn');
    const cancelBtn = dialog.querySelector('.confirmation-dialog-actions [onclick="Dialog.cancel()"]');
    const iconEl = dialog.querySelector('.confirmation-dialog-icon');

    // Icon visibility based on mode (Issue #462)
    // - 'confirm' mode: Show warning icon for destructive actions
    // - 'form' mode: Hide icon for create/edit actions
    if (iconEl) {
      iconEl.style.display = mode === 'form' ? 'none' : 'block';
    }

    // Button styling based on mode (Issue #462)
    // - 'confirm' mode: btn-danger (red) for destructive actions
    // - 'form' mode: btn-primary (blue) for positive actions
    if (confirmBtn) {
      if (mode === 'form') {
        confirmBtn.classList.remove('btn-danger');
        confirmBtn.classList.add('btn-primary');
      } else {
        confirmBtn.classList.remove('btn-primary');
        confirmBtn.classList.add('btn-danger');
      }
    }

    // Title and border styling based on mode (Issue #478)
    // - 'confirm' mode: danger red title and border
    // - 'form' mode: primary blue title and neutral border
    const dialogContent = dialog.querySelector('.confirmation-dialog-content');
    if (title) {
      title.style.color = mode === 'form' ? '#2c3e50' : '';  // Dark text for forms, default (red) for confirm
    }
    if (dialogContent) {
      dialogContent.style.borderColor = mode === 'form' ? '#ecf0f1' : '';  // Neutral border for forms, default (red) for confirm
    }

    if (title) title.textContent = config.title || 'Confirm Action';
    // Support both 'content' (HTML for forms) and 'message' (text for confirmations)
    // Issue #462: Form dialogs pass HTML in 'content', confirmation dialogs use 'message'
    if (message) {
      if (config.content) {
        // HTML content for form dialogs (e.g., create todo/list/project)
        message.innerHTML = config.content;
      } else {
        // Text message for confirmation dialogs
        message.textContent = config.message || 'Are you sure you want to proceed? This action cannot be undone.';
      }
    }
    // Button text: use provided text, or default based on mode
    if (confirmBtn) confirmBtn.textContent = config.confirmText || (mode === 'form' ? 'Create' : 'Confirm');
    if (cancelBtn) cancelBtn.textContent = config.cancelText || 'Cancel';

    // Store callbacks
    Dialog.confirmCallback = config.onConfirm || null;
    Dialog.cancelCallback = config.onCancel || null;

    // Save focused element to restore later
    Dialog.focusedElementBeforeOpen = document.activeElement;

    // Show dialog
    dialog.classList.add('active');
    dialog.setAttribute('aria-hidden', 'false');
    Dialog.isOpen = true;

    // Focus: for form dialogs, focus first input; for confirmations, focus confirm button
    setTimeout(() => {
      if (config.content) {
        // Form dialog: focus first input field
        const firstInput = dialog.querySelector('input, select, textarea');
        if (firstInput) firstInput.focus();
      } else if (confirmBtn) {
        confirmBtn.focus();
      }
    }, 100);

    // Set up keyboard handler for Escape key
    document.addEventListener('keydown', Dialog._handleKeydown);

    // Announce to screen readers
    if (typeof Toast !== 'undefined' && Toast.warning) {
      Toast.info(config.title || 'Confirm Action', 'Press Tab to navigate buttons, Enter to confirm, Escape to cancel');
    }
  },

  /**
   * Show confirmation dialog (alias for show with confirm-mode defaults)
   * Used by templates: Dialog.confirm({ title, message, onConfirm })
   * @param {Object} config - Same as show() config
   */
  confirm(config = {}) {
    // (1) No-arg invocation = the legacy confirm-button action (back-compat with
    //     the #confirmation-dialog partial's onclick="Dialog._doConfirm()").
    if (!config || (!config.title && !config.message && !config.body && !config.onConfirm)) {
      return Dialog._doConfirm();
    }
    // (2) Callback style (back-compat): existing onConfirm callers render through
    //     the legacy partial path. Unchanged behavior — 15 callers depend on it.
    if (typeof config.onConfirm === 'function') {
      Dialog.show({
        mode: 'confirm',
        confirmText: config.confirmText || 'Remove',
        ...config,
      });
      return;
    }
    // (3) Promise style (F1 #1170): self-contained via open(), no partial needed.
    //     Usage: `if (await Dialog.confirm({ title, message })) { ...proceed... }`
    const danger = config.danger !== false; // confirms default to danger styling
    return new Promise((resolve) => {
      Dialog.open({
        title: config.title,
        body: config.message || config.body || 'Are you sure?',
        danger,
        icon: config.icon || (danger ? '⚠️' : null),
        dismissible: config.dismissible !== false,
        onDismiss: () => resolve(false),
        actions: [
          { label: config.cancelText || 'Cancel', style: 'ghost', onClick: () => resolve(false) },
          { label: config.confirmText || 'Confirm', style: danger ? 'danger' : 'primary', onClick: () => resolve(true) },
        ],
      });
    });
  },

  /**
   * Execute confirmation action and close dialog
   * For form dialogs, callback can return false to keep dialog open (validation failed)
   * @private
   */
  async _doConfirm() {
    if (!Dialog.isOpen) return;

    if (Dialog.confirmCallback && typeof Dialog.confirmCallback === 'function') {
      // Call the callback and check return value
      // If callback returns false, don't close the dialog (validation failed)
      const result = await Dialog.confirmCallback();
      if (result === false) {
        return; // Keep dialog open
      }
    }

    Dialog.close();
  },

  /**
   * Cancel action and close dialog
   */
  cancel() {
    if (!Dialog.isOpen) return;

    Dialog.close();

    if (Dialog.cancelCallback && typeof Dialog.cancelCallback === 'function') {
      Dialog.cancelCallback();
    }
  },

  /**
   * Close dialog and restore focus
   */
  close() {
    const dialog = document.getElementById('confirmation-dialog');
    if (!dialog) return;

    dialog.classList.remove('active');
    dialog.setAttribute('aria-hidden', 'true');
    Dialog.isOpen = false;

    // Remove keyboard handler
    document.removeEventListener('keydown', Dialog._handleKeydown);

    // Restore focus
    if (Dialog.focusedElementBeforeOpen) {
      Dialog.focusedElementBeforeOpen.focus();
    }

    // Clear callbacks
    Dialog.confirmCallback = null;
    Dialog.cancelCallback = null;
  },

  /**
   * Handle keyboard events (Escape to close)
   * @private
   */
  _handleKeydown(event) {
    if (!Dialog.isOpen) return;

    if (event.key === 'Escape') {
      event.preventDefault();
      Dialog.cancel();
    }

    // Focus trap: keep Tab within dialog
    if (event.key === 'Tab') {
      Dialog._handleTabKey(event);
    }
  },

  /**
   * Implement focus trap for Tab key
   * @private
   */
  _handleTabKey(event) {
    const dialog = document.getElementById('confirmation-dialog');
    if (!dialog || !dialog.classList.contains('active')) return;

    const focusableElements = dialog.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    if (focusableElements.length === 0) return;

    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];
    const activeElement = document.activeElement;

    if (event.shiftKey) {
      // Shift+Tab: move focus backward
      if (activeElement === firstElement) {
        event.preventDefault();
        lastElement.focus();
      }
    } else {
      // Tab: move focus forward
      if (activeElement === lastElement) {
        event.preventDefault();
        firstElement.focus();
      }
    }
  },

  // ===========================================================================
  // F1 #1170 — generalized, self-contained Dialog primitive (CXO-confirmed API).
  // open() builds + tears down its own DOM (no #confirmation-dialog partial
  // dependency), so it works on ANY page. alert/prompt + the promise branch of
  // confirm() are thin wrappers over open(). Reuses the token'd
  // .confirmation-dialog* chrome — adds no hardcoded color/spacing CSS.
  // ===========================================================================

  _seq: 0,

  /**
   * Open a general modal dialog. Self-contained: no page-level partial required.
   * @param {Object} opts
   * @param {string} opts.title
   * @param {string|HTMLElement} opts.body - text (rendered pre-wrap) or an element (forms)
   * @param {Array<{label:string, style:string, onClick:Function}>} opts.actions
   *        style ∈ 'primary'|'danger'|'ghost'. Rendered in array order into the
   *        row-reverse action bar (first action sits rightmost — matches the
   *        platform confirmation-dialog convention: primary left, cancel right).
   *        An action's onClick may return false to keep the dialog OPEN (validation).
   * @param {boolean} [opts.dismissible=true] - ESC + backdrop + ✕ close the dialog
   * @param {boolean} [opts.danger=false] - danger border styling (else neutral)
   * @param {?string} [opts.icon] - optional emoji/glyph shown above the title
   * @param {?Function} [opts.onDismiss] - called when closed via ESC/backdrop/✕ (NOT via an action)
   * @returns {{close: Function, el: HTMLElement}} closeHandle
   */
  open(opts = {}) {
    const {
      title = '', body = '', actions = [],
      dismissible = true, danger = false, icon = null, onDismiss = null,
    } = opts;

    const seq = ++Dialog._seq;
    const titleId = `dialog-title-${seq}`;
    const bodyId = `dialog-message-${seq}`;
    const prevFocus = document.activeElement;

    const overlay = document.createElement('div');
    overlay.className = 'confirmation-dialog active';
    overlay.setAttribute('role', 'alertdialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-labelledby', titleId);
    overlay.setAttribute('aria-describedby', bodyId);

    const content = document.createElement('div');
    content.className = 'confirmation-dialog-content' + (danger ? '' : ' dialog-neutral');

    const closeX = document.createElement('button');
    closeX.className = 'confirmation-dialog-close';
    closeX.type = 'button';
    closeX.setAttribute('aria-label', 'Close dialog');
    closeX.innerHTML = '&times;';
    content.appendChild(closeX);

    if (icon) {
      const iconEl = document.createElement('div');
      iconEl.className = 'confirmation-dialog-icon';
      iconEl.textContent = icon;
      content.appendChild(iconEl);
    }

    const titleEl = document.createElement('h2');
    titleEl.className = 'confirmation-dialog-title';
    titleEl.id = titleId;
    titleEl.textContent = title;
    content.appendChild(titleEl);

    const bodyEl = document.createElement('div');
    bodyEl.className = 'confirmation-dialog-message';
    bodyEl.id = bodyId;
    if (body instanceof HTMLElement) {
      bodyEl.appendChild(body);
    } else {
      bodyEl.textContent = String(body);
      bodyEl.style.whiteSpace = 'pre-wrap';
    }
    content.appendChild(bodyEl);

    const actionsEl = document.createElement('div');
    actionsEl.className = 'confirmation-dialog-actions';

    let closed = false;
    const close = (viaAction) => {
      if (closed) return;
      closed = true;
      document.removeEventListener('keydown', onKey);
      overlay.remove();
      if (prevFocus && typeof prevFocus.focus === 'function') prevFocus.focus();
      if (!viaAction && typeof onDismiss === 'function') onDismiss();
    };

    const styleClass = (s) => (
      s === 'danger' ? 'btn btn-danger'
        : s === 'ghost' ? 'btn btn-ghost'
          : 'btn btn-primary'
    );

    (actions || []).forEach((a) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = styleClass(a.style);
      btn.textContent = a.label || 'OK';
      btn.addEventListener('click', async () => {
        let keepOpen = false;
        if (typeof a.onClick === 'function') {
          keepOpen = (await a.onClick()) === false;
        }
        if (!keepOpen) close(true);
      });
      actionsEl.appendChild(btn);
    });

    content.appendChild(actionsEl);
    overlay.appendChild(content);

    closeX.addEventListener('click', () => { if (dismissible) close(false); });
    overlay.addEventListener('mousedown', (e) => {
      if (e.target === overlay && dismissible) close(false);
    });

    function onKey(e) {
      if (e.key === 'Escape') {
        if (dismissible) { e.preventDefault(); close(false); }
        return;
      }
      if (e.key === 'Tab') {
        const f = overlay.querySelectorAll(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        if (!f.length) return;
        const first = f[0];
        const last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault(); last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault(); first.focus();
        }
      }
    }

    document.body.appendChild(overlay);
    document.addEventListener('keydown', onKey);

    // Focus the first input (forms), else the first action button.
    setTimeout(() => {
      const input = content.querySelector('input, select, textarea');
      if (input) { input.focus(); return; }
      const firstBtn = actionsEl.querySelector('button');
      if (firstBtn) firstBtn.focus();
    }, 50);

    return { close: () => close(true), el: overlay };
  },

  /**
   * Alert: a single-button informational modal. Resolves when acknowledged/dismissed.
   * @param {Object} opts - { title, body|message, okLabel?, icon? }
   * @returns {Promise<void>}
   */
  alert(opts = {}) {
    const { title = '', body = '', message = '', okLabel = 'OK', icon = null } = opts;
    return new Promise((resolve) => {
      Dialog.open({
        title,
        body: body || message,
        icon,
        onDismiss: () => resolve(),
        actions: [{ label: okLabel, style: 'primary', onClick: () => resolve() }],
      });
    });
  },

  /**
   * Prompt: single-line text input. Resolves the value on confirm, null on
   * cancel/dismiss. Optional validate(value) => true | errorString gates confirm
   * (inline error shown + dialog kept open until valid).
   * @param {Object} opts - { title, label?, placeholder?, value?, confirmText?, cancelText?, validate? }
   * @returns {Promise<string|null>}
   */
  prompt(opts = {}) {
    const {
      title = '', label = '', placeholder = '', value = '',
      confirmText = 'OK', cancelText = 'Cancel', validate = null,
    } = opts;
    return new Promise((resolve) => {
      const group = document.createElement('div');
      group.className = 'form-group';
      if (label) {
        const lbl = document.createElement('label');
        lbl.textContent = label;
        group.appendChild(lbl);
      }
      const input = document.createElement('input');
      input.type = 'text';
      input.value = value;
      input.placeholder = placeholder;
      group.appendChild(input);
      const err = document.createElement('div');
      err.className = 'dialog-error';
      err.setAttribute('role', 'alert');
      group.appendChild(err);

      input.addEventListener('input', () => { err.textContent = ''; });

      Dialog.open({
        title,
        body: group,
        dismissible: true,
        onDismiss: () => resolve(null),
        actions: [
          { label: cancelText, style: 'ghost', onClick: () => resolve(null) },
          {
            label: confirmText,
            style: 'primary',
            onClick: () => {
              const v = input.value;
              if (typeof validate === 'function') {
                const res = validate(v);
                if (res !== true) {
                  err.textContent = typeof res === 'string' ? res : 'Invalid value';
                  input.focus();
                  return false; // keep dialog open
                }
              }
              resolve(v);
              return true;
            },
          },
        ],
      });
    });
  },
};

// Alternative syntax for inline usage
function confirmDelete(config = {}) {
  Dialog.show({
    title: config.title || 'Delete this item?',
    message: config.message || 'This action cannot be undone.',
    confirmText: 'Delete',
    ...config,
  });
}

function confirmReset(config = {}) {
  Dialog.show({
    title: config.title || 'Reset to defaults?',
    message: config.message || 'This will reset all settings. This action cannot be undone.',
    confirmText: 'Reset',
    ...config,
  });
}

function confirmClear(config = {}) {
  Dialog.show({
    title: config.title || 'Clear all data?',
    message: config.message || 'This will permanently remove all data. This action cannot be undone.',
    confirmText: 'Clear',
    ...config,
  });
}
