import pandas as pd
import re
import contractions
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

# NLTK
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# NLP
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    """Clean and preprocess text."""
    if pd.isnull(text):
        return ""

    # Fixing contractions
    text = contractions.fix(text)
    # Removing URLs
    # text = re.sub(r'http[s]?://\S+|www\.\S+|ftp://\S+', '', text)
    # Removing special characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Tokenize the text converted to lower case
    words = word_tokenize(text.lower())
    # Remove stopwords and lemmatize
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]

    return ' '.join(words).strip()

def run_preprocessing(data):
    """Apply preprocessing to the data"""#
    # Standardize column names
    data.columns = [col.strip().lower() for col in data.columns]

    # Clean subject and body
    data['clean_subject'] = data['subject'].apply(preprocess)
    data['clean_body'] = data['body'].apply(preprocess)
