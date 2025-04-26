import requests
import sqlite3
import pandas as pd
import re
import os

DB_PATH = '../data/compromised_domains.db'

def connect_db():
    """Connect to the SQLite database"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def create_table():
    """Create a table for compromised domains if it does not exist"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS domains (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT UNIQUE,
            added_on TEXT DEFAULT CURRENT_DATE
        )
    ''')
    conn.commit()
    conn.close()

def fetch_phishtank_domains():
    """Fetch domains from PhishTank"""
    """
FUNCTION extract_domain(url):
    SEARCH for domain pattern in the URL using regex
    IF match found:
        RETURN lowercase domain
    ELSE:
        RETURN None
"""
    url = "https://data.phishtank.com/data/online-valid.csv"
    try:
        df = pd.read_csv(url)
        domains = set(df['url'].apply(lambda x: extract_domain(x)))
        return domains
    except Exception as e:
        print(f"Error fetching data from PhishTnak: {e}")
        return set()

def fetch_openphish_domains():
    """Fetch domains from OpenPhish"""
    url = "https://openphish.com/feed.txt"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            domains = set(extract_domain(line) for line in response.text.split("\n") if line)
            return domains
        else:
            print("OpenPhish data fetch error")
            return set()
    except Exception as e:
        print(f"Error fetching OpenPhish data: {e}")
        return set()

def fetch_abusech_domains():
    """Fetch domains from Abuse.ch"""
    url = "https://urlhaus.abuse.ch/downloads/text_online/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            domains = set(extract_domain(line) for line in response.text.split("\n") if line and not line.startswith("#"))
            return domains
        else:
            print("Abuse.ch data fetch error")
            return set()
    except Exception as e:
        print(f"Error fetching Abuse.ch data: {e}")
        return set()

def extract_domain(url):
    """Extract the domain from a URL"""
    match = re.search(r"https?://([a-zA-Z0-9.-]+)", url)
    return match.group(1).lower() if match else None

def update_database(domains):
    """Inserting the new domains into the SQLite database"""
    conn = connect_db()
    cursor = conn.cursor()
    for domain in domains:
        cursor.execute("INSERT OR IGNORE INTO domains (domain) VALUES (?)", (domain,))
    conn.commit()
    conn.close()
    print(f"Updated {len(domains)} domains in the database.")

def run_scraper():
    """Run all scrapers and update the database"""
    print(" Fetching phishing domains...")
    all_domains = fetch_phishtank_domains() | fetch_openphish_domains() | fetch_abusech_domains()
    if all_domains:
        update_database(all_domains)
    else:
        print("No new domains found.")

if __name__ == '__main__':
    create_table()
    run_scraper()
    print("Phishing domain scraper is running")

