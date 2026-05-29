import { render, screen } from "@testing-library/react";
import { SentimentDonut } from "@/components/charts/SentimentDonut";

// Recharts uses SVG — mock ResizeObserver for JSDOM
global.ResizeObserver = class {
  observe() {}
  unobserve() {}
  disconnect() {}
};

const mockSummary = { positive: 80, neutral: 15, negative: 5 };

describe("SentimentDonut", () => {
  it("renders without crashing", () => {
    const { container } = render(<SentimentDonut summary={mockSummary} />);
    expect(container).toBeTruthy();
  });

  it("renders a PieChart SVG element", () => {
    const { container } = render(<SentimentDonut summary={mockSummary} />);
    expect(container.querySelector("svg")).toBeInTheDocument();
  });

  it("renders three legend labels", () => {
    render(<SentimentDonut summary={mockSummary} />);
    expect(screen.getByText("Positive")).toBeInTheDocument();
    expect(screen.getByText("Neutral")).toBeInTheDocument();
    expect(screen.getByText("Negative")).toBeInTheDocument();
  });

  it("renders with all-zero values without crashing", () => {
    const { container } = render(
      <SentimentDonut summary={{ positive: 0, neutral: 0, negative: 0 }} />
    );
    expect(container).toBeTruthy();
  });
});
