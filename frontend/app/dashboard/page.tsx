"use client";

import { useTrends } from "@/lib/hooks/useTrends";
import { KPICard } from "@/components/ui/KPICard";
import { SentimentDonut } from "@/components/charts/SentimentDonut";
import { VolumeBar } from "@/components/charts/VolumeBar";

export default function DashboardPage() {
  const { data, isLoading, isError } = useTrends("7d");

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <span className="text-gray-400 animate-pulse">Loading dashboard…</span>
      </div>
    );
  }

  if (isError || !data) {
    return (
      <p className="text-red-400">Failed to load dashboard data. Is the API running?</p>
    );
  }

  const { summary, timeline } = data;
  const total = summary.total || 1;
  const positiveRate = ((summary.positive / total) * 100).toFixed(1);
  const negativeRate = ((summary.negative / total) * 100).toFixed(1);
  const neutralRate = ((summary.neutral / total) * 100).toFixed(1);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Overview</h1>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard label="Total Feedback" value={summary.total.toLocaleString()} />
        <KPICard label="Positive" value={`${positiveRate}%`} color="text-green-400" />
        <KPICard label="Negative" value={`${negativeRate}%`} color="text-red-400" />
        <KPICard label="Neutral" value={`${neutralRate}%`} color="text-yellow-400" />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-900 rounded-xl p-4">
          <h2 className="text-lg font-semibold mb-4">Sentiment Distribution</h2>
          <SentimentDonut summary={summary} />
        </div>
        <div className="bg-gray-900 rounded-xl p-4">
          <h2 className="text-lg font-semibold mb-4">Daily Feedback Volume</h2>
          <VolumeBar timeline={timeline} />
        </div>
      </div>
    </div>
  );
}
