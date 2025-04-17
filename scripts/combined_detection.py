import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def combined_detection():
    """Combine predictions from Random Forest, XGBoost, and Anomaly Detection models on the small dataset."""

    # Load small test dataset
    X_test = pd.read_csv('../data/X_test_small.csv')
    y_test = pd.read_csv('../data/y_test_small.csv').values.ravel()

    # Keep numeric columns only
    X_test_numeric = X_test.select_dtypes(include=['number'])

    # Load pre-trained models
    rf_model = joblib.load('../models/random_forest_small.pkl')
    xgb_model = joblib.load('../models/xgboost_small.pkl')
    anomaly_detector = joblib.load('../models/isolation_forest.pkl')

    # Predict using Random Forest and XGBoost
    rf_pred = rf_model.predict(X_test_numeric)
    xgb_pred = xgb_model.predict(X_test_numeric)

    # Anomaly Detection predictions (Isolation Forest: -1 = anomaly/phishing, 1 = normal)
    anomaly_pred = anomaly_detector.predict(X_test_numeric)
    anomaly_pred = [0 if pred == -1 else 1 for pred in anomaly_pred]

    # Combined predictions (phishing if any model flags as phishing)
    combined_pred = []
    for rf, xgb, anomaly in zip(rf_pred, xgb_pred, anomaly_pred):
        if rf == 1 or xgb == 1 or anomaly == 0:
            combined_pred.append("Phishing")
        else:
            combined_pred.append("Legitimate")

    # Evaluate combined model performance
    binary_pred = [1 if label == "Phishing" else 0 for label in combined_pred]
    accuracy = accuracy_score(y_test, binary_pred)
    print(f"Combined Detection Accuracy (small dataset): {accuracy:.4f}")

    print("\nClassification Report:")
    print(classification_report(y_test, binary_pred))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, binary_pred))

    # Add actual labels and prediction results
    X_test['Actual Label'] = ["Phishing" if label == 1 else "Legitimate" for label in y_test]
    X_test['Result'] = combined_pred

    # Select specific columns to save
    columns_to_keep = [
        'sender', 'receiver', 'date', 'subject', 'body', 'urls', 'clean_subject',
        'clean_body', 'sender_domain', 'compromised_sender', 'extracted_domains',
        'compromised_url', 'phishing_words_in_subject', 'phishing_words_in_body',
        'Actual Label', 'Result'
    ]
    results_df = X_test[columns_to_keep]

    # Save results to CSV
    results_df.to_csv('../data/combined_detection_results_small.csv', index=False)
    print("Combined detection results saved as combined_detection_results_small.csv")

if __name__ == "__main__":
    combined_detection()