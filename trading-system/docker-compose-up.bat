@echo off
REM docker-compose-up.bat

echo Stopping existing containers...
docker compose down

echo Building and starting services...
docker compose -f docker/docker-compose.yml up -d --build

echo Waiting for services to start...
timeout /t 10

echo Checking container status...
docker compose -f docker/docker-compose.yml ps

echo Backend logs:
docker compose -f docker/docker-compose.yml logs backend
