# ling165_lab3.py   28-August-2013 Final version: Best possible result is 82% correct. The "lab3_error.log" file contains
# incorrectly labeled sentences and the bag-of-words that comprised the sentence. 
# Ling 165 kwiseth
# Lab 3 
# Disambiguating the word 'drug' using Naive Bayes-bag'o words model
# We have but two choices for meaning of 'drug': illegal = 0, medical = 1
# so this is our "c" for which we to maximize in order to disambiguate.

import sys, re, math

sys.path.append('/home/students/ling165/lab2')
sys.path.append('/home/students/ling165/lab3')

import smooth165

import nltk
sw = nltk.corpus.stopwords.words('english')

# Global variables for this script
fd = {} # Frequency dictionary
ctx_word_list = [] # Variable for list used during training phase
tst_word_list =[]  # Variable for list used during testing phas
p_1_ctr = 0  # Counter used during training to keep count of sentences identified as 'medical' sense 
p_0_ctr = 0  # Counter used during training to keep count of sentences identified as 'illegal' sense
wsd_ctr = 0  # Keep track of correctly scored test sentences
wrong_ctr = 0 # Keep track of incorrect answers (may get rid of this after debugging script)
num_lines = 0 # Number of lines in test file

def get_clean_line(some_line):
    """ Accept a line (a string), break into chunks (words), and then remove any extraneous punctuation marks. This is
    being used to process both the training data and the test data. """
    cleaned_line = ''
    chunks = some_line.strip().split() # Eliminate extra blank lines and extra whitespace
    word_list = []
    for i in range(0, len(chunks)): # Remove any leading and closing punctuation from each word in the sentence
        word = chunks[i].strip("()-~\"\':;).?!")
        word_list.append(word)
        cleaned_line = ' '.join(word_list) + ' '
    return cleaned_line

def get_bag_of_words(some_line):
    """Accepts a line, removes the target word, breaks up into words, and returns the bag of words. """
    sans_target_word = re.sub('([Dd]rug\'?s?[-;:,]?)', '', some_line)  # Remove the target word from each line
    words = set(sans_target_word.split()) # Should use the set() function in here i think????? 
    bag_list = [word for word in words if word not in sw] # Build new list without the stopwords
    return bag_list
   
def update_class_word_counts(some_bow_list, current_freq_dict, some_class):   # pass the bag of words (bow) list and dict
    list = some_bow_list
    ctx_word_list = []
    current_class = some_class
    for word in list:
        ctx_word = (current_class, word)
        ctx_word_list.append(ctx_word)
    for item in ctx_word_list:
        if item in current_freq_dict:
            current_freq_dict[item] = current_freq_dict[item] + 1
        else:
            current_freq_dict[item] = 1
    return current_freq_dict

def get_sense(some_list, some_smoothed_dict):
    probs = some_smoothed_dict
    score_0 = []
    score_1 = []
    word_score_0 = 0
    word_score_1 = 0
    for word in some_list:  # let's get the probabilities for each word in this sentence
        if word not in probs['0']:
            score_0.append(-1 * math.log(probs['0']['<UNK>']))
        else:
            score_0.append(-1 * math.log(probs['0'][word]))
        if word not in probs['1']:
            score_1.append(-1 * math.log(probs['1']['<UNK>']))
        else:
            score_1.append(-1 * math.log(probs['1'][word]))
    # Let's accumulate our scores 
    for i in range(0, len(score_0)-1):
        word_score_0 += score_0[i]
    word_score_0 = (-1 * word_score_0) + len(some_smoothed_dict['0'])/len(some_smoothed_dict['0']) + len(some_smoothed_dict['1'])
    for j in range(0, len(score_1)-1):
        word_score_1 += score_1[j]
    word_score_1 = (-1 * word_score_1) + len(some_smoothed_dict['1'])/len(some_smoothed_dict['0']) + len(some_smoothed_dict['1'])
    if word_score_0 > word_score_1: 
        word_sense = 0
    else:
        word_sense = 1
    return word_sense

# **************************************************************************************

# main processing starts here. No menu. The script starts by opening the training file
# and processing the data, building a dictionary of words associated with the two senses
# of the target-word 'drug' (in various forms) with their counts.
# Does not include stop-words. 

# Training process
trnfile = open('/home/students/ling165/lab3/train.drug', 'r')
train_data = trnfile.readlines()
trnfile.close()

for line in train_data:
    c = line[-2]   # pick up the class value (0=illegal | 1 = medical) from end of each sentence (line)
    if c == '1':
        p_1_ctr +=1
    elif c == '0':
        p_0_ctr +=1
    nuline = get_clean_line(line[0:-3].lower())
    bag_of_words_list = get_bag_of_words(nuline)
    fd = update_class_word_counts(bag_of_words_list, fd, c)

#print ("here is the dictionary... examine the words being counted and look for problems ")
#print fd
    
# Smooth the counts.
print("Smoothing the frequency counts in the dictionary...")
p = smooth165.lab2(fd)   #returns the smoothed probabilities
#print p
print("Training completed.")

# Use the smooth probabilities to calculate the P(c) for '1' and '0'
prob_0 = p_0_ctr / float(len(train_data))
log_p_0 = math.log(prob_0)
prob_1 = p_1_ctr / float(len(train_data))
log_p_1 = math.log(p_1_ctr/float(len(train_data)))
pos_log_1 = -1*log_p_1
pos_log_0 = -1*log_p_0

''' # testing... results confirm that file is 50% illegal, 50% medical
print (" mle for 'illegal' is  p_0_ctr/len(train_data), (prob_0 variable) which is: ")
print prob_0
print (" prob_0 as log is: ")
print log_p_0

print (" mle for 'medical' is  p_1_ctr/len(train_data), (prob_1 variable) which is: ")
print prob_1
print (" prob_1 as log is: ")
print log_p_1
'''

# Disambiguation phase ****
print("Disambiguation phase begins...")
print("Opening test file... ")

tstfile = open('/home/students/ling165/lab3/test.drug', 'r')
test_data = tstfile.readlines()
tstfile.close()

print("Disambiguating sentences in test file...")

for line in test_data:
    correct_answer = int(line[-2])   # pick up the correct sense value from the end of the line in the file
    num_lines += 1    # Add to the num_lines counter for use in percent-correct calculation
    nuline = get_clean_line(line[0:-3].lower())  # get just the sentence text, sans "sense" value
    tst_word_list = get_bag_of_words(nuline)
    sense = get_sense(tst_word_list, p)  # apply my classifier
    wsd = str(sense) + "\t" + line + "\n"  # insert my answer in front of the line being processed
    outfile = open('test_drug.wsd', 'a')  # add to my output file
    outfile.writelines(wsd)
    outfile.close()
# testing/dev snips...
#    print sense
#    print correct_answer
    if int(sense) == int(correct_answer): # Compare the answer provided by the classifier to that at the end of the line in the file
        wsd_ctr += 1
#        print wsd_ctr
#        print ("answer is correct and correct counter is now " + str(wsd_ctr))
    else:
        wrong_ctr += 1
        wrong = str(line) + "\n" + str(tst_word_list) + "\n\n" # Update the log of mis-identified senses
        errfile = open('lab3_wsd_error.log', 'a')
        errfile.writelines(wrong)
        errfile.close()

percent_correct = float(wsd_ctr/float(num_lines))*100

print("Processing complete.")
print("")
print("Lab 3 Results")
print("----------------------------------------------")
print("Total test lines: " + str(num_lines))
print("Correct: " + str(wsd_ctr) + "\tIncorrect:  " + str(wrong_ctr))
print("----------------------------------------------")


print("Correctly disambiguated: " + str(percent_correct) + "%")

print("See output file 'lab3_wsd_error.log' for errors. ")
print("See output file 'test_drug.wsd' for sentences labeled per classifier.")
