import React, { useEffect, useState } from "react";
import "./NewsFeed.css"; // ✅ подключаем CSS

function NewsFeed() {
  const [news, setNews] = useState([]);
  const [status, setStatus] = useState("Disconnected");

  const apiUrl = process.env.REACT_APP_API_URL || "/api/news/";
  const wsUrl = process.env.REACT_APP_WS_URL || "ws://" + window.location.host + "/ws/";

  useEffect(() => {
    fetch(apiUrl)
      .then(res => res.json())
      .then(data => setNews(data));

    const ws = new WebSocket(wsUrl);
    ws.onopen = () => setStatus("Connected");
    ws.onclose = () => setStatus("Disconnected");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const newItem = data.id ? data : { id: Math.random(), message: data.message };
      setNews(prev => [newItem, ...prev]);
    };

    return () => ws.close();
  }, [apiUrl, wsUrl]);

  return (
    <div className="news-container">
      <h1 className="news-title">Новости</h1>
      <p className={`status ${status === "Connected" ? "online" : "offline"}`}>
        WebSocket статус: {status}
      </p>
      <ul className="news-list">
        {news.map((item) => (
          <li key={item.id} className="news-item">{item.message}</li>
        ))}
      </ul>
    </div>
  );
}

export default NewsFeed;
