#!/usr/bin/env bash
set -euo pipefail

uv run python -c "from pyjd.jd_device import JDDevice"
sh tests/docker/start_jdownloader.sh
uv run pytest -v --cov || true
docker compose down
