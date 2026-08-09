import React, { useEffect, useState } from "react";

export default function App() {
  const [anon, setAnon] = useState(null);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    fetch("/api/auth/anonymous").then((r) => r.json()).then((d) => setAnon(d.identity_token)).catch(console.error);
  }, []);

  async function send() {
    if (!message) return;
    const payload = { message, conversation_id: null, mode: "melimi" };
    const res = await fetch("/api/chat/message", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    setMessages((s) => [...s, { role: "user", content: message }, { role: "assistant", content: data.message }]);
    setMessage("");
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <h2>మెలిమి తెలుగు AI</h2>
        <button className="new">New Chat</button>
      </aside>
      <main className="chat">
        <div className="messages">
          {messages.map((m, i) => (
            <div key={i} className={`msg ${m.role}`}>
              <div className="role">{m.role}</div>
              <div className="text">{m.content}</div>
            </div>
          ))}
        </div>
        <div className="composer">
          <input value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Type in Telugu..." />
          <button onClick={send}>Send</button>
        </div>
      </main>
    </div>
  );
}
