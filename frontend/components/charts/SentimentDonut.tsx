"use client";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

interface Props {
  summary: { positive: number; neutral: number; negative: number };
}

const COLORS = ["#22c55e", "#f59e0b", "#ef4444"];

export function SentimentDonut({ summary }: Props) {
  const data = [
    { name: "Positive", value: summary.positive },
    { name: "Neutral", value: summary.neutral },
    { name: "Negative", value: summary.negative },
  ];

  return (
    <ResponsiveContainer width="100%" height={260}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={70}
          outerRadius={110}
          paddingAngle={3}
          dataKey="value"
        >
          {data.map((_, i) => (
            <Cell key={i} fill={COLORS[i]} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{ background: "#1f2937", border: "none", borderRadius: 8 }}
          itemStyle={{ color: "#e5e7eb" }}
        />
        <Legend wrapperStyle={{ color: "#9ca3af" }} />
      </PieChart>
    </ResponsiveContainer>
  );
}
