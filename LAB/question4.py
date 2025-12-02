def get_channel_probability(candidate, misspelled):
    """
    Calculates P(s|w): The probability of the misspelling 's' given the word 'w'.
    
    Assumption (from problem statement):
    - If words are identical: Probability is 1.0 (No error)
    - If words have a single edit distance (likely error): Probability is 0.001
    - If words are very different: Probability is effectively 0.0
    """
    if candidate == misspelled:
        return 1.0
    
    # Check for single character error (Substitution or Transposition) manually
    # 1. Length check: Only consider candidates with same length for substitution/transposition
    if len(candidate) != len(misspelled):
        return 0.000001 # Very low probability for length mismatches in this simple model

    diff_count = 0
    for c1, c2 in zip(candidate, misspelled):
        if c1 != c2:
            diff_count += 1
            
    # CASE A: Substitution (e.g., "word" vs "ward") -> 1 char different
    if diff_count == 1:
        return 0.001 # Fixed small probability for single substitution
        
    # CASE B: Transposition (e.g., "word" vs "wrod") -> 2 chars different, but same set of chars
    if diff_count == 2 and sorted(candidate) == sorted(misspelled):
         return 0.001 # Fixed small probability for transposition
         
    return 0.000001 # Default low prob for other cases

def spelling_corrector():
    # 1. Corpus and Dictionary (V) with Prior Probabilities P(w)
    # We assume 'word' is more common than 'weird' or 'ward'
    dictionary_V = {
        "word":  0.4,
        "work":  0.3,
        "world": 0.2,
        "ward":  0.05,
        "weird": 0.05
    }
    
    # 2. Error Simulation
    target_word = "word"
    misspelled_word = "wrod"  # Simulated Transposition Error
    
    print(f"Target Word: '{target_word}'")
    print(f"Observed Error (s): '{misspelled_word}'")
    print(f"Dictionary V: {dictionary_V}\n")

    # 3. Candidate Generation & Probability Calculation
    # We will score ALL words in our small dictionary to find the best candidate.
    
    best_candidate = None
    highest_score = -1
    
    print(f"{'Candidate (w)':<15} {'Prior P(w)':<12} {'Channel P(s|w)':<15} {'Score'}")
    print("-" * 60)
    
    for word, prior_prob in dictionary_V.items():
        # Calculate Likelihood P(s|w)
        likelihood = get_channel_probability(word, misspelled_word)
        
        # Calculate Final Score: P(w) * P(s|w)
        # Bayes Theorem numerator
        score = prior_prob * likelihood
        
        print(f"{word:<15} {prior_prob:<12} {likelihood:<15} {score:.7f}")
        
        if score > highest_score:
            highest_score = score
            best_candidate = word

    # 4. Finding the Best Correction
    print("-" * 60)
    print(f"Best Correction: '{best_candidate}' with score {highest_score:.7f}")

if __name__ == "__main__":
    spelling_corrector()