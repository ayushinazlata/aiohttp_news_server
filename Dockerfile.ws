FROM python:3.10-slim

WORKDIR /app

COPY ws_server/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY ws_server /app

CMD ["python", "server.py"]
