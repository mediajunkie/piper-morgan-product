#!/bin/bash
# Issue 2386, acceptance row 2 (run layer): two throwaway stacks side by side on one machine.
# Built to Arch's seven conditions (issue comment of 2026-11-16 11:51 PT). It needs CIO's go too.
#
# What it never does: `down -v`; a compose command without -p, -f and --project-directory;
# a pull; anything to the shared containers piper-postgres, piper-redis, piper-chromadb or the
# volume piper_postgres_data_v1. On any failed check it STOPS where it is and prints the state.
# It does not clean up after a failure.
#
# Usage: two_stack_run_2386.sh <path to docker-compose.yml> <work folder (must exist, empty)>
set -euo pipefail

COMPOSE_SRC="$1"
WORK="$2"
SHARED_CONTAINERS="piper-postgres piper-redis piper-chromadb"
SHARED_VOLUME="piper_postgres_data_v1"

say() { printf '%s\n' "$*"; }
stop() {
  say ""
  say "STOPPED: $*"
  say "State left as it is. Containers now:"
  docker ps -a --format '  {{.Names}}  {{.Status}}' | grep -E 't2386|piper-' || true
  say "Volumes now:"
  docker volume ls --format '  {{.Name}}' | grep -E 't2386|piper_postgres' || true
  exit 1
}

[ -f "$COMPOSE_SRC" ] || stop "no compose file at the path given"
[ -d "$WORK" ] || stop "the work folder does not exist"
[ -z "$(ls -A "$WORK")" ] || stop "the work folder is not empty"

# ---- stacks -----------------------------------------------------------------------------
# name : folder : postgres port : redis port : chroma port
stack_dir()   { echo "$WORK/$1"; }
port_pg()     { case "$1" in t2386a) echo 5561 ;; t2386b) echo 5562 ;; esac; }
port_redis()  { case "$1" in t2386a) echo 6461 ;; t2386b) echo 6462 ;; esac; }
port_chroma() { case "$1" in t2386a) echo 8161 ;; t2386b) echo 8162 ;; esac; }

make_folder() {  # make_folder <folder> <stack>
  mkdir "$1"
  cp "$COMPOSE_SRC" "$1/docker-compose.yml"
  # Condition 7: only the stack name and the three ports.
  printf 'PIPER_STACK=%s\nPOSTGRES_PORT=%s\nREDIS_PORT=%s\nCHROMADB_PORT=%s\n' \
    "$2" "$(port_pg "$2")" "$(port_redis "$2")" "$(port_chroma "$2")" > "$1/.env"
}

# Condition 1: every compose command names its stack three ways. Clean environment, so
# nothing from this shell reaches the render.
dc() {  # dc <stack> <folder> <compose args...>
  local stack="$1" dir="$2"; shift 2
  env -i PATH="$PATH" HOME="$HOME" docker compose -p "$(project "$stack")" -f "$dir/docker-compose.yml" \
    --project-directory "$dir" --env-file "$dir/.env" "$@"
}

# The project is named in full (CIO's condition 1: it must match ^t2386[ab]-). It is the name
# the file itself gives a stack called t2386a, passed with -p so nothing depends on the folder.
project() { echo "$1-morgan-stable"; }
FORBIDDEN_PORTS="5433 6379 8000 8001 8082 80 5434 6380 8010"

port_free() { ! (exec 3<>"/dev/tcp/127.0.0.1/$1") >/dev/null 2>&1; }

shared_state() {
  for c in $SHARED_CONTAINERS; do
    docker inspect -f '{{.Name}} {{.Id}} started {{.State.StartedAt}} {{range .Mounts}}{{.Type}}:{{.Source}}->{{.Destination}} {{end}}' "$c"
  done
  docker volume inspect -f "$SHARED_VOLUME created {{.CreatedAt}}" "$SHARED_VOLUME"
}

# ---- the guard (conditions 4 and Lead's plan step 2) -------------------------------------
guard_render() {  # guard_render <stack> <folder>
  # Every check reads a captured variable through a here-string, never a pipe into
  # `grep -q`: under pipefail an early-exiting grep can break the pipe and hide a match.
  local stack="$1" dir="$2" cfg bad
  cfg="$(dc "$stack" "$dir" config)" || stop "guard: the config for $stack did not render"
  grep -q "^name: $(project "$stack")\$" <<<"$cfg" || stop "guard: project name for $stack is not $(project "$stack")"
  grep -Eq '^name: t2386[ab]-' <<<"$cfg" || stop "guard: the project name does not match ^t2386[ab]-"
  if grep -Eq '(container_name|name): piper' <<<"$cfg"; then stop "guard: $stack renders a name that starts with piper"; fi
  bad="$(grep 'container_name:' <<<"$cfg" | grep -v "container_name: $stack-" || true)"
  [ -z "$bad" ] || stop "guard: a container name in $stack does not start with $stack-"
  [ "$(grep -c 'container_name:' <<<"$cfg")" = "7" ] || stop "guard: $stack does not render seven container names"
  grep -q "name: ${stack}_postgres_data_v1\$" <<<"$cfg" || stop "guard: volume name for $stack is wrong"
  grep -q "name: ${stack}-network\$" <<<"$cfg" || stop "guard: network name for $stack is wrong"
  bad="$(grep -E '^[[:space:]]+source: /' <<<"$cfg" | grep -v "source: $dir" | grep -v 'source: /var/run/docker.sock' || true)"
  [ -z "$bad" ] || stop "guard: a bind path in $stack is outside its throwaway folder"
  if grep -q "name: piper_postgres_data_v1\$" <<<"$cfg"; then stop "guard: $stack renders the shared volume name"; fi
  if grep -q "container_name: piper-" <<<"$cfg"; then stop "guard: $stack renders a shared container name"; fi
  if grep -q "name: piper-network\$" <<<"$cfg"; then stop "guard: $stack renders the shared network name"; fi
  bad="$(grep -E 'ENCRYPTION_MASTER_KEY: ' <<<"$cfg" | grep -v 'ENCRYPTION_MASTER_KEY: ""' || true)"
  [ -z "$bad" ] || stop "guard: a key value reached the render"
  return 0
}

guard_before_up() {  # guard_before_up <stack> <folder>
  local stack="$1" dir="$2" containers networks volumes
  guard_render "$stack" "$dir"
  for p in "$(port_pg "$stack")" "$(port_redis "$stack")" "$(port_chroma "$stack")"; do
    for f in $FORBIDDEN_PORTS; do [ "$p" != "$f" ] || stop "guard: port $p is on the forbidden list"; done
    port_free "$p" || stop "guard: port $p for $stack is in use"
  done
  containers="$(docker ps -a --format '{{.Names}}')" || stop "guard: could not list containers"
  networks="$(docker network ls --format '{{.Name}}')" || stop "guard: could not list networks"
  volumes="$(docker volume ls --format '{{.Name}}')" || stop "guard: could not list volumes"
  if grep -q "^$stack-" <<<"$containers"; then stop "guard: a container named $stack-* already exists"; fi
  if grep -q "^$stack-network\$" <<<"$networks"; then stop "guard: network $stack-network already exists"; fi
  if grep -q "^${stack}_postgres_data_v1\$" <<<"$volumes"; then stop "guard: volume ${stack}_postgres_data_v1 already exists"; fi
  grep -q "^$SHARED_VOLUME\$" <<<"$volumes" || stop "guard: the shared volume $SHARED_VOLUME is not listed"
  return 0
}

ids() {  # ids <stack>
  for s in postgres redis chromadb; do
    docker inspect -f "{{.Name}} {{.Id}} {{range .Mounts}}{{.Type}}:{{.Source}}->{{.Destination}} {{end}}" "$1-$s"
  done
}

wait_pg() {  # wait_pg <stack>
  for _ in $(seq 40); do
    docker exec "$1-postgres" pg_isready -U piper >/dev/null 2>&1 && return 0
    sleep 2
  done
  stop "postgres in $1 did not become ready in 80 seconds"
}

psql_in() { docker exec "$1-postgres" psql -U piper -d piper_morgan -tA -c "$2"; }

# ---- run ---------------------------------------------------------------------------------
A="$(stack_dir a)"; B="$(stack_dir b)"; A2="$(stack_dir a-second-folder)"
make_folder "$A" t2386a
make_folder "$B" t2386b
make_folder "$A2" t2386a

if [ "${DRY:-}" = "1" ]; then
  say "== DRY: guards only; nothing is started"
  guard_before_up t2386a "$A"; say "guard passed for t2386a"
  guard_before_up t2386b "$B"; say "guard passed for t2386b"
  guard_render t2386a "$A2"; say "render guard passed for the second folder"
  say "shared stack (read only):"; shared_state
  exit 0
fi

say "== 0. shared stack before"
SHARED_BEFORE="$(shared_state)"; say "$SHARED_BEFORE"

say "== 1. guard, then up t2386a"
guard_before_up t2386a "$A"
dc t2386a "$A" up -d --pull never postgres redis chromadb
IDS_A1="$(ids t2386a)"; say "$IDS_A1"

say "== 2. guard, then up t2386b"
guard_before_up t2386b "$B"
dc t2386b "$B" up -d --pull never postgres redis chromadb
IDS_B1="$(ids t2386b)"; say "$IDS_B1"

say "== 3. t2386a's containers after t2386b came up"
IDS_A2="$(ids t2386a)"
[ "$IDS_A1" = "$IDS_A2" ] || stop "t2386a's containers changed when t2386b came up"
say "unchanged"

say "== 4. one row in each database; neither reads the other's"
wait_pg t2386a; wait_pg t2386b
psql_in t2386a "create table t2386_probe (who text); insert into t2386_probe values ('row-of-a');" >/dev/null
psql_in t2386b "create table t2386_probe (who text); insert into t2386_probe values ('row-of-b');" >/dev/null
ROWS_A="$(psql_in t2386a 'select who from t2386_probe order by 1;')"
ROWS_B="$(psql_in t2386b 'select who from t2386_probe order by 1;')"
say "t2386a holds: $ROWS_A"
say "t2386b holds: $ROWS_B"
[ "$ROWS_A" = "row-of-a" ] || stop "t2386a does not hold exactly its own row"
[ "$ROWS_B" = "row-of-b" ] || stop "t2386b does not hold exactly its own row"

say "== 5. shared stack after both came up"
SHARED_MID="$(shared_state)"
[ "$SHARED_BEFORE" = "$SHARED_MID" ] || stop "the shared stack changed"
say "unchanged"

say "== 6. Arch's extra row: the SAME stack name brought up from a second folder"
guard_render t2386a "$A2"
dc t2386a "$A2" up -d --pull never postgres redis chromadb
IDS_A3="$(ids t2386a)"; say "$IDS_A3"
if [ "$IDS_A1" = "$IDS_A3" ]; then
  say "RESULT 6: no container was re-created"
else
  say "RESULT 6: containers were re-created; compare the ids and bind sources above with step 1"
fi
ROWS_A_AFTER="$(wait_pg t2386a; psql_in t2386a 'select who from t2386_probe order by 1;' 2>&1 || true)"
say "t2386a's database after the second folder's up holds: $ROWS_A_AFTER"

say "== 7. teardown: down without -v, then each volume by its literal name"
for pair in "t2386a:$A2" "t2386b:$B"; do
  stack="${pair%%:*}"; dir="${pair#*:}"
  guard_render "$stack" "$dir"
  dc "$stack" "$dir" down
  vol="${stack}_postgres_data_v1"
  label="$(docker volume inspect -f '{{index .Labels "com.docker.compose.project"}}' "$vol")"
  [ "$label" = "$(project "$stack")" ] || stop "volume $vol carries project label '$label', not $(project "$stack"); not removed"
  docker volume rm "$vol" >/dev/null
  say "removed volume $vol (label $label)"
done

say "== 8. shared stack after teardown"
SHARED_AFTER="$(shared_state)"
[ "$SHARED_BEFORE" = "$SHARED_AFTER" ] || stop "the shared stack changed across the run"
say "unchanged"
say "$SHARED_AFTER"
say "== 9. nothing left behind (each listing filtered on t2386; empty means none)"
say "containers: [$(docker ps -a --format '{{.Names}}' | grep t2386 | tr '\n' ' ' || true)]"
say "volumes:    [$(docker volume ls --format '{{.Name}}' | grep t2386 | tr '\n' ' ' || true)]"
say "networks:   [$(docker network ls --format '{{.Name}}' | grep t2386 | tr '\n' ' ' || true)]"
say "RUN COMPLETE. The work folder is left in place: $WORK"
