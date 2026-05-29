import axios from "axios";

const BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
  timeout: 15_000,
});

// ── Typed response shapes ────────────────────────────────────────────────────

export interface SentimentScores {
  positive: number;
  neutral: number;
  negative: number;
}

export interface AnalyzeResponse {
  id: string;
  sentiment: string;
  confidence: number;
  scores: SentimentScores;
  timestamp: string;
}

export interface TrendDataPoint {
  date: string;
  positive: number;
  neutral: number;
  negative: number;
}

export interface TrendSummary {
  positive: number;
  neutral: number;
  negative: number;
  total: number;
}

export interface TrendResponse {
  period: string;
  summary: TrendSummary;
  timeline: TrendDataPoint[];
}

export interface FeedbackItem {
  id: string;
  raw_text: string;
  sentiment?: string | null;
  confidence?: number | null;
  source?: string | null;
  created_at: string;
}

export interface FeedbackListResponse {
  items: FeedbackItem[];
  total: number;
  page: number;
  page_size: number;
}
