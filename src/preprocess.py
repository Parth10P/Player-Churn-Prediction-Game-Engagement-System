import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os

df = pd.read_csv("data/online_gaming_behavior_dataset.csv")

# print(df.isnull().sum()) 
# no missing values found in any column so no need to fill with median/mode
df["Churned"] = df["EngagementLevel"].apply(lambda x: 1 if x == "Low" else 0)

categorical_cols = ["Gender", "Location", "GameGenre", "GameDifficulty"]
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le
    print(f"{col}: {list(le.classes_)}")


os.makedirs("models", exist_ok=True)
joblib.dump(label_encoders, "models/label_encoders.pkl")

X = df.drop(columns=["PlayerID", "EngagementLevel", "Churned"])
y = df["Churned"]

# print(list(X.columns))
# print(X.shape)
# print(y.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns, index=X_train.index)
X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns, index=X_test.index)

joblib.dump(scaler, "models/scaler.pkl")
print("\nScaler saved to models/scaler.pkl")

print("\n--- Scaled Data Sample ---")
print(X_train_scaled.head())

print("\nPreprocessing done!")
