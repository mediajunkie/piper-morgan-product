// piper-guards — R6 step 6 (stage 7 of dev/2026/10/03/spec-eval/D-propose-ruleset.md). CIO, 2026-10-12.
//
// Rules: M-1 and M-4 (below). M-1, ported from .claude/hooks/guard_pm_checkout.py (same rules, same messages): refuse git commands that
// discard working-tree state when they target PM's main checkout. PM edits there without committing, so the
// discarded changes are unrecoverable (CLAUDE.md HARD RULE). Target = `git -C <dir>` if given, else the last
// `cd <dir>` earlier in the command, else the session cwd.
//
// Fails OPEN on its own error (the .catch passes the call on): a bug here must never wedge a seat's ordinary
// work, and the settings hook (guard-pm-checkout.sh) still runs behind it during the parallel week.
// Cost: string parsing per Bash call, no subprocess. Benefit: none yet: measuring (prevention guard).
// Review: 2026-12-01. Owner: CIO.

export function splitSegments(cmd) {
  return cmd.split(/&&|\|\||;|\n|\|/)
}

// Minimal POSIX-ish tokenizer: handles '…', "…" and backslash escapes; good enough for git argv.
export function tokenize(seg) {
  const out = []
  let cur = null
  let q = null
  for (let i = 0; i < seg.length; i++) {
    const c = seg[i]
    if (q) {
      if (c === q) q = null
      else if (c === '\\' && q === '"' && i + 1 < seg.length) cur += seg[++i]
      else cur += c
      continue
    }
    if (c === "'" || c === '"') { q = c; if (cur === null) cur = ''; continue }
    if (c === '\\' && i + 1 < seg.length) { cur = (cur ?? '') + seg[++i]; continue }
    if (/\s/.test(c)) { if (cur !== null) { out.push(cur); cur = null } continue }
    cur = (cur ?? '') + c
  }
  if (cur !== null) out.push(cur)
  return out
}

function norm(p) {
  const parts = []
  for (const s of p.split('/')) {
    if (s === '' || s === '.') continue
    if (s === '..') parts.pop()
    else parts.push(s)
  }
  return '/' + parts.join('/')
}

export function resolve(p, base, home) {
  let x = p
  if (x === '~' || x.startsWith('~/')) x = home + x.slice(1)
  return norm(x.startsWith('/') ? x : base + '/' + x)
}

// Returns [{seg, why}] for every segment that would discard state in PM's checkout.
export function findViolations(cmd, cwd, pm, home) {
  const isPm = (p) => p === pm || p.startsWith(pm + '/')
  let base = cwd
  const bad = []
  for (const seg of splitSegments(cmd)) {
    const toks = tokenize(seg)
    if (!toks.length) continue
    if (toks[0] === 'cd' && toks.length > 1) { base = resolve(toks[1], base, home); continue }
    const gi = toks.indexOf('git')
    if (gi < 0) continue
    let rest = toks.slice(gi + 1)
    let tgt = base
    while (rest.length && rest[0].startsWith('-')) {
      if (rest[0] === '-C' && rest.length > 1) { tgt = resolve(rest[1], tgt, home); rest = rest.slice(2); continue }
      if (rest[0] === '-c' && rest.length > 1) { rest = rest.slice(2); continue }
      rest = rest.slice(1)
    }
    if (!rest.length || !isPm(tgt)) continue
    const sub = rest[0]
    const args = rest.slice(1)
    let why = null
    if (sub === 'checkout' && (args.includes('--') || args.includes('.'))) why = 'checkout overwrites working-tree files'
    else if (sub === 'restore' && !args.includes('--staged') && !args.includes('-S')) why = 'restore (without --staged) overwrites working-tree files'
    else if (sub === 'reset' && args.includes('--hard')) why = 'reset --hard discards working-tree changes'
    else if (sub === 'clean' && args.some((a) => a.startsWith('-') && (a.includes('f') || a.includes('x')))) why = 'clean deletes untracked files'
    else if (sub === 'stash' && !(args.length && (args[0] === 'list' || args[0] === 'show'))) why = 'stash removes working-tree changes (and the stack is shared)'
    if (why) bad.push({ seg: seg.trim(), why })
  }
  return bad
}

export function denyMessage(bad, pm) {
  const lines = bad.map((b) => `BLOCKED by piper-guards M-1 (R6): \`${b.seg}\` targets PM's main checkout (${pm}): ${b.why}.`)
  lines.push("PM edits there without committing; discarded changes are unrecoverable (CLAUDE.md HARD RULE).")
  lines.push('Do the work from your own worktree instead. If PM explicitly asked for this, PM runs it.')
  return lines.join('\n')
}

// M-4 (new; no settings hook today): refuse a Projects v2 single-select option-list write. `updateProjectV2Field`
// with `singleSelectOptions` is a FULL replace: omitting existing options wipes every item's value for them, with no
// undo (2026-07-05: 1,175 items lost their sprint). CLAUDE.md "GitHub Projects v2"; skill assign-sprint-safely.
export function isProjectsFullReplace(cmd) {
  return /\bgh\b[^\n]*\bapi\b/.test(cmd) && /updateProjectV2Field/.test(cmd) && /singleSelectOptions/.test(cmd)
}

export const M4_MESSAGE = [
  'BLOCKED by piper-guards M-4 (R6): this GraphQL call rewrites a Projects v2 single-select field\'s option list.',
  '`updateProjectV2Field` with `singleSelectOptions` REPLACES the whole list: any option you leave out is deleted,',
  'and every item assigned to it loses that value, with no undo (2026-07-05: 1,175 sprint assignments wiped).',
  'Add options in the GitHub web UI instead; to change items, use the skill assign-sprint-safely.',
].join('\n')

// ---- shared: git invocations in a command, with the directory each runs in (cd / -C tracked like M-1) ----
export function gitInvocations(cmd, cwd, home) {
  let base = cwd
  const out = []
  for (const seg of splitSegments(cmd)) {
    const toks = tokenize(seg)
    if (!toks.length) continue
    if (toks[0] === 'cd' && toks.length > 1) { base = resolve(toks[1], base, home); continue }
    const gi = toks.indexOf('git')
    if (gi < 0) continue
    let rest = toks.slice(gi + 1)
    let dir = base
    while (rest.length && rest[0].startsWith('-')) {
      if (rest[0] === '-C' && rest.length > 1) { dir = resolve(rest[1], dir, home); rest = rest.slice(2); continue }
      if (rest[0] === '-c' && rest.length > 1) { rest = rest.slice(2); continue }
      rest = rest.slice(1)
    }
    if (!rest.length) continue
    out.push({ seg: seg.trim(), dir, sub: rest[0], args: rest.slice(1) })
  }
  return out
}

// ---- M-2: diff before `git checkout <ref> -- <paths>` / `git restore --source=<ref> <paths>` (SCOPE is not DIRECTION) ----
// Returns [{seg, dir, paths}] for each command that overwrites working-tree paths from a ref.
export function checkoutFromRef(cmd, cwd, home) {
  const hits = []
  for (const g of gitInvocations(cmd, cwd, home)) {
    if (g.sub === 'checkout') {
      const dd = g.args.indexOf('--')
      if (dd > 0 && g.args.slice(0, dd).some((a) => !a.startsWith('-')) && g.args.length > dd + 1) {
        hits.push({ seg: g.seg, dir: g.dir, paths: g.args.slice(dd + 1) })
      }
    } else if (g.sub === 'restore') {
      const hasSource = g.args.some((a) => a === '-s' || a === '--source' || a.startsWith('--source='))
      if (!hasSource || g.args.includes('--staged') || g.args.includes('-S')) continue
      const paths = []
      for (let i = 0; i < g.args.length; i++) {
        const a = g.args[i]
        if (a === '-s' || a === '--source') { i++; continue }
        if (a.startsWith('-')) continue
        paths.push(a)
      }
      if (paths.length) hits.push({ seg: g.seg, dir: g.dir, paths })
    }
  }
  return hits
}

export const hasDiffReviewed = (cmd) => /\bdiff-reviewed\b/.test(cmd)

export function m2Message(h, stat) {
  return [
    `BLOCKED by piper-guards M-2 (diff before checkout): \`${h.seg}\` would overwrite uncommitted changes (git diff HEAD --stat):`,
    stat.trimEnd(),
    'Review it (`git diff HEAD -- <paths>`): checkout from a ref overwrites the working tree and the discarded version is unrecoverable.',
    'Once reviewed, add `diff-reviewed` to the command (e.g. as a trailing comment) to override.',
  ].join('\n')
}

// ---- M-3: mail on main. Parses the command string, so it is not blind to a compound `git add && git commit`
// (check-branch.sh reads the index before the add has run). ----
// Returns [{kind: 'add' | 'commit-all', seg, dir}] for each git invocation that stages mailbox paths (add, mv, rm) or commits everything.
export function mailboxGitOps(cmd, cwd, home) {
  const ops = []
  for (const g of gitInvocations(cmd, cwd, home)) {
    // mv and rm stage too: `git mv inbox/x read/x` slipped past an add-only check on 11-01 (#2251).
    if (g.sub === 'add' || g.sub === 'mv' || g.sub === 'rm') {
      if (g.args.some((a) => !a.startsWith('-') && /(^|\/)mailboxes(\/|$)/.test(a))) ops.push({ kind: 'add', seg: g.seg, dir: g.dir })
    } else if (g.sub === 'commit') {
      if (g.args.some((a) => a === '--all' || /^-[a-zA-Z]*a[a-zA-Z]*$/.test(a))) ops.push({ kind: 'commit-all', seg: g.seg, dir: g.dir })
    }
  }
  return ops
}

export const M3_MESSAGE = (seg, branch) => [
  `BLOCKED by piper-guards M-3 (mail on main): \`${seg}\` stages or commits mailbox files on branch \`${branch}\` (not main).`,
  'Mail is cross-agent infrastructure and lands on main only. Write the memo files, then use scripts/mail-send.sh with every changed path;',
  'it commits straight to origin/main and cleans up your worktree. Do not git add / mv / rm / commit mailboxes/ on a branch;',
  'to file read mail, use plain `mv` (mail-send.sh takes both the old and the new path).',
].join('\n')

// ---- M-5: bearer credentials in Write/Edit content under mailboxes/, docs/, dev/ (public repo; #1845) ----
export function guardedPath(filePath) {
  const m = /^(.*?)\/(mailboxes|docs|dev)\/(.+)$/.exec(String(filePath ?? ''))
  return m ? { root: m[1], rel: m[2] + '/' + m[3] } : null
}

export const M5_MESSAGE = (rel, out) => [
  `BLOCKED by piper-guards M-5 (bearer credential): the new content for ${rel} contains what scripts/mailbox_bearer_lint.py reads as a bearer credential.`,
  out.trim(),
  'Never write a full invite code / API key / token into the repo (it is PUBLIC). Use the masked form: first four, an ellipsis, last four.',
].join('\n')

// ---- M-6: dispatch tier (Agent tool call must set `model`) ----
export const M6_MESSAGE = [
  'BLOCKED by piper-guards M-6 (dispatch tier): this Agent call sets no `model`, so the subagent silently inherits yours.',
  'Set model explicitly (haiku for mechanical work, sonnet for bounded implementation, opus for hard reasoning) and log the tier in your session-log entry for the dispatch.',
].join('\n')
// A fork can't take `model` (it always inherits the parent; Agent input docs, 2.1.296), so it is exempt.
export const isModelUnset = (e) => e.subagent_type !== 'fork' && (e.model === undefined || e.model === null || e.model === '')

// ---- M-9 (prototype): status line text from CI state and briefing age ----
export function statusText({ ci, briefingDays }) {
  const parts = []
  if (ci) parts.push(`CI main: ${ci}`)
  if (briefingDays !== undefined && briefingDays !== null) parts.push(`briefing ${briefingDays}d`)
  return parts.length ? parts.join(' · ') : undefined
}

// M-9: main's CI verdict by scripts/main-ci-status.sh's rule. Per workflow, the newest run that ENDED in success or
// failure (a cancelled or skipped run says nothing about the code); red if any is a failure. 10-19 (Pard, on CXO): the
// first version read `--limit 1` across all workflows and fell back to that run's `status`, so it showed "completed".
// Runs come newest first. Returns undefined when no workflow has a verdict, rather than a word that isn't one.
export function ciVerdict(runs) {
  const seen = new Map()
  for (const r of runs || []) {
    if (seen.has(r.workflowName)) continue
    if (r.conclusion === 'success' || r.conclusion === 'failure') seen.set(r.workflowName, r.conclusion)
  }
  if (!seen.size) return undefined
  const red = [...seen.values()].filter((c) => c === 'failure').length
  return red ? `red (${red} of ${seen.size})` : 'green'
}

// M-9: read main-ci-status.sh's last line ("main-ci-status: 12 workflows: 11 green, 1 red, 0 unmeasured").
export function mainCiSummary(out) {
  const m = /main-ci-status: (\d+) workflows: (\d+) green, (\d+) red, (\d+) unmeasured/.exec(out || '')
  if (!m) return undefined
  const [n, red, unm] = [m[1], m[3], m[4]].map(Number)
  if (red) return `red (${red} of ${n})`
  return unm ? `green (${n - unm} of ${n})` : 'green'
}

// M-5 hook: lint the NEW content (Write: content; Edit: new_string) with the repo's own script, via a temp file.
// Declared at the top of the file because the mod loader requires hooks to be top-level functions.
async function m5($, e, next) {
  const g = guardedPath(e.file_path)
  if (!g) return next(e)
  const text = typeof e.content === 'string' ? e.content : e.new_string
  if (typeof text !== 'string' || !text) return next(e)
  const script = g.root + '/scripts/mailbox_bearer_lint.py'
  if (!(await $.fs.exists(script))) return next(e)
  const tmp = `/tmp/piper-guards-m5-${Date.now()}-${Math.floor(Math.random() * 1e9)}.md`
  await $.fs.write(tmp, text)
  try {
    const r = await $.process.run(['python3', script, '--files', tmp], { cwd: g.root, timeoutMs: 15000 })
    if (r.exitCode === 1 && /bearer credential/.test(r.stdout)) {
      return { deny: M5_MESSAGE(g.rel, r.stdout.split('\n').filter((l) => /FAIL|:\d+ /.test(l)).join('\n').replaceAll(tmp, g.rel)) }
    }
  } finally {
    await $.process.run(['rm', '-f', tmp]).catch(() => {})
  }
  return next(e)
}

// M-9 prototype: status line (CI on main, briefing age), refreshed at most every 10 minutes.
let lastStatusRefresh = 0
async function refresh($) {
  if (Date.now() - lastStatusRefresh < 600000) return
  lastStatusRefresh = Date.now()
  let ci
  let briefingDays
  try {
    // The repo's own definition first (every push workflow, about 30 s), so the status line and main-ci-status can't
    // disagree; the last 100 runs miss low-frequency workflows (9 of 12 seen, 10-19). Then the quick fallback.
    if (await $.fs.exists('scripts/main-ci-status.sh')) {
      const r = await $.process.run(['bash', 'scripts/main-ci-status.sh'], { timeoutMs: 90000 })
      ci = mainCiSummary(r.stdout)
    }
    if (!ci) {
      const r = await $.process.run(['gh', 'run', 'list', '--branch', 'main', '--limit', '100', '--json', 'workflowName,conclusion'], { timeoutMs: 8000 })
      if (r.exitCode === 0) ci = ciVerdict(JSON.parse(r.stdout))
    }
  } catch (_) {}
  try {
    const r = await $.process.run(['git', 'log', '-1', '--format=%ct', '--', 'docs/briefing/BRIEFING-CURRENT-STATE.md'], { timeoutMs: 8000 })
    const t = parseInt(r.stdout.trim(), 10)
    if (r.exitCode === 0 && t) briefingDays = Math.floor((Date.now() / 1000 - t) / 86400)
  } catch (_) {}
  $.ui.status(statusText({ ci, briefingDays }))
}

export function register(on, options) {
  const pm = norm(options.pm_checkout || '/Users/xian/Development/piper-morgan-product')
  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const cmd = String(e.command ?? '')
    if (isProjectsFullReplace(cmd)) return { deny: M4_MESSAGE }
    if (!cmd.includes('git')) return next(e)
    const cwd = norm(String(await $.session.cwd()))
    const home = cwd.match(/^\/Users\/[^/]+/)?.[0] || '/Users/xian'
    const bad = findViolations(cmd, cwd, pm, home)
    if (bad.length) return { deny: denyMessage(bad, pm) }
    return next(e)
  }).catch(async ($, e, next) => next(e))

  // M-2: needs $.process.run (argv, no shell).
  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const cmd = String(e.command ?? '')
    if (!cmd.includes('git') || hasDiffReviewed(cmd)) return next(e)
    const cwd = norm(String(await $.session.cwd()))
    const home = cwd.match(/^\/Users\/[^/]+/)?.[0] || '/Users/xian'
    for (const h of checkoutFromRef(cmd, cwd, home)) {
      const r = await $.process.run(['git', 'diff', 'HEAD', '--stat', '--', ...h.paths], { cwd: h.dir, timeoutMs: 10000 })
      if (r.exitCode === 0 && r.stdout.trim()) return { deny: m2Message(h, r.stdout) }
    }
    return next(e)
  }).catch(async ($, e, next) => next(e))

  // M-3
  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const cmd = String(e.command ?? '')
    if (!cmd.includes('git')) return next(e)
    const cwd = norm(String(await $.session.cwd()))
    const home = cwd.match(/^\/Users\/[^/]+/)?.[0] || '/Users/xian'
    for (const op of mailboxGitOps(cmd, cwd, home)) {
      const b = await $.process.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], { cwd: op.dir, timeoutMs: 10000 })
      const branch = b.stdout.trim()
      if (b.exitCode !== 0 || !branch || branch === 'main') continue
      if (op.kind === 'commit-all') {
        const s = await $.process.run(['git', 'status', '--porcelain', 'mailboxes/'], { cwd: op.dir, timeoutMs: 10000 })
        if (s.exitCode !== 0 || !s.stdout.trim()) continue
      }
      return { deny: M3_MESSAGE(op.seg, branch) }
    }
    return next(e)
  }).catch(async ($, e, next) => next(e))

  // M-5: lint the NEW content (Write: content; Edit: new_string) with the repo's own script, via a temp file.
  on('tool.call', { tool: 'Write' }, m5).catch(async ($, e, next) => next(e))
  on('tool.call', { tool: 'Edit' }, m5).catch(async ($, e, next) => next(e))

  // M-6
  on('tool.call', { tool: 'Agent' }, async ($, e, next) => {
    if (isModelUnset(e)) return { deny: M6_MESSAGE }
    return next(e)
  }).catch(async ($, e, next) => next(e))

  // M-9 prototype: status line (CI on main, briefing age). Refreshed at most every 10 minutes, never awaited:
  // the CI read takes about 30 s and must not hold up a session start or a Bash call.
  on('session.start', async ($, e, next) => { refresh($).catch(() => {}); return next(e) }).catch(async ($, e, next) => next(e))
  on('tool.call', { tool: 'Bash' }, async ($, e, next) => { refresh($).catch(() => {}); return next(e) }).catch(async ($, e, next) => next(e))
}
