#!/usr/bin/env node
// Dummy stand-in for the browser half of seat_session.py (CIO, 2026-11-15; ADR-084 D3).
//
// Talks to a browser's debug port, places one httpOnly cookie read from a FILE, then opens the
// dummy page and prints what the page says. It prints the page's words and the cookie's flags
// only, never the cookie's value. Usage:
//   node place_dummy_cookie.mjs <debug-port> <cookie-file> [--read-only]
import { readFileSync } from "node:fs";

const [port, cookieFile, mode] = process.argv.slice(2);
const SITE = "http://127.0.0.1:8791/whoami";

const version = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json();
const ws = new WebSocket(version.webSocketDebuggerUrl);
await new Promise((ok, bad) => { ws.onopen = ok; ws.onerror = bad; });

let nextId = 1;
const waiting = new Map();
ws.onmessage = (ev) => {
  const msg = JSON.parse(ev.data);
  if (msg.id && waiting.has(msg.id)) { waiting.get(msg.id)(msg); waiting.delete(msg.id); }
};
const send = (method, params = {}, sessionId) =>
  new Promise((ok) => {
    const id = nextId++;
    waiting.set(id, ok);
    ws.send(JSON.stringify({ id, method, params, ...(sessionId ? { sessionId } : {}) }));
  });

if (mode !== "--read-only") {
  const value = readFileSync(cookieFile, "utf8").trim();
  const res = await send("Storage.setCookies", {
    cookies: [{
      name: "dummy_session", value, domain: "127.0.0.1", path: "/",
      httpOnly: true, expires: Math.floor(Date.now() / 1000) + 7 * 86400,
    }],
  });
  console.log("place:", res.error ? `FAILED (${res.error.message})` : "ok (httpOnly, 7-day expiry)");
}

const { result: target } = await send("Target.createTarget", { url: SITE });
const { result: attached } = await send("Target.attachToTarget", { targetId: target.targetId, flatten: true });
await new Promise((r) => setTimeout(r, 1500));
const page = await send("Runtime.evaluate",
  { expression: "document.getElementById('who')?.textContent" }, attached.sessionId);
const js = await send("Runtime.evaluate",
  { expression: "document.cookie.includes('dummy_session')" }, attached.sessionId);
console.log("page says:", page.result?.result?.value);
console.log("page script can see the cookie:", js.result?.result?.value, "(false is right for httpOnly)");
await send("Target.closeTarget", { targetId: target.targetId });
ws.close();
