# Ling 165 Lab 1 kwiseth Feb and Mar 2013
# bigram.py
# Methods that will be used to create dictionary and process bigrams
# The get_bigrams and update_counts functions (methods) in this file
# have been adapted from Hahn Koo's Ling 115 lecture of 7-Nov-2012
# March 2013: Added functions to retrieve word lists and update
# a vocabulary dictionary.


def get_bigrams(some_line):
	some_line = some_line.strip() 
	words = some_line.split()
	line_length = len(words)
	index_list = range(0,line_length-1)
	bigram_list = []
	for index in index_list:
		bigram = words[index:index+2] # get a bigram slice
		bigram = tuple(bigram) # convert the slice into a tuple
		bigram_list.append(bigram) # add the tuple to bigram_list
	return bigram_list

def update_bigram_counts(some_bigram_list, current_freq_dict):
	for bigram in some_bigram_list:
		if bigram in current_freq_dict:
			current_freq_dict[bigram] = current_freq_dict[bigram]+1
		else:
			current_freq_dict[bigram] = 1
	return current_freq_dict

def get_words(some_line):
	some_line = some_line.strip()
	words = some_line.split()
	word_list = words
	return word_list

def update_vocabulary(some_word_list, current_vocab_dict):
	for word in some_word_list:
		if word in current_vocab_dict:
			current_vocab_dict[word] = current_vocab_dict[word]+1
		else:
			current_vocab_dict[word]= 1
	return current_vocab_dict

