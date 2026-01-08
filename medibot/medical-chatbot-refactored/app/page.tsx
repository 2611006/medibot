"use client";
import { useState } from "react";

export default function Home() {
  const [q, setQ] = useState("");
  const [a, setA] = useState("");

  async function ask() {
    const res = await fetch("/api/chat", {
      method: "POST",
      body: JSON.stringify({ question: q })
    });
    const data = await res.json();
    setA(data.answer);
  }

  return (
    <main style={{ padding: 40 }}>
      <h1>🩺 Medibot</h1>
      <input value={q} onChange={e => setQ(e.target.value)} />
      <button onClick={ask}>Ask</button>
      <p>{a}</p>
    </main>
  );
}
