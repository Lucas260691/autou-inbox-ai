import type { PredictOut } from "./types";

const baseUrl = (import.meta.env.VITE_API_BASE_URL as string) || "/api";

export async function predictText(text: string): Promise<PredictOut> {
  const res = await fetch(`${baseUrl}/predict-text`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export async function predictFile(file: File): Promise<PredictOut> {
  const fd = new FormData();
  fd.append("file", file);
  const res = await fetch(`${baseUrl}/predict-file`, { method: "POST", body: fd });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}