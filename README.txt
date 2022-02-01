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

This program performs all the requirements of the assignment problem statement. More specifically, it constructs 4-grams from the itraining input text, and uses the 4-grams to predict the language of the test input. As some parts of the problem statement are open to interpretation or experimentation, these will be elaborated on below.

**The 4-gram units are characters**. Every 4-gram consists not of 4 tokens or 4 words, as per normal usage, but instead they consist of 4 characters. They are also treated using regular, **absolute probabilities**, and not conditional probabilities as per normal 4-gram usage. Because we are not considering context, this means that we will be multiplying very small probabilities. To ensure that we do not have computational rounding errors, we substitute probability multiplication with **log probability summing*, which gives an equivalent effect. Since the log function is an increasing function, we can still take the maximum to find out the most likely label. 
The main functions of the program `build_LM` and `test_LM` also have a few possible options which are passed by arguments. To avoid changing the function signature, these have default values that will be used if no argument is provided; if an argument is provided, these values can be overridden. The default values were chosen to maximize the model's performance. These are the options:

* `pad` (default: `True`): determines whether the strings are padded with 


they were tested on train and test set and uh reuslts/  

Give an overview of your program, describe the important algorithms/steps 
in your program, and discuss your experiments in general.  A few paragraphs 
are usually sufficient. talk about log probs too.

== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

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
