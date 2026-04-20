"use client";

import { useState } from "react";
import { scenarios } from "../data/scenarios";
import { PipelinePanel } from "../components/PipelineView"

const backendApi = process.env.NEXT_PUBLIC_BACKEND_API || "http://localhost:5000"

export default function Home() {
  const [selectedScenario, setSelectedScenario] = useState(0);
  const [messages, setMessages] = useState(scenarios[0].messages);
  const [context, setContext] = useState(scenarios[0].context);
  const [input, setInput] = useState("");
  const [result, setResult] = useState(null);
  const [disableBut, setDisableBut] = useState(false);

  const loadScenario = (index) => {
    const s = scenarios[index];
    setSelectedScenario(index);
    setMessages(s.messages);
    setContext(s.context);
    setInput(s.input);
    setResult(null);
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput("");

    const res = await fetch(backendApi + "/decide", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        action: "chat_action",
        message: input,
        context: context
      })
    });

    const data = await res.json();

    setResult(data);
    setDisableBut(false);
    setContext(data.context); // update summary

    setMessages([
      ...newMessages,
      {
        role: "assistant",
        content: data.reply
      }
    ]);
  };

  return (
    <div style={{ display: "flex", height: "100vh" }}>

      {/* LEFT */}
      <div style={{ width: "50%", borderRight: "1px solid #ddd", display: "flex", flexDirection: "column" }}>
        
        <div style={{
          padding: 12,
          borderBottom: "1px solid #eee",
          background: "#fafafa"
        }}>
          <label style={{
            display: "block",
            fontSize: 12,
            color: "#666",
            marginBottom: 6
          }}>
            Scenario
          </label>

          <select
            value={selectedScenario}
            onChange={(e) => loadScenario(Number(e.target.value))}
            style={{
              width: "100%",
              padding: "10px 12px",
              fontSize: 14,
              borderRadius: 10,
              border: "1px solid #ddd",
              background: "white",
              outline: "none",
              cursor: "pointer",
              transition: "all 0.2s ease"
            }}
            onFocus={(e) => e.target.style.border = "1px solid #0070f3"}
            onBlur={(e) => e.target.style.border = "1px solid #ddd"}
          >
            {scenarios.map((s, i) => (
              <option key={i} value={i}>
                {s.name}
              </option>
            ))}
          </select>
        </div>

        <div style={{ flex: 1, overflowY: "auto", padding: 10 }}>
          {messages.map((msg, i) => (
            <div key={i} style={{ textAlign: msg.role === "user" ? "right" : "left", marginBottom: 12 }}>
              <span style={{
                display: "inline-block",
                padding: 10,
                marginBottom: 5,
                borderRadius: 10,
                background: msg.role === "user" ? "#0070f3" : "#eee",
                color: msg.role === "user" ? "white" : "black"
              }}>
                {msg.content}
              </span>
            </div>
          ))}
        </div>

        <div style={{
          display: "flex",
          gap: "10px",
          padding: "12px",
          borderTop: "1px solid #ddd",
          background: "#fafafa"

        }}>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
            rows={3}
            style={{
              flex: 1,
              resize: "none",
              padding: "12px",
              fontSize: "14px",
              borderRadius: "10px",
              border: "1px solid #ccc",
              outline: "none"
            }}
          />
          <button
            onClick={() => {
              setResult(null)
              setDisableBut(true)
              sendMessage()
            }}
            style={{
              padding: "10px 16px",
              disabled: {disableBut},
              borderRadius: "10px",
              border: "none",
              background: "#0070f3",
              color: "white",
              fontWeight: "bold",
              cursor: "pointer",
            }}
          >
            Send
          </button>
        </div>
      </div>

      {/* RIGHT */}
      <div style={{ width: "50%", padding: 20, overflowY: "auto" }}>
        <PipelinePanel
          input={input}
          context={context}
          result={result}
        />
      </div>
    </div>
  );
}