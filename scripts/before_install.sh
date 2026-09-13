#!/bin/bash
set -e

APP_DIR="/home/ubuntu/entrapeer-agentic-api"

echo "Preparing Entrapeer Agentic API deployment..."

mkdir -p "$APP_DIR"

if [ -f "$APP_DIR/docker-compose.yml" ]; then
  cd "$APP_DIR"
  docker compose down || true
fi