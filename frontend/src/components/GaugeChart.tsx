"use client";

interface Props {
  probability: number; // 0 – 1
  riskLevel: "HIGH" | "MEDIUM" | "LOW";
}

export default function GaugeChart({ probability, riskLevel }: Props) {
  const pct = Math.round(probability * 100);

  const riskColor =
    riskLevel === "HIGH"
      ? "#ef4444"
      : riskLevel === "MEDIUM"
        ? "#f59e0b"
        : "#22c55e";

  // Gauge geometry
  const strokeW = 14;
  const r = 70;
  const padding = strokeW + 12; // extra room for stroke + drop-shadow
  const cx = r + padding;
  const cy = r + padding;
  const svgWidth = (r + padding) * 2;
  const svgHeight = r + padding + 30; // semicircle top half + room for text below center

  // Semicircle: from left (180°) to right (0°)
  const bgPath = `M ${cx - r} ${cy} A ${r} ${r} 0 1 1 ${cx + r} ${cy}`;

  // Filled arc
  const angle = Math.PI * (1 - probability);
  const endX = cx + r * Math.cos(angle);
  const endY = cy - r * Math.sin(angle);
  const largeArc = probability > 0.5 ? 1 : 0;
  const fillPath = `M ${cx - r} ${cy} A ${r} ${r} 0 ${largeArc} 1 ${endX} ${endY}`;

  return (
    <div className="flex flex-col items-center">
      <svg
        width="100%"
        viewBox={`0 0 ${svgWidth} ${svgHeight}`}
        className="w-48 sm:w-56"
      >
        {/* Background arc */}
        <path
          d={bgPath}
          fill="none"
          stroke="#2a2a4a"
          strokeWidth={strokeW}
          strokeLinecap="round"
        />
        {/* Filled arc */}
        <path
          d={fillPath}
          fill="none"
          stroke={riskColor}
          strokeWidth={strokeW}
          strokeLinecap="round"
          className="transition-all duration-700 ease-out"
          style={{
            filter: `drop-shadow(0 0 8px ${riskColor}66)`,
          }}
        />
        {/* Percentage text */}
        <text
          x={cx}
          y={cy - 12}
          textAnchor="middle"
          dominantBaseline="middle"
          className="fill-current text-[var(--foreground)]"
          style={{ fontSize: "30px", fontWeight: 800 }}
        >
          {pct}%
        </text>
        {/* Label */}
        <text
          x={cx}
          y={cy + 10}
          textAnchor="middle"
          dominantBaseline="middle"
          style={{ fontSize: "11px", fill: "#8888aa", letterSpacing: "0.05em" }}
        >
          Churn Risk
        </text>
      </svg>
    </div>
  );
}
