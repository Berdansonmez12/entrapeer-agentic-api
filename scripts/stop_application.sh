#!/bin/bash

echo "Stopping Entrapeer Agentic API..."

cd /home/ubuntu/entrapeer-agentic-api

docker compose down || true
