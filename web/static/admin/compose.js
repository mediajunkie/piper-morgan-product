// Editorial Compose — Phase 2: autosave + placeholder warnings
(function () {
  'use strict';

  const form = document.getElementById('compose-form');
  if (!form) return;

  const saveUrl = form.dataset.saveUrl;
  const statusEl = document.getElementById('save-status');
  const warningsEl = document.getElementById('placeholder-warnings');
  const bodyEl = document.getElementById('field-body');
  const AUTOSAVE_MS = 30_000;

  let saveTimer = null;
  let lastSaved = null;

  function getPayload() {
    return {
      image: document.getElementById('field-image')?.value ?? '',
      alt: document.getElementById('field-alt')?.value ?? '',
      caption: document.getElementById('field-caption')?.value ?? '',
      body: bodyEl?.value ?? '',
    };
  }

  function payloadUnchanged(p) {
    return lastSaved !== null && JSON.stringify(p) === lastSaved;
  }

  function setStatus(text, cls) {
    statusEl.textContent = text;
    statusEl.className = 'save-status' + (cls ? ' ' + cls : '');
  }

  async function doSave() {
    const payload = getPayload();
    if (payloadUnchanged(JSON.stringify(payload))) return;
    setStatus('Saving…', '');
    try {
      const res = await fetch(saveUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      lastSaved = JSON.stringify(payload);
      const t = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      setStatus('Saved at ' + t, 'saved');
    } catch (e) {
      setStatus('Save failed: ' + e.message, 'error');
    }
  }

  function scheduleAutosave() {
    clearTimeout(saveTimer);
    if (statusEl.className.indexOf('saved') === -1) {
      setStatus('Unsaved changes', 'unsaved');
    }
    saveTimer = setTimeout(doSave, AUTOSAVE_MS);
  }

  function scanPlaceholders() {
    const body = bodyEl?.value ?? '';
    // Match any [...] block — generic per Comms guidance (future-proof against new markers)
    const matches = Array.from(body.matchAll(/\[[^\]]{1,120}\]/g), m => m[0]);
    if (matches.length === 0) {
      warningsEl.hidden = true;
      warningsEl.innerHTML = '';
    } else {
      const items = matches
        .map(m => '<li><code>' + m.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</code></li>')
        .join('');
      warningsEl.hidden = false;
      warningsEl.innerHTML = '<strong>⚠️ Placeholder blocks remaining:</strong><ul>' + items + '</ul>';
    }
  }

  // Wire events
  form.querySelectorAll('input, textarea').forEach(el => {
    el.addEventListener('input', scheduleAutosave);
  });
  bodyEl?.addEventListener('input', scanPlaceholders);

  // Save on focus-out of any field (supplements the timer)
  form.addEventListener('focusout', function (e) {
    if (!form.contains(e.relatedTarget)) {
      // Focus left the form entirely
      clearTimeout(saveTimer);
      doSave();
    }
  });

  // Initial placeholder scan on page load
  scanPlaceholders();
})();
