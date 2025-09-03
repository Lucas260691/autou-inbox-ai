import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { predictText } from "../lib/api";
import type { PredictOut } from "../lib/types";

const schema = z.object({
  text: z.string().min(8, "Digite pelo menos 8 caracteres."),
});

type Props = { onResult: (r: PredictOut) => void };

export default function TextForm({ onResult }: Props) {
  const { register, handleSubmit, formState, reset } = useForm<z.infer<typeof schema>>({
    resolver: zodResolver(schema),
    defaultValues: { text: "" },
  });
  const { errors, isSubmitting } = formState;

  async function onSubmit(v: z.infer<typeof schema>) {
    const res = await predictText(v.text);
    onResult(res);
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-3">
      <textarea
        {...register("text")}
        className="w-full rounded-2xl border p-4 outline-none focus:ring-2 min-h-[140px]"
        placeholder="Cole aqui o conteúdo do e-mail..."
      />
      {errors.text && <div className="text-sm text-red-600">{errors.text.message}</div>}
      <div className="flex gap-2">
        <button
          type="submit"
          disabled={isSubmitting}
          className="px-4 py-2 rounded-xl bg-black text-white disabled:opacity-50"
        >
          {isSubmitting ? "Analisando..." : "Analisar"}
        </button>
        <button
          type="button"
          onClick={() => reset({ text: "" })}
          className="px-4 py-2 rounded-xl border"
        >
          Limpar
        </button>
      </div>
    </form>
  );
}