import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

def extract_text_features(data):
    """Convert text into TFIDF vectors."""

    # Initialize TFIDF Vectorizer
    subject_vectorizer = TfidfVectorizer(max_features=5000)
    body_vectorizer = TfidfVectorizer(max_features=5000)

    subject_tfidf = subject_vectorizer.fit_transform(data['clean_subject'].fillna(''))
    body_tfidf = body_vectorizer.fit_transform(data['clean_body'].fillna(''))

    # Convert to DataFrame
    subject_df = pd.DataFrame(subject_tfidf.toarray(), columns=[f"sub_tfidf_{i}" for i in range(subject_tfidf.shape[1])])
    body_df = pd.DataFrame(body_tfidf.toarray(), columns=[f"body_tfidf_{i}" for i in range(body_tfidf.shape[1])])

    # Save vectorizers for later use
    joblib.dump(subject_vectorizer, '../models/subject_vectorizer.pkl')
    joblib.dump(body_vectorizer, '../models/body_vectorizer.pkl')

    return subject_df, body_df

def run_feature_extraction(data):
    """Run feature extraction and return the features extracted."""

    # Extract features
    subject_tfidf, body_tfidf = extract_text_features(data)

    # Combine all extracted features into a new DataFrame
    feature_data = pd.concat([subject_tfidf, body_tfidf], axis=1)

    return feature_data