type Props = { value: number };
export default function ConfidenceBar({ value }: Props) {
  const percent = Math.round((value ?? 0) * 100);
  return (
    <div className="w-full">
      <div className="mb-1 text-sm opacity-80">Confiança: {percent}%</div>
      <div className="h-2 w-full rounded-full bg-gray-200">
        <div
          className={`h-2 rounded-full ${percent >= 70 ? "bg-green-500" : "bg-yellow-500"}`}
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  );
}