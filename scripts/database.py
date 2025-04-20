import sqlite3

# Function to connect to the SQLite database
def connect_db():
    return sqlite3.connect('../data/compromised_domains.db')

# Create tables for compromised domains and phishing keywords
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Table for compromised domains
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS domains (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT UNIQUE,
            added_on TEXT
        )
    ''')

    # Table for phishing words/phrases
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS phishing_keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT UNIQUE,
            added_on TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Insert compromised domains from file
def insert_domains():
    conn = connect_db()
    cursor = conn.cursor()

    with open('../data/compromised_domains_live.txt', 'r', encoding='utf-8') as file:
        for line in file:
            domain = line.strip().lower()
            if domain:
                cursor.execute("INSERT OR IGNORE INTO domains (domain, added_on) VALUES (?, CURRENT_DATE)", (domain,))

    conn.commit()
    conn.close()

# Insert phishing keywords from file
def insert_phishing_keywords():
    conn = connect_db()
    cursor = conn.cursor()

    with open('../data/phishing_words.txt', 'r', encoding='utf-8') as file:
        for line in file:
            keyword = line.strip().lower()
            if keyword:
                cursor.execute("INSERT OR IGNORE INTO phishing_keywords (keyword, added_on) VALUES (?, CURRENT_DATE)", (keyword,))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
    insert_domains()
    insert_phishing_keywords()
    print("Database updated with compromised domains and phishing keywords.")
