"use client";
import { useState } from "react";

export default function Home() {
  const [gifUrl, setGifUrl] = useState<string | null>(null);

  const handleUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    if (!event.target.files) return;

    const file = event.target.files[0];
    const text = await file.text();
    let jsonData;
    try {
      jsonData = JSON.parse(text);
    } catch (err) {
      console.error("Invalid JSON file", err);
      return;
    }

    // API Route に POST リクエスト
    const response = await fetch("/api/upload", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(jsonData),
    });

    if (!response.ok) {
      console.error("Failed to get GIF");
      return;
    }

    const blob = await response.blob();
    setGifUrl(URL.createObjectURL(blob));
  };

  return (
    <div style={{ padding: "2rem", textAlign: "center" }}>
      <h1>JSON Upload and GIF Display</h1>
      <input type="file" accept=".json" onChange={handleUpload} />
      {gifUrl && (
        <div style={{ marginTop: "2rem" }}>
          <img src={gifUrl} alt="Generated GIF" />
        </div>
      )}
    </div>
  );
}
