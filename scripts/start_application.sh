#!/bin/bash
set -e

echo "Starting Entrapeer Agentic API..."

cd /home/ubuntu/entrapeer-agentic-api

docker compose up -d
