#!/usr/bin/python3/get_words_utf8_clean_less_function.py


def get_words_utf8_clean_less(some_line):
    """ Function that accepts a line from the New Yorker article (processed using Hahn's clean.py script) and replaces the UTF-8 codepoints with ASCII chars.
    After re-doing some portions of lab 3, I see that some basic string functions are better than regex for punctuation items, so this
    is a simpler version of the get_words_utf8_clean function above. This function doesn't make any copyedit changes. """
    cleaned_word_list = []
    # Replacing some utf-8 codepoints with ascii. 
    nuline = some_line.replace('\xe2\x80\x99', '\'') # right-single quote -> single quote
    nuline = nuline.replace('\xe2\x80\x94', ' -- ') # em-dash -> hyphens and spacebands
    nuline = nuline.replace('\xe2\x80\x93', ' -- ') # en-dash -> hyphens and spacebands
    nuline = nuline.replace('\xe2\x80\x90', '-') # hyphen -> hyphen
    nuline = nuline.replace('\xe2\x80\x98', '\'') # right-single-quote -> right-single-quote
    nuline = nuline.replace('\xe2\x80\x9c', '"') # double-quote -> right-double quote
    nuline = nuline.replace('\xe2\x80\x9d', '"') # quote -> quote
    dash_patt = re.compile('(--)')
    nuline = dash_patt.sub('', nuline)
    prelim_word_list = nuline.strip().split()   
    for i in range(0, len(prelim_word_list)): # Remove any leading and closing punctuation from each word in the sentence
        word = prelim_word_list[i].strip("()-~\"\':;).?!")
        cleaned_word_list.append(word)
    word_list = [w for w in cleaned_word_list if w.lower() not in sw]  # without stopwords
    words = [w for w in word_list if w.isalpha()]      # without numbers and dates eg, 2004, 1.5 etc.
    return words
