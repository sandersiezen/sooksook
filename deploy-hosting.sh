#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
echo "▶ Deploying Firebase Hosting..."
firebase deploy --only hosting --project sooksookshootschat
echo "✓ Hosting deployed → https://sooksookshootschat.web.app"
