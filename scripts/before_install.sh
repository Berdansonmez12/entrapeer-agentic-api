#!/bin/bash
set -e

echo "Preparing Entrapeer Agentic API deployment..."

cd /home/ubuntu/entrapeer-agentic-api

docker compose pull || true
docker compose build
