#!/bin/bash

# Stop any container using port 8000
PORT=8000
PID=$(lsof -t -i:$PORT)
if [ -n \"$PID\" ]; then
  echo \"Killing process on port $PORT...\"
  kill -9 $PID
fi

# Stop and remove all Docker containers named notes-api (if running)
if [ $(docker ps -q -f name=notes-api) ]; then
  echo \"Stopping existing notes-api container...\"
  docker stop notes-api
  docker rm notes-api
fi

# Rebuild Docker backend
echo \"Rebuilding Docker image...\"
docker build -t notes-api .

# Start backend container (port 8000)
echo \"Starting backend Docker container...\"
docker run -d --name notes-api -p 8000:8000 notes-api

# Launch React frontend
cd frontend || exit

if [ ! -d \"node_modules\" ]; then
  echo \"Installing React dependencies...\"
  npm install
fi

echo \"Starting React frontend...\"
npm start
