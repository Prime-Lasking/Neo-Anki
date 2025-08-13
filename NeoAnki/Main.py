import os
import random
import time

full_file_path = "Stored Flashcards/Flashcards.txt"

# Load flashcards
flashcards = []
if os.path.exists(full_file_path):
    with open(full_file_path, 'r') as f:
        flashcards = [line.strip() for line in f if line.strip()]
else:
    print("Warning: Flashcards file not found. Starting with an empty set.")

# Menu loop
flag = True
print("\nFlashcard Menu:")
print("1. Make new flashcards")
print("2. Remove flashcard")
print("3. Review flashcards")
print("4. Flashcard Challenge")
print("5. Test Mode (Mark Know/Don't Know)")
print("6. Shut-down")
while flag:
    user_choice = int(input("What is your choice (only enter number): "))

    # Add new flashcard with autosave
    if user_choice == 1:
        side1 = input("Side 1: ")
        side2 = input("Side 2: ")
        flashcard = f"{side1}|{side2}"
        flashcards.append(flashcard)
        with open(full_file_path, 'w') as f:
            f.write('\n'.join(flashcards))
        print("Flashcard added and saved.")

    # Remove flashcard + autosave
    elif user_choice == 2:
        term = input("Enter term to remove: ")
        original_count = len(flashcards)
        flashcards = [fc for fc in flashcards if not fc.startswith(f"{term}|")]
        if len(flashcards) < original_count:
            with open(full_file_path, 'w') as f:
                f.write('\n'.join(flashcards))
            print("Flashcard removed and saved.")
        else:
            print("No matching flashcard found.")

    # Review flashcards (only 'don't know' ones)
    elif user_choice == 3:
        if not flashcards:
            print("No flashcards to review.")
        else:
            random.shuffle(flashcards)
            for fc in flashcards:
                parts = fc.split('|')
                # Only show cards marked as not known
                if len(parts) == 3 and parts[2].strip().lower() in ("non-know", "dont-know", "don't know"):
                    side1, side2 = parts[0], parts[1]
                else:
                    continue
                input(f"\n{side1} — Press Enter to reveal...")
                print(f"→ {side2}")

    # Flashcard Challenge Game
    elif user_choice == 4:
        if not flashcards:
            print("No flashcards available for challenge.")
        else:
            print("\nFlashcard Challenge Begins!")
            random.shuffle(flashcards)
            correct = 0
            total = len(flashcards)
            start_time = time.time()

            for fc in flashcards:
                parts = fc.split('|')
                side1, side2 = parts[0], parts[1]
                answer = input(f"\n{side1}: ").strip()
                if answer.lower() == side2.lower():
                    print("Correct!")
                    correct += 1
                else:
                    print(f"Incorrect. Correct answer: {side2}")

            end_time = time.time()
            time_taken = round(end_time - start_time, 2)
            accuracy = correct / total
            score = int(accuracy * 1000 / (time_taken + 1))

            print("\nChallenge Results:")
            print(f"Correct: {correct}/{total}")
            print(f"Accuracy: {accuracy:.2%}")
            print(f"Time Taken: {time_taken} seconds")
            print(f"Score: {score}")

    # Test Mode: Mark flashcards as 'know' or 'don't know'
    elif user_choice == 5:
        if not flashcards:
            print("No flashcards to test.")
        else:
            print("\nTest Mode: Mark each flashcard as 'know' or 'dont know'")
            updated_flashcards = []
            for fc in flashcards:
                parts = fc.split('|')
                if len(parts) == 3:
                    side1, side2 = parts[0], parts[1]
                else:
                    side1, side2 = parts
                input(f"\n{side1} — Press Enter to reveal...")
                print(f"→ {side2}")
                status = input("Do you know this? (y/n): ").strip().lower()
                tag = "know" if status == 'y' else "non-know"
                updated_flashcards.append(f"{side1}|{side2}|{tag}")
            flashcards = updated_flashcards
            with open(full_file_path, 'w') as f:
                f.write('\n'.join(flashcards))
            print("Flashcards updated with knowledge status.")

    # Shut-down
    elif user_choice == 6:
        print("Shutting Down")
        for _ in range(3):
            time.sleep(1)
            print('.')
        break

    else:
        print("Invalid choice. Please enter a number from 1 to 6.")