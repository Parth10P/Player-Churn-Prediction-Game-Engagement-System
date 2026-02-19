"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Gamepad2, BarChart3, Shield, Zap } from "lucide-react";

const FEATURES = [
  {
    icon: BarChart3,
    title: "ML-Powered Predictions",
    desc: "Random Forest model trained on 40 000+ player records with 95% accuracy.",
  },
  {
    icon: Shield,
    title: "Risk Assessment",
    desc: "Instant HIGH / MEDIUM / LOW risk classification with probability scores.",
  },
  {
    icon: Zap,
    title: "Actionable Insights",
    desc: "Smart recommendations tailored to each player's behaviour profile.",
  },
];

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.15, duration: 0.5 },
  }),
};

export default function HomePage() {
  return (
    <div className="hero-glow">
      {/* ── Hero ── */}
      <section className="flex flex-col items-center justify-center gap-6 pb-20 pt-16 text-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="flex items-center gap-2 rounded-full border border-brand-500/30 bg-brand-600/10 px-4 py-1.5 text-sm text-brand-300"
        >
          <Gamepad2 className="h-4 w-4" />
          AI-Powered Player Analytics
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.6 }}
          className="max-w-3xl text-4xl font-extrabold leading-tight sm:text-5xl lg:text-6xl"
        >
          Predict Player Churn{" "}
          <span className="gradient-text">Before It Happens</span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.6 }}
          className="max-w-2xl text-lg text-gray-400"
        >
          ChurnGuard uses machine learning to identify at-risk players and
          delivers personalised engagement strategies — so you can keep your
          community thriving.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.6 }}
          className="flex flex-wrap justify-center gap-4 pt-4"
        >
          <Link href="/predict" className="btn-primary text-lg">
            Start Predicting →
          </Link>
          <Link
            href="/about"
            className="rounded-xl border border-[var(--border)] px-6 py-3 text-lg font-semibold text-gray-300 transition-colors hover:border-brand-500/40 hover:text-white"
          >
            Learn More
          </Link>
        </motion.div>
      </section>

      {/* ── Feature Cards ── */}
      <section className="grid gap-6 pb-20 sm:grid-cols-2 lg:grid-cols-3">
        {FEATURES.map((f, i) => (
          <motion.div
            key={f.title}
            custom={i}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeUp}
            className="glass-card flex flex-col gap-4"
          >
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-600/20 text-brand-400">
              <f.icon className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-semibold">{f.title}</h3>
            <p className="text-gray-400">{f.desc}</p>
          </motion.div>
        ))}
      </section>

      {/* ── Stats bar ── */}
      <section className="grid grid-cols-2 gap-4 pb-16 sm:grid-cols-4">
        {[
          { label: "Accuracy", value: "95%" },
          { label: "ROC AUC", value: "0.94" },
          { label: "Players Analysed", value: "40K+" },
          { label: "Features", value: "16" },
        ].map((stat, i) => (
          <motion.div
            key={stat.label}
            custom={i}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeUp}
            className="glass-card text-center"
          >
            <p className="text-3xl font-bold gradient-text">{stat.value}</p>
            <p className="mt-1 text-sm text-gray-400">{stat.label}</p>
          </motion.div>
        ))}
      </section>
    </div>
  );
}
