import os
import sqlite3
import pandas as pd
from scripts import domain_checker

# sample temporary test database
TEST_DB_PATH = "test_compromised_domains.db"

def setup_test_db():
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS domains (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT UNIQUE,
            added_on TEXT DEFAULT CURRENT_DATE
        )
    ''')
    cursor.executemany("INSERT OR IGNORE INTO domains (domain) VALUES (?)", [
        ("bad-domain.com",),
        ("phish-site.net",)
    ])
    conn.commit()
    conn.close()

def test_domain_functions():
    # Setup test DB
    setup_test_db()

    # Replace connect_db to point to test DB manually
    original_connect = domain_checker.connect_db
    domain_checker.connect_db = lambda: sqlite3.connect(TEST_DB_PATH)

    # Sample test data
    test_data = pd.DataFrame({
        'sender': ['user@bad-domain.com', 'friend@safe.com'],
        'body': ['visit now: http://phish-site.net/alert', 'all safe here'],
    })

    # Run domain check
    domain_checker.run_domain_check(test_data)

    # Assertions
    assert test_data['compromised_sender'].tolist() == [True, False]
    assert test_data['compromised_url'].tolist() == [True, False]

    # Revert and delete the test database
    domain_checker.connect_db = original_connect
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
