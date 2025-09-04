import { useState } from "react";
import TextForm from "./components/TextForm";
import DropUpload from "./components/DropUpload";
import ResultCard from "./components/ResultCard";
import type { PredictOut } from "./lib/types";
import Header from "./components/Header";
import EmptyState from "./components/EmptyState";
import SkeletonCard from "./components/SkeletonCard";

type Tab = "texto" | "arquivo";

export default function App() {
  const [tab, setTab] = useState<Tab>("texto");
  const [result, setResult] = useState<PredictOut | null>(null);
  const [loading, setLoading] = useState(false);
  const [prefill, setPrefill] = useState<string | null>(null);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-neutral-950 dark:text-neutral-100">
      <Header />
      <div className="border-b bg-white/60 backdrop-blur dark:bg-neutral-900/60">
        <div className="mx-auto max-w-5xl px-6 py-3">
          <div className="inline-flex rounded-xl border p-1 dark:border-neutral-800">
            <button
              className={`px-3 py-1.5 rounded-lg text-sm ${tab==="texto" ? "bg-black text-white dark:bg-white dark:text-black" : ""}`}
              onClick={() => setTab("texto")}
            >Texto</button>
            <button
              className={`px-3 py-1.5 rounded-lg text-sm ${tab==="arquivo" ? "bg-black text-white dark:bg-white dark:text-black" : ""}`}
              onClick={() => setTab("arquivo")}
            >Arquivo</button>
          </div>
        </div>
      </div>

      <main className="px-6 py-8">
        <div className="mx-auto max-w-5xl">
          <div className="grid gap-6 md:grid-cols-2">
            <section className="rounded-2xl border bg-white p-5 shadow-sm dark:bg-neutral-900 dark:border-neutral-800">
              <h2 className="text-lg font-medium mb-3">
                {tab === "texto" ? "Analisar texto" : "Enviar arquivo"}
              </h2>
              {tab === "texto" ? (
                <TextForm
                  onResult={setResult}
                  onLoading={setLoading}
                  prefillText={prefill}
                />
              ) : (
                <DropUpload onResult={setResult} onLoading={setLoading} />
              )}
              <p className="mt-3 text-xs opacity-60">
                O conteúdo não é armazenado; processamos apenas para classificar e sugerir resposta.
              </p>
            </section>

            <section>
              {loading ? (
                <SkeletonCard />
              ) : result ? (
                <ResultCard data={result} onClear={() => setResult(null)} />
              ) : (
                <EmptyState onPick={(t) => {
                  setTab("texto");
                  setPrefill(t);
                }} />
              )}
            </section>
          </div>
        </div>
      </main>

      <footer className="px-6 py-6 border-t bg-white dark:bg-neutral-900 dark:border-neutral-800">
        <div className="mx-auto max-w-5xl text-sm opacity-70">
          © {new Date().getFullYear()} AutoU Inbox AI. Desenvolvido por{"AutoU"}
        </div>
      </footer>
    </div>
  );
}