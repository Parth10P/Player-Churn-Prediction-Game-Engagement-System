"use client";

import { motion } from "framer-motion";
import type { PredictionResponse } from "@/lib/types";
import GaugeChart from "./GaugeChart";
import {
  AlertTriangle,
  CheckCircle2,
  ShieldAlert,
  Lightbulb,
  Loader2,
} from "lucide-react";

interface Props {
  result: PredictionResponse | null;
  loading: boolean;
}

export default function ResultsDisplay({ result, loading }: Props) {
  if (loading) {
    return (
      <div className="glass-card flex min-h-[520px] flex-col items-center justify-center gap-4 text-gray-400">
        <Loader2 className="h-10 w-10 animate-spin text-brand-400" />
        <p className="text-sm">Analysing player data…</p>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="glass-card flex min-h-[520px] flex-col items-center justify-center gap-4 text-gray-500">
        <ShieldAlert className="h-14 w-14 text-gray-600" />
        <div className="text-center">
          <p className="text-lg font-semibold text-gray-400">
            No prediction yet
          </p>
          <p className="mt-1 text-sm">
            Fill in the form and click{" "}
            <strong className="text-brand-300">Predict Churn</strong>.
          </p>
        </div>
      </div>
    );
  }

  const { churn_probability, will_churn, risk_level, recommendations } = result;

  const riskConfig = {
    HIGH: {
      badge: "risk-badge-high",
      icon: AlertTriangle,
      label: "High Risk",
      border: "border-risk-high/30",
    },
    MEDIUM: {
      badge: "risk-badge-medium",
      icon: AlertTriangle,
      label: "Medium Risk",
      border: "border-risk-medium/30",
    },
    LOW: {
      badge: "risk-badge-low",
      icon: CheckCircle2,
      label: "Low Risk",
      border: "border-risk-low/30",
    },
  }[risk_level];

  const RiskIcon = riskConfig.icon;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.4 }}
      className={`glass-card space-y-6 ${riskConfig.border}`}
    >
      {/* Title + Badge */}
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">Prediction Results</h2>
        <span className={riskConfig.badge}>
          <RiskIcon className="mr-1.5 h-4 w-4" />
          {riskConfig.label}
        </span>
      </div>

      {/* Gauge */}
      <div className="flex justify-center py-2">
        <GaugeChart probability={churn_probability} riskLevel={risk_level} />
      </div>

      {/* Status card */}
      <div className="rounded-xl border border-[var(--border)] bg-[var(--background)]/60 p-5 text-center">
        <p className="text-xs font-medium uppercase tracking-wider text-gray-500">
          Prediction
        </p>
        <p className="mt-2 text-lg font-semibold">
          {will_churn ? (
            <span className="text-risk-high">⚠ Player Likely to Churn</span>
          ) : (
            <span className="text-risk-low">✅ Player Likely to Stay</span>
          )}
        </p>
        <p className="mt-2 text-sm text-gray-400">
          Churn Probability:{" "}
          <span className="font-mono font-bold text-white">
            {(churn_probability * 100).toFixed(1)}%
          </span>
        </p>
      </div>

      {/* Recommendations */}
      <div>
        <div className="mb-3 flex items-center gap-2 text-sm font-semibold text-gray-300">
          <Lightbulb className="h-4 w-4 text-brand-400" />
          Recommendations
        </div>
        <ul className="space-y-2">
          {recommendations.map((rec, i) => (
            <motion.li
              key={i}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 * i }}
              className="rounded-xl border border-[var(--border)] bg-[var(--background)]/60 px-4 py-3 text-sm text-gray-300"
            >
              {rec}
            </motion.li>
          ))}
        </ul>
      </div>
    </motion.div>
  );
}
