#!/bin/bash

APP_DIR="/home/ubuntu/entrapeer-agentic-api"

echo "Stopping Entrapeer Agentic API..."

if [ -f "$APP_DIR/docker-compose.yml" ]; then
  cd "$APP_DIR"
  docker compose down || true
fi