import { clsx } from "clsx";

interface Props {
  label: string;
  value: string | number;
  color?: string;
}

export function KPICard({ label, value, color = "text-white" }: Props) {
  return (
    <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
      <p className="text-xs text-gray-500 uppercase tracking-wider">{label}</p>
      <p className={clsx("text-3xl font-bold mt-1", color)}>{value}</p>
    </div>
  );
}
