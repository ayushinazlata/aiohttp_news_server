📌 News Project – WebSocket + Django + React

🔹 Overview
Real-time news application built with Django, React, and aiohttp WebSockets.  

Features:
- Django REST API for storing news
- WebSocket server for broadcasting messages to connected clients
- React frontend for displaying history and live updates
- Docker + Nginx production setup


⚙️ Environment Setup

1. Copy .env.example:

    cp .env.example .env

2. Fill in:

    DJANGO_SECRET_KEY
    DJANGO_ALLOWED_HOSTS
    WebSocket and API URLs


🛠️ Development Mode (without Docker)

Backend:
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver

WebSocket server:
    cd ws_server
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python server.py

Frontend:
    cd frontend
    npm install
    npm start



🚀 Production with Docker

docker compose -f docker-compose.prod.yml build --no-cache
docker compose -f docker-compose.prod.yml up -d

Open http://localhost

Test WebSocket:
    curl -X POST http://localhost/news \
    -H "Content-Type: application/json" \
    -d '{"message": "Test message"}'



✅ Requirements Check (based on task)

✔️ Clients can connect via WebSocket
✔️ /news POST endpoint broadcasts to all clients
✔️ /ping endpoint for connection checks
✔️ Page displays both history and real-time updates