import re

class ManualTokenizer:
    def __init__(self):
        # 1. Define Regex Patterns (Compiled for efficiency)
        self.rules = [
            # Abbreviations: Matches sequences like U.S.A. or e.g.
            ('ABBREVIATION', re.compile(r'(?:[a-zA-Z]\.)+')),
            
            # Internal Hyphenation: Matches words like ice-cream, state-of-the-art
            ('HYPHENATED', re.compile(r'\w+(?:-\w+)+')),
            
            # Contractions: Matches words ending in n't, 's, 're, 'll, etc.
            ('CONTRACTION', re.compile(r"\w+(?:n't|'s|'re|'ll|'ve|'m|'d)")),
            
            # Standard Words: Alphanumeric sequences
            ('WORD', re.compile(r'\w+')),
            
            # Symbols/Punctuation: Any single non-word, non-whitespace character
            ('SYMBOL', re.compile(r'[^\w\s]'))
        ]
        
        # Map for expanding common contractions
        self.contraction_map = {
            "isn't": ["is", "not"],
            "aren't": ["are", "not"],
            "can't": ["can", "not"],
            "won't": ["will", "not"],
            "it's": ["it", "is"],
            "i'm": ["i", "am"],
            "he's": ["he", "is"],
            "they're": ["they", "are"]
        }

    def tokenize(self, text):
        tokens = []
        position = 0
        length = len(text)
        
        # Manual scanning loop
        while position < length:
            # 1. Skip over whitespace manually
            if text[position].isspace():
                position += 1
                continue
            
            match_found = False
            
            # 2. Try to match each rule at the current position
            for token_type, pattern in self.rules:
                match = pattern.match(text, position)
                
                if match:
                    value = match.group()
                    
                    if token_type == 'CONTRACTION':
                        # Check if we have a known expansion
                        lower_val = value.lower()
                        if lower_val in self.contraction_map:
                            tokens.extend(self.contraction_map[lower_val])
                        else:
                            # Fallback: split roughly (e.g., "John's" -> "John", "'s")
                            # This mimics simple rule-based splitting
                            if "'s" in value:
                                base, suffix = value.rsplit("'s", 1)
                                tokens.extend([base, "'s"])
                            elif "n't" in value:
                                base, suffix = value.rsplit("n't", 1)
                                tokens.extend([base, "not"])
                            else:
                                tokens.append(value)
                                
                    else:
                        # For Abbreviations, Hyphenated, Words, and Symbols
                        tokens.append(value)
                    
                    # Move the cursor forward by the length of the match
                    position = match.end()
                    match_found = True
                    break
            
            # 3. Safety catch: If no rule matched, skip character (or handle error)
            if not match_found:
                position += 1
                
        return tokens

if __name__ == "__main__":
    # Test Data
    input_text = "It's a sunny day in the U.S.A. I love ice-cream! He isn't going."
    
    # Initialize our manual tokenizer
    tokenizer = ManualTokenizer()
    
    print("--- Input Text ---")
    print(input_text)
    
    print("\n--- Tokenization Result ---")
    tokens = tokenizer.tokenize(input_text)
    print(tokens)
    
    # Validation of requirements:
    print("\n--- Checks ---")
    print(f"1. Contraction 'It's' split? {'Yes' if 'it' in tokens and 'is' in tokens else 'No'}")
    print(f"2. Abbreviation 'U.S.A.' kept? {'Yes' if 'U.S.A.' in tokens else 'No'}")
    print(f"3. Hyphenation 'ice-cream' kept? {'Yes' if 'ice-cream' in tokens else 'No'}")
    print(f"4. Symbols '!' and '.' separate? {'Yes' if '!' in tokens and '.' in tokens else 'No'}")