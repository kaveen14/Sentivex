interface FeedbackItem {
  id: string;
  raw_text: string;
  sentiment?: string | null;
  confidence?: number | null;
  source?: string | null;
  created_at: string;
}

const SENTIMENT_BADGE: Record<string, string> = {
  Positive: "bg-green-900 text-green-300",
  Neutral: "bg-yellow-900 text-yellow-300",
  Negative: "bg-red-900 text-red-300",
};

export function FeedbackTable({ items }: { items: FeedbackItem[] }) {
  if (items.length === 0) {
    return <p className="text-gray-500 text-sm">No feedback found.</p>;
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-gray-800">
      <table className="w-full text-sm">
        <thead className="bg-gray-800 text-gray-400 uppercase text-xs tracking-wider">
          <tr>
            <th className="px-4 py-3 text-left">Feedback</th>
            <th className="px-4 py-3 text-left">Sentiment</th>
            <th className="px-4 py-3 text-left">Confidence</th>
            <th className="px-4 py-3 text-left">Source</th>
            <th className="px-4 py-3 text-left">Date</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-800">
          {items.map((item) => (
            <tr key={item.id} className="hover:bg-gray-800/50 transition-colors">
              <td className="px-4 py-3 max-w-xs truncate text-gray-200">{item.raw_text}</td>
              <td className="px-4 py-3">
                {item.sentiment ? (
                  <span
                    className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                      SENTIMENT_BADGE[item.sentiment] ?? "bg-gray-700 text-gray-300"
                    }`}
                  >
                    {item.sentiment}
                  </span>
                ) : (
                  <span className="text-gray-600">—</span>
                )}
              </td>
              <td className="px-4 py-3 text-gray-400">
                {item.confidence != null
                  ? `${(item.confidence * 100).toFixed(0)}%`
                  : "—"}
              </td>
              <td className="px-4 py-3 text-gray-400">{item.source ?? "—"}</td>
              <td className="px-4 py-3 text-gray-500 whitespace-nowrap">
                {new Date(item.created_at).toLocaleDateString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
