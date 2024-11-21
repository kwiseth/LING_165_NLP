# Ling 165 Lab 1 kwiseth (updated 2024)
# Used OpenDevin to modify sgt.py (20-June-2024)
# Original code provided by Hahn Koo (2013)
# This documented version generated by PaLM API (DeepLearningAI short-course)


def get_mle (bigram, train_dict, train_tokens_ct, test_tokens_ct):

    """
    Calculates the expected frequency of a bigram using the Maximum Likelihood Estimate (MLE)

    Args:
        bigram (str): The bigram to be evaluated.
        train_dict (dict): A dictionary of bigrams and their frequencies.
        train_tokens_ct (int): The total number of tokens in the training data.
        test_tokens_ct (int): The total number of tokens in the test data.

    Returns:
        float: The expected frequency of the bigram.
    """

    if bigram in train_dict:
        train_ct = train_dict[bigram]
        mle_prob = float(train_ct)/float(train_tokens_ct)
        exp_f_mle = float(mle_prob) * float(test_tokens_ct)
    else:
        exp_f_mle = 0
    return exp_f_mle

def get_one (bigram, train_dict, vocab, test_tokens_ct):

    """
    Calculates the expected frequency of a bigram using the One Probability Estimate (1-prob).

    Args:
        bigram (str): The bigram to be evaluated.
        train_dict (dict): A dictionary of bigrams and their frequencies.
        vocab (list): A list of all unique words in the training data.
        test_tokens_ct (int): The total number of tokens in the test data.

    Returns:
        float: The expected frequency of the bigram.
    """

    if bigram in train_dict:
        train_ct = train_dict[bigram]
    else:
        train_ct = 0
    one_prob = float(train_ct + 1)/float(len(train_dict) + len(vocab)**2)
    exp_f_one = float(one_prob) * float(test_tokens_ct)
    return exp_f_one

def get_sgt (bigram, train_dict, train_tokens_ct, train_hapax, vocab, adj_freq_dict, test_tokens_ct):

    """
    Calculates the expected frequency of a bigram using the Smoothed Good-Turing (SGT) estimate.

    Args:
        bigram (str): The bigram to be evaluated.
        train_dict (dict): A dictionary of bigrams and their frequencies.
        train_tokens_ct (int): The total number of tokens in the training data.
        train_hapax (int): The number of hapax legomena in the training data.
        vocab (list): A list of all unique words in the training data.
        adj_freq_dict (dict): A dictionary of adjusted frequencies for each bigram.
        test_tokens_ct (int): The total number of tokens in the test data.

    Returns:
        float: The expected frequency of the bigram.
    """

    poss_bgm_B = len(vocab)**2

    if bigram in train_dict:
        sgt_prob = adj_freq_dict[bigram]/train_tokens_ct
    else:
        sgt_prob = train_hapax/(poss_bgm_B-len(train_dict))*train_tokens_ct

    exp_f_sgt = sgt_prob * test_tokens_ct
    return exp_f_sgt