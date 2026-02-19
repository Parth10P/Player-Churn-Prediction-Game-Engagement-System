import axios from "axios";
import type { PlayerInput, PredictionResponse, HealthResponse, ModelInfoResponse } from "./types";

const API = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
  timeout: 15000,
});

/** Predict churn for a single player */
export async function predictChurn(data: PlayerInput): Promise<PredictionResponse> {
  const res = await API.post<PredictionResponse>("/predict", data);
  return res.data;
}

/** Check if the API is alive */
export async function checkHealth(): Promise<HealthResponse> {
  const res = await API.get<HealthResponse>("/health");
  return res.data;
}

/** Get model metadata */
export async function getModelInfo(): Promise<ModelInfoResponse> {
  const res = await API.get<ModelInfoResponse>("/model/info");
  return res.data;
}
