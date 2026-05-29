import { useQuery } from "@tanstack/react-query";
import { api, TrendResponse } from "@/lib/api";

export function useTrends(period: string = "7d", source?: string) {
  return useQuery<TrendResponse>({
    queryKey: ["trends", period, source],
    queryFn: async () => {
      const params: Record<string, string> = { period };
      if (source) params.source = source;
      const res = await api.get<TrendResponse>("/trends", { params });
      return res.data;
    },
    refetchInterval: 30_000,
  });
}
