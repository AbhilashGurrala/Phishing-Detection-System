import joblib
import pandas as pd
import argparse
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def combined_detection(X_path, y_path, rf_model_path, xgb_model_path, anomaly_model_path, output_path):
    """Combine predictions from RF, XGBoost, and Anomaly Detection models."""
    X_test = pd.read_csv(X_path)
    y_test = pd.read_csv(y_path).values.ravel()

    # Keep numeric columns only for model input
    X_test_numeric = X_test.select_dtypes(include=['number'])

    # Load models
    rf_model = joblib.load(rf_model_path)
    xgb_model = joblib.load(xgb_model_path)
    anomaly_detector = joblib.load(anomaly_model_path)

    # Predictions
    rf_probs = rf_model.predict_proba(X_test_numeric)[:, 1]
    xgb_probs = xgb_model.predict_proba(X_test_numeric)[:, 1]

    rf_pred = (rf_probs >= 0.5).astype(int)
    xgb_pred = (xgb_probs >= 0.5).astype(int)
    anomaly_pred = [0 if pred == -1 else 1 for pred in anomaly_detector.predict(X_test_numeric)]

    # Combine logic
    # Adjusted logic: require at least 2 phishing votes
    combined_pred = [
        "Phishing" if (rf + xgb + (1 if anomaly == 0 else 0)) >= 2 else "Legitimate"
        for rf, xgb, anomaly in zip(rf_pred, xgb_pred, anomaly_pred)
    ]

    binary_pred = [1 if label == "Phishing" else 0 for label in combined_pred]
    accuracy = accuracy_score(y_test, binary_pred)

    # Calculate average confidence score between Random Forest and XGBoost
    confidence_scores = ((rf_probs + xgb_probs) / 2).round(4)

    print(f"\nCombined Detection Accuracy ({output_path}): {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, binary_pred))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, binary_pred))

    # Add results to the original data
    X_test['Actual Label'] = ["Phishing" if y == 1 else "Legitimate" for y in y_test]
    X_test['Result'] = combined_pred
    X_test['Confidence Score'] = (confidence_scores * 100).round(2).astype(str) + '%'

    # Ensure columns exist before selecting
    columns_to_keep = [
        'sender', 'receiver', 'date', 'subject', 'body', 'urls', 'clean_subject',
        'clean_body', 'sender_domain', 'compromised_sender', 'extracted_domains',
        'compromised_url', 'phishing_words_in_subject', 'phishing_words_in_body',
        'is_thread_reply', 'deviates_from_thread','Actual Label', 'Result', 'Confidence Score'
    ]
    available_columns = [col for col in columns_to_keep if col in X_test.columns]
    results_df = X_test[available_columns]

    results_df.to_csv(output_path, index=False)
    print(f"Results saved to {output_path}")
    return accuracy

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
        anomaly_model_path = "../models/isolation_forest_large.pkl"
        output_path = "../data/combined_detection_results_small.csv"
    else:
        X_path = "../data/X_test_large.csv"
        y_path = "../data/y_test_large.csv"
        rf_model_path = "../models/random_forest_large.pkl"
        xgb_model_path = "../models/xgboost_large.pkl"
        anomaly_model_path = "../models/isolation_forest_large.pkl"
        output_path = "../data/combined_detection_results_large.csv"

    combined_detection(
        X_path, y_path, rf_model_path, xgb_model_path, anomaly_model_path, output_path
    )