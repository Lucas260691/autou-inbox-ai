export type PredictOut = {
  category: "Produtivo" | "Improdutivo";
  confidence: number;           // 0..1
  reply: string;
  provider: "baseline" | "openai";
  intents: string[];            // ex: ["status", "attachment"]
};