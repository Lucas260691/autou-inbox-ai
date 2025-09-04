type Props = { onPick: (text: string) => void };

const samples = [
  "Olá, podem informar o status do chamado #123?",
  "Segue anexo a fatura para conferência.",
  "Feliz aniversário! 🎉 Tudo de bom!",
];

export default function EmptyState({ onPick }: Props) {
  return (
    <div className="rounded-2xl border bg-white p-6 text-center dark:bg-neutral-900 dark:border-neutral-800">
      <div className="text-base font-medium">Pronto para começar</div>
      <p className="mt-1 text-sm opacity-70">Cole um texto ou envie um .txt/.pdf. Exemplos rápidos:</p>
      <div className="mt-4 flex flex-wrap justify-center gap-2">
        {samples.map((s) => (
          <button
            key={s}
            onClick={() => onPick(s)}
            className="px-3 py-1.5 rounded-full border text-sm hover:bg-gray-50 dark:border-neutral-700 dark:hover:bg-neutral-800"
            title="Usar este exemplo"
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}