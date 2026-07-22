#!/usr/bin/env python3
"""Build a self-contained HTML calendar GUI from the editorial calendar CSV.

Reads docs/internal/planning/comms/editorial-calendar.csv and emits a single
openable HTML file (data embedded inline — no server needed) with a month-grid
layout: click any day to see what's planned/published that day.

Regenerate after calendar changes:  python3 scripts/build-editorial-calendar-view.py

Output: docs/internal/planning/comms/editorial-calendar-view.html
"""

import csv, json, os, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "docs/internal/planning/comms/editorial-calendar.csv")
OUT_PATH = os.path.join(ROOT, "docs/internal/planning/comms/editorial-calendar-view.html")


def main():
    with open(CSV_PATH) as f:
        rows = list(csv.DictReader(f))
    posts = []
    for r in rows:
        posts.append({k: (r.get(k) or "").strip() for k in r.keys()})
    generated = (
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M") if False else "(regenerate to stamp)"
    )
    data_json = json.dumps(posts, ensure_ascii=False)
    html = (
        HTML_TEMPLATE.replace("__DATA__", data_json)
        .replace("__GENERATED__", generated)
        .replace("__COUNT__", str(len(posts)))
    )
    with open(OUT_PATH, "w") as f:
        f.write(html)
    print(f"wrote {OUT_PATH} ({len(posts)} posts)")


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Editorial Calendar — Piper Morgan</title>
<style>
  :root { --pub:#2e7d32; --pub-bg:#e8f5e9; --queued:#1565c0; --queued-bg:#e3f2fd; --drafted:#e65100; --drafted-bg:#fff3e0; --fg:#1a1a1a; --muted:#666; --line:#ddd; }
  * { box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; color: var(--fg); margin: 0; padding: 20px; background:#fafafa; }
  h1 { font-size: 20px; margin: 0 0 4px; }
  .sub { color: var(--muted); font-size: 13px; margin-bottom: 14px; }
  .toolbar { display:flex; align-items:center; gap:12px; margin-bottom:12px; flex-wrap:wrap; }
  .toolbar button { font-size:14px; padding:6px 12px; border:1px solid var(--line); background:#fff; border-radius:6px; cursor:pointer; }
  .toolbar button:hover { background:#f0f0f0; }
  #monthLabel { font-size:17px; font-weight:600; min-width:170px; text-align:center; }
  .legend { display:flex; gap:14px; font-size:12px; color:var(--muted); flex-wrap:wrap; }
  .legend span { display:inline-flex; align-items:center; gap:5px; }
  .dot { width:10px; height:10px; border-radius:50%; display:inline-block; }
  .layout { display:flex; gap:18px; align-items:flex-start; flex-wrap:wrap; }
  .cal { flex: 1 1 640px; }
  table { border-collapse: collapse; width:100%; background:#fff; border:1px solid var(--line); }
  th { font-size:11px; text-transform:uppercase; letter-spacing:.04em; color:var(--muted); padding:6px; border:1px solid var(--line); background:#f7f7f7; }
  td { border:1px solid var(--line); vertical-align:top; height:88px; width:14.28%; padding:4px; cursor:pointer; }
  td.empty { background:#fbfbfb; cursor:default; }
  td:hover:not(.empty) { background:#f5f9ff; }
  td.sel { outline:2px solid #1565c0; outline-offset:-2px; }
  .daynum { font-size:12px; color:var(--muted); }
  td.today .daynum { color:#c62828; font-weight:700; }
  .chip { display:block; font-size:10.5px; line-height:1.25; margin-top:3px; padding:2px 4px; border-radius:4px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; border-left:3px solid; }
  .chip.published { background:var(--pub-bg); border-color:var(--pub); }
  .chip.queued { background:var(--queued-bg); border-color:var(--queued); }
  .chip.drafted { background:var(--drafted-bg); border-color:var(--drafted); }
  .detail { flex: 1 1 320px; background:#fff; border:1px solid var(--line); border-radius:8px; padding:16px; min-height:200px; position:sticky; top:20px; }
  .detail h2 { font-size:15px; margin:0 0 8px; }
  .detail .empty-msg { color:var(--muted); font-size:13px; }
  .post { border-top:1px solid var(--line); padding:10px 0; }
  .post:first-of-type { border-top:none; }
  .post .ttl { font-weight:600; font-size:14px; }
  .badge { display:inline-block; font-size:10px; padding:1px 6px; border-radius:10px; margin-right:5px; text-transform:uppercase; letter-spacing:.03em; }
  .badge.published { background:var(--pub-bg); color:var(--pub); }
  .badge.queued { background:var(--queued-bg); color:var(--queued); }
  .badge.drafted { background:var(--drafted-bg); color:var(--drafted); }
  .badge.theme { background:#ede7f6; color:#5e35b1; }
  .kv { font-size:12px; color:#333; margin:5px 0; }
  .kv b { color:var(--muted); font-weight:600; }
  .post a { color:#1565c0; text-decoration:none; font-size:12px; }
  .post a:hover { text-decoration:underline; }
  .links { margin-top:5px; display:flex; gap:10px; flex-wrap:wrap; }
  .unsched { margin-top:20px; font-size:12px; }
  .unsched summary { cursor:pointer; color:var(--muted); }
  .unsched li { margin:3px 0; }
</style>
</head>
<body>
<h1>Editorial Calendar</h1>
<div class="sub">__COUNT__ entries · click any day to see what's planned / was published · regenerate: <code>python3 scripts/build-editorial-calendar-view.py</code></div>
<div class="toolbar">
  <button id="prev">‹ Prev</button>
  <span id="monthLabel"></span>
  <button id="next">Next ›</button>
  <button id="today">Today</button>
  <div class="legend">
    <span><i class="dot" style="background:var(--pub)"></i>published</span>
    <span><i class="dot" style="background:var(--queued)"></i>queued</span>
    <span><i class="dot" style="background:var(--drafted)"></i>drafted</span>
  </div>
</div>
<div class="layout">
  <div class="cal" id="cal"></div>
  <div class="detail" id="detail"><div class="empty-msg">Select a day to see its post(s).</div></div>
</div>
<div class="unsched" id="unsched"></div>
<script>
const POSTS = __DATA__;
const byDate = {};
const unscheduled = [];
for (const p of POSTS) {
  const d = (p.pubDate || "").trim();
  if (/^\d{4}-\d{2}-\d{2}$/.test(d)) { (byDate[d] = byDate[d] || []).push(p); }
  else { unscheduled.push(p); }
}
const dates = Object.keys(byDate).sort();
const MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"];
function ymd(y,m,d){ return `${y}-${String(m+1).padStart(2,"0")}-${String(d).padStart(2,"0")}`; }
const todayStr = new Date().toISOString().slice(0,10);
// default to current month if in range, else latest post month
let cur;
{ const t = new Date(); cur = {y:t.getFullYear(), m:t.getMonth()};
  if (dates.length) { const last = dates[dates.length-1]; const first = dates[0];
    const tk = ymd(cur.y,cur.m,1);
    if (tk < first.slice(0,7)+"-01") cur = {y:+first.slice(0,4), m:+first.slice(5,7)-1};
    if (tk > last.slice(0,7)+"-01") cur = {y:+last.slice(0,4), m:+last.slice(5,7)-1};
  }
}
let selected = null;
const cal = document.getElementById("cal"), detail = document.getElementById("detail"), monthLabel = document.getElementById("monthLabel");
function statusOf(p){ const s=(p.status||"").toLowerCase(); if(s==="distributed") return "published"; return ["published","queued","drafted"].includes(s)?s:"drafted"; }
function esc(s){ return (s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }
function renderMonth(){
  monthLabel.textContent = MONTHS[cur.m] + " " + cur.y;
  const first = new Date(cur.y, cur.m, 1), startDow = first.getDay();
  const days = new Date(cur.y, cur.m+1, 0).getDate();
  let html = "<table><thead><tr>" + ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"].map(d=>`<th>${d}</th>`).join("") + "</tr></thead><tbody><tr>";
  for (let i=0;i<startDow;i++) html += '<td class="empty"></td>';
  for (let d=1; d<=days; d++) {
    const key = ymd(cur.y, cur.m, d);
    const posts = byDate[key] || [];
    const cls = [(key===todayStr?"today":""), (key===selected?"sel":"")].filter(Boolean).join(" ");
    html += `<td class="${cls}" data-key="${key}"><span class="daynum">${d}</span>`;
    for (const p of posts) html += `<span class="chip ${statusOf(p)}" title="${esc(p.title)}">${esc(p.title)}</span>`;
    html += "</td>";
    if ((startDow + d) % 7 === 0 && d !== days) html += "</tr><tr>";
  }
  const cells = (startDow + days); const rem = (7 - (cells % 7)) % 7;
  for (let i=0;i<rem;i++) html += '<td class="empty"></td>';
  html += "</tr></tbody></table>";
  cal.innerHTML = html;
  cal.querySelectorAll("td[data-key]").forEach(td => td.onclick = () => { selected = td.dataset.key; renderMonth(); renderDetail(selected); });
}
function linkRow(p){
  const links=[];
  if (p.blogURL) links.push(`<a href="${esc(p.blogURL)}" target="_blank">blog ↗</a>`);
  if (p.mediumURL) links.push(`<a href="${esc(p.mediumURL)}" target="_blank">Medium ↗</a>`);
  if (p.linkedinURL) links.push(`<a href="${esc(p.linkedinURL)}" target="_blank">LinkedIn ↗</a>`);
  return links.length ? `<div class="links">${links.join("")}</div>` : "";
}
function renderDetail(key){
  const posts = byDate[key] || [];
  if (!posts.length) { detail.innerHTML = `<h2>${key}</h2><div class="empty-msg">Nothing scheduled or published this day.</div>`; return; }
  let html = `<h2>${key}</h2>`;
  for (const p of posts) {
    const s = statusOf(p);
    html += `<div class="post"><div class="ttl">${esc(p.title)}</div>`;
    html += `<div style="margin:5px 0"><span class="badge ${s}">${s}</span>`;
    if (p.theme) html += `<span class="badge theme">${esc(p.theme)}</span>`;
    html += `</div>`;
    if (p.workDate) html += `<div class="kv"><b>work:</b> ${esc(p.workDate)}${p.endWorkDate?(" – "+esc(p.endWorkDate)):""}</div>`;
    if (p.canonicalSite) html += `<div class="kv"><b>canonical:</b> ${esc(p.canonicalSite)}</div>`;
    if (p.notes) html += `<div class="kv"><b>notes:</b> ${esc(p.notes)}</div>`;
    if (p.draftPath) html += `<div class="kv"><b>draft:</b> ${esc(p.draftPath)}</div>`;
    html += linkRow(p) + `</div>`;
  }
  detail.innerHTML = html;
}
document.getElementById("prev").onclick = ()=>{ cur.m--; if(cur.m<0){cur.m=11;cur.y--;} renderMonth(); };
document.getElementById("next").onclick = ()=>{ cur.m++; if(cur.m>11){cur.m=0;cur.y++;} renderMonth(); };
document.getElementById("today").onclick = ()=>{ const t=new Date(); cur={y:t.getFullYear(),m:t.getMonth()}; selected=todayStr; renderMonth(); renderDetail(todayStr); };
// unscheduled list
if (unscheduled.length) {
  const items = unscheduled.map(p=>`<li><span class="badge ${statusOf(p)}">${statusOf(p)}</span> ${esc(p.title)}${p.theme?(" · "+esc(p.theme)):""}</li>`).join("");
  document.getElementById("unsched").innerHTML = `<details><summary>${unscheduled.length} entries with no pubDate (unscheduled / drafts)</summary><ul>${items}</ul></details>`;
}
renderMonth();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
