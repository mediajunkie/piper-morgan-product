/*
 * home-modules.js — #1225: collapse + dismiss for the home ambient modules
 * ("what i'm seeing" / "recently").
 *
 * - Collapse/minimize: hides the module body, keeps the header. Persisted per
 *   module in localStorage. The biggest screen-real-estate win PM flagged.
 * - Dismiss ("not now"): hides the whole module, but RE-SURFACES when the
 *   module's content changes (CXO 2026-06-17: dismiss != "never"; the permanent
 *   "don't show again" opt-out is a separate, future control). We persist a
 *   content signature at dismiss time and compare it on the next load.
 *
 * Persistence is localStorage (per browser) — the same house pattern home.html
 * already uses for `sidebarCollapsed`. Server-side per-user sync is a future
 * follow-up (tracked on #1225); for the single-user beta, per-browser is enough.
 *
 * Exposes window.HomeModules.{init, refreshAsync} so the async places loader can
 * re-evaluate the dismiss state after it renders its cards.
 */
(function () {
  "use strict";

  var COLLAPSE_KEY = "piper_module_collapsed_";
  var DISMISS_KEY = "piper_module_dismissed_";
  var EMPTY_SIGNATURE = "∅"; // ∅ — stable signature for an empty/loading module

  function lsGet(key) {
    try {
      return window.localStorage.getItem(key);
    } catch (e) {
      return null;
    }
  }
  function lsSet(key, value) {
    try {
      window.localStorage.setItem(key, value);
    } catch (e) {
      /* private mode / quota — degrade to in-session only */
    }
  }
  function lsRemove(key) {
    try {
      window.localStorage.removeItem(key);
    } catch (e) {
      /* no-op */
    }
  }

  /* A stable fingerprint of the module's current content. New content (a new
     place / insight id appearing) changes the signature → a dismissed module
     re-surfaces. */
  function computeSignature(moduleEl) {
    var body = moduleEl.querySelector(".card__body");
    if (!body) return EMPTY_SIGNATURE;
    var ids = [];
    var nodes = body.querySelectorAll("[data-place-id], [data-insight-id]");
    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      var id = n.getAttribute("data-place-id") || n.getAttribute("data-insight-id");
      if (id) ids.push(id);
    }
    if (ids.length === 0) return EMPTY_SIGNATURE;
    ids.sort();
    return ids.join("|");
  }

  function applyCollapse(moduleEl) {
    var id = moduleEl.dataset.moduleId;
    var btn = moduleEl.querySelector(".module-collapse");
    var collapsed = lsGet(COLLAPSE_KEY + id) === "1";
    moduleEl.classList.toggle("is-collapsed", collapsed);
    if (btn) btn.setAttribute("aria-expanded", collapsed ? "false" : "true");
  }

  /* Evaluate dismiss state against the CURRENT content signature.
     - stored == current  → keep dismissed (nothing new since dismiss)
     - stored != current  → content changed → re-surface (clear the stored dismiss)
     - no stored value     → visible */
  function applyDismiss(moduleEl) {
    var id = moduleEl.dataset.moduleId;
    var stored = lsGet(DISMISS_KEY + id);
    if (stored === null) {
      moduleEl.classList.remove("is-dismissed");
      return;
    }
    var current = computeSignature(moduleEl);
    if (stored === current) {
      moduleEl.classList.add("is-dismissed");
    } else {
      lsRemove(DISMISS_KEY + id);
      moduleEl.classList.remove("is-dismissed");
    }
  }

  function wireControls(moduleEl) {
    var id = moduleEl.dataset.moduleId;
    var collapseBtn = moduleEl.querySelector(".module-collapse");
    var dismissBtn = moduleEl.querySelector(".module-dismiss");

    if (collapseBtn && !collapseBtn.dataset.wired) {
      collapseBtn.dataset.wired = "1";
      collapseBtn.addEventListener("click", function () {
        var nowCollapsed = !moduleEl.classList.contains("is-collapsed");
        moduleEl.classList.toggle("is-collapsed", nowCollapsed);
        collapseBtn.setAttribute("aria-expanded", nowCollapsed ? "false" : "true");
        lsSet(COLLAPSE_KEY + id, nowCollapsed ? "1" : "0");
      });
    }

    if (dismissBtn && !dismissBtn.dataset.wired) {
      dismissBtn.dataset.wired = "1";
      dismissBtn.addEventListener("click", function () {
        moduleEl.classList.add("is-dismissed");
        lsSet(DISMISS_KEY + id, computeSignature(moduleEl));
      });
    }
  }

  function initModule(moduleEl, evaluateDismiss) {
    wireControls(moduleEl);
    applyCollapse(moduleEl);
    if (evaluateDismiss) {
      applyDismiss(moduleEl);
    } else if (lsGet(DISMISS_KEY + moduleEl.dataset.moduleId) !== null) {
      // Async module that was previously dismissed: hide it NOW rather than
      // waiting for its content to fetch. Otherwise it renders visible, then
      // refreshAsync() hides it once the fetch completes → a show-then-hide
      // flash on reload (#1225 follow-up). refreshAsync() still re-evaluates
      // against the real content and re-surfaces it if the content changed.
      moduleEl.classList.add("is-dismissed");
    }
  }

  function init() {
    var modules = document.querySelectorAll("[data-ambient-module]");
    for (var i = 0; i < modules.length; i++) {
      var m = modules[i];
      // Async modules (their body fills in after a fetch) defer the dismiss
      // evaluation to refreshAsync() — at init their signature is still empty.
      var isAsync = m.dataset.moduleAsync === "true";
      initModule(m, !isAsync);
    }
  }

  /* Called by the async loader (e.g. loadPlaces) after it renders content, so the
     dismiss signature is computed against the real content, not the loading state. */
  function refreshAsync(id) {
    var m = document.querySelector('[data-ambient-module][data-module-id="' + id + '"]');
    if (m) applyDismiss(m);
  }

  window.HomeModules = { init: init, refreshAsync: refreshAsync };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
