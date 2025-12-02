import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

def preprocess_text(text):
    print("--- Original Text ---")
    print(text)
    print("\n")

    # 1. Tokenization
    tokens = word_tokenize(text)
    print(f"1. Tokenization:\n{tokens}\n")

    # 2. Remove Punctuation
    tokens_no_punct = [word for word in tokens if word.isalnum()]
    print(f"2. Remove Punctuation:\n{tokens_no_punct}\n")

    # 3. Lowercase
    tokens_lower = [word.lower() for word in tokens_no_punct]
    print(f"3. Lowercase:\n{tokens_lower}\n")

    # 4. Stemming (Porter Stemmer)
    stemmer = PorterStemmer()
    stems = [stemmer.stem(word) for word in tokens_lower]
    print(f"4. Stemming:\n{stems}\n")

    # 5. Lemmatization (WordNet)
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(word) for word in tokens_lower]
    print(f"5. Lemmatization:\n{lemmas}\n")

if __name__ == "__main__":
    paragraph = "The quick brown foxes are jumping over the lazy dog's back! They aren't waiting for the rabbit, are they? 1234."
    preprocess_text(paragraph)