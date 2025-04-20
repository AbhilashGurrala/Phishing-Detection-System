import pandas as pd
from scripts.feature_extraction import run_feature_extraction

def test_run_feature_extraction():
    # Create sample test DataFrame
    data = pd.DataFrame({
        'clean_subject': [
            "urgent account verification required",
            "update your account information",
            "win a free prize now"
        ],
        'clean_body': [
            "click on the link to verify your account",
            "please update your payment method as soon as possible",
            "you won a prize. Click here to claim"
        ]
    })

    # Run feature extraction
    features = run_feature_extraction(data)

    assert isinstance(features, pd.DataFrame)
    assert features.shape[0] == len(data)
    assert features.isnull().sum().sum() == 0
    assert any(col.startswith("sub_tfidf_") for col in features.columns)
    assert any(col.startswith("body_tfidf_") for col in features.columns)

    print("Feature extraction test ran successfully")