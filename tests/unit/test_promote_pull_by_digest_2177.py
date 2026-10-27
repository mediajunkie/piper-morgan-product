"""#2177 (Arch's three conditions, HOST concurs, 2026-10-25): alpha promotes staging's
image by digest, never by tag.

1. The digest is read from every started machine; none, several, or a machine with no
   digest refuses (""), never falling back to the tag.
2. The copy step pulls `repo@sha256:…` and refuses unless the pulled RepoDigests include it.
3. The served-sha attestation is unchanged.
"""

import os
import subprocess
from pathlib import Path

import yaml

from scripts.read_staging_image_digest import pinned_image

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "fly-deploy.yml"
D1 = "sha256:" + "a" * 64
D2 = "sha256:" + "b" * 64
TAG = "registry.fly.io/piper-morgan-staging:deployment-01M5TWP04GW77KF0QZKQXD3CD6"


def _m(state="started", image=TAG, digest=D1):
    m = {"state": state, "config": {"image": image}}
    if digest is not None:
        m["image_ref"] = {
            "registry": "registry.fly.io",
            "repository": "piper-morgan-staging",
            "tag": "deployment-01M5TWP04GW77KF0QZKQXD3CD6",
            "digest": digest,
        }
    return m


class TestPinnedImage:
    def test_agreeing_machines_give_repo_at_digest(self):
        assert (
            pinned_image({"Machines": [_m(), _m()]}) == f"registry.fly.io/piper-morgan-staging@{D1}"
        )

    def test_stopped_machines_are_ignored(self):
        assert pinned_image({"Machines": [_m(), _m(state="stopped", digest=D2)]}).endswith(D1)

    def test_no_started_machine_refuses(self):
        assert pinned_image({"Machines": [_m(state="stopped")]}) == ""
        assert pinned_image({}) == ""

    def test_disagreeing_digests_refuse(self):
        assert pinned_image({"Machines": [_m(), _m(digest=D2)]}) == ""

    def test_a_machine_without_a_digest_refuses_and_never_falls_back_to_the_tag(self):
        assert pinned_image({"Machines": [_m(), _m(digest=None)]}) == ""
        assert pinned_image({"Machines": [_m(digest="")]}) == ""
        assert pinned_image({"Machines": [_m(digest="sha256:short")]}) == ""

    def test_an_image_already_named_by_digest_keeps_its_repository(self):
        img = f"registry.fly.io/piper-morgan-staging@{D1}"
        assert pinned_image({"Machines": [_m(image=img)]}) == img

    def test_cli_prints_empty_on_bad_json(self):
        out = subprocess.run(
            ["python3", str(ROOT / "scripts/read_staging_image_digest.py")],
            input="not json",
            capture_output=True,
            text=True,
            check=True,
        )
        assert out.stdout.strip() == ""


def _steps():
    steps = yaml.safe_load(WORKFLOW.read_text())["jobs"]["promote-alpha"]["steps"]
    return {s.get("name"): s for s in steps}


class TestWorkflow:
    def test_both_staging_reads_use_the_digest_reader(self):
        run = _steps()["Read the image AND the sha currently running on staging"]["run"]
        assert run.count("python3 scripts/read_staging_image_digest.py") == 2
        assert 'config",{}).get("image"' not in run  # the tag read is gone

    def test_the_job_checks_out_the_repo_before_reading(self):
        steps = yaml.safe_load(WORKFLOW.read_text())["jobs"]["promote-alpha"]["steps"]
        assert "actions/checkout" in steps[0]["uses"]

    def test_attestation_still_expects_stagings_sha(self):
        text = WORKFLOW.read_text()
        assert "EXPECTED: ${{ steps.img.outputs.sha }}" in text


PUSHED = "sha256:" + "c" * 64


def _copy_run(tmp_path, src, repo_digests):
    """Run the copy step's bash with a stub docker that records calls (its push prints a
    digest line, as `docker push` does; #2181 deploys by it)."""
    bindir = tmp_path / "bin"
    bindir.mkdir()
    log = tmp_path / "docker.log"
    stub = bindir / "docker"
    stub.write_text(
        "#!/bin/bash\n"
        f'echo "$@" >> "{log}"\n'
        'if [ "$1" = "image" ] && [ "$2" = "inspect" ]; then\n'
        f"  printf '%s\\n' {' '.join(repr(d) for d in repo_digests)}\n"
        "fi\n"
        'if [ "$1" = "push" ]; then\n'
        f'  echo "promote-4f487d494835: digest: {PUSHED} size: 3461"\n'
        "fi\n"
        "exit 0\n"
    )
    stub.chmod(0o755)
    run = _steps()["Copy that exact image into alpha's own registry repository"]["run"]
    out_file = tmp_path / "out"
    env = {
        **os.environ,
        "PATH": f"{bindir}:{os.environ['PATH']}",
        "SRC": src,
        "SHA": "4f487d49483559d667988c8574ec93a7e5cfd75e",
        "STAGING_TOKEN": "fake-token-s",
        "ALPHA_TOKEN": "fake-token-a",
        "GITHUB_OUTPUT": str(out_file),
    }
    r = subprocess.run(["bash", "-e", "-c", run], env=env, capture_output=True, text=True)
    return (
        r,
        (log.read_text() if log.exists() else ""),
        (out_file.read_text() if out_file.exists() else ""),
    )


class TestCopyStep:
    SRC = f"registry.fly.io/piper-morgan-staging@{D1}"

    def test_pulls_by_digest_and_pushes_when_the_digest_matches(self, tmp_path):
        r, log, out = _copy_run(tmp_path, self.SRC, [self.SRC])
        assert r.returncode == 0, r.stdout + r.stderr
        assert f"pull {self.SRC}" in log
        assert "push registry.fly.io/piper-morgan:promote-4f487d494835" in log
        assert f"ref=registry.fly.io/piper-morgan@{PUSHED}" in out  # #2181: the pushed digest

    def test_a_pulled_image_with_another_digest_refuses_before_push(self, tmp_path):
        other = f"registry.fly.io/piper-morgan-staging@{D2}"
        r, log, out = _copy_run(tmp_path, self.SRC, [other])
        assert r.returncode != 0
        assert "Digest mismatch" in r.stdout
        assert " push " not in f" {log}" and "push registry" not in log
        assert out == ""

    def test_a_tag_refuses_before_any_pull(self, tmp_path):
        r, log, _ = _copy_run(tmp_path, TAG, [TAG])
        assert r.returncode != 0
        assert "Not a digest" in r.stdout
        assert "pull" not in log
