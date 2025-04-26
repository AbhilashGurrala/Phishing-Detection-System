import pandas as pd
import time
from preprocessing import run_preprocessing
from domain_checker import run_domain_check
from phishing_words_checker import run_phishing_check
from feature_extraction import run_feature_extraction
from scripts.thread_analysis import add_thread_features
from dataset_split import split_dataset
from combined_detection import combined_detection
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
from email_notification import send_email_notification, notify_if_phishing

if __name__ == "__main__":
    start_time = time.time()

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

    data['phishing_words_in_subject'] = data['phishing_words_in_subject'].apply(lambda x: int(bool(x)))
    data['phishing_words_in_body'] = data['phishing_words_in_body'].apply(lambda x: int(bool(x)))
    data['compromised_sender'] = data['compromised_sender'].astype(int)
    data['compromised_url'] = data['compromised_url'].astype(int)
    # Extract features and merge with the main DataFrame
    print("Starting feature extraction")
    features = run_feature_extraction(data)
    data = pd.concat([data, features], axis=1)
    print("Feature Extraction completed")
    # Save the updated processed data
    data.to_csv('processed_data.csv', index=False)

    print("Pre-processing, thread analysis, domain check, phishing words check, and feature extraction completed successfully.")

    # Split the dataset
    print("Starting dataset split...")
    split_dataset('processed_data.csv', small_size=3000)
    print("Dataset split completed.")

    # Run combined detection on large dataset
    print("Running combined detection...")
    combined_detection(
        X_path='../data/X_test_large.csv',
        y_path='../data/y_test_large.csv',
        rf_model_path='../models/random_forest_large.pkl',
        xgb_model_path='../models/xgboost_large.pkl',
        anomaly_model_path='../models/isolation_forest_large.pkl',
        output_path='../data/combined_detection_results_large.csv'
    )
    print("Combined detection completed.")

    # Send email notifications
    print("Checking for phishing notifications...")
    notify_if_phishing()
    print("Email notifications have been sent.")

    end_time = time.time()  # End timer
    elapsed_time = round(end_time - start_time, 2)
    print(f"\nScript finished in {elapsed_time} seconds.")