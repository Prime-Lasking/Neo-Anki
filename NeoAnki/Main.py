import random
import time
from Functions import (
    load_flashcards, save_flashcards, fsrs_update,
    format_flashcard, parse_flashcard, search_flashcards,
    select_deck,print_Banner
)

# Banner
print_Banner()
full_file_path = select_deck()
flashcards = load_flashcards(full_file_path)

# Main Menu
print("\nFlashcard Menu:")
print("1. Make new flashcards")
print("2. Remove flashcard")
print("3. Review flashcards")
print("4. Shut-down")
print("5. Search flashcards")

while True:
    try:
        user_choice = int(input("What is your choice (only enter number): "))
    except ValueError:
        print("Invalid input. Please enter a number from 1 to 5.")
        continue

    if user_choice == 1:
        side1 = input("Side 1: ")
        side2 = input("Side 2: ")
        flashcard = format_flashcard(side1, side2)
        flashcards.append(flashcard)
        save_flashcards(full_file_path, flashcards)
        print("Flashcard added and saved.")

    elif user_choice == 2:
        term = input("Enter term to remove: ")
        original_count = len(flashcards)
        flashcards = [fc for fc in flashcards if not fc.startswith(f"{term}|")]
        if len(flashcards) < original_count:
            save_flashcards(full_file_path, flashcards)
            print("Flashcard removed and saved.")
        else:
            print("No matching flashcard found.")

    elif user_choice == 3:
        print(f"\nReviewing flashcards — {time.strftime('%Y-%m-%d')}")
        random.shuffle(flashcards)
        updated_flashcards = []
        for fc in flashcards:
            card = parse_flashcard(fc)
            if card["tag"] in ("learning", "non-know", "dont-know", "don't know"):
                input(f"\n{card['side1']} — Press Enter to reveal...")
                print(f"Answer: {card['side2']}")
                rating = input("Rating (again/good/easy): ").strip().lower()
                if rating in ("again", "good", "easy"):
                    stability, difficulty = fsrs_update(card["stability"], card["difficulty"], rating)
                    tag = "mastered" if stability > 15 else "learning"
                    updated_flashcards.append(format_flashcard(card["side1"], card["side2"], tag, stability, difficulty))
                else:
                    print("Invalid rating. Skipping.")
                    updated_flashcards.append(fc)
            else:
                updated_flashcards.append(fc)

        flashcards = updated_flashcards
        save_flashcards(full_file_path, flashcards)
        print("Flashcards updated with FSRS review data.")

    elif user_choice == 4:
        print("Shutting Down")
        for _ in range(3):
            print(".")
            time.sleep(1)
        break

    elif user_choice == 5:
        keyword = input("Enter keyword to search: ").lower()
        matches = search_flashcards(flashcards, keyword)
        if matches:
            print(f"\nFound {len(matches)} matching flashcards:")
            for m in matches:
                print("Match:", m.replace('|', ' | '))
        else:
            print("No matches found.")

    else:
        print("Invalid choice. Please enter a number from 1 to 5.")

