import pandas as pd

def is_reply(subject):
    """Check if the email is a reply based on subject"""
    if pd.isnull(subject):
        return 0
    return int(str(subject).strip().lower().startswith("re:"))

def find_previous_message(row, df):
    """Try to find the previous email in the same thread based on subject and receiver"""
    clean_subject = row.get('clean_subject')
    sender = row.get('sender')

    try:
        date = pd.to_datetime(row['date'], utc=True).tz_convert(None)
    except Exception:
        return None

    # Look for previous emails in the same subject thread from same receiver
    candidates = df[(df['clean_subject'] == clean_subject) & (df['receiver'] == sender)].copy()

    try:
        candidates['date'] = pd.to_datetime(candidates['date'], utc=True).dt.tz_localize(None)
    except Exception:
        return None

    previous = candidates[candidates['date'] < date]
    if not previous.empty:
        return previous.sort_values(by='date', ascending=False).iloc[0]
    return None

def compare_with_previous(row, df):
    """Compare email body to previous message in thread and return the score of deviation"""
    previous = find_previous_message(row, df)
    if previous is None:
        return 0

    body = str(row.get('clean_body', ''))
    prev_body = str(previous.get('clean_body', ''))

    if not prev_body:
        return 0

    overlap = len(set(body.split()) & set(prev_body.split()))
    total = len(set(prev_body.split()))
    similarity = overlap / total if total > 0 else 0

    return int(similarity < 0.3)

def add_thread_features(df):
    """Add contextual features based on thread analysis"""
    df['is_thread_reply'] = df['subject'].apply(is_reply)
    df['deviates_from_thread'] = df.apply(lambda row: compare_with_previous(row, df), axis=1)
    return df