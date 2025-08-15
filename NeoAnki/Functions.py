import os
def list_decks(deck_folder):
    if not os.path.exists(deck_folder):
        os.makedirs(deck_folder)
    return [f[:-4] for f in os.listdir(deck_folder) if f.endswith(".txt")]

def select_deck():
    deck_folder = "Decks"
    decks = list_decks(deck_folder)
    print("\nAvailable Decks:")
    for i, deck in enumerate(decks, 1):
        print(f"{i}. {deck}")
    print(f"{len(decks)+1}. Create new deck")

    while True:
        try:
            choice = int(input("Select a deck: "))
            if 1 <= choice <= len(decks):
                return os.path.join(deck_folder, decks[choice - 1] + ".txt")
            elif choice == len(decks) + 1:
                new_deck = input("Enter new deck name: ").strip()
                return os.path.join(deck_folder, new_deck + ".txt")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")
def load_flashcards(path):
    if not os.path.exists(path):
        print("Warning: Flashcards file not found. Starting with an empty set.")
        return []
    with open(path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def save_flashcards(path, flashcards):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write('\n'.join(flashcards))

def format_flashcard(side1, side2, tag="learning", stability=1.0, difficulty=3.0):
    return f"{side1}|{side2}|{tag}|{stability:.2f}|{difficulty:.2f}"

def parse_flashcard(fc):
    parts = fc.split('|')
    while len(parts) < 5:
        parts += ["learning", "1.0", "3.0"]
    return {
        "side1": parts[0],
        "side2": parts[1],
        "tag": parts[2],
        "stability": float(parts[3]),
        "difficulty": float(parts[4])
    }

def fsrs_update(stability, difficulty, rating):
    if rating == "again":
        stability = 1.0
        difficulty = min(difficulty + 0.5, 5.0)
    elif rating == "good":
        stability *= 1.8
        difficulty = max(difficulty - 0.2, 1.0)
    elif rating == "easy":
        stability *= 2.5
        difficulty = max(difficulty - 0.4, 1.0)
    return stability, difficulty

def search_flashcards(flashcards, keyword):
    return [fc for fc in flashcards if keyword.lower() in fc.lower()]
