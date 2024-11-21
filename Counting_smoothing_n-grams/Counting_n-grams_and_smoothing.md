### Compare bigram frequency counts using three different smoothing algorithms

Using the provided training data and test data, write Python scripts to estimate expected frequencies based on observed frequencies in the training data using three different approaches:
1. Maximum likelihood estimate
2. Add-one smoothing
3. Good-Turning smoothing

Compare the results of the three different approaches. Output the results in a tabular list.

The Python scripts accomplish this as follows:

1. train.py Opens the training data file and creates a dictionary of bigrams and their frequencies. (Uses the imported "bigram.py" script to identify bigrams and count frequencies.)
2. bigram.py Contains the functions needed to identify the bigrams.
3. guess.py Uses the frequency counts that result from train.py to estimate expected bigram frequencies using the three different smoothing algorithms.
4. probs.py This script includes calls to the smoothing functions provided by Hahn Koo (get_mle, get_one, get_sgt).
