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

import sys, os
from operator import itemgetter


#brown_f = open('my.words', 'r')  # preliminary testing
#brown_f = open('brown.words', 'r') #local testing
brown_f = open('/home/students/ling165/lab5/brown.words', 'r') 
brown_words = brown_f.readlines()
brown_f.close()

brown_words = [word.strip() for word in sorted(brown_words, key=len)] # Get rid of line endingsand sort by length of word

def lookup_word(some_word):
    test_word = some_word
    if test_word in brown_words:
        return True
    else:
        return False

def get_brown_ltd(some_word):
    """This method is intended to limit the search space to which edit distance (levenshtein) is applied for each word look-up. This is less restrictive
    than get_brown_ltd_narrow in that we only look at word length and not initial character or ending character."""
    wd_len = len(some_word)
    len_lim_start = wd_len-1 # beginning word length
    len_lim_end = wd_len+2 # ending word length
    brown_subset = []  
    brown_subset = [word for word in brown_words if len(word) in range(len_lim_start, len_lim_end)]
    return brown_subset

def get_brown_ltd_narrow(some_word):
    """This method is intended to limit the search space to which edit distance (levenshtein) is applied for each word look-up. """
    wd_len = len(some_word)
    len_lim_start = wd_len-1 # beginning word length
    len_lim_end = wd_len+2 # ending word length
    brown_subset = []  
    wd_start = some_word[0]
    wd_end = some_word[-1]
    brown_subset = [word for word in brown_words if len(word) in range(len_lim_start, len_lim_end)]
    # Doing lookup against initial/final characters in string ... this turned out to be too limiting (eg swelcom didn't find welcome)
    # but the words returned seem more 'real'
    brown_less = [word for word in brown_subset if word[0] == wd_start or word[-1] == wd_end]
    return brown_less

def minimumEditDistance(source, target):
    """ Minimum edit distance based on Jurafsky-Martin text p. 76 Figure 3.25. This is basically the same
    process we used in class with paper/pencil to fill-in the table of minimum values between a source word (down) and
    a target word (across). """
    n = len(target)
    m = len(source)
    # Creates the distance matrix and initializes values that will capture the minimum distances between each 'slot' in traversing the table 
    distance = [[0 for i in range(m + 1)] for j in range(n + 1)]  
    for i in range(1, n + 1): # Creates a vector from empty string with distance for each add'l char in string (row) eg '#dog' = [0, 1, 2, 3]
        distance[i][0] = distance[i-1][0] + insert_char_cost(target[i-1]) # empty string
    for j in range(1, m + 1): # Creates a vector from empty string with distance for each add'l char in string (column) eg '#cat' = [0, 1, 2,3]
        distance[0][j] = distance[0][j-1] + delete_char_cost(source[j-1]) # Fill the first column from empty string 
    for i in range(1, n + 1):  # loop through the substrings and populate the 'slots' in the matrix with minimum values
        for j in range(1, m + 1):
            distance[i][j] = min(distance[i-1][j] + 1,
                                 distance[i][j-1] + 1,
                                 distance[i-1][j-1] + diff_char_cost(source[j-1], target[i-1]))
    return distance[n][m]

def insert_char_cost(some_char):
    """Cost add a character (one by one) from the empty string. """
    return 1

def delete_char_cost(some_char):
    """Cost to delete a character one by one to the empty string."""
    return 1

def diff_char_cost(source_char, target_char):
    """ Cost for substituting character.  """
    if source_char == target_char:
        return 0
    else:
        return 1


# Menu setup for processing choice (file or individual word entered at command prompt)
selection = ""
valid_num = [0, 9]

# Welcome message and character-based menu to display options.
print(' ')
print('Ling 165 Lab 5: Spelling Correction and Levenshtein Distance')
print('-' * 80 )
print('This script looks-up a word in the Brown dictionary and (if found) prints it,')
print('otherwise, calculates the Levenshtein distance to the words closest ')
print('to it. (You\'ll be notified if no words can be found within edit distance of 4.)')
print('')
print('9: Run-through the test.me file. ')
print('0: Quit this script. ')
print(' ')

while selection != "0":  # While-loop and menu-selections not needed if script to be part of actual spell correction module 
  
    # selected numbers that will drive the file selection
    selection = raw_input('Enter a word (or enter 9 or 0): ')

    if selection.isalpha():
        test_word = selection.upper()
        if lookup_word(test_word.strip()):
            print("Word found in the brown.words file: ")
            print test_word
        else:
            brown_words_limited = get_brown_ltd_narrow(test_word) # Reduce the search space
            word_pair_lev = {} # Create a dictionary of the results (to be further processed)
            sorted_wd_pr = []
            for word in brown_words_limited:
                word_pair_lev[test_word, word] = minimumEditDistance(test_word, word)
                sorted_wd_pr = sorted(word_pair_lev.items(), key=itemgetter(1, 0)) # Sort by the levenshtein distance value
                sorted_wd_pr_first = [item for item in sorted_wd_pr if item[1] <=2] # Reduce down to just those with edit distance <=2
                sorted_wd_pr_second = [item for item in sorted_wd_pr if item[1] > 2 and item[1]<=4] # Reduce down to just between 2 and 4
            if len(sorted_wd_pr_first)>0:
                for item in sorted_wd_pr_first:
                    print item[0][0] + " \t-->  " + item[0][1] + "\t\t" + str(item[1])
            elif len(sorted_wd_pr_first) == 0 and len(sorted_wd_pr_second) >0:
                print("No words in brown dictionary within levenshtein distance of 2, so here are words between 3 and 4")
                for item in sorted_wd_pr_second:
                    print item[0][0] + " \t-->  " + item[0][1] + "\t\t" + str(item[1])
            elif len(sorted_wd_pr_first) == 0 and len(sorted_wd_pr_second) == 0:
                print("Cannot find any words within 4 edits of the word you entered.")
                
           
    elif selection.isdigit():
        selection = int(selection)
        if selection in valid_num:
            if selection == 9:
                # Open the test.me file, lookup each word in the dictionary, and
                # if it's in the dictionary, print out the word; if not, print out similar
                # words and Levenshtein distance
                print("Processing the test.me file...")
                file = open('/home/students/ling165/lab5/test.me', 'r') 
                test_word = file.readlines()
                file.close()

                for line in test_word: # each line in the file is a word
                    if lookup_word(line.strip()):
                        print("Word found in the brown.words file: ")
                        print(line)
                    else:
                        test_word = line.strip() # Get rid of the \n 
                        brown_words_limited = get_brown_ltd_narrow(test_word)
                        word_pair_lev = {} # Create a dictionary of the results (to be further processed)
                        sorted_wd_pr = []  # To be used to create a list of word choices
                        for word in brown_words_limited:
                        # create a dictionary of word pairs and levenshtein distance and then process that
                            word_pair_lev[test_word, word] = minimumEditDistance(test_word, word)
                            sorted_wd_pr = sorted(word_pair_lev.items(), key=itemgetter(1)) #items or iteritems??
                            sorted_wd_pr = [item for item in sorted_wd_pr if item[1] <=2 ]
                        for item in sorted_wd_pr:
                            print item[0][0] + " \t-->  " + item[0][1] + "\t\t" + str(item[1])                          

            elif selection == 0:
                print("Goodbye.")
                sys.exit()  

        else:
            print("Please enter a word or valid menu selection. ")

    else:
        print("Please enter a word or valid menu selection.")

