import pandas as pd
import joblib
import argparse
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from sklearn.impute import SimpleImputer

def train_svm(dataset_size="large"):
    """Train and evaluate an SVM model on the specified dataset size (small or large)."""

    # Define file paths based on dataset size
    if dataset_size == "small":
        X_train_file = '../data/X_train_small.csv'
        X_test_file = '../data/X_test_small.csv'
        y_train_file = '../data/y_train_small.csv'
        y_test_file = '../data/y_test_small.csv'
        model_path = '../models/svm_small.pkl'
    else:
        X_train_file = '../data/X_train_large.csv'
        X_test_file = '../data/X_test_large.csv'
        y_train_file = '../data/y_train_large.csv'
        y_test_file = '../data/y_test_large.csv'
        model_path = '../models/svm_large.pkl'

    # Load training and testing data
    X_train = pd.read_csv(X_train_file)
    X_test = pd.read_csv(X_test_file)
    y_train = pd.read_csv(y_train_file).values.ravel()
    y_test = pd.read_csv(y_test_file).values.ravel()

    # Ensure only numeric features are used
    X_train = X_train.select_dtypes(include=['number'])
    X_test = X_test.select_dtypes(include=['number'])

    # Handle missing values using mean imputation
    imputer = SimpleImputer(strategy="mean")
    X_train = imputer.fit_transform(X_train)
    X_test = imputer.transform(X_test)

    # Initialize SVM model
    model = SVC(kernel='linear', probability=True, random_state=42)

    # Train the model
    print(f"Training SVM model on {dataset_size} dataset...")
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate performance
    accuracy = accuracy_score(y_test, y_pred)
    print(f"SVM Model Accuracy ({dataset_size} dataset): {accuracy:.4f}")

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Save the trained model
    joblib.dump(model, model_path)
    print(f"Model saved successfully as {model_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", choices=["small", "large"], default="large", help="Choose dataset size (small or large)")
    args = parser.parse_args()

    train_svm(args.size)