# Ling 165 kwiseth
# 27-August-2013 Final version
# This script demonstrates using a first-order HMM (built from training data) for determining POS tags
# on another dataset (the test file). The "datasets" mentioned comprise a suite of training, test,
# and answer files that were created by Prof. Hahn Koo using 5-fold cross-validation technique, meaning that this
# script is more-or-less hard-wired to train, test, and evaluate the results (tagged output) against the appropriately numbered
# answered file. 

# ling165_lab2.py

import sys, os
import cPickle as pickle

sys.path.append('/home/students/ling165/lab2')

import smooth165, viterbi


def print_report(report_data):
    """ Function that accepts report data (a dictionary data structure) and prints the results."""
    print("=" * 80)
    print ("Ling 165 Lab 2 Summary Report")
    print("\t\t\tPOS tag counts...")
    print("Dataset\tTotal words\tCorrect\tIncorrect\t% Accuracy")
    print("_" * 80)
    for num in report_data:
        print(str(num) + "\t" + str(report_data[num][0]) + "\t\t" + str(report_data[num][1]) + "\t" + str(report_data[num][2]) + "\t\t%0.4f" % report_data[num][3] + " %")

def do_training(some_dataset_number):
    """ Opens the appropriate training file and create the two dictionaries we need.
    afd {} will be used to identify and count POS-tag-to-POS-tag
    bfd {} will be used to keep track of emission counts POS-tag for
    each word.
    Training file structure is e.g, Dancers_#_nns do_#_do have_#_hv flexibility_#_nn ._#_.
    Returns the dictionaries a, b """
    afd = {}
    bfd = {}
    
    trn_f = '/home/students/ling165/lab2/data/brown.train.' + str(some_dataset_number)
    afd_f = 'afd_' + str(some_dataset_number) + '.save' # Pickled dictionary file to save
    bfd_f = 'bfd_' + str(some_dataset_number) + '.save' # Pickeled dictionary file to save
 
    print("Training phase starting for " + trn_f)

    trnfile = open(trn_f, 'r')
    train_data = trnfile.readlines()
    trnfile.close()
    for line in train_data:
        line = line.strip().lower()
        chunks = line.split(' ')  # Break into chunks at spaceband
        pos_list = []    
        for chunk in chunks:
            word_pos_pair = chunk.split('_#_') # We use the _#_ to get a list of 'word' 'pos'
            pos = word_pos_pair[1]
            word = word_pos_pair[0]
            pos_word = (pos, word)
            if pos_word in bfd:
                bfd[pos_word] = bfd[pos_word]+1
            else:
                bfd[pos_word] = 1
            pos_list.append(pos)
        pos_list= ["<s>"] + pos_list + ["</s>"]

        for num in range(0, len(pos_list)-1):  
            pos_to_pos_seq=(pos_list[num], pos_list[num+1])
            if pos_to_pos_seq in afd:
                afd[pos_to_pos_seq] = afd[pos_to_pos_seq]+1
            else:
                afd[pos_to_pos_seq] = 1
   
    # We have our dictionaries, so now let's use Hahn's smoothing
    # functions to make our adjustments.
    a = smooth165.lab2(afd)
    print("Smoothing afd dictionary (transmission probabilities) completed.")
    b = smooth165.lab2(bfd)
    print("Smoothing bfd dictionary (emission probabilities) completed.")

    # pickling and storing dictionaries. These saved dictionaries aren't used in the batch mode, but
    # may be used for single-dataset processing, or to provide more flexibility in the future.
    afd_handle = open(afd_f,'w')
    pickle.dump(a, afd_handle)
    afd_handle.close() 
    print("Dictionary afd pickled and saved: " + afd_f)
    bfd_handle = open(bfd_f,'w')
    pickle.dump(b, bfd_handle)
    bfd_handle.close() 
    print("Dictionary bfd pickled and saved: " + bfd_f)
    print("Training completed.")
    return a, b

def do_tagging(some_dataset_number, some_dict_a, some_dict_b):
    """ Accepts a test file along with the matching dictionarie (from training) and
    tags the words and outputs the file to a file name matching the dataset."""

    tag_f = '/home/students/ling165/lab2/data/brown.test.' + str(some_dataset_number)
    out_f = 'tagged_output_' + str(some_dataset_number) + '.save'

    tstfile = open(tag_f, 'r')
    test_data = tstfile.readlines()
    tstfile.close()
    a = some_dict_a
    b = some_dict_b

    print("Tagging process started.")
    print("Using testfile " + str(tag_f))

    # Process the data in the test file. Here we use Hahn's Viterbi
    # module to determine the best path for the sequence of words.
    print("Using Hahn's viterbi module to build trellis and retrace to obtain optimal path")
    print("for tagging test file, writing output to file " + str(out_f))
    print("Please be patient--this may take a couple of minutes...")

    output_file=open(out_f, 'w')
    for line in test_data:
        line = line.strip().lower()
        word_list = line.split(' ')
        t = viterbi.trellis(a, b, word_list)
        t.update(a, b, word_list)
        path = t.backtrace()
        # Reset these variables for use in the subsequent for-loop
        index = 0
        tagged_wd_list=[]
        words_tags = ''
        # Loop through the tags in the path and each word 
        for tag in path[1:-1]:
            tagged_word = word_list[index] + "_#_" + tag
            index += 1
            tagged_wd_list.append(tagged_word)
           # at this point, the tagged_word datastructure contains a long list of items such as
           # ['word_#_pos', 'word2_#_pos', etc ] for each line in the test_data file.

        for word in tagged_wd_list:
            words_tags += word + ' '

        output_file.writelines(words_tags + "\n")
    output_file.close()
    return output_file
        

def do_evaluate(some_dataset_number):
    """Given a dataset number, this function opens the answerfile and output file (tagged-test-file), breaks up into
    chunks, and then compares the results, keeping track of total word count, correct tags, and calculating the percentage
    of correct tags. """

    ans_f = '/home/students/ling165/lab2/data/brown.test.answers.' + str(some_dataset_number)
    tagged_file = 'tagged_output_' + str(some_dataset_number) + '.save'
  
    ansfile = open(ans_f, 'r')
    answer_data = ansfile.readlines()
    ansfile.close()

    evalfile = open(tagged_file, 'r')
    eval_data = evalfile.readlines()
    evalfile.close()

    tru_tag = 0
    false_tag = 0
    a_wd_ctr = 0
    e_wd_ctr = 0 # use this to confirm the word count
    a_wd_tag_seq = []
    print("Evaluating results")

    current_result = []
    for i in range(len(answer_data)): #process each line in the answer_file
        cur_ans_line = answer_data[i].rstrip().lower()
        cur_a_wd_tag_prs = cur_ans_line.split(' ')
        cur_eval_line = eval_data[i].rstrip().lower()
        cur_e_wd_tag_prs = cur_eval_line.split(' ')
        a_wd_ctr += len(cur_a_wd_tag_prs) # this gives us actual word count
        for j in range(len(cur_a_wd_tag_prs)):
            a_wd_tag_seq = cur_a_wd_tag_prs[j].split('_#_')
            e_wd_tag_seq = cur_e_wd_tag_prs[j].split('_#_')
            if a_wd_tag_seq[0] == e_wd_tag_seq[0]:
                e_wd_ctr += 1
                if a_wd_tag_seq[1] == e_wd_tag_seq[1]:
                    tru_tag +=1
                else:
                    false_tag +=1
            else:
                print ("problem mismatch on the word string")
    current_result = [a_wd_ctr, tru_tag, false_tag, (float(tru_tag)/float(a_wd_ctr)*100)]
    return current_result

        
# main
# Trying to improve this lab so that it's menu-driven and provides flexibility. Using
# example from Dawson book, "high_scores.py" for menu setup with some minor changes. 

sel_num = ''

while sel_num != 0:
    print(
    """
    Ling 165 Lab 2: POS tagging using first-order HMM
   ---------------------------------------------------------------
    This script executes the training, tagging, and evaluating
    processes for selected datasets, or for all five as a batch.
    Results are printed at the end.
    0 - Exit
    1-5 Process any single training/testing/answer dataset 
    6 - Process all five datasets
    9 - Print report
    --------------------------------------------------------------
    """
    )
    sel_num = raw_input("Choice:  ")
    
    if sel_num.isdigit():
        sel_num = int(sel_num)
        valid_num = [1, 2, 3, 4, 5]
        # exit
        if sel_num == 0:
            print("Good-bye.")

        elif sel_num in valid_num:
            num = sel_num
            a, b = do_training(num)
            out_file = do_tagging(num, a, b)
            result = do_evaluate(num)

            if os.path.exists ('lab2_report'):   # if we already have pickled/stored results data, let's load it 
                rpt_handle = open('lab2_report', 'r')
                report_data = pickle.load(rpt_handle)
                rpt_handle.close()
            else:
                report_data = {}
            report_data[num] = result
            # add result to report dictionary
            # pickle and save dictionary
            rpt_handle = open('lab2_report', 'w')
            pickle.dump(report_data, rpt_handle)
            rpt_handle.close()
            print_report(report_data)

        elif sel_num == 6:
            print("Batch processing of all training, tagging datasets...")
            report_data = {}
            for num in range(1, 6):
                a, b = do_training(num)
                out_file = do_tagging(num, a, b)
                result = do_evaluate(num)
                print("Current result:")
                print result
                # add result to report dictionary
                report_data[num] = result
                # pickle and save dictionary
            rpt_handle = open('lab2_report', 'w')
            pickle.dump(report_data, rpt_handle)
            rpt_handle.close()
            print_report(report_data)

        elif sel_num == 9:
            if os.path.exists ('lab2_report'):   # if we already have pickled/stored results data, let's load it 
                rpt_handle = open('lab2_report', 'r')
                report_data = pickle.load(rpt_handle)
                rpt_handle.close()
                print_report(report_data)
            else:
                print("No data in report.")
                print("Please enter a testset number (1 - 5), or select 6 for batch processing.")        
    else:
        print("Please enter a valid menu selection.")

