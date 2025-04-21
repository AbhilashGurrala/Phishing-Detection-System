import pandas as pd
from scripts.thread_analysis import add_thread_features

def test_add_thread_features():
    test_data = pd.DataFrame({
        'subject': [
            'Re: Account update',
            'Fw: Your invoice',
            'Important security alert',
            'RE: Account update'
        ],
        'sender': [
            'user1@example.com',
            'user2@example.com',
            'hacker@evil.com',
            'user3@example.com'
        ],
        'receiver': [
            'support@example.com',
            'billing@example.com',
            'admin@example.com',
            'support@example.com'
        ],
        'date': [
            '2024-04-01 09:00:00',
            '2024-04-01 10:00:00',
            '2024-04-01 11:00:00',
            '2024-04-01 12:00:00'
        ]
    })

    # Add clean_subject
    test_data['clean_subject'] = test_data['subject'].str.lower().str.replace(r"^(re|fw):\s*", "", regex=True)

    updated = add_thread_features(test_data)

    assert 'is_thread_reply' in updated.columns
    assert 'deviates_from_thread' in updated.columns

    print("DataFrame after thread analysis:")
    print(updated.to_string(index=False))

if __name__ == "__main__":
    test_add_thread_features()
