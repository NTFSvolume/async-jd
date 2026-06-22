#!/usr/bin/env bash
set -euo pipefail

docker compose up -d jdownloader
echo "Waiting for Jdownloader to start up..." >&2
until curl --fail --silent http://localhost:3128/device/ping > /dev/null 2>&1 ; do
  echo "container not ready, retrying in 30s..." >&2
  sleep 30
done

echo "Jdownloader is up!" >&2
