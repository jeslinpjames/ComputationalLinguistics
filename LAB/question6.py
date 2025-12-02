import stanza
import sys


stanza.download('fr')

def pos_tagging_french():
    try:
        # 1. Load Pretrained Model (French)
        # Processors: 'tokenize' (split words), 'pos' (part of speech), 'mwt' (multi-word token expansion for French)
        print("Loading French Pipeline (Stanza)...")
        nlp = stanza.Pipeline(lang='fr', processors='tokenize,mwt,pos', verbose=False)
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Please run 'stanza.download(\"fr\")' to download the model first.")
        return

    # 2. Load Sentences (Target Language)
    # Sentence 1: "The cat eats the mouse."
    # Sentence 2: "The students study artificial intelligence."
    french_text = "Le chat mange la souris. Les étudiants étudient l'intelligence artificielle."
    
    print(f"\nTarget Text (French): \"{french_text}\"")
    print("-" * 60)

    # 3. Perform Tagging
    doc = nlp(french_text)

    # 4. Display Tags
    # UPOS: Universal Part of Speech (Standard across languages)
    # XPOS: Language-specific Part of Speech (Specific to French grammar)
    print(f"{'Word':<15} {'UPOS (Universal)':<20} {'XPOS (Specific)'}")
    print("-" * 60)

    unique_tags = set()

    for sentence in doc.sentences:
        for word in sentence.words:
            print(f"{word.text:<15} {word.upos:<20} {word.xpos}")
            unique_tags.add(word.upos)

    # 5. Analysis & Discussion (Required by Lab Question)
    print("-" * 60)
    print("--- Analysis & Discussion ---")
    
    # c. Identify common tags and compare with English
    print("1. Common Tags Found:")
    print(f"   {sorted(list(unique_tags))}")
    print("   Comparison with English:")
    print("   - DET (Determiner): French has gendered determiners ('le' vs 'la') unlike English ('the').")
    print("   - NOUN/VERB: Standard categories exist in both languages.")
    print("   - ADJ: French adjectives often follow the noun (e.g., 'intelligence artificielle'),")
    print("     whereas English adjectives usually precede the noun.")

    # d. Challenges in Morphologically Rich Languages
    print("\n2. Challenges in Morphologically Rich Languages (like French):")
    print("   - Ambiguity: A single word form can have multiple grammatical functions depending on gender/number.")
    print("   - Compound Words: French uses contractions (e.g., 'au' = 'à' + 'le').")
    print("     The tagger must perform 'Multi-Word Token expansion' (MWT) to tag them correctly.")
    print("   - Agreement: Adjectives and articles must agree in gender and number with the noun,")
    print("     increasing the complexity of the state space for the model.")

if __name__ == "__main__":
    pos_tagging_french()