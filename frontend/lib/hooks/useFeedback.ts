import { useQuery } from "@tanstack/react-query";
import { api, FeedbackListResponse } from "@/lib/api";

interface Options {
  page?: number;
  pageSize?: number;
  sentiment?: string;
  source?: string;
}

export function useFeedback({ page = 1, pageSize = 20, sentiment, source }: Options = {}) {
  return useQuery<FeedbackListResponse>({
    queryKey: ["feedback", page, pageSize, sentiment, source],
    queryFn: async () => {
      const params: Record<string, string | number> = { page, page_size: pageSize };
      if (sentiment) params.sentiment = sentiment;
      if (source) params.source = source;
      const res = await api.get<FeedbackListResponse>("/feedback", { params });
      return res.data;
    },
  });
}
