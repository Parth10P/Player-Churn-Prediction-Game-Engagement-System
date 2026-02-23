"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    Cell,
} from "recharts";
import { getModelComparison, getFeatureImportance } from "@/lib/api";
import type {
    ModelCompareResponse,
    FeatureImportanceItem,
} from "@/lib/types";
import { BarChart3, GitCompareArrows, Loader2 } from "lucide-react";

/* ─── Colour palette for feature-importance bars ─── */
const BAR_COLOURS = [
    "#6366f1", "#8b5cf6", "#a855f7", "#c084fc", "#d8b4fe",
    "#818cf8", "#7c3aed", "#6d28d9", "#5b21b6", "#4f46e5",
    "#4338ca", "#3730a3", "#312e81", "#6366f1", "#818cf8",
    "#a5b4fc",
];

/* ──────────────────────────────────────────────────── */

export default function ModelComparison() {
    const [comparison, setComparison] = useState<ModelCompareResponse | null>(null);
    const [features, setFeatures] = useState<FeatureImportanceItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function fetchData() {
            try {
                const [cmp, fi] = await Promise.all([
                    getModelComparison(),
                    getFeatureImportance(),
                ]);
                setComparison(cmp);
                setFeatures(fi.feature_importance);
            } catch (err: unknown) {
                setError(
                    err instanceof Error ? err.message : "Failed to fetch model data"
                );
            } finally {
                setLoading(false);
            }
        }
        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="glass-card flex items-center justify-center gap-3 py-16 text-gray-400">
                <Loader2 className="h-6 w-6 animate-spin text-brand-400" />
                Loading model data…
            </div>
        );
    }

    if (error) {
        return (
            <div className="glass-card py-10 text-center text-gray-500">
                <p className="text-sm">{error}</p>
                <p className="mt-1 text-xs text-gray-600">
                    Make sure both models have been trained.
                </p>
            </div>
        );
    }

    const metricKeys = comparison
        ? Object.keys(
            comparison.logistic_regression ?? comparison.random_forest ?? {}
        )
        : [];

    return (
        <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.35 }}
            className="mt-12 space-y-8"
        >
            {/* ── Metrics comparison table ─── */}
            {comparison && (
                <div className="glass-card">
                    <div className="mb-5 flex items-center gap-2">
                        <GitCompareArrows className="h-5 w-5 text-brand-400" />
                        <h2 className="text-xl font-semibold">Model Comparison</h2>
                    </div>

                    <div className="overflow-x-auto">
                        <table className="w-full text-sm">
                            <thead>
                                <tr className="border-b border-[var(--border)] text-left text-gray-400">
                                    <th className="pb-3 pr-4 font-medium">Metric</th>
                                    <th className="pb-3 pr-4 font-medium">Logistic Regression</th>
                                    <th className="pb-3 font-medium">Random Forest</th>
                                </tr>
                            </thead>
                            <tbody>
                                {metricKeys.map((metric) => {
                                    const lr = comparison.logistic_regression?.[metric];
                                    const rf = comparison.random_forest?.[metric];
                                    const better =
                                        lr !== undefined && rf !== undefined
                                            ? rf > lr
                                                ? "rf"
                                                : rf < lr
                                                    ? "lr"
                                                    : "tie"
                                            : null;

                                    return (
                                        <tr
                                            key={metric}
                                            className="border-b border-[var(--border)]/50 last:border-0"
                                        >
                                            <td className="py-3 pr-4 font-medium text-gray-300">
                                                {metric}
                                            </td>
                                            <td
                                                className={`py-3 pr-4 font-mono ${better === "lr"
                                                        ? "text-brand-400 font-semibold"
                                                        : "text-gray-400"
                                                    }`}
                                            >
                                                {lr !== undefined ? lr.toFixed(4) : "—"}
                                            </td>
                                            <td
                                                className={`py-3 font-mono ${better === "rf"
                                                        ? "text-brand-400 font-semibold"
                                                        : "text-gray-400"
                                                    }`}
                                            >
                                                {rf !== undefined ? rf.toFixed(4) : "—"}
                                            </td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}

            {/* ── Feature importance chart ─── */}
            {features.length > 0 && (
                <div className="glass-card">
                    <div className="mb-5 flex items-center gap-2">
                        <BarChart3 className="h-5 w-5 text-brand-400" />
                        <h2 className="text-xl font-semibold">
                            Feature Importance{" "}
                            <span className="text-sm font-normal text-gray-500">
                                (Random Forest)
                            </span>
                        </h2>
                    </div>

                    <ResponsiveContainer width="100%" height={features.length * 36 + 20}>
                        <BarChart
                            data={features}
                            layout="vertical"
                            margin={{ left: 140, right: 20, top: 5, bottom: 5 }}
                        >
                            <XAxis type="number" tick={{ fill: "#9ca3af", fontSize: 12 }} />
                            <YAxis
                                type="category"
                                dataKey="feature"
                                tick={{ fill: "#d1d5db", fontSize: 12 }}
                                width={130}
                            />
                            <Tooltip
                                contentStyle={{
                                    background: "var(--card)",
                                    border: "1px solid var(--border)",
                                    borderRadius: "0.75rem",
                                    color: "var(--foreground)",
                                }}
                                formatter={(value: number) => [value.toFixed(4), "Importance"]}
                            />
                            <Bar dataKey="importance" radius={[0, 6, 6, 0]}>
                                {features.map((_, index) => (
                                    <Cell
                                        key={index}
                                        fill={BAR_COLOURS[index % BAR_COLOURS.length]}
                                    />
                                ))}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            )}
        </motion.section>
    );
}
