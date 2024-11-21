"""Top-twenty informative words (tf-idf, llr)"""

__author__ = """Kelli Wiseth (kelli@alameda-tech-lab.com)"""

# ling165_lab4.py       30-August-2013
# Ling 165 kwiseth
# Lab 4 
# Top-twenty informative words based on two different approaches (tf-idf, llr). 

import sys, re, math, os, string
import llr

import nltk
from operator import itemgetter

""" Several different functions for processing the New Yorker article, each with different amounts of text cleanup and additional processing, for
experimentation purposes."""

def get_words(some_line):
    """ Function that accepts a line from the New Yorker article and minimally processes, returning a list of words."""
    nuline = some_line.strip().split()
    word_list = [w for w in nuline if w.isalpha()]  # By-pass punctuation, numbers, dates
    return word_list

def get_words_utf8_clean(some_line): # This is an alternative 'get_words()' function that does a lot of additional massaging of the New Yorker article text, mostly to clean-up UTF/ASCII differences.
    """ Function that accepts a line from the New Yorker article (processed using Hahn's clean.py script) and replaces the UTF-8 codepoints with ASCII chars."""
    sw = nltk.corpus.stopwords.words('english')  
    nuline = some_line.replace('per cent', 'percent') # New Yorker copyedit style is unique; these two fixes seem important
    nuline = nuline.replace('output per hour', 'output-per-hour') # New Yorker copyedit style is unique.
    # Replacing some utf-8 codepoints with ascii. 
    nuline = nuline.replace('\xe2\x80\x99', '\'') # right-single quote -> single quote
    nuline = nuline.replace('\xe2\x80\x94', ' -- ') # em-dash -> hyphens and spacebands
    nuline = nuline.replace('\xe2\x80\x93', ' -- ') # en-dash -> hyphens and spacebands
    nuline = nuline.replace('\xe2\x80\x90', '-') # hyphen -> hyphen
    nuline = nuline.replace('\xe2\x80\x98', '\'') # right-single-quote -> right-single-quote
    nuline = nuline.replace('\xe2\x80\x9c', '"') # double-quote -> right-double quote
    nuline = nuline.replace('\xe2\x80\x9d', '"') # quote -> quote
    dot_patt = re.compile('\.(?!\d)')  # Clean periods from words (period not followed by digit) don't need to do this given string.strip() below
    nuline = dot_patt.sub('', nuline)
    punc_patt = re.compile('[();:\?\",*!]*')  # Clean miscellaneous punctuation
    nuline = punc_patt.sub('', nuline)
#    dash_patt = re.compile('(--)')
#    nuline = dash_patt.sub('', nuline)
    big_word_list = nuline.lower().strip("()-~\"\':;).?!").split() # Get rid of any extraneous punctuation attached to word
    prelim_word_list = [w for w in big_word_list if w not in sw]  # without stopwords
    word_list = [w for w in prelim_word_list if w.isalpha()]      # without numbers and dates eg, 2004, 1.5 etc.
    return word_list

def process_corpus_docs(some_list_of_docs):
    ''' Accepts a list of files (the directory-corpus) to process for use by both tf-idf and llr. '''
    doc_ctr = 0
    doc_map = {} # A dictionary containing an index for each brown document (0-499) and a big string comprising
                   # the content of each document, without the /POS-bits.
    doc_list = some_list_of_docs
    for num in range(0, len(doc_list)):
        doc_words = ' '
        file = open(doc_list[num], 'r')
        doc_data = file.readlines()
        file.close()
#        print("Processing document number " + str(num+1) + " from the corpus.")
        for line in doc_data:
             doc_line_words = '' # This is a string of just the words that we pull from Brown docs
             line = line.strip() # Files contain lots of extra whitespace and extra blank lines--eliminate.
             if line: # Here's how we avoid blank lines
                 chunks = line.lower().strip().split() # This first chunking gives us a list of separate 'word/POS-string' chunks
                 word_list = []
                 for i in range(0, len(chunks)):
                     nuchunk = chunks[i].split('/') # for each of these nuchunks, index [0] will be the word by itself
                     word = nuchunk[0]
                     word_list.append(word)
                 doc_line_words = ' '.join(word_list) + ' ' # Put the words in each line back together.
             doc_words += doc_line_words                    # Add to the document content
#            print num, brown_doc_line_words
        doc_map[num] = doc_words # Add to the dictionary (the mapping of doc-id (index number) to document content (content is now just a big string)
    return doc_map # the entire map should be returned to the caller

def update_word_counts(some_list, current_freq_dict):
    '''Accepts a list of words and a dictionary tf { 'word' : int } and updates the count of the 'word' in the dictionary.'''
    for word in some_list:
        if word in current_freq_dict:
            current_freq_dict[word] = current_freq_dict[word] + 1
        else:
            current_freq_dict[word] = 1
    return current_freq_dict

def update_word_doc_dict(some_list, doc_type, some_dict):
    '''Accepts a list of words, a document type, and a dictionary fd { (word, doc) : int } and updates the count. I only ended up using this for the 'ny' document itself. '''
    for word in some_list:
        if (word, doc_type) in some_dict:
            some_dict[(word, doc_type)] = some_dict[(word, doc_type)] + 1
        else:
            some_dict[(word, doc_type)] = 1
    return some_dict


# ****************************************************************************************
# main processing starts here.

# Global variables for this script
tf = {} # Frequency dictionary for tf-idf
fd = {} # Frequency dictionary for llr
tf_idf = {}  # Use this to keep track of scores for tf-idf
brown_doc_map = {} 

# local testing
'''
print("Pre-processing documents in mini /brown directory... ")
path = 'brown/'
file_list = os.listdir(path)
brown_doc_list = ['brown/' + str(i) for i in file_list]
'''

print("Pre-processing documents in /data/brown directory... ")
path = '/data/brown/'
file_list = os.listdir(path)
brown_doc_list = ['/data/brown/' + str(i) for i in file_list]

brown_doc_map = process_corpus_docs(brown_doc_list)
#print len(brown_doc_map)
#print brown_doc_map[0]
#print brown_doc_map[len(brown_doc_map)-1]
               
# Processing New Yorker article. 
print("Processing New Yorker article textfile...")
ny_file = open('newyawker.txt', 'r') # file created using Hahn's clean.py script
#ny_file = open('newyorker.txt', 'r') 
#ny_file = open('newyawker2.txt', 'r') # file created using my slightly modified version of Hahn's script
ny_data = ny_file.readlines()
ny_file.close()

# Obtaining word counts for tf dictionary. Structure { word : int } name is tf
# We should likely be able to use the tf dictionary as a starting point for the llr portion, since we'll have
# the words and their counts from the New Yorker article

print("Building list of words from text file...")

#ny_words = []
for line in ny_data:
    word_list = get_words_utf8_clean(line)
#    ny_words += word_list                           # Create a list of just the words that we want, for subsequent use
    # tf-idf processing.
    tf = update_word_counts(word_list, tf)          # Update the tf dictionary
   

ny_word_list = tf.keys()                            # Get the list of keys in tf before we starting modifying this structure. We'll use this as the
                                                    # list against which to process the brown documents
                                                    
# print ny_words # this should not have any stopwords, but it does (eg., 'new') or so it seems and I cannot seem to figure out what I'm doing wrong. 30-Aug

 
print("tf dictionary completed.")

# Creating the fd dictionary for the 'ny' values. The brown doc values will be added to this in a subsequent step, in the llr processing).
for key in tf:
    fd[(key, 'ny')] = tf[key]

# Debugging and testing. These values are all okay at this point.

'''
print("fd dictionary partially created based on word counts from New Yorker article { ['word', 'ny'] : count } ")
print("total counts for both dictionaries should be equal at this point")

print("tf counts total")
print sum(tf.values())   
print("fd counts total")
print sum(fd.values())
print ("lend all_words ")
print len(all_words)

'''       
print("Calculating and storing tf-idf values...")

# tf-idf calculations 

for key in tf:                                             # for every word in the dictionary tf... 
    ny_doc_ctr = tf[key]                                   # get its count and set to variable ny_doc_ctr
    brown_doc_ctr = 0                                      # brown doc counter initialized to 0
    for i in range(0, len(brown_doc_map)):                 # the length of brown_doc_map is the number of documents we have to look at
        if key in brown_doc_map[i]:                        # if my word is anywhere in the text of document (the string located at brown_doc_map[i] 
            brown_doc_ctr += 1                             # increment my doc counter for this word
    tf[key] = [ny_doc_ctr, brown_doc_ctr]                  # update the key with values of ny_doc_ctr (should be the same as orig above) and number of brown docs
    idf = (len(brown_doc_map) + 1) / (brown_doc_ctr + 1)   # adding 1 to account for the New Yorker article itself to calc the idf
    log_of_idf = math.log(idf)                             # calculate the log value 
    tf_idf[key] = (ny_doc_ctr * log_of_idf)                # store the result in the tf_idf dictionary

# Sort results in our dictionary by value starting from highest tf-idf. This is what we'll print below. 
sorted_tf_idf = sorted(tf_idf.items(), key = itemgetter(1), reverse=True) #

print("Counting words from New Yorker article in the rest of the corpus...")
print("This takes a while. Please be patient...")

# Processing for llr (and dictionary) continues. The fd dictionary thus far comprises {('word', 'ny') : count }
# Here we need to find the counts for each of the words in the brown documents. Unlike tf-idf, here we need
# actual word counts across all docs.


for word in ny_word_list:                                       # Look for each of the words in all the brown documents
    brown_wd_ctr = 0                                            # The count for the word in brown is initialized to 0 and will be reset after processing all brown docs
    for num in range(0, len(brown_doc_map)):                    # we have our word. let's start looking through brown
        temp_brown_doc = brown_doc_map[num]                     # Get the content and set it to temp_string
        brown_wd_list = temp_brown_doc.lower().strip().split()  # This should get the entire document as a list of words. Lower-casing to be consistent with how i handled new yorker artcle.
        for i in range(0, len(brown_wd_list)):                  # Go through all words in the brown list
            if brown_wd_list[i] == word:                        # Looking for the word and if found, add 1 to the counter
                brown_wd_ctr += 1                               # When we're finished with this document, we need to go on to the next document. Need to add word and brown ctr to fd
    fd[word, 'brown'] = brown_wd_ctr                            # This should be what we need for llr 
    
        
# At the end of this loop, we should have a completed brown_fd containing all word counts from brown.

'''
print ("here is our fd")
print fd
'''

# Debugging
#print fd

print("Calculating and storing llr scores (using Hahn's llr function)...")
# Looks like Hahn's llr takes care of "total number of words (tokens) " 
llr_score_dict = {} # Use this to keep track of words and their llr scores

for word in ny_word_list:
    llr_score = llr.llr(word, 'ny', fd)
    llr_score_dict[word] = llr_score
sorted_llr_score_dict = sorted(llr_score_dict.items(), key = itemgetter(1), reverse=True)  # Sort by the value (the score) from high to low


# Printing routine for results of tf-idf and llr scores, top twenty
print("Processing data complete. ")
print("")
print("Lab 4 Results: Top-twenty Words (Descending order)")
print("-" * 80)
print("\tWord ranked by tf-idf\t\tWord ranked by llr")
print("-" * 80)

for i in range(0, 20): # just need the top twenty words from each algorithm
   
    if len(sorted_tf_idf[i][0]) >= 8:
        print ( str(i+1) + "\t" + str(sorted_tf_idf[i][0]) + "\t\t\t" + str(sorted_llr_score_dict[i][0]) )
    else:
        print ( str(i+1) + "\t" + str(sorted_tf_idf[i][0]) + "\t\t\t\t" + str(sorted_llr_score_dict[i][0]) )

