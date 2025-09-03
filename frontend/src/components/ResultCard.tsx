import ConfidenceBar from "./ConfidenceBar";
import IntentChips from "./IntentChips";
import type { PredictOut } from "../lib/types";

type Props = { data: PredictOut | null; onClear?: () => void };

export default function ResultCard({ data, onClear }: Props) {
  if (!data) return null;
  const prod = data.category === "Produtivo";
  const pill = prod ? "bg-green-100 text-green-800 border-green-300" : "bg-gray-100 text-gray-800 border-gray-300";

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(data.reply || "");
      alert("Resposta copiada!");
    } catch {
      alert("Não foi possível copiar.");
    }
  };

  return (
    <div className="mt-6 rounded-2xl border bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <span className={`px-3 py-1 rounded-full text-sm border ${pill}`}>{data.category}</span>
          <span className="text-xs uppercase opacity-60 border rounded px-2 py-0.5">provider: {data.provider}</span>
        </div>
        {onClear && (
          <button onClick={onClear} className="text-sm underline opacity-70 hover:opacity-100">
            Limpar
          </button>
        )}
      </div>

      <div className="mt-4">
        <ConfidenceBar value={data.confidence} />
      </div>

      <div className="mt-4">
        <IntentChips intents={data.intents} />
      </div>

      <div className="mt-4">
        <label className="text-sm opacity-70">Resposta sugerida</label>
        <textarea
          className="mt-1 w-full rounded-xl border p-3 outline-none focus:ring-2"
          rows={4}
          readOnly
          value={data.reply}
        />
        <div className="mt-2 flex gap-2">
          <button onClick={copy} className="px-3 py-1.5 rounded-lg border hover:bg-gray-50">
            Copiar texto
          </button>
        </div>
      </div>
    </div>
  );
}