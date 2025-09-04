import { intentLabel } from "../lib/format";

export default function IntentChips({ intents }: { intents: string[] }) {
  if (!intents?.length) return null;
  return (
    <div className="flex flex-wrap gap-2">
      {intents.map((i) => (
        <span key={i} className="px-2 py-1 text-xs rounded-full bg-gray-100 border">
          {intentLabel(i)}
        </span>
      ))}
    </div>
  );
}