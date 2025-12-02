import math
from collections import defaultdict

class NaiveBayesClassifier:
    def __init__(self):
        self.vocab = set()
        self.word_counts = {'Positive': defaultdict(int), 'Negative': defaultdict(int)}
        self.class_counts = {'Positive': 0, 'Negative': 0}
        self.priors = {}
        self.total_words_in_class = {'Positive': 0, 'Negative': 0}

    def preprocess(self, text):
        # Simple tokenization: Lowercase and split by space
        return text.lower().split()

    def train(self, data):
        total_docs = len(data)
        
        # 1. Calculate Counts
        for text, label in data:
            self.class_counts[label] += 1
            words = self.preprocess(text)
            
            for word in words:
                self.vocab.add(word)
                self.word_counts[label][word] += 1
                self.total_words_in_class[label] += 1
        
        # 2. Calculate Priors: P(Class)
        # Formula: P(c) = N_c / N_total
        for label in self.class_counts:
            self.priors[label] = self.class_counts[label] / total_docs

    def get_word_probability(self, word, label):
        # 3. Calculate Likelihood: P(word | Class)
        # Using Laplace Smoothing (Add-1) to handle unknown words
        # Formula: (Count(w, c) + 1) / (Count(all_words_in_c) + |Vocabulary|)
        
        count_w_c = self.word_counts[label][word]
        count_c = self.total_words_in_class[label]
        vocab_size = len(self.vocab)
        
        return (count_w_c + 1) / (count_c + vocab_size)

    def predict(self, text):
        words = self.preprocess(text)
        scores = {}

        # 4. Apply Bayes Theorem: P(c|d) ∝ P(c) * Π P(w_i|c)
        # We compute score for both Positive and Negative
        for label in self.class_counts:
            # Start with Prior P(c)
            # We use Log Probability to prevent underflow (multiplying tiny numbers)
            score = math.log(self.priors[label])
            
            for word in words:
                # Add Log Likelihoods (equivalent to multiplying probabilities)
                prob = self.get_word_probability(word, label)
                score += math.log(prob)
            
            scores[label] = score
        
        # Return class with highest score (Argmax)
        return max(scores, key=scores.get)

if __name__ == "__main__":
    # 1. Training Data (Text, Label)
    train_data = [
        ("I love this movie", "Positive"),
        ("This is fantastic", "Positive"),
        ("What a wonderful place", "Positive"),
        ("I feel great", "Positive"),
        ("I hate this movie", "Negative"),
        ("This is terrible", "Negative"),
        ("I am angry and sad", "Negative"),
        ("What a bad experience", "Negative")
    ]

    # 2. Train Model
    nb = NaiveBayesClassifier()
    nb.train(train_data)
    
    print(f"Vocab Size: {len(nb.vocab)}")
    print(f"Priors: {nb.priors}\n")

    # 3. Test Data
    test_sentences = [
        "I love this place",       # Contains positive words
        "This is a bad movie",     # Contains negative words
        "I feel wonderful",        # Mixed/Positive
    ]

    print("--- Predictions ---")
    for sent in test_sentences:
        prediction = nb.predict(sent)
        print(f"Sentence: '{sent}'")
        print(f"Predicted Sentiment: {prediction}")
        print("-" * 30)