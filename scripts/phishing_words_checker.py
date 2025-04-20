import sqlite3
import pandas as pd
import re

#  Connect to the database
def connect_db():
    return sqlite3.connect('../data/compromised_domains.db')

def get_phishing_words():
    """Get the phishing words from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT keyword FROM phishing_keywords")
    keywords = {row[0].lower() for row in cursor.fetchall()}
    conn.close()
    return keywords

def check_phishing_words(text, keywords):
    """Check if the text contains any phishing words."""
    if pd.isnull(text):
        return None
    text = text.lower()
    matched_words = [word for word in keywords if re.search(rf'\b{re.escape(word)}\b', text)]
    return ', '.join(matched_words) if matched_words else None

def run_phishing_check(data):
    """Apply the check for phishing words."""
    phishing_keywords = get_phishing_words()

    # Check phishing words in subject and body
    data['phishing_words_in_subject'] = data['subject'].apply(lambda x: check_phishing_words(x, phishing_keywords))
    data['phishing_words_in_body'] = data['body'].apply(lambda x: check_phishing_words(x, phishing_keywords))

    data = data.assign(
        phishing_words_in_subject=data['phishing_words_in_subject'].fillna(""),
        phishing_words_in_body=data['phishing_words_in_body'].fillna("")
    )

    return data
