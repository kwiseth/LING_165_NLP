#!/usr/bin/python3/guess.py
# Ling 165 Lab 1 kwiseth Feb-Mar 2013
# guess.py
# Uses frequency counts from train.py to estimate expected
# bigram frequencies using three different 
# smoothing algorithms. 
# Reports mean frequencies for F_true = 1 through 10.

import sys, pickle
import bigram, probs

import sgt_new

sys.path.append('lab_1/')


# Open the test file and process bigrams.

testfile = open('data/brown.test', 'r') 
#testfile = open('my.test', 'r')
#testfile = open('my.test.SMALL', 'r')
test_data = testfile.readlines()
testfile.close()

# Create a dictionary to keep track of bigrams and counts
# from test file. The counts are the f_true values.
true_bgm_freq = {}

for line in test_data:
	bigram_list = bigram.get_bigrams(line)
	true_bgm_freq = bigram.update_bigram_counts(bigram_list,true_bgm_freq)
	

# Let's open the training dictionary for use
# in our estimates. We can also make our adjusted_freq_dict
# at this same time (using Hahn's script) since we have the file open.
# bfd is handle for bigram_freq_dict (bigram frequency dictionary)

bfd = open('bigram_freq.save','rb')
bfd_train = pickle.load(bfd)
adjusted_freq_dict = sgt_new.gt_freq(bfd_train)    # Dictionary of adjusted freqs for sgt
bfd.close()

# Let's get some of the values we'll need from training data Bigrams.
train_N_types = len(bfd_train)
train_N_tokens = sum(bfd_train.values())
train_N_hapax = sum(bfd_train[word] for word in bfd_train if bfd_train[word] == 1 ) #hapax


# Need to get our vocabulary count details, so let's open
# the unigram frequency dictionary we saved.
voc = open('vocab.save','rb')
voc_train = pickle.load(voc)
voc.close()


# Let's get values from our training data Vocabulary
train_V_types = len(voc_train.items()) # word types
train_V_tokens = sum(voc_train.values()) # total word tokens
train_V_hapax = sum(voc_train[word] for word in voc_train if voc_train[word] == 1 ) #hapax

# From test data, let's get the value of N_test which helps us get f_guesses
test_N_bgm_toks = sum(true_bgm_freq.values())     #N_test


# Let's calculate any values that will be used in our various formulae.
pos_bgm_B = float(train_V_types**2)
#print " Value of B: possible bigrams |V|**2"
#print pos_bgm_B

add_one_denom = float(train_N_tokens + pos_bgm_B)
#print " denominator for probability for add_one "
#print  add_one_denom

# might be getting types confused here. try using types instead of hapax
#N_zero = pos_bgm_B - train_N_hapaX
N_zero = pos_bgm_B - train_N_types


# print(rpy2.__version__)

# print("F_true\t\t\tF_mle\t\t\tF_one")
print("F_true\t\t\tF_mle\t\t\tF_one\t\t\tF_sgt")

for tru_freq in range(1, 11):
	bucket = [bigram for bigram, count in true_bgm_freq.items() if count == tru_freq]
	mle_counts = [probs.get_mle(bigram, bfd_train, train_N_tokens, test_N_bgm_toks) for bigram in bucket]
	one_counts = [probs.get_one(bigram, bfd_train, voc_train, test_N_bgm_toks) for bigram in bucket]
	sgt_counts = [probs.get_sgt(bigram, bfd_train, train_N_tokens, train_N_hapax, voc_train, adjusted_freq_dict, test_N_bgm_toks) for bigram in bucket]
	#print sum(mle_counts)/len(mle_counts)
	#print "**************"
	#print sum(one_counts)/len(one_counts)
	print(str(tru_freq) + '\t\t' + str(sum(mle_counts)/len(mle_counts)) + '\t\t' + str(sum(one_counts)/len(one_counts)) \
		  + '\t\t' + str(sum(sgt_counts)/len(sgt_counts)))
#	print(str(tru_freq) + '\t\t' + str(sum(mle_counts)/len(mle_counts)) + '\t\t' + str(sum(one_counts)/len(one_counts)))
	

print("Lab 1 results.")