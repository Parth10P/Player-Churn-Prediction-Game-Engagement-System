import pandas as pd
import numpy as np

df = pd.read_csv("data/online_gaming_behavior_dataset.csv")
df["Churned"] = df["EngagementLevel"].apply(lambda x: 1 if x == "Low" else 0)

print("Original columns:", list(df.columns))
print("Shape:", df.shape)

# players who play more often and longer.
df["EngagementScore"] = df["SessionsPerWeek"] * df["AvgSessionDurationMinutes"]

# how fast the player levels up relative to time spent
df["ProgressionRate"] = df["PlayerLevel"] / (df["PlayTimeHours"] + 1)

df["PurchaseFrequency"] = df["InGamePurchases"] / (df["PlayTimeHours"] + 1)

# using low session count as proxy for inactivity
df["IsInactive"] = (df["SessionsPerWeek"] <= 2).astype(int)

df["SessionConsistency"] = (df["SessionsPerWeek"] > 3).astype(int)
# print("SessionConsistency created (1 if SessionsPerWeek > 3)")

new_features = ["EngagementScore", "ProgressionRate", "PurchaseFrequency", "IsInactive", "SessionConsistency"]

print("\n--- Feature Statistics ---")
print(df[new_features].describe().round(2))

for feat in new_features:
    corr = df[feat].corr(df["Churned"])
    print(f"  {feat}: {corr:.4f}")


print("\nFeature engineering done!")
