import { expect, test } from 'claude-code/testing'
import { mailboxGitOps } from '../hooks/register.js'

const WT = '/Users/xian/Development/piper-morgan-worktrees/cio'
const H = '/Users/xian'
const ops = (cmd: string) => mailboxGitOps(cmd, WT, H).map((o) => o.kind)

test('M-3 parses mailbox staging, including the compound idiom', async () => {
  expect(ops('git add mailboxes/exec/inbox/m.md && git commit -m x')).toEqual(['add'])
  expect(ops('git add "mailboxes/exec/inbox/m.md"')).toEqual(['add'])
  expect(ops('git add -A mailboxes/')).toEqual(['add'])
  expect(ops('git commit -am "x"')).toEqual(['commit-all'])
  expect(ops('git commit --all -m x')).toEqual(['commit-all'])
  expect(ops('git mv mailboxes/cio/inbox/m.md mailboxes/cio/read/m.md')).toEqual(['add'])
  expect(ops('git rm -q mailboxes/cio/inbox/m.md')).toEqual(['add'])
})

test('M-3 ignores everything else', async () => {
  expect(ops('git add docs/a.md && git commit -m x')).toEqual([])
  expect(ops('git commit -m "mail: add mailboxes/x"')).toEqual([])
  expect(ops('scripts/mail-send.sh "mail(cio): s" mailboxes/exec/inbox/m.md')).toEqual([])
  expect(ops('git status')).toEqual([])
  expect(ops('mv mailboxes/cio/inbox/m.md mailboxes/cio/read/m.md')).toEqual([])
  expect(ops('git mv docs/a.md docs/b.md')).toEqual([])
})

const run = (stdout: string, exitCode = 0) => ({ exitCode, stdout, stderr: '', isStdoutTruncated: false, isStderrTruncated: false })

test('M-3 hook denies off main, allows on main', async ($, on) => {
  let branch = 'claude/cio-cycle'
  on('session.cwd', () => ({ value: WT }))
  on('process.run', () => ({ value: run(branch + '\n') }))
  on('tool.call', () => ({ result: 'ran' }))
  const denied: any = await $.tool.call({ tool: 'Bash', command: 'git add mailboxes/a/inbox/m.md && git commit -m x' })
  expect(denied.deny).toMatch(/BLOCKED by piper-guards M-3/)
  expect(denied.deny).toMatch(/mail-send\.sh/)
  expect(await $.tool.call({ tool: 'Bash', command: 'git add docs/a.md' })).toEqual({ result: 'ran' })
  branch = 'main'
  expect(await $.tool.call({ tool: 'Bash', command: 'git add mailboxes/a/inbox/m.md' })).toEqual({ result: 'ran' })
})

test('M-3 commit -a only denies when mailboxes/ is dirty', async ($, on) => {
  let porcelain = ' M mailboxes/a/MANIFEST.md\n'
  on('session.cwd', () => ({ value: WT }))
  on('process.run', (_: any, e: any) => ({ value: run(e.argv[1] === 'rev-parse' ? 'claude/cio-cycle\n' : porcelain) }))
  on('tool.call', () => ({ result: 'ran' }))
  const denied: any = await $.tool.call({ tool: 'Bash', command: 'git commit -am x' })
  expect(denied.deny).toMatch(/M-3/)
  porcelain = ''
  expect(await $.tool.call({ tool: 'Bash', command: 'git commit -am x' })).toEqual({ result: 'ran' })
})
