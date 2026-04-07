import React, { useState } from "react";

export default function Interface() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([
    { sender: "assistant", text: "Hello! Ask me about real estate properties." }
  ]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!question.trim()) return;

    const userMessage = { sender: "user", text: question };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ question })
      });

      const data = await response.json();

      const botMessage = {
        sender: "assistant",
        text: data.answer || "No response."
      };

      setMessages((prev) => [...prev, botMessage]);
    } 
    catch (error) {
      setMessages((prev) => [...prev,{ sender: "assistant", text: "Error connecting to backend." }
      ]);
    }

    setQuestion("");
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: "800px", margin: "30px auto", fontFamily: "Arial" }}>
      <h1>Real Estate AI Assistant</h1>

      <div
        style={{
          border: "1px solid #ccc",
          borderRadius: "10px",
          padding: "20px",
          minHeight: "400px",
          marginBottom: "20px"
        }}
      >
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              textAlign: msg.sender === "user" ? "right" : "left",
              marginBottom: "15px"
            }}
          >
            <span
              style={{
                display: "inline-block",
                padding: "10px 15px",
                borderRadius: "10px",
                backgroundColor: msg.sender === "user" ? "#dbeafe" : "#f3f4f6"
              }}
            >
              <strong>{msg.sender === "user" ? "You" : "Assistant"}:</strong>{" "}
              {msg.text}
            </span>
          </div>
        ))}

        {loading && <p>Thinking...</p>}
      </div>

      <div style={{ display: "flex", gap: "10px" }}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask about properties..."
          style={{
            flex: 1,
            padding: "12px",
            borderRadius: "8px",
            border: "1px solid #ccc"
          }}
        />

        <button
          onClick={sendMessage}
          style={{
            padding: "12px 20px",
            border: "none",
            borderRadius: "8px",
            backgroundColor: "#2563eb",
            color: "white",
            cursor: "pointer"
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}