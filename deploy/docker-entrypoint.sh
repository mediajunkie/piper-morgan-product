#!/bin/bash
# docker-entrypoint.sh — root-phase volume preparation, then privilege drop (#1656).
#
# WHY THIS EXISTS: Fly mounts volumes root-owned at their destination (/data).
# The app runs as the non-root user `piper` (created in the Dockerfile), so
# with the old `USER piper` directive the very first upload's
# `mkdir /data/uploads/...` raised EACCES and EVERY upload 500'd (issue #1656;
# broken silently since the #1401 volume cutover — the #1401 "live durability
# proof" ran via `fly ssh`, which is a ROOT shell, so it verified root's
# access, not the app user's).
#
# THE FIX: start as root, prepare UPLOAD_DIR (create + chown to piper), then
# drop to piper via setpriv (util-linux, present in slim-bookworm) and exec
# the real command. The app process itself never runs as root.
#
# If the container is started with a non-root user anyway (e.g.
# `docker run --user`), there is nothing we can prepare — exec straight
# through and let the boot-time writability probe (web/startup.py
# UploadStorageProbePhase) report loudly if the mount is unusable.
set -e

if [ "$(id -u)" = "0" ]; then
    if [ -n "${UPLOAD_DIR:-}" ]; then
        mkdir -p "$UPLOAD_DIR"
        # -R: also repairs anything root left behind inside the dir (e.g. the
        # #1401 probe file written via fly ssh). The dir is small by design.
        chown -R piper:piper "$UPLOAD_DIR"
    fi
    exec setpriv --reuid=piper --regid=piper --init-groups --inh-caps=-all "$@"
fi

exec "$@"
