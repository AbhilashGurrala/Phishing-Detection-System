import sqlite3
import os
import pandas as pd
import scripts.phishing_words_checker as phishing_words_checker

TEST_DB_PATH = 'test_phishing_keywords.db'

def setup_test_db():
    """Create a temporary test database with sample phishing keywords."""
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS phishing_keywords (keyword TEXT)")
    sample_keywords = ['urgent', 'prize', 'password']
    cursor.executemany("INSERT INTO phishing_keywords (keyword) VALUES (?)", [(kw,) for kw in sample_keywords])
    conn.commit()
    conn.close()

def teardown_test_db():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def test_run_phishing_check():
    setup_test_db()

    # Patch the connect_db function to use test DB
    original_connect_db = phishing_words_checker.connect_db
    phishing_words_checker.connect_db = lambda: sqlite3.connect(TEST_DB_PATH)

    # Using some sample test data
    df = pd.DataFrame({
        'subject': ['You won a prize!', 'Meeting tomorrow', 'Update your password'],
        'body': ['Click urgently', 'Link for meeting', 'Password reset now']
    })

    # Run the phishing checker
    result_df = phishing_words_checker.run_phishing_check(df)

    # Check that output columns exist
    assert 'phishing_words_in_subject' in result_df.columns
    assert 'phishing_words_in_body' in result_df.columns

    # Verify that the detection is correct
    assert result_df['phishing_words_in_subject'].tolist() == ['prize', '', 'password']
    assert result_df['phishing_words_in_body'].tolist() == ['', '', 'password']
    # Restore original DB connection function
    phishing_words_checker.connect_db = original_connect_db
    teardown_test_db()