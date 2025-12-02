import stanza
import sys

# stanza.download('hi')

def pos_tagging_hindi():
    try:
        # 1. Load Pretrained Model (Hindi)
        # Processors: 'tokenize' (split words), 'pos' (part of speech)
        print("Loading Hindi Pipeline (Stanza)...")
        nlp = stanza.Pipeline(lang='hi', processors='tokenize,pos', verbose=False)
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Please run 'stanza.download(\"hi\")' to download the model first.")
        return

    # 2. Load Sentences (Target Language)
    # Sentence 1: "The cat eats the mouse." -> "बिल्ली चूहा खाती है।"
    # Sentence 2: "Students study artificial intelligence." -> "छात्र कृत्रिम बुद्धिमत्ता का अध्ययन करते हैं।"
    hindi_text = "बिल्ली चूहा खाती है। छात्र कृत्रिम बुद्धिमत्ता का अध्ययन करते हैं।"
    
    print(f"\nTarget Text (Hindi): \"{hindi_text}\"")
    print("-" * 65)

    # 3. Perform Tagging
    doc = nlp(hindi_text)

    # 4. Display Tags
    # UPOS: Universal Part of Speech (Standard across languages)
    # XPOS: Language-specific Part of Speech (Specific to Hindi grammar)
    print(f"{'Word':<20} {'UPOS (Universal)':<20} {'XPOS (Specific)'}")
    print("-" * 65)

    unique_tags = set()

    for sentence in doc.sentences:
        for word in sentence.words:
            print(f"{word.text:<20} {word.upos:<20} {word.xpos}")
            unique_tags.add(word.upos)

    # 5. Analysis & Discussion (Required by Lab Question)
    print("-" * 65)
    print("--- Analysis & Discussion ---")
    
    # c. Identify common tags and compare with English
    print("1. Common Tags Found:")
    print(f"   {sorted(list(unique_tags))}")
    print("   Comparison with English:")
    print("   - ADP (Adposition): Hindi uses 'Postpositions' (after the noun, e.g., 'table par')")
    print("     unlike English 'Prepositions' (before the noun, e.g., 'on table').")
    print("   - AUX (Auxiliary): Hindi often places auxiliary verbs (like 'hai') at the very end.")
    print("   - Word Order: Hindi follows SOV (Subject-Object-Verb), whereas English is SVO.")

    # d. Challenges in Morphologically Rich Languages
    print("\n2. Challenges in Morphologically Rich Languages (like Hindi):")
    print("   - Free Word Order: While SOV is standard, words can be moved for emphasis without")
    print("     changing meaning, making it harder for sequence-based models (n-grams).")
    print("   - Complex Morphology: Verbs change forms based on Gender, Number, and Person")
    print("     (e.g., 'khata' vs 'khati' vs 'khate').")
    print("   - Ambiguity: Words like 'kal' can mean both 'yesterday' and 'tomorrow' depending on tense.")

if __name__ == "__main__":
    pos_tagging_hindi()