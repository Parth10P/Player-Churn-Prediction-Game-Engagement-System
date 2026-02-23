"use client";

import { motion } from "framer-motion";
import {
  Brain,
  BarChart3,
  Layers,
  Server,
  Monitor,
  Paintbrush,
  Info,
} from "lucide-react";

const MODEL_STATS = [
  { label: "Algorithm", value: "Random Forest" },
  { label: "Estimators", value: "200" },
  { label: "Accuracy", value: "95.0%" },
  { label: "ROC AUC", value: "0.94" },
  { label: "Dataset", value: "40,034 records" },
  { label: "Features", value: "16 (11 + 5)" },
];

const TECH_STACK = [
  {
    icon: Brain,
    layer: "Machine Learning",
    tools: "scikit-learn · pandas · NumPy · joblib",
  },
  {
    icon: Server,
    layer: "Backend",
    tools: "FastAPI · Pydantic · Uvicorn",
  },
  {
    icon: Monitor,
    layer: "Frontend",
    tools: "Next.js 14 · React 18 · TypeScript",
  },
  {
    icon: Paintbrush,
    layer: "Styling & UI",
    tools: "Tailwind CSS · Framer Motion · Lucide Icons",
  },
];

const ENGINEERED = [
  { name: "EngagementScore", formula: "SessionsPerWeek × AvgSessionDuration" },
  { name: "ProgressionRate", formula: "PlayerLevel / (PlayTimeHours + 1)" },
  { name: "PurchaseFrequency", formula: "InGamePurchases (binary)" },
  { name: "IsInactive", formula: "1 if SessionsPerWeek ≤ 2" },
  { name: "SessionConsistency", formula: "1 if SessionsPerWeek > 3" },
];

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.08, duration: 0.45 },
  }),
};

export default function AboutPage() {
  return (
    <div className="space-y-14 pb-16">
      {/* ── Header ── */}
      <section className="text-center">
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-4 inline-flex items-center gap-2 rounded-full border border-brand-500/30 bg-brand-600/10 px-4 py-1.5 text-sm text-brand-300"
        >
          <Info className="h-4 w-4" />
          About ChurnGuard
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="text-3xl font-extrabold tracking-tight sm:text-4xl"
        >
          How <span className="gradient-text">It Works</span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mx-auto mt-3 max-w-xl text-gray-400"
        >
          A deep dive into the model, the features it uses, and the technology
          powering ChurnGuard.
        </motion.p>
      </section>

      {/* ── Model Stats ── */}
      <section>
        <h2 className="section-heading mb-6 flex items-center gap-3">
          <BarChart3 className="h-7 w-7 text-brand-400" />
          Model Performance
        </h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {MODEL_STATS.map((s, i) => (
            <motion.div
              key={s.label}
              custom={i}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              variants={fadeUp}
              className="glass-card text-center"
            >
              <p className="text-2xl font-bold gradient-text">{s.value}</p>
              <p className="mt-1 text-sm text-gray-400">{s.label}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ── Engineered Features ── */}
      <section>
        <h2 className="section-heading mb-6 flex items-center gap-3">
          <Layers className="h-7 w-7 text-brand-400" />
          Engineered Features
        </h2>
        <div className="space-y-3">
          {ENGINEERED.map((f, i) => (
            <motion.div
              key={f.name}
              custom={i}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              variants={fadeUp}
              className="glass-card flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between"
            >
              <span className="font-semibold text-brand-300 font-mono text-sm">
                {f.name}
              </span>
              <span className="text-sm text-gray-400">{f.formula}</span>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ── Tech Stack ── */}
      <section>
        <h2 className="section-heading mb-6 flex items-center gap-3">
          <Brain className="h-7 w-7 text-brand-400" />
          Tech Stack
        </h2>
        <div className="grid gap-4 sm:grid-cols-2">
          {TECH_STACK.map((t, i) => (
            <motion.div
              key={t.layer}
              custom={i}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              variants={fadeUp}
              className="glass-card flex items-start gap-4"
            >
              <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-brand-600/20 text-brand-400">
                <t.icon className="h-5 w-5" />
              </div>
              <div>
                <p className="font-semibold">{t.layer}</p>
                <p className="mt-0.5 text-sm text-gray-400">{t.tools}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </section>
    </div>
  );
}
