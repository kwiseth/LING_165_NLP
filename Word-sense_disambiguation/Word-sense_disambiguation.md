### Word sense disambiguation

Use the naive Bayes ("bag-of-words") model to classify the use of the word 'drug' in various sentence as meaning 'medical' (1) or 'illegal' (0).
Naive Bayes [todo add brief definition]

0 | 1
--|--
illegal | medical

The bag-of-words model relies on a simplifying assumption. It disregards word order when counting frequencies. 


The script processes the training data and uses the results to classify the test data. The results of the classification are compared to the actual data. The output is shown in the following screenshot:

![screenshot-of-output](http://alameda-tech-lab.com/ling/spr2013/lab3_screenshot.png)
