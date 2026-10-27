import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK data dependencies silently if needed
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

def preprocess_text(text):
    """
    Cleans and normalizes text using NLTK:
    - Lowercasing
    - Non-alphanumeric removal
    - Tokenization
    - Stopword removal
    Returns clean normalized space-separated text string.
    """
    if not text:
        return ""
    
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s,]', ' ', text)
    
    try:
        tokens = word_tokenize(text)
    except Exception:
        tokens = text.split()

    try:
        stop_words = set(stopwords.words('english'))
    except Exception:
        stop_words = {'and', 'the', 'is', 'in', 'to', 'for', 'of', 'with', 'a', 'an', 'on', 'at', 'by', 'this', 'that'}
        
    filtered_tokens = [w for w in tokens if w not in stop_words and len(w) > 1]
    
    return " ".join(filtered_tokens)

def extract_keywords(text):
    """
    Extracts normalized set of unique keyword tokens.
    """
    cleaned = preprocess_text(text)
    return set(cleaned.split())
