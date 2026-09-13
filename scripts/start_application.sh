#!/bin/bash
set -e

APP_DIR="/home/ubuntu/entrapeer-agentic-api"

echo "Starting Entrapeer Agentic API..."

cd "$APP_DIR"

docker compose up -d --build