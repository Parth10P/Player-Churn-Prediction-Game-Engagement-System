"use client";

import { motion } from "framer-motion";
import {
  Brain,
  Database,
  Code2,
  BarChart3,
  Server,
  Layout,
  Github,
} from "lucide-react";

const MODEL_METRICS = [
  { label: "Accuracy", value: "95.0%", color: "text-green-400" },
  { label: "ROC AUC", value: "0.94", color: "text-brand-400" },
  { label: "Precision", value: "93%", color: "text-purple-400" },
  { label: "Recall", value: "91%", color: "text-pink-400" },
];

const TECH_STACK = [
  { icon: Brain, label: "Scikit-learn", desc: "Random Forest model training" },
  { icon: Server, label: "FastAPI", desc: "High-performance REST API" },
  { icon: Layout, label: "Next.js 14", desc: "React framework with App Router" },
  { icon: Code2, label: "TypeScript", desc: "Type-safe frontend codebase" },
  { icon: Database, label: "Pandas / NumPy", desc: "Data preprocessing pipeline" },
  { icon: BarChart3, label: "Recharts", desc: "Interactive data visualisation" },
];

const FEATURES_USED = [
  "Age",
  "Gender",
  "Location",
  "GameGenre",
  "PlayTimeHours",
  "InGamePurchases",
  "GameDifficulty",
  "SessionsPerWeek",
  "AvgSessionDurationMinutes",
  "PlayerLevel",
  "AchievementsUnlocked",
  "EngagementScore (engineered)",
  "ProgressionRate (engineered)",
  "PurchaseFrequency (engineered)",
  "IsInactive (engineered)",
  "SessionConsistency (engineered)",
];

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.08, duration: 0.4 },
  }),
};

export default function AboutPage() {
  return (
    <div className="space-y-16 pb-16">
      {/* ── Header ── */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h1 className="section-heading">
          About <span className="gradient-text">ChurnGuard</span>
        </h1>
        <p className="mx-auto mt-4 max-w-2xl text-gray-400">
          An end-to-end machine learning system that predicts player churn risk
          in online games and delivers actionable engagement strategies.
        </p>
      </motion.section>

      {/* ── Model Performance ── */}
      <section>
        <h2 className="mb-6 text-2xl font-bold">Model Performance</h2>
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
          {MODEL_METRICS.map((m, i) => (
            <motion.div
              key={m.label}
              custom={i}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              variants={fadeUp}
              className="glass-card text-center"
            >
              <p className={`text-3xl font-bold ${m.color}`}>{m.value}</p>
              <p className="mt-1 text-sm text-gray-400">{m.label}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ── How It Works ── */}
      <section>
        <h2 className="mb-6 text-2xl font-bold">How It Works</h2>
        <div className="glass-card space-y-6">
          <div className="grid gap-6 md:grid-cols-3">
            {[
              {
                step: "1",
                title: "Data Input",
                desc: "Enter 11 player behaviour metrics through the prediction form.",
              },
              {
                step: "2",
                title: "Feature Engineering",
                desc: "The pipeline generates 5 additional features — EngagementScore, ProgressionRate, and more.",
              },
              {
                step: "3",
                title: "Prediction",
                desc: "A Random Forest classifier returns churn probability, risk level, and personalised recommendations.",
              },
            ].map((s, i) => (
              <motion.div
                key={s.step}
                custom={i}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true }}
                variants={fadeUp}
                className="flex gap-4"
              >
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-brand-600/20 text-brand-400 font-bold">
                  {s.step}
                </div>
                <div>
                  <h3 className="font-semibold">{s.title}</h3>
                  <p className="mt-1 text-sm text-gray-400">{s.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Features Used ── */}
      <section>
        <h2 className="mb-6 text-2xl font-bold">
          Model Features{" "}
          <span className="text-base font-normal text-gray-400">
            (16 total)
          </span>
        </h2>
        <div className="glass-card">
          <div className="flex flex-wrap gap-2">
            {FEATURES_USED.map((f) => (
              <span
                key={f}
                className={`rounded-lg border px-3 py-1.5 text-sm ${
                  f.includes("engineered")
                    ? "border-purple-500/30 bg-purple-600/10 text-purple-300"
                    : "border-[var(--border)] bg-[var(--background)] text-gray-300"
                }`}
              >
                {f}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* ── Tech Stack ── */}
      <section>
        <h2 className="mb-6 text-2xl font-bold">Tech Stack</h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {TECH_STACK.map((t, i) => (
            <motion.div
              key={t.label}
              custom={i}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              variants={fadeUp}
              className="glass-card flex items-start gap-4"
            >
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-brand-600/20 text-brand-400">
                <t.icon className="h-5 w-5" />
              </div>
              <div>
                <h3 className="font-semibold">{t.label}</h3>
                <p className="text-sm text-gray-400">{t.desc}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ── Source code link ── */}
      <motion.section
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        className="text-center"
      >
        <a
          href="https://github.com/Parth10P/Player-Churn-Prediction-Game-Engagement-System"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 rounded-xl border border-[var(--border)] px-5 py-3 text-gray-300 transition-colors hover:border-brand-500/40 hover:text-white"
        >
          <Github className="h-5 w-5" />
          View on GitHub
        </a>
      </motion.section>
    </div>
  );
}
