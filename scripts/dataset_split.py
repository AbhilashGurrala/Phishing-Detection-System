import pandas as pd
from sklearn.model_selection import train_test_split

def split_dataset(file_path, small_size=1000, test_size=0.2, random_state=42):
    """Splits the dataset into small and large training/testing sets."""

    # Load the dataset
    data = pd.read_csv(file_path)

    # Create small dataset (first `small_size` rows)
    small_data = data[:small_size]

    # Create large dataset (full dataset)
    large_data = data

    # small dataset split
    X_train_small, X_test_small, y_train_small, y_test_small = train_test_split(
        small_data.drop(columns=['label']), small_data['label'], test_size=test_size, random_state=random_state)

    # large dataset split
    X_train_large, X_test_large, y_train_large, y_test_large = train_test_split(
        large_data.drop(columns=['label']), large_data['label'], test_size=test_size, random_state=random_state)

    # Save small dataset splits
    X_train_small.to_csv('../data/X_train_small.csv', index=False)
    X_test_small.to_csv('../data/X_test_small.csv', index=False)
    y_train_small.to_csv('../data/y_train_small.csv', index=False)
    y_test_small.to_csv('../data/y_test_small.csv', index=False)

    # Save large dataset splits
    X_train_large.to_csv('../data/X_train_large.csv', index=False)
    X_test_large.to_csv('../data/X_test_large.csv', index=False)
    y_train_large.to_csv('../data/y_train_large.csv', index=False)
    y_test_large.to_csv('../data/y_test_large.csv', index=False)

    print("Dataset split completed for both small and large datasets.")

if __name__ == "__main__":
    split_dataset('processed_data.csv')