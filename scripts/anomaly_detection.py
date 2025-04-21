import pandas as pd
import joblib
import argparse
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer

def train_anomaly_detector(dataset_size="large"):
    if dataset_size == "small":
        X_train_file = '../data/X_train_small.csv'
        model_path = '../models/isolation_forest_small.pkl'
    else:
        X_train_file = '../data/X_train_large.csv'
        model_path = '../models/isolation_forest_large.pkl'

    X_train = pd.read_csv(X_train_file)
    X_train = X_train.select_dtypes(include=['number'])

    imputer = SimpleImputer(strategy="mean")
    X_train_imputed = imputer.fit_transform(X_train)

    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(X_train_imputed)

    joblib.dump(model, model_path)
    print(f"Isolation Forest model saved as {model_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", choices=["small", "large"], default="large", help="Choose dataset size (small or large)")
    args = parser.parse_args()

    train_anomaly_detector(args.size)