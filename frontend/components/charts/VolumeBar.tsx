"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

interface DataPoint {
  date: string;
  positive: number;
  neutral: number;
  negative: number;
}

export function VolumeBar({ timeline }: { timeline: DataPoint[] }) {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <BarChart data={timeline}>
        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
        <XAxis dataKey="date" tick={{ fill: "#9ca3af", fontSize: 11 }} />
        <YAxis tick={{ fill: "#9ca3af", fontSize: 11 }} />
        <Tooltip
          contentStyle={{ background: "#1f2937", border: "none", borderRadius: 8 }}
          itemStyle={{ color: "#e5e7eb" }}
        />
        <Legend wrapperStyle={{ color: "#9ca3af" }} />
        <Bar dataKey="positive" stackId="a" fill="#22c55e" />
        <Bar dataKey="neutral" stackId="a" fill="#f59e0b" />
        <Bar dataKey="negative" stackId="a" fill="#ef4444" />
      </BarChart>
    </ResponsiveContainer>
  );
}
