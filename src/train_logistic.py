import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

from preprocess import X_train_scaled, X_test_scaled, y_train, y_test

def main():
    os.makedirs("models", exist_ok=True)
    os.makedirs("notebooks/plots", exist_ok=True)
    
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train_scaled, y_train)
    
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    
    print(f"Model trained successfully! F1 Score: {f1:.4f}")
    
    # Save results
    results_path = "models/logistic_results.txt"
    with open(results_path, "w") as f:
        f.write("Logistic Regression Evaluation Metrics\n")
        f.write("======================================\n")
        f.write(f"Accuracy: {acc:.4f}\n")
        f.write(f"Precision: {prec:.4f}\n")
        f.write(f"Recall: {rec:.4f}\n")
        f.write(f"F1 Score: {f1:.4f}\n")
        f.write(f"ROC-AUC: {roc_auc:.4f}\n")
    
    model_path = "models/logistic_model.pkl"
    joblib.dump(model, model_path)
    
    print(f"Exported metrics to {results_path}")
    print(f"Exported model to {model_path}")
    
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Active', 'Churned'], 
                yticklabels=['Active', 'Churned'])
    plt.title('Logistic Regression Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.tight_layout()
    cm_path = "notebooks/plots/confusion_matrix_logistic.png"
    plt.savefig(cm_path)
    plt.close()

if __name__ == "__main__":
    main()
