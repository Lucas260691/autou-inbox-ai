export const pct = (x: number) => `${Math.round((x ?? 0) * 100)}%`;

export const intentLabel = (s: string) => {
  const map: Record<string,string> = {
    status: "Status",
    attachment: "Anexo",
    support: "Suporte",
    billing: "Financeiro",
  };
  return map[s] || s;
};
