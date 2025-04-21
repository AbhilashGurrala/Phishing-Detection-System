import pandas as pd
import re

def is_reply(subject):
    """Check if the email is a reply based on subject"""
    return int(subject.strip().lower().startswith("re:"))

def find_previous_message(row, df):
    """find the previous email in the same thread based on subject and receiver"""
    clean_subject = row['clean_subject']
    sender = row['sender']
    date = pd.to_datetime(row['date'])

    # Look for previous emails in the same subject thread from same receiver
    candidates = df[(df['clean_subject'] == clean_subject) & (df['receiver'] == sender)]
    candidates['date'] = pd.to_datetime(candidates['date'])
    previous = candidates[candidates['date'] < date]
    if not previous.empty:
        return previous.sort_values(by='date', ascending=False).iloc[0]
    return None

def compare_with_previous(row, df):
    """Compare email body to previous message in thread and then return deviation score"""
    previous = find_previous_message(row, df)
    if previous is None:
        return 0

    body = str(row['clean_body'])
    prev_body = str(previous['clean_body'])

    if not prev_body:
        return 0

    overlap = len(set(body.split()) & set(prev_body.split()))
    total = len(set(prev_body.split()))
    similarity = overlap / total if total > 0 else 0

    # If very low then consider it as deviation
    return int(similarity < 0.3)

def add_thread_features(df):
    """Add contextual features based on thread analysis"""
    df['is_thread_reply'] = df['subject'].apply(is_reply)
    df['deviates_from_thread'] = df.apply(lambda row: compare_with_previous(row, df), axis=1)
    return df
