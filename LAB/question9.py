class PluralFSA:
    def __init__(self):
        self.vowels = set('aeiou')
        self.reset()

    def reset(self):
        self.state = 'q_start'
        self.last_char_type = None # 'vowel' or 'consonant'

    def process_word(self, word):
        self.reset()
        print(f"Processing '{word}':", end=" ")
        
        for char in word:
            self.transition(char)
            
        if self.state == 'q_accept':
            print("ACCEPTED")
        else:
            print("REJECTED")

    def transition(self, char):
        # Helper to identify character type
        is_vowel = char in self.vowels
        is_consonant = char.isalpha() and not is_vowel

        # --- STATE TRANSITIONS ---
        
        if self.state == 'q_start':
            if is_vowel: self.state = 'q_vowel'
            elif is_consonant: self.state = 'q_consonant'
            
        elif self.state == 'q_vowel':
            # Logic: We are inside the word, last char was a vowel.
            # If we see 'y', check next for 's'.
            if char == 'y': self.state = 'q_vowel_y'
            # If we see 'i', it might be valid logic for other words, but for 'y' plurals, 
            # vowel + ies (boies) is invalid. We treat it as standard char processing.
            elif is_vowel: self.state = 'q_vowel'
            elif is_consonant: self.state = 'q_consonant'

        elif self.state == 'q_consonant':
            # Logic: We are inside word, last char was consonant.
            # Consonant + y is usually invalid for plural (ponys).
            # Consonant + i is start of 'ies'.
            if char == 'y': self.state = 'q_consonant_y' 
            elif char == 'i': self.state = 'q_consonant_i'
            elif is_vowel: self.state = 'q_vowel'
            elif is_consonant: self.state = 'q_consonant'

        # --- SUFFIX CHECKING STATES ---

        elif self.state == 'q_vowel_y':
            # We saw Vowel + y (e.g., 'boy'). Expect 's'.
            if char == 's': self.state = 'q_accept'
            else: self.reset_state_based_on_char(char) # Word continued (e.g., 'boyish')

        elif self.state == 'q_consonant_y':
            # We saw Consonant + y (e.g., 'pony'). 
            # If we see 's' now ('ponys'), it is INVALID.
            if char == 's': self.state = 'q_reject' 
            else: self.reset_state_based_on_char(char)

        elif self.state == 'q_consonant_i':
            # We saw Consonant + i. Expect 'e'.
            if char == 'e': self.state = 'q_consonant_ie'
            else: self.reset_state_based_on_char(char)

        elif self.state == 'q_consonant_ie':
            # We saw Consonant + ie. Expect 's'.
            if char == 's': self.state = 'q_accept'
            else: self.reset_state_based_on_char(char)
            
        elif self.state == 'q_accept':
            # If we are already accepted but characters keep coming, 
            # the word isn't finished (e.g. 'boys' -> 'boyss'). Reset.
            self.reset_state_based_on_char(char)

        elif self.state == 'q_reject':
            # Once rejected, stay rejected for this word
            pass

    def reset_state_based_on_char(self, char):
        """Helper to jump back to general processing if a suffix pattern breaks."""
        if char in self.vowels: self.state = 'q_vowel'
        elif char.isalpha(): self.state = 'q_consonant'
        else: self.state = 'q_reject'

if __name__ == "__main__":
    fsa = PluralFSA()
    
    # Test Cases
    test_words = [
        "boys",     # Valid (Vowel + ys)
        "toys",     # Valid
        "ponies",   # Valid (Consonant + ies)
        "skies",    # Valid
        "puppies",  # Valid
        "boies",    # Invalid (Vowel + ies)
        "ponys",    # Invalid (Consonant + ys)
        "toies",    # Invalid
        "cats"      # Invalid (Ends in s, but not y-plural rule specific logic covers this)
    ]
    
    print("--- Finite State Automaton Output ---")
    for w in test_words:
        fsa.process_word(w)