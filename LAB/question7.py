import pandas as pd
from collections import defaultdict

def compute_translation_probabilities():
    # 1. Manually Construct Corpus (English, Malayalam)
    # Using transliterated Malayalam to ensure code runs on all terminals without font issues.
    corpus = [
        ("the book", "pusthakam"),
        ("a book", "oru pusthakam"),
        ("read book", "pusthakam vayikuka"),
        ("read the book", "pusthakam vayikuka"),
        ("read a book", "oru pusthakam vayikuka")
    ]

    print("--- Parallel Corpus (English -> Malayalam) ---")
    for eng, mal in corpus:
        print(f"English: '{eng}'  |  Malayalam: '{mal}'")
    print("-" * 60)

    # 2. Tokenization & Vocabulary Building
    english_vocab = set()
    malayalam_vocab = set()
    
    # Store tokenized sentences
    tokenized_corpus = []

    for eng, mal in corpus:
        e_tokens = eng.lower().split()
        m_tokens = mal.lower().split()
        
        tokenized_corpus.append((e_tokens, m_tokens))
        
        english_vocab.update(e_tokens)
        malayalam_vocab.update(m_tokens)

    english_vocab = sorted(list(english_vocab))
    malayalam_vocab = sorted(list(malayalam_vocab))

    # 3. Calculate Co-occurrence Counts
    # How many times does English word 'e' appear in a sentence with Malayalam word 'f'?
    co_occurrence_counts = defaultdict(lambda: defaultdict(int))
    
    # Simple word counts (for normalization)
    count_e = defaultdict(int)
    count_f = defaultdict(int)

    for e_tokens, m_tokens in tokenized_corpus:
        # Update word counts
        for e in set(e_tokens): count_e[e] += 1
        for f in set(m_tokens): count_f[f] += 1
        
        # Update co-occurrence
        for e in e_tokens:
            for f in m_tokens:
                co_occurrence_counts[e][f] += 1

    # 4. Compute Probabilities
    # We use a DataFrame for nice visualization of the matrix
    df_p_f_given_e = pd.DataFrame(0.0, index=english_vocab, columns=malayalam_vocab)
    df_p_e_given_f = pd.DataFrame(0.0, index=malayalam_vocab, columns=english_vocab)

    # Compute P(f|e) = Count(e, f) / Count(e)
    # "Probability that 'f' translates to 'e' given 'e'"
    for e in english_vocab:
        for f in malayalam_vocab:
            if co_occurrence_counts[e][f] > 0:
                prob = co_occurrence_counts[e][f] / count_e[e]
                df_p_f_given_e.loc[e, f] = round(prob, 4)

    # Compute P(e|f) = Count(e, f) / Count(f)
    # "Probability that 'e' translates to 'f' given 'f'"
    for f in malayalam_vocab:
        for e in english_vocab:
            if co_occurrence_counts[e][f] > 0:
                prob = co_occurrence_counts[e][f] / count_f[f]
                df_p_e_given_f.loc[f, e] = round(prob, 4)

    # 5. Output Results
    print("\n--- Translation Probabilities P(f|e) ---")
    print("(Probability of Malayalam word given English word)")
    print(df_p_f_given_e)
    
    print("\n\n--- Translation Probabilities P(e|f) ---")
    print("(Probability of English word given Malayalam word)")
    print(df_p_e_given_f)

    # Verification Example
    print("\n--- Verification ---")
    print(f"P('pusthakam' | 'book') = {df_p_f_given_e.loc['book', 'pusthakam']}")
    print("Reason: 'book' appears 5 times, 'pusthakam' appears 5 times with it. 5/5 = 1.0")

if __name__ == "__main__":
    compute_translation_probabilities()