import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
import numpy as np

def train_anomaly_detector(X_train, model_path='../models/isolation_forest.pkl'):
    """Train Isolation Forest for anomaly detection."""
    # Impute missing values
    imputer = SimpleImputer(strategy="mean")
    X_train_imputed = imputer.fit_transform(X_train)

    # Train Isolation Forest
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(X_train_imputed)

    # Save model
    joblib.dump(model, model_path)
    print(f"Isolation Forest model saved as {model_path}")

if __name__ == "__main__":
    # Load the training dataset (large dataset recommended)
    X_train = pd.read_csv('../data/X_train_small.csv')

    # Select numeric columns only
    X_train = X_train.select_dtypes(include=['number'])

    # Convert to NumPy array
    X_train_np = np.array(X_train)

    # Train and save the model
    train_anomaly_detector(X_train_np)