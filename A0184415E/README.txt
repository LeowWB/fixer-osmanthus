things to note:

things to try.
	try padding front and back and not padding, see which is better. is not too hard. can justify it easily too. 
	remove punct
	all one case
	digits to 1

	also talka bout ur add1 to observed things in the test query 



code is minally commented cuz of functions and var names.






This is the README file for A0184415E's submission

== Python Version ==

I'm using Python Version 3.8.10 for
this assignment.

== General Notes about this assignment ==

This program performs all the requirements of the assignment problem statement. More specifically, it constructs 4-grams from the itraining input text, and uses the 4-grams to predict the language of the test input.  

As some parts of the problem statement are open to interpretation or experimentation, these will be elaborated on below.

**The 4-gram units are characters**. Every 4-gram consists not of 4 tokens or 4 words, as per normal usage, but instead they consist of 4 characters which occur consecutively within the string. They are also treated using regular, **absolute probabilities**, and not conditional probabilities as per normal 4-gram usage. Because we are not considering context, this means that we will be multiplying very small probabilities. To ensure that we do not have computational rounding errors, we substitute probability multiplication with **log probability summing*, which gives an equivalent effect. Since the log function is an increasing function, we can still take the maximum to find out the most likely label - the string will hence be classified as the language with the highest log probability. There is one exception: when classifying a string as "other" language, we do not use probabilities. Instead we simply observe the set of all 4-grams within the string. **If more than half of the 4-grams in the string are not in our vocabulary, then we assume it to be "other" language**.
 
The main functions of the program `build_LM` and `test_LM` also have a few possible options which are passed by arguments. To avoid changing the function signature, these have default values that will be used if no argument is provided; if an argument is provided, these values can be overridden. The default values were chosen to maximize the model's performance. These are the options:

* `pad` (default: True): determines whether the input strings are padded with characters at the start and end of the string. For our usage we use '@' as a character to represent the start and '^' to represent the end of a string. We choose to use these characters because they only occur in email addresses, mathematical equations, and kaomojis, and not in natural language. The intuition behind this option is that the model will be able to learn which characters are more likely to occur at the start and end of a sentence, which may be useful for prediction. 
* `homogenize_digits` (default: True): if True, all numeric sequences (e.g. '12345') will be replaced by '1'. This is because, intuitively, the distribution of numeric sequences is the same regardless of language. As such we remove one variable which the model does not need to consider.
* `no_punc` (default: False): determines whether punctuation characters are removed. The intuition is that punctuation does not convey much semantic meaning in natural language. 
* `lowercase` (default: True): determines whether all characters are converted to lowercase. The intuition is that a Tamil string is still a Tamil string regardless of the letter casing, and the same is true for the other languages. As such changing all characters to lowercase allows the model to use less space, since it does not need to store uppercase characters.
* `smooth_unseen` (default: False): if True, add-one smoothing will be applied to 4-grams which are not in the vocabulary, as long as they appear in the test string. 

The above default options were chosen after some testing. These options were shown to have perfect performance (100%) on both the test set and training set. 

== Files included with this submission ==

* `README.txt`: this file
* `build_test_LM.py`: file from which the code is run
* `build_test_LM_funcs.py`: actual code to build and test models
* `combination_tester.py`: utility code for testing models with different combinations of options
* `eval.py`: evaluation code

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] I, A0000000X, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

I suggest that I should be graded as follows:

Graded for all parts, because I did all parts

== References ==

-nil-
