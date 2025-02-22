import pandas as pd

from preprocessing import run_preprocessing
from domain_checker import run_domain_check
from phishing_words_checker import run_phishing_check

if __name__ == "__main__":
    data = pd.read_csv('../data/sample.csv')

    run_preprocessing(data)
    run_domain_check(data)
    run_phishing_check(data)

    data.to_csv('processed_data.csv', index=False)

    print("Pre-processing, domain check and phishing words check completed successfully.")
