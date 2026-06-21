/* #1286 D2 Slice 3 — mobile nav drawer toggle.
 *
 * On mobile (< tablet breakpoint) the nav-rail is an off-canvas drawer. The top-bar
 * hamburger opens it; the backdrop click and Escape close it. On tablet/desktop the
 * top-bar + backdrop are display:none, so this is a no-op (the rail is in-flow).
 */
(function () {
  "use strict";
  var hamburger = document.getElementById("app-shell-hamburger");
  var rail = document.getElementById("nav-rail");
  var backdrop = document.getElementById("app-shell-backdrop");
  if (!hamburger || !rail) return;

  function setOpen(open) {
    rail.classList.toggle("nav-rail--open", open);
    hamburger.setAttribute("aria-expanded", open ? "true" : "false");
    if (backdrop) backdrop.hidden = !open;
    document.body.classList.toggle("app-shell-drawer-open", open);
  }

  hamburger.addEventListener("click", function () {
    setOpen(!rail.classList.contains("nav-rail--open"));
  });
  if (backdrop) {
    backdrop.addEventListener("click", function () { setOpen(false); });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") setOpen(false);
  });
})();
