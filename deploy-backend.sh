#!/usr/bin/env bash
set -euo pipefail

PROJECT=sooksookshootschat
SERVICE=sooksook-chat
REGION=us-central1
IMAGE="gcr.io/${PROJECT}/${SERVICE}"

cd "$(dirname "$0")"
echo "▶ Building and pushing image..."
gcloud builds submit backend/ --tag "${IMAGE}" --project "${PROJECT}"

echo "▶ Deploying to Cloud Run..."
gcloud run deploy "${SERVICE}" \
  --image "${IMAGE}" \
  --region "${REGION}" \
  --platform managed \
  --project "${PROJECT}"

echo "✓ Backend deployed → https://${SERVICE}-396837120203.${REGION}.run.app"
