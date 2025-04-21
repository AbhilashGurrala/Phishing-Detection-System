import pandas as pd

from preprocessing import run_preprocessing
from domain_checker import run_domain_check
from phishing_words_checker import run_phishing_check
from feature_extraction import run_feature_extraction
from scripts.thread_analysis import add_thread_features

if __name__ == "__main__":
    # Load the full dataset
    data = pd.read_csv('../data/CEAS_08.csv')
    # Run preprocessing
    run_preprocessing(data)
    # Add thread analysis features
    data = add_thread_features(data)
    # Run domain check
    run_domain_check(data)
    # Run phishing words check
    run_phishing_check(data)

    # Extract features and merge with the main DataFrame
    features = run_feature_extraction(data)
    data = pd.concat([data, features], axis=1)

    # Save the updated processed data
    data.to_csv('processed_data.csv', index=False)

    print("Pre-processing, domain check, phishing words check, and feature extraction completed successfully.")
