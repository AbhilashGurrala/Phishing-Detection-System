import sqlite3
import pandas as pd
import re

def connect_db():
    return sqlite3.connect('compromised_domains.db')

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
    """Check if a domain is compromised."""
    if not domain:
        # if there is no domain then return false
        return False
    domain = domain.lower()
    return any(domain == comp or domain.endswith(f".{comp}") for comp in compromised_domains)

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
    """Apply domain checking on preprocessed data."""
    compromised_domains = get_compromised_domains()

    # Check domain in sender's email address
    data['sender_domain'] = data['sender'].apply(extract_sender_domain)
    data['compromised_sender'] = data['sender_domain'].apply(lambda domain: check_domain(domain, compromised_domains))

    # Check domains in body
    data['extracted_domains'] = data['body'].apply(extract_body_domain)
    data['compromised_url'] = data['extracted_domains'].apply(lambda x: any(check_domain(domain.strip(), compromised_domains) for domain in x.split(',')) if pd.notna(x) else False)
