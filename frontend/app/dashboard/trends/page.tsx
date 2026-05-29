"use client";

import { useState } from "react";
import { useTrends } from "@/lib/hooks/useTrends";
import { TrendLine } from "@/components/charts/TrendLine";

const PERIODS = ["1d", "7d", "30d", "90d"] as const;
type Period = (typeof PERIODS)[number];

export default function TrendsPage() {
  const [period, setPeriod] = useState<Period>("7d");
  const { data, isLoading, isError } = useTrends(period);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Trend Analysis</h1>
        <div className="flex gap-2">
          {PERIODS.map((p) => (
            <button
              key={p}
              onClick={() => setPeriod(p)}
              className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
                period === p
                  ? "bg-indigo-600 text-white"
                  : "bg-gray-800 text-gray-300 hover:bg-gray-700"
              }`}
            >
              {p}
            </button>
          ))}
        </div>
      </div>

      {isLoading && (
        <p className="text-gray-400 animate-pulse">Loading trend data…</p>
      )}
      {isError && (
        <p className="text-red-400">Failed to load trend data.</p>
      )}
      {data && (
        <div className="bg-gray-900 rounded-xl p-4">
          <TrendLine timeline={data.timeline} />
        </div>
      )}
    </div>
  );
}
