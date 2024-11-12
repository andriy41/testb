#!/bin/bash
# Script to run docker-compose from the correct directory

# Change to the directory containing docker-compose.yml
cd "$(dirname "$0")"

# Run docker compose with all arguments passed to the script
docker compose up -d --build "$@"
