import { useState } from "react";
import TextForm from "./components/TextForm";
import DropUpload from "./components/DropUpload";
import ResultCard from "./components/ResultCard";
import type { PredictOut } from "./lib/types";

type Tab = "texto" | "arquivo";

export default function App() {
  const [tab, setTab] = useState<Tab>("texto");
  const [result, setResult] = useState<PredictOut | null>(null);

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="px-6 py-4 border-b bg-white">
        <div className="mx-auto max-w-5xl flex items-center justify-between">
          <h1 className="text-xl font-semibold">AutoU Inbox AI</h1>
          <nav className="flex gap-2">
            <button
              className={`px-3 py-1.5 rounded-lg border ${tab==="texto" ? "bg-black text-white" : ""}`}
              onClick={() => setTab("texto")}
            >
              Texto
            </button>
            <button
              className={`px-3 py-1.5 rounded-lg border ${tab==="arquivo" ? "bg-black text-white" : ""}`}
              onClick={() => setTab("arquivo")}
            >
              Arquivo
            </button>
          </nav>
        </div>
      </header>

      <main className="px-6 py-8">
        <div className="mx-auto max-w-5xl">
          <div className="grid gap-6 md:grid-cols-2">
            <section className="rounded-2xl border bg-white p-5 shadow-sm">
              <h2 className="text-lg font-medium mb-3">
                {tab === "texto" ? "Analisar texto" : "Enviar arquivo"}
              </h2>
              {tab === "texto" ? (
                <TextForm onResult={setResult} />
              ) : (
                <DropUpload onResult={setResult} />
              )}
              <p className="mt-3 text-xs opacity-60">
                O conteúdo não é armazenado; processamos apenas para classificar e sugerir resposta.
              </p>
            </section>

            <section>
              <ResultCard data={result} onClear={() => setResult(null)} />
            </section>
          </div>
        </div>
      </main>

      <footer className="px-6 py-6 border-t bg-white">
        <div className="mx-auto max-w-5xl text-sm opacity-70">
          Conectado a <code>/api</code> via proxy (Nginx). Use <code>docker compose up --build</code>.
        </div>
      </footer>
    </div>
  );
}

