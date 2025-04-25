import pandas as pd
from sklearn.model_selection import train_test_split
import os

def split_dataset(file_path, small_size=3000, test_size=0.2, random_state=42, output_dir=None):
    """Splits the dataset into small and large training/testing sets."""

    if output_dir is None:
        output_dir = '../data'
    os.makedirs(output_dir, exist_ok=True)

    # Load the dataset
    data = pd.read_csv(file_path)

    # Separate the test email if it exists
    test_email_row = data[data['receiver'] == 'bobtestemail30@gmail.com']
    data = data[data['receiver'] != 'bobtestemail30@gmail.com']

    # Create small dataset (first `small_size` rows)
    small_data = data[:small_size]

    # Create large dataset (full dataset)
    large_data = data

    # small dataset split
    X_train_small, X_test_small, y_train_small, y_test_small = train_test_split(
        small_data.drop(columns=['label']), small_data['label'], test_size=test_size, random_state=random_state)

    # Append test email if it exists
    if not test_email_row.empty:
        X_test_small = pd.concat([X_test_small, test_email_row.drop(columns=['label'])], ignore_index=True)
        y_test_small = pd.concat([y_test_small, test_email_row['label']], ignore_index=True)

    # large dataset split
    X_train_large, X_test_large, y_train_large, y_test_large = train_test_split(
        large_data.drop(columns=['label']), large_data['label'], test_size=test_size, random_state=random_state)

    if not test_email_row.empty:
        X_test_large = pd.concat([X_test_large, test_email_row.drop(columns=['label'])], ignore_index=True)
        y_test_large = pd.concat([y_test_large, test_email_row['label']], ignore_index=True)

    # Save small dataset splits
    X_train_small.to_csv(os.path.join(output_dir, 'X_train_small.csv'), index=False)
    X_test_small.to_csv(os.path.join(output_dir, 'X_test_small.csv'), index=False)
    y_train_small.to_csv(os.path.join(output_dir, 'y_train_small.csv'), index=False)
    y_test_small.to_csv(os.path.join(output_dir, 'y_test_small.csv'), index=False)

    X_train_large.to_csv(os.path.join(output_dir, 'X_train_large.csv'), index=False)
    X_test_large.to_csv(os.path.join(output_dir, 'X_test_large.csv'), index=False)
    y_train_large.to_csv(os.path.join(output_dir, 'y_train_large.csv'), index=False)
    y_test_large.to_csv(os.path.join(output_dir, 'y_test_large.csv'), index=False)

    print("Dataset split completed for both small and large datasets.")

if __name__ == "__main__":
    split_dataset('processed_data.csv')