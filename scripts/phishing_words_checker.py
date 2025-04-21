import sqlite3
import pandas as pd
import re
import os
#  Connect to the database
DB_PATH = 'data/compromised_domains.db'

def connect_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def get_phishing_words():
    """Get the phishing words from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT keyword FROM phishing_keywords")
    keywords = [row[0].lower() for row in cursor.fetchall()]
    conn.close()
    pattern = r'\b(?:' + '|'.join(re.escape(word) for word in keywords) + r')\b'
    return re.compile(pattern, re.IGNORECASE), keywords

def check_phishing_words(text, pattern, keywords):
    """Check if the text contains any phishing words."""
    if pd.isnull(text):
        return ""
    matches = pattern.findall(text.lower())
    matched_words = sorted({match for match in matches if match in keywords})
    return ', '.join(matched_words) if matched_words else ""

def run_phishing_check(data):
    """Apply the check for phishing words"""
    pattern, keywords = get_phishing_words()

    # Check phishing words in subject and body
    data['phishing_words_in_subject'] = data['subject'].apply(lambda x: check_phishing_words(x, pattern, keywords))
    data['phishing_words_in_body'] = data['body'].apply(lambda x: check_phishing_words(x, pattern, keywords))

    data = data.assign(
        phishing_words_in_subject=data['phishing_words_in_subject'].fillna(""),
        phishing_words_in_body=data['phishing_words_in_body'].fillna("")
    )

    return data