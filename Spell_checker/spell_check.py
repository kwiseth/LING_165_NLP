# spell_check.py
# 21-Nov-2024 Revising lab 5 from Ling 165 for python and other improvements.
# Ling 165 kwiseth  1-Sept-2013
# This script looks-up a word entered at the command line in the brown.words file, and if found, prints the word.
# If not found, the script then narrows the search space in brown to words that are +2/-1 length of word entered and
# further narrrows to words within that space that either begin with or end with the same beginning and ending character
# of the word entered. NOTE: This may be narrowing too far, but in testing, it seems that more appropriate choices are
# presented to the user.
# This script doesn't actually "correct" the spelling, but merely offers an ordered list of choices by levenshtein distance.
# NOTE: Rather than presenting all words in the dictionary, this script presents only those choices within a Levenshtein
# distance of 1, 2, 3, or 4 from closest to furthest edit distance.


# ling165_lab5.py

import sys
from operator import itemgetter

# Open and process the Brown dictionary
with open('brown.words', 'r') as brown_f:
    brown_words = [word.strip().upper() for word in sorted(brown_f.readlines(), key=len)]

def lookup_word(some_word):
    """Check if the word exists in the Brown dictionary."""
    return some_word in brown_words

def get_brown_ltd(some_word):
    """Limit search space to words within +2/-1 length of `some_word`."""
    wd_len = len(some_word)
    return [word for word in brown_words if wd_len - 1 <= len(word) <= wd_len + 2]

def get_brown_ltd_narrow(some_word):
    """Further limit search space by length and matching start/end characters."""
    wd_len = len(some_word)
    wd_start, wd_end = some_word[0], some_word[-1]
    brown_subset = [word for word in brown_words if wd_len - 1 <= len(word) <= wd_len + 2]
    return [word for word in brown_subset if word[0] == wd_start or word[-1] == wd_end]

def minimumEditDistance(source, target):
    """Calculate minimum edit distance between source and target."""
    n, m = len(target), len(source)
    distance = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        distance[i][0] = i
    for j in range(1, m + 1):
        distance[0][j] = j
        
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if source[j - 1] == target[i - 1] else 1
            distance[i][j] = min(
                distance[i - 1][j] + 1,
                distance[i][j - 1] + 1,
                distance[i - 1][j - 1] + cost
            )
    return distance[n][m]

def spell_check(word):
    """Perform spell check, returning close matches within edit distance 4."""
    word = word.upper().strip()
    if lookup_word(word):
        print("Word found in the Brown dictionary:", word)
    else:
        brown_words_limited = get_brown_ltd_narrow(word)
        word_distances = {
            (word, candidate): minimumEditDistance(word, candidate) for candidate in brown_words_limited
        }
        sorted_wd_pr = sorted(word_distances.items(), key=itemgetter(1))

        # Display results by distance
        close_matches = [item for item in sorted_wd_pr if item[1] <= 2]
        further_matches = [item for item in sorted_wd_pr if 2 < item[1] <= 4]

        if close_matches:
            for item in close_matches:
                print(f"{item[0][0]} --> {item[0][1]} \t {item[1]}")
        elif further_matches:
            print("No words within Levenshtein distance of 2. Here are words with distance 3 or 4:")
            for item in further_matches:
                print(f"{item[0][0]} --> {item[0][1]} \t {item[1]}")
        else:
            print("No words within edit distance of 4 found.")

def process_file(filename):
    """Process words from a file, applying spell check to each."""
    with open(filename, 'r') as file:
        for line in file:
            spell_check(line.strip())

# Main program
def main():
    print("\nLing 165 Lab 5: Spelling Correction and Levenshtein Distance")
    print('-' * 80)
    print("This script looks up a word in the Brown dictionary and calculates Levenshtein distances for spelling correction.")
    print("\n9: Run test.me file\n0: Quit\n")

    while True:
        selection = input('Enter a word (or enter 9 or 0): ')
        
        if selection.isdigit() and int(selection) == 9:
            print("Processing the test.me file...")
            process_file('test.me')
        elif selection.isdigit() and int(selection) == 0:
            print("Goodbye.")
            sys.exit()
        elif selection.isalpha():
            spell_check(selection)
        else:
            print("Invalid input. Please enter a word, or choose 9 to run the test file, or 0 to exit.")

if __name__ == "__main__":
    main()
