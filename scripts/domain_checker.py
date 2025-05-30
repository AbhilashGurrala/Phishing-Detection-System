import sqlite3
import pandas as pd
import re
import os

DB_PATH = '../data/compromised_domains.db'

def connect_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def get_compromised_domains():
    """Get the compromised domains from the database."""
    # Connection to the db
    conn = connect_db()
    cursor = conn.cursor()
    # fetch all domains
    cursor.execute("SELECT domain FROM domains")
    # convert domains to lower case
    domains = {row[0].lower() for row in cursor.fetchall()}
    # Close connection to the db
    conn.close()
    return domains

def check_domain(domain, compromised_domains):
    """Check for exact match or subdomain"""
    if not domain:
        return False
    domain = domain.lower()
    # Split domain and check each suffix level
    parts = domain.split('.')
    for i in range(len(parts)):
        suffix = '.'.join(parts[i:])
        if suffix in compromised_domains:
            return True
    return False

def extract_sender_domain(email):
    """Extract domain from sender's email."""
    # Extract domain after the @ symbol
    match = re.search(r'@([\w.-]+)', str(email))
    return match.group(1).lower() if match else None

def extract_body_domain(text):
    """Extract domains from body if it exists."""
    if pd.isnull(text):
        return None

    text = text.lower()
    matched_domains = set(re.findall(r'\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', text))

    return ', '.join(matched_domains) if matched_domains else None

def run_domain_check(data):
    """Checking domains in preprocessed data."""
    compromised_domains = get_compromised_domains()

    # Check domain in sender's email address
    data['sender_domain'] = data['sender'].apply(extract_sender_domain)
    data['compromised_sender'] = data['sender_domain'].apply(lambda domain: check_domain(domain, compromised_domains))

    # Check domains in body
    data['extracted_domains'] = data['body'].apply(extract_body_domain)
    data['compromised_url'] = data['extracted_domains'].apply(lambda x: any(check_domain(domain.strip(), compromised_domains) for domain in x.split(',')) if pd.notna(x) else False)
