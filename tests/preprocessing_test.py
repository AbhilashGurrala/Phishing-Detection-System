import pandas as pd
from scripts.preprocessing import preprocess

def test_sample_text():
    text = "This is an important update regarding your account."
    result = preprocess(text)
    assert "important" in result and "update" in result
    assert "is" not in result

def test_url_removal():
    text = "Click here: https://phishing.com/login"
    result = preprocess(text)
    assert "http" not in result and "www" not in result and "click" in result

def test_contractions():
    text = "You don't want to miss this offer!"
    result = preprocess(text)
    assert "do not" in result or "dont" not in result

def test_special_characters():
    text = "Get 1000$$$ now!!!"
    result = preprocess(text)
    assert "$" not in result and "!" not in result

def test_empty_string():
    result = preprocess("  ")
    assert result == ""

def test_nan_input():
    result = preprocess(pd.NA)
    assert result == ""

def test_lemmatization():
    text = "There is an offer waiting for those who act quickly."
    result = preprocess(text)

    assert "who" not in result
    assert "is an" not in result



