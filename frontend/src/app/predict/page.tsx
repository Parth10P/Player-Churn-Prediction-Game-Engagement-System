"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import PredictionForm from "@/components/PredictionForm";
import ResultsDisplay from "@/components/ResultsDisplay";
import type { PredictionResponse } from "@/lib/types";
import { Sparkles } from "lucide-react";

export default function PredictPage() {
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [loading, setLoading] = useState(false);

  return (
    <div>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-10 text-center"
      >
        <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-brand-500/30 bg-brand-600/10 px-3 py-1 text-sm text-brand-300">
          <Sparkles className="h-4 w-4" />
          Real-time Prediction
        </div>
        <h1 className="section-heading">
          Predict <span className="gradient-text">Player Churn</span>
        </h1>
        <p className="mx-auto mt-3 max-w-xl text-gray-400">
          Enter player behaviour data below and our ML model will predict the
          likelihood of churn along with tailored recommendations.
        </p>
      </motion.div>

      {/* Two-column layout */}
      <div className="grid gap-8 lg:grid-cols-2">
        {/* Left — Form */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.15 }}
        >
          <PredictionForm
            onResult={setResult}
            loading={loading}
            setLoading={setLoading}
          />
        </motion.div>

        {/* Right — Results */}
        <motion.div
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.25 }}
        >
          <ResultsDisplay result={result} loading={loading} />
        </motion.div>
      </div>
    </div>
  );
}
