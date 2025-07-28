import os
import json
from aiohttp import web
from dotenv import load_dotenv
import aiohttp   # ✅ для отправки POST в Django

load_dotenv()

routes = web.RouteTableDef()
connected_clients = set()

@routes.get('/')
async def index(request):
    return web.Response(text="WebSocket server is running")

@routes.get('/ws')
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    connected_clients.add(ws)
    print("🔌 Client connected")

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                await ws.send_str(f"Echo: {msg.data}")
            elif msg.type == web.WSMsgType.ERROR:
                print(f"WS connection closed with exception {ws.exception()}")
    finally:
        connected_clients.remove(ws)
        print("❌ Client disconnected")

    return ws

@routes.post('/news')
async def post_news(request):
    data = await request.json()
    message = data.get("message")

    if not message:
        return web.json_response({"error": "Message is required"}, status=400)

    # ✅ Сохраняем новость в Django API
    django_url = os.getenv("DJANGO_API_URL", "http://backend:8000/api/news/")
    async with aiohttp.ClientSession() as session:
        await session.post(django_url, json={"message": message})

    # ✅ Рассылаем всем подключённым клиентам
    for ws in connected_clients:
        await ws.send_str(json.dumps({"message": message}))

    return web.json_response({"status": "sent", "message": message})

@routes.get('/ping')
async def ping(request):
    return web.json_response({"status": "ok"})

app = web.Application()
app.add_routes(routes)

WS_PORT = int(os.getenv("WS_PORT", 8080))

if __name__ == '__main__':
    web.run_app(app, port=WS_PORT)
