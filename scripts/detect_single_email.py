import pandas as pd
import re
import joblib
from preprocessing import preprocess
from thread_analysis import is_reply  # Using only basic thread logic
from domain_checker import check_domain, extract_sender_domain, get_compromised_domains
from phishing_words_checker import get_phishing_words, check_phishing_words
from sklearn.impute import SimpleImputer
from scipy.sparse import hstack

# Load trained models and vectorizers
rf_model = joblib.load("../models/random_forest_large.pkl")
xgb_model = joblib.load("../models/xgboost_large.pkl")
anomaly_model = joblib.load("../models/isolation_forest_large.pkl")
subject_vectorizer = joblib.load("../models/subject_vectorizer.pkl")
body_vectorizer = joblib.load("../models/body_vectorizer.pkl")

# Load external data
compromised_domains = get_compromised_domains()
phishing_pattern, phishing_keywords = get_phishing_words()

def detect_single_email(sender, receiver, subject, body):
    # Clean text
    clean_subject = preprocess(subject)
    clean_body = preprocess(body)

    # TF-IDF features
    subject_tfidf = subject_vectorizer.transform([clean_subject])
    body_tfidf = body_vectorizer.transform([clean_body])

    # Thread + domain + phishing word checks
    sender_domain = extract_sender_domain(sender)
    compromised_sender = int(check_domain(sender_domain, compromised_domains))

    body_domains = re.findall(r'\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', body.lower())
    compromised_url = any(check_domain(domain, compromised_domains) for domain in body_domains)

    phishing_sub = check_phishing_words(subject, phishing_pattern, phishing_keywords)
    phishing_body = check_phishing_words(body, phishing_pattern, phishing_keywords)

    is_thread_reply = is_reply(subject)
    deviates_from_thread = 0  # Not applicable in single email detection

    # Build numeric feature set
    extra_features = pd.DataFrame([{
        "urls": int(bool(body_domains)),
        "compromised_sender": compromised_sender,
        "compromised_url": int(compromised_url),
        "phishing_words_in_subject": int(bool(phishing_sub)),
        "phishing_words_in_body": int(bool(phishing_body)),
        "is_thread_reply": is_thread_reply,
        "deviates_from_thread": deviates_from_thread
    }])

    imputer = SimpleImputer(strategy="mean")
    numeric_data = imputer.fit_transform(extra_features)

    # Combine TF-IDF + numeric features
    full_input = hstack([subject_tfidf, body_tfidf, numeric_data])
    print("Prediction input shape:", full_input.shape)
    # Predictions
    rf_probs = rf_model.predict_proba(full_input)[:, 1]
    xgb_probs = xgb_model.predict_proba(full_input)[:, 1]
    anomaly_pred = anomaly_model.predict(full_input)
    rf_pred = int(rf_probs[0] >= 0.5)
    xgb_pred = int(xgb_probs[0] >= 0.5)
    anomaly_flag = int(anomaly_pred[0] != -1)
    print("RF pred:", rf_pred)
    print("XGB pred:", xgb_pred)
    print("Anomaly pred:", anomaly_flag)

    # Final result
    is_phishing = rf_pred == 1 or xgb_pred == 1 or anomaly_flag == 0
    result = "Phishing" if is_phishing else "Legitimate"

    # Confidence score
    confidence = round(((rf_probs[0] + xgb_probs[0]) / 2) * 100, 2)

    return result, confidence