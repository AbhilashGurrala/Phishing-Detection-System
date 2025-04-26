import pandas as pd
import numpy as np
import joblib
import argparse
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
import warnings
warnings.filterwarnings("ignore")

# Function to evaluate a model
def evaluate_model(model_path, X_test, y_test, model_name):
    """Load a trained model and evaluate its performance on the test set."""
    print(f"\nLoading model: {model_name}")
    model = joblib.load(model_path)

    # Make predictions
    y_pred = model.predict(X_test)

    # Check if model supports probability predictions
    y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None

    # Evaluation metrics
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.4f}\n")

    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    if y_prob is not None:
        roc_auc = roc_auc_score(y_test, y_prob)
        print(f"\nROC-AUC Score: {roc_auc:.4f}")

# Command-line argument for dataset size
parser = argparse.ArgumentParser()
parser.add_argument("--size", choices=["small", "large"], default="small", help="Choose dataset size (small or large)")
args = parser.parse_args()

# Define file paths based on dataset size
if args.size == "small":
    X_test_file = '../data/X_test_small.csv'
    y_test_file = '../data/y_test_small.csv'
else:
    X_test_file = '../data/X_test_large.csv'
    y_test_file = '../data/y_test_large.csv'

# Load the test dataset
X_test = pd.read_csv(X_test_file)
y_test = pd.read_csv(y_test_file).values.ravel()

# Ensure only numeric columns are used
X_test = X_test.select_dtypes(include=['number'])

# Convert X_test to NumPy array to prevent feature name warning
X_test = np.array(X_test)

# Paths to trained models based on dataset size
if args.size == "small":
    models = {
        "Logistic Regression": "../models/logistic_regression_small.pkl",
        "Random Forest": "../models/random_forest_small.pkl",
        "XGBoost": "../models/xgboost_small.pkl",
        # "Support Vector Machine (SVM)": "../models/svm_small.pkl",
        "Naïve Bayes": "../models/naive_bayes_small.pkl",
        "Decision Tree": "../models/decision_tree_small.pkl"
    }
else:
    models = {
        "Logistic Regression": "../models/logistic_regression_large.pkl",
        "Random Forest": "../models/random_forest_large.pkl",
        "XGBoost": "../models/xgboost_large.pkl",
        # "Support Vector Machine (SVM)": "../models/svm_large.pkl",
        "Naïve Bayes": "../models/naive_bayes_large.pkl",
        "Decision Tree": "../models/decision_tree_large.pkl"
    }

# Evaluate each model
for model_name, model_path in models.items():
    evaluate_model(model_path, X_test, y_test, model_name)