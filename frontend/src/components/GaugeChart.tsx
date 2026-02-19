"use client";

interface Props {
  probability: number;          // 0 – 1
  riskLevel: "HIGH" | "MEDIUM" | "LOW";
}

export default function GaugeChart({ probability, riskLevel }: Props) {
  const pct = Math.round(probability * 100);

  // SVG arc parameters
  const cx = 100;
  const cy = 100;
  const r = 80;
  const startAngle = Math.PI;      // 180°
  const endAngle = 0;               // 0°
  const totalArc = Math.PI;         // semicircle

  const filledAngle = startAngle - totalArc * probability;

  // Convert angle → SVG point
  const point = (angle: number) => ({
    x: cx + r * Math.cos(angle),
    y: cy - r * Math.sin(angle),
  });

  const bgStart = point(startAngle);
  const bgEnd = point(endAngle);
  const fillEnd = point(filledAngle);

  const largeArc = probability > 0.5 ? 1 : 0;

  const bgPath = `M ${bgStart.x} ${bgStart.y} A ${r} ${r} 0 1 1 ${bgEnd.x} ${bgEnd.y}`;
  const fillPath = `M ${bgStart.x} ${bgStart.y} A ${r} ${r} 0 ${largeArc} 1 ${fillEnd.x} ${fillEnd.y}`;

  const riskColor =
    riskLevel === "HIGH"
      ? "#ef4444"
      : riskLevel === "MEDIUM"
      ? "#f59e0b"
      : "#22c55e";

  return (
    <div className="flex flex-col items-center">
      <svg viewBox="0 0 200 120" className="w-full max-w-[240px]">
        {/* Background arc */}
        <path
          d={bgPath}
          fill="none"
          stroke="#2a2a4a"
          strokeWidth="14"
          strokeLinecap="round"
        />
        {/* Filled arc */}
        <path
          d={fillPath}
          fill="none"
          stroke={riskColor}
          strokeWidth="14"
          strokeLinecap="round"
          className="transition-all duration-700 ease-out"
          style={{
            filter: `drop-shadow(0 0 8px ${riskColor}66)`,
          }}
        />
        {/* Center text */}
        <text
          x={cx}
          y={cy - 10}
          textAnchor="middle"
          className="fill-current text-[var(--foreground)]"
          style={{ fontSize: "28px", fontWeight: 700 }}
        >
          {pct}%
        </text>
        <text
          x={cx}
          y={cy + 10}
          textAnchor="middle"
          style={{ fontSize: "11px", fill: "#8888aa" }}
        >
          Churn Risk
        </text>
      </svg>
    </div>
  );
}
