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
      <div className="glass-card flex min-h-[400px] flex-col items-center justify-center gap-4 text-gray-400">
        <Loader2 className="h-10 w-10 animate-spin text-brand-400" />
        <p>Analysing player data…</p>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="glass-card flex min-h-[400px] flex-col items-center justify-center gap-3 text-gray-500">
        <ShieldAlert className="h-12 w-12 text-gray-600" />
        <p className="text-lg font-medium">No prediction yet</p>
        <p className="text-sm">
          Fill in the form and click <strong>Predict Churn</strong>.
        </p>
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
      {/* Title */}
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">Prediction Results</h2>
        <span className={riskConfig.badge}>
          <RiskIcon className="mr-1.5 h-4 w-4" />
          {riskConfig.label}
        </span>
      </div>

      {/* Gauge */}
      <GaugeChart probability={churn_probability} riskLevel={risk_level} />

      {/* Status */}
      <div className="rounded-xl border border-[var(--border)] bg-[var(--background)] p-4 text-center">
        <p className="text-sm text-gray-400">Prediction</p>
        <p className="mt-1 text-lg font-semibold">
          {will_churn ? (
            <span className="text-risk-high">⚠ Player Likely to Churn</span>
          ) : (
            <span className="text-risk-low">✅ Player Likely to Stay</span>
          )}
        </p>
        <p className="mt-1 text-sm text-gray-400">
          Churn Probability:{" "}
          <span className="font-mono font-semibold text-white">
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
              className="rounded-lg border border-[var(--border)] bg-[var(--background)] px-4 py-2.5 text-sm text-gray-300"
            >
              {rec}
            </motion.li>
          ))}
        </ul>
      </div>
    </motion.div>
  );
}
