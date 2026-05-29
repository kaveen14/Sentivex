import { render, screen } from "@testing-library/react";
import { FeedbackTable } from "@/components/tables/FeedbackTable";

const mockItems = [
  {
    id: "uuid-1",
    raw_text: "Excellent product, highly recommend!",
    sentiment: "Positive",
    confidence: 0.95,
    source: "app_review",
    created_at: "2026-05-28T12:00:00Z",
  },
  {
    id: "uuid-2",
    raw_text: "Product arrived damaged.",
    sentiment: "Negative",
    confidence: 0.88,
    source: "support_ticket",
    created_at: "2026-05-27T08:30:00Z",
  },
  {
    id: "uuid-3",
    raw_text: "It is okay, nothing special.",
    sentiment: "Neutral",
    confidence: 0.72,
    source: null,
    created_at: "2026-05-26T15:00:00Z",
  },
];

describe("FeedbackTable", () => {
  it("renders without crashing", () => {
    const { container } = render(<FeedbackTable items={mockItems} />);
    expect(container).toBeTruthy();
  });

  it("renders a table element", () => {
    const { container } = render(<FeedbackTable items={mockItems} />);
    expect(container.querySelector("table")).toBeInTheDocument();
  });

  it("renders all feedback rows", () => {
    render(<FeedbackTable items={mockItems} />);
    expect(screen.getByText(/Excellent product/)).toBeInTheDocument();
    expect(screen.getByText(/Product arrived damaged/)).toBeInTheDocument();
    expect(screen.getByText(/nothing special/)).toBeInTheDocument();
  });

  it("renders sentiment badges", () => {
    render(<FeedbackTable items={mockItems} />);
    expect(screen.getByText("Positive")).toBeInTheDocument();
    expect(screen.getByText("Negative")).toBeInTheDocument();
    expect(screen.getByText("Neutral")).toBeInTheDocument();
  });

  it("renders confidence percentages", () => {
    render(<FeedbackTable items={mockItems} />);
    expect(screen.getByText("95%")).toBeInTheDocument();
    expect(screen.getByText("88%")).toBeInTheDocument();
    expect(screen.getByText("72%")).toBeInTheDocument();
  });

  it("renders source names", () => {
    render(<FeedbackTable items={mockItems} />);
    expect(screen.getByText("app_review")).toBeInTheDocument();
    expect(screen.getByText("support_ticket")).toBeInTheDocument();
  });

  it("renders — when source is null", () => {
    render(<FeedbackTable items={mockItems} />);
    const dashes = screen.getAllByText("—");
    expect(dashes.length).toBeGreaterThan(0);
  });

  it("shows empty message when items list is empty", () => {
    render(<FeedbackTable items={[]} />);
    expect(screen.getByText(/No feedback found/)).toBeInTheDocument();
  });

  it("renders column headers", () => {
    render(<FeedbackTable items={mockItems} />);
    expect(screen.getByText("Feedback")).toBeInTheDocument();
    expect(screen.getByText("Sentiment")).toBeInTheDocument();
    expect(screen.getByText("Confidence")).toBeInTheDocument();
    expect(screen.getByText("Source")).toBeInTheDocument();
    expect(screen.getByText("Date")).toBeInTheDocument();
  });
});
