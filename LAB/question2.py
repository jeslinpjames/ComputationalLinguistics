def extract_digits_manual(text):
    extracted_numbers = []
    current_num = ""

    for char in text:
        # Check if the character is a digit using ASCII values or isdigit()
        # '0' is ASCII 48, '9' is ASCII 57
        if char.isdigit():
            current_num += char
        else:
            # If we hit a non-digit and have a number stored, save it
            if current_num:
                extracted_numbers.append(current_num)
                current_num = ""
    
    # If the string ends with a number, append it
    if current_num:
        extracted_numbers.append(current_num)
        
    return extracted_numbers

if __name__ == "__main__":
    # Test Data
    strings = ["Order ID: 45231", "Price: $99", "Year: 2025"]
    paragraph = "In 2023, the population increased by 15000. Contact us at 555-0199."

    print("--- Extracting from Strings (Manual Logic) ---")
    for s in strings:
        digits = extract_digits_manual(s)
        print(f"String: '{s}' -> Digits: {digits}")

    print("\n--- Extracting from Paragraph (Manual Logic) ---")
    print(f"Paragraph: {paragraph}")
    print(f"Digits found: {extract_digits_manual(paragraph)}")