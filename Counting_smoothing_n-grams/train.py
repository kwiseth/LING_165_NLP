#!/usr/bin/python3/train.py
# Updated 2024-30-March (kwiseth)
# Ling 165 Lab 1 kwiseth Feb and Mar 2013
# train.py
# Create dictionary of bigrams from training data (brown.train)
# Functions get_bigrams and update_counts adapted from Hahn Koo Ling115 lecture of 7-Nov-2012

# Extract bigrams from each line in a file and update a bigram_frequency_dictionary.
# Additional functions for building a word list and word counts.
# 22-Feb stripped this down to the bare essentials-- just get the dictionary built from training data
#		and also build a list of words (for vocabulary)
# 23-Mar completed my 'refactoring' to include method for getting words and word counts
#       and also using more Python-esque approaches (list comprehensions replacing counters/loops)



import sys, pickle, bigram
sys.path.append('lab_1/data')

# This is the main processing loop. We open the training data file.close
# At runtime, enable/disable appropriate path as needed.

trainfile = open('data/brown.train', 'r') 
#trainfile = open('my.train', 'r')
#trainfile = open('my.train.SMALL', 'r')
train_data = trainfile.readlines()
trainfile.close()

# Define the data structures that we'll use to process the training data.
bigram_freq_dict = {}
vocab_freq_dict = {}

# Create the bigram dictionary and keep track of the number of
# tokens of each bigram type. Data structure is {(w1, w2) : int}
# Create a unigram dictionary while we're at it using the same
# line that's being processed. 

for line in train_data:
	bigram_list = bigram.get_bigrams(line)
	bigram_freq_dict = bigram.update_bigram_counts(bigram_list,bigram_freq_dict)
	vocab_list = bigram.get_words(line)
	vocab_freq_dict = bigram.update_vocabulary(vocab_list,vocab_freq_dict)
		  
print("**************************************")
print("Training Data Summary Information ")
print("-------------------")
print("Bigram details: ")
print("number of bigrams: (length of bigram_freq_dict)")
print(len(bigram_freq_dict))
print("number of tokens: (sum of bigram_freq_dict values) ")
print(sum(bigram_freq_dict.values()))
print("unique bigrams: (sum of all bigram_freq_dict bigrams that are equal to 1 )")
print(sum(bigram_freq_dict[bigram] for bigram in bigram_freq_dict if bigram_freq_dict[bigram]==1))
print("-------------------")
print("Vocabulary details: ")
print("Words (types) in vocabulary: ")
print(len(vocab_freq_dict))
print("Word count (tokens) in vocabulary")
print(sum(vocab_freq_dict.values()))
print("Unique words in vocabulary")
print(sum(vocab_freq_dict[word] for word in vocab_freq_dict if vocab_freq_dict[word] == 1 )) #hapax
print("*****************************************")

# Bigram frequency dictionary has been created.
# Save the bigram dictionary for later use.
bd = open('bigram_freq.save','wb')
pickle.dump(bigram_freq_dict,bd)
bd.close() 

# Vocabulary frequency dictionary has been created.
# Save this for later use.
voc = open('vocab.save', 'wb')
pickle.dump(vocab_freq_dict, voc)
voc.close()

print("Training data processed. Bigram dictionary and vocabulary dictionary saved. ")
