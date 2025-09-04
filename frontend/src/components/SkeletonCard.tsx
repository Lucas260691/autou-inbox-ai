export default function SkeletonCard() {
  return (
    <div className="rounded-2xl border bg-white p-5 shadow-sm animate-pulse dark:bg-neutral-900 dark:border-neutral-800">
      <div className="h-6 w-40 rounded bg-gray-200 dark:bg-neutral-800" />
      <div className="mt-4 h-3 w-full rounded bg-gray-200 dark:bg-neutral-800" />
      <div className="mt-2 h-3 w-3/4 rounded bg-gray-200 dark:bg-neutral-800" />
      <div className="mt-6 h-24 w-full rounded-xl bg-gray-200 dark:bg-neutral-800" />
    </div>
  );
}

