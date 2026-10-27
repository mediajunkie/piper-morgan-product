"""#2181 (Arch ruling, 2026-10-27): alpha is deployed by the digest its own push produced,
never by the promote-<sha12> tag.

1. The digest comes from the push's `digest: sha256:… size: N` line, else from the pushed
   ref's RepoDigests for registry.fly.io/piper-morgan.
2. No digest readable: refuse before `flyctl deploy`, never fall back to the tag.
3. It need not equal staging's digest (a re-push can change the manifest digest).
4. The deploy line uses steps.copy.outputs.ref.
"""

import os
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "fly-deploy.yml"
STAGING = "sha256:" + "a" * 64
PUSHED = "sha256:" + "c" * 64
SRC = f"registry.fly.io/piper-morgan-staging@{STAGING}"
COPY_STEP = "Copy that exact image into alpha's own registry repository"
DEPLOY_STEP = "Promote that exact image to alpha"


def _steps():
    steps = yaml.safe_load(WORKFLOW.read_text())["jobs"]["promote-alpha"]["steps"]
    return {s.get("name"): s for s in steps}


def _copy_run(tmp_path, push_line, dst_repo_digests=()):
    """Run the copy step with a stub docker: the pull's RepoDigests include SRC (condition 2
    holds), the push prints `push_line`, and an inspect of the pushed ref returns
    `dst_repo_digests`."""
    bindir = tmp_path / "bin"
    bindir.mkdir()
    log = tmp_path / "docker.log"
    stub = bindir / "docker"
    dst_lines = " ".join(repr(d) for d in dst_repo_digests) or "''"
    stub.write_text(
        "#!/bin/bash\n"
        f'echo "$@" >> "{log}"\n'
        'if [ "$1" = "image" ] && [ "$2" = "inspect" ]; then\n'
        f'  if [ "${{@: -1}}" = "{SRC}" ]; then echo "{SRC}"; else printf \'%s\\n\' {dst_lines}; fi\n'
        "fi\n"
        f'if [ "$1" = "push" ]; then echo {push_line!r}; fi\n'
        "exit 0\n"
    )
    stub.chmod(0o755)
    out_file = tmp_path / "out"
    env = {
        **os.environ,
        "PATH": f"{bindir}:{os.environ['PATH']}",
        "SRC": SRC,
        "SHA": "36bdcf09bb06433d7d3db6a3deb569571eee4ef3",
        "STAGING_TOKEN": "fake-token-s",
        "ALPHA_TOKEN": "fake-token-a",
        "GITHUB_OUTPUT": str(out_file),
    }
    r = subprocess.run(
        ["bash", "-e", "-c", _steps()[COPY_STEP]["run"]], env=env, capture_output=True, text=True
    )
    return r, (out_file.read_text() if out_file.exists() else "")


class TestPushedDigest:
    def test_the_ref_is_the_digest_from_the_push_line(self, tmp_path):
        r, out = _copy_run(tmp_path, f"promote-36bdcf09bb06: digest: {PUSHED} size: 3461")
        assert r.returncode == 0, r.stdout + r.stderr
        assert out.strip() == f"ref=registry.fly.io/piper-morgan@{PUSHED}"

    def test_it_need_not_equal_stagings_digest(self, tmp_path):
        r, out = _copy_run(tmp_path, f"promote-36bdcf09bb06: digest: {PUSHED} size: 3461")
        assert r.returncode == 0
        assert STAGING not in out

    def test_without_a_push_line_the_pushed_refs_repo_digest_is_used(self, tmp_path):
        r, out = _copy_run(
            tmp_path,
            "pushed",
            dst_repo_digests=[SRC, f"registry.fly.io/piper-morgan@{PUSHED}"],
        )
        assert r.returncode == 0, r.stdout + r.stderr
        assert out.strip() == f"ref=registry.fly.io/piper-morgan@{PUSHED}"

    def test_no_readable_digest_refuses_and_never_emits_the_tag(self, tmp_path):
        r, out = _copy_run(tmp_path, "pushed", dst_repo_digests=[SRC])
        assert r.returncode != 0
        assert "No pushed digest" in r.stdout
        assert out == ""

    def test_a_short_digest_is_not_a_digest(self, tmp_path):
        r, out = _copy_run(tmp_path, "promote-x: digest: sha256:abc size: 1")
        assert r.returncode != 0
        assert out == ""


class TestDeployStep:
    def test_deploy_uses_the_copy_steps_ref(self):
        run = _steps()[DEPLOY_STEP]["run"]
        assert '--image "${{ steps.copy.outputs.ref }}"' in run
        assert "promote-" not in run

    def test_the_emitted_ref_is_digest_shaped_never_the_tag(self):
        run = _steps()[COPY_STEP]["run"]
        assert 'echo "ref=$ref" >> "$GITHUB_OUTPUT"' in run
        assert 'ref="registry.fly.io/piper-morgan@$pushed_digest"' in run
        assert 'echo "ref=$DST"' not in run
