import { useRef, useState } from "react";
import { predictFile } from "../lib/api";
import type { PredictOut } from "../lib/types";

type Props = { onResult: (r: PredictOut) => void };

export default function DropUpload({ onResult }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [drag, setDrag] = useState(false);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  async function send(file: File) {
    setErr(null);
    setLoading(true);
    try {
      const res = await predictFile(file);
      onResult(res);
    } catch (e: any) {
      setErr(e?.message || "Falha no upload");
    } finally {
      setLoading(false);
    }
  }

  function onFiles(fs: FileList | null) {
    const file = fs?.[0];
    if (!file) return;
    const ok = /(\.txt|\.pdf)$/i.test(file.name) || /(pdf|text)/i.test(file.type);
    if (!ok) { setErr("Formato não suportado. Envie .txt ou .pdf"); return; }
    void send(file);
  }

  return (
    <div
      className={`rounded-2xl border-2 border-dashed p-8 text-center ${drag ? "bg-gray-50" : ""}`}
      onDragOver={(e) => { e.preventDefault(); setDrag(true); }}
      onDragLeave={() => setDrag(false)}
      onDrop={(e) => { e.preventDefault(); setDrag(false); onFiles(e.dataTransfer.files); }}
      onClick={() => inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".txt,.pdf,application/pdf,text/plain"
        className="hidden"
        onChange={(e) => onFiles(e.target.files)}
      />
      <div className="text-lg">Arraste e solte seu .txt/.pdf aqui</div>
      <div className="opacity-60 text-sm">ou clique para selecionar um arquivo</div>
      <div className="mt-4">
        <button className="px-4 py-2 rounded-xl border">Selecionar arquivo</button>
      </div>
      {loading && <div className="mt-3 text-sm opacity-70">Processando...</div>}
      {err && <div className="mt-3 text-sm text-red-600">{err}</div>}
    </div>
  );
}