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

  const fillDeg = probability * 180;
  const size = 200;
  const stroke = 16;
  const innerSize = size - stroke * 2;

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        width: size,
        margin: "0 auto",
      }}
    >
      {/* Gauge wrapper — clips to semicircle */}
      <div
        style={{
          width: size,
          height: size / 2,
          overflow: "hidden",
          position: "relative",
        }}
      >
        {/* Full circle with conic-gradient, only top half visible */}
        <div
          style={{
            width: size,
            height: size,
            borderRadius: "50%",
            background: `conic-gradient(
              from 270deg,
              ${riskColor} 0deg ${fillDeg}deg,
              #2a2a4a ${fillDeg}deg 180deg,
              transparent 180deg 360deg
            )`,
          }}
        />
        {/* Inner circle cutout → donut shape */}
        <div
          style={{
            position: "absolute",
            top: stroke,
            left: stroke,
            width: innerSize,
            height: innerSize,
            borderRadius: "50%",
            background: "var(--card, #1a1a2e)",
          }}
        />
      </div>

      {/* Text positioned inside the gauge arc */}
      <div
        style={{
          textAlign: "center",
          marginTop: -(size / 2 - stroke - 8),
          position: "relative",
          zIndex: 2,
        }}
      >
        <span
          style={{
            fontSize: 36,
            fontWeight: 800,
            color: "var(--foreground, #f0f0ff)",
            display: "block",
            lineHeight: 1,
            filter: `drop-shadow(0 0 12px ${riskColor}44)`,
          }}
        >
          {pct}%
        </span>
        <span
          style={{
            fontSize: 11,
            color: "#8888aa",
            letterSpacing: "0.06em",
            display: "block",
            marginTop: 4,
          }}
        >
          Churn Risk
        </span>
      </div>
    </div>
  );
}
