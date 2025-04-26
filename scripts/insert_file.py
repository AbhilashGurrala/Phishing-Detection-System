import pandas as pd

def insert_sample_phishing_row(csv_path):
    # Define the phishing row
    phishing_row = {
        'sender': 'Scam Department <alert@paypal-verification.com>',
        'receiver': 'bobtestemail30@gmail.com',
        'date': 'Fri, 19 Apr 2024 14:12:00 -0700',
        'subject': 'Your PayPal account is on hold',
        'body': """Dear customer,

We noticed suspicious activity on your PayPal account. To avoid suspension, please verify your account immediately.

Click the link below to restore full access:
http://paypal-security-verification.com/login

Failure to comply will result in permanent account termination.

Thank you,
PayPal Security Team""",
        'label': 1,
        'urls': 1
    }

    # Load original dataset
    df = pd.read_csv(csv_path)

    # Append the new row
    df = pd.concat([df, pd.DataFrame([phishing_row])], ignore_index=True)

    # Save it back to the same file
    df.to_csv(csv_path, index=False)
    print("Row inserted successfully.")

# Example usage:
insert_sample_phishing_row('../data/CEAS_08.csv')