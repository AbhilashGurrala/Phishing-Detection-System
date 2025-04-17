import pandas as pd
import joblib
import argparse
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.impute import SimpleImputer

def train_naive_bayes(dataset_size="large"):
    """Train a Naive Bayes model on the specified dataset size (small or large)."""

    # Define file paths based on dataset size
    if dataset_size == "small":
        X_train_file = '../data/X_train_small.csv'
        y_train_file = '../data/y_train_small.csv'
        model_path = '../models/naive_bayes_small.pkl'
    else:
        X_train_file = '../data/X_train_large.csv'
        y_train_file = '../data/y_train_large.csv'
        model_path = '../models/naive_bayes_large.pkl'

    # Load training data only
    X_train = pd.read_csv(X_train_file)
    y_train = pd.read_csv(y_train_file).values.ravel()

    # Ensure only numeric features are used
    X_train = X_train.select_dtypes(include=['number'])

    # Handle missing values using mean imputation
    imputer = SimpleImputer(strategy="mean")
    X_train = imputer.fit_transform(X_train)

    # Initialize Naive Bayes model
    model = GaussianNB()

    # Train the model
    print(f"Training Naive Bayes model on {dataset_size} dataset...")
    model.fit(X_train, y_train)

    # Make predictions on training data
    y_train_pred = model.predict(X_train)

    # Evaluate performance on training data
    accuracy = accuracy_score(y_train, y_train_pred)
    print(f"Naive Bayes Model Training Accuracy ({dataset_size} dataset): {accuracy:.4f}")

    print("\nTraining Classification Report:")
    print(classification_report(y_train, y_train_pred))

    # Save the trained model
    joblib.dump(model, model_path)
    print(f"Model saved successfully as {model_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", choices=["small", "large"], default="large", help="Choose dataset size (small or large)")
    args = parser.parse_args()

    train_naive_bayes(args.size)