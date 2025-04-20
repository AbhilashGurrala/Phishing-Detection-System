import joblib
import pandas as pd
import argparse
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def combined_detection(X_path, y_path, rf_model_path, xgb_model_path, anomaly_model_path, output_path):
    """Combine predictions from RF, XGBoost, and Anomaly Detection models."""
    X_test = pd.read_csv(X_path)
    y_test = pd.read_csv(y_path).values.ravel()

    # Keep numeric columns only
    X_test_numeric = X_test.select_dtypes(include=['number'])

    # Load models
    rf_model = joblib.load(rf_model_path)
    xgb_model = joblib.load(xgb_model_path)
    anomaly_detector = joblib.load(anomaly_model_path)

    # Predictions
    rf_pred = rf_model.predict(X_test_numeric)
    xgb_pred = xgb_model.predict(X_test_numeric)
    anomaly_pred = [0 if pred == -1 else 1 for pred in anomaly_detector.predict(X_test_numeric)]

    # Combine logic
    combined_pred = [
        "Phishing" if rf == 1 or xgb == 1 or anomaly == 0 else "Legitimate"
        for rf, xgb, anomaly in zip(rf_pred, xgb_pred, anomaly_pred)
    ]

    binary_pred = [1 if label == "Phishing" else 0 for label in combined_pred]
    accuracy = accuracy_score(y_test, binary_pred)

    print(f"\nCombined Detection Accuracy ({output_path}): {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, binary_pred))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, binary_pred))

    # Add results to the original data
    X_test['Actual Label'] = ["Phishing" if y == 1 else "Legitimate" for y in y_test]
    X_test['Result'] = combined_pred

    # Save only selected columns
    columns_to_keep = [
        'sender', 'receiver', 'date', 'subject', 'body', 'urls', 'clean_subject',
        'clean_body', 'sender_domain', 'compromised_sender', 'extracted_domains',
        'compromised_url', 'phishing_words_in_subject', 'phishing_words_in_body',
        'Actual Label', 'Result'
    ]
    results_df = X_test[columns_to_keep]
    results_df.to_csv(output_path, index=False)
    print(f"Results saved to {output_path}")
    return accuracy

# Only runs if this script is called directly
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", choices=["small", "large"], default="small", help="Choose dataset size")
    args = parser.parse_args()

    # File paths for small and large
    if args.size == "small":
        X_path = "../data/X_test_small.csv"
        y_path = "../data/y_test_small.csv"
        rf_model_path = "../models/random_forest_small.pkl"
        xgb_model_path = "../models/xgboost_small.pkl"
        anomaly_model_path = "../models/isolation_forest.pkl"  # same for both sizes
        output_path = "../data/combined_detection_results_small.csv"
    else:
        X_path = "../data/X_test_large.csv"
        y_path = "../data/y_test_large.csv"
        rf_model_path = "../models/random_forest_large.pkl"
        xgb_model_path = "../models/xgboost_large.pkl"
        anomaly_model_path = "../models/isolation_forest.pkl"
        output_path = "../data/combined_detection_results_large.csv"

    combined_detection(
        X_path, y_path, rf_model_path, xgb_model_path, anomaly_model_path, output_path
    )