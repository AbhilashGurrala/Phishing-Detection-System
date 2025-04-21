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
    print("Starting Preprocessing")
    run_preprocessing(data)
    print("Preprocessing and cleaning successfully completed.")
    # Add thread analysis features
    print("Starting Thread Analysis")
    data = add_thread_features(data)
    print("Thread Analysis completed")

    # Run domain check
    print("Starting domain check")
    run_domain_check(data)
    print("Domain check successfully completed.")
    # Run phishing words check
    print("Starting phishing words check")
    run_phishing_check(data)
    print("Phishing words check completed")


    # Extract features and merge with the main DataFrame
    print("Starting feature extraction")
    features = run_feature_extraction(data)
    data = pd.concat([data, features], axis=1)
    print("Feature Extraction completed")
    # Save the updated processed data
    data.to_csv('processed_data.csv', index=False)

    print("Pre-processing, thread analysis, domain check, phishing words check, and feature extraction completed successfully.")
