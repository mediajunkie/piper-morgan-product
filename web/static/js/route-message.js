/**
 * route-message.js — the one reader for a refused background request (issue 2431).
 *
 * When a request is refused before its route runs (the capacity guard's outage, rate
 * limit or at-capacity reply; the sign-in check's outage reply), the JSON carries the
 * sentence a person should read as `message`. The `error` key is a code for scripts and
 * the log: this reader never shows it.
 *
 *   RouteMessage.read(body, fallback)  -> the route's `message`, or `fallback` when none came
 *   RouteMessage.show(element, body, fallback) -> sets that text with textContent
 *
 * Text only: a route's words are never parsed as HTML here.
 */
(function () {
  function read(body, fallback) {
    if (body && typeof body === 'object' && typeof body.message === 'string' && body.message.trim()) {
      return body.message;
    }
    return fallback;
  }

  function show(element, body, fallback) {
    const text = read(body, fallback);
    element.textContent = text;
    return text;
  }

  window.RouteMessage = { read, show };
})();
