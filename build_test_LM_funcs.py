#!/usr/bin/python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import nltk
from math import log

COUNT_KEY = '_count' # for dictionaries
PAD_CHAR = '@' # we use this character to pad the start and end of each string
OTHER_STRING = 'other' # classify as other
OTHER_THRESHOLD = 0.5 # threshold for classifying as other
EPSILON = 0.00001 # avoid division by 0

DEFAULT_PAD = True
DEFAULT_HOMOGENIZE_DIGITS = True
DEFAULT_NO_PUNC = False
DEFAULT_LOWERCASE = True
DEFAULT_SMOOTH_UNSEEN = False

def build_LM(in_file, pad=DEFAULT_PAD, homogenize_digits=DEFAULT_HOMOGENIZE_DIGITS, no_punc=DEFAULT_NO_PUNC, lowercase=DEFAULT_LOWERCASE):
    """
    build language models for each label
    each line in in_file contains a label and a string separated by a space
    """
    print("building language models...")
    lines = read_lines(in_file)
    train_set = input_lines_to_train_set(lines, pad, homogenize_digits, no_punc, lowercase)
    model = build_model(train_set)
    return model

def build_model(train_set):
    """
    builds the model from a training set
    """
    model = dict()
    vocab = set()
    
    # this loop will build the initial table and smooth the observed entries
    for datum in train_set:
        label, features = datum
        four_grams = line_to_4grams(features)
        for four_gram in four_grams:
            vocab.add(four_gram)
            model[label] = model.get(label, dict())
            model[label][four_gram] = model[label].get(four_gram, 1) + 1 # default value of 1 due to add-1 smoothing.
    
    # this loop does smoothing for 4grams in the vocabulary that were not observed in each language
    for four_gram in vocab:
        for label in model.keys():
            if not (four_gram in model[label].keys()):
                model[label][four_gram] = 1 # default value of 1 due to add-1 smoothing

    # this loop counts the number of occurrences for each language in total
    for label in model.keys():
        total = 0
        for four_gram in model[label].keys():
            total += model[label][four_gram]
        model[label][COUNT_KEY] = total
    return model

def line_to_4grams(line):
    """
    converts a string to a list of 4-grams
    """
    four_grams = []
    for i in range(len(line)-3):
        four_grams.append(line[i:i+4])
    return four_grams

def input_lines_to_train_set(lines, pad, homogenize_digits, no_punc, lowercase):
    """
    converts the lines from the input training corpus into a training set with (label, features) pairs.
    """
    train_set = []
    for line in lines:
        label = line.split()[0]
        features = line[len(label)+1:]
        features = process_line(features, pad, homogenize_digits, no_punc, lowercase)
        train_set.append((label,features))
    return train_set

def process_line(line, pad, homogenize_digits, no_punc, lowercase):
    if no_punc:
        line = re.sub(r'[^\s\w]', '', line)
    if lowercase:
        line = line.lower()
    if homogenize_digits:
        line = re.sub(r'[\d]+', '1', line)
    line = line.strip()
    if pad:
         line = f'{PAD_CHAR}{PAD_CHAR}{PAD_CHAR}{line}{PAD_CHAR}{PAD_CHAR}{PAD_CHAR}'

    return line

def read_lines(in_file):
    """
    reads the lines from a file, removing whitespace including newline
    """
    with open(in_file, "r") as f:
        lines = f.readlines()
    print(f'{len(lines)} lines')
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    return lines

def test_LM(in_file, out_file, LM, pad=DEFAULT_PAD, homogenize_digits=DEFAULT_HOMOGENIZE_DIGITS, no_punc=DEFAULT_NO_PUNC, lowercase=DEFAULT_LOWERCASE, smooth_unseen=DEFAULT_SMOOTH_UNSEEN):
    """
    test the language models on new strings
    each line of in_file contains a string
    you should print the most probable label for each string into out_file
    """
    print("testing language models...")
    lines = read_lines(in_file)
    output_str = ''
    for i in range(len(lines)):
        line = process_line(lines[i], pad, homogenize_digits, no_punc, lowercase)
        if smooth_unseen:
            lang = classify_smooth_unseen(line, LM)
        else:
            lang = classify_ignore_unseen(line, LM)
        output_str += f'{lang} {lines[i]}\n'
    with open(out_file, "w") as f:
        f.write(output_str)

def classify_ignore_unseen(line, model):

    """
    classifies a given string according to a language model. ignore unseen 4grams.
    """
    four_grams = line_to_4grams(line)
    log_prob = dict() # multiplying probabilities can lead to very small numbers, which are often not handled well by computers. so we sum up log probabilities instead. 
    unseen_4grams = set()
    for lang in model.keys():
        for four_gram in four_grams:
            if not (four_gram in model[lang].keys()):
                unseen_4grams.add(four_gram)

    # we assume it's some alien language if there are many 4grams that we haven't seen before
    if len(unseen_4grams) / (len(set(four_grams))+EPSILON) > OTHER_THRESHOLD:
        return OTHER_STRING

    for lang in model.keys():
        log_prob[lang] = 0
        count = model[lang][COUNT_KEY]
        for four_gram in four_grams:
            if four_gram in unseen_4grams:
                continue
            four_gram_count = model[lang][four_gram]
            log_prob[lang] += log(four_gram_count/(EPSILON+count))
    return max(log_prob, key=log_prob.get) # logarithm functions are increasing so we can still take the max

def classify_smooth_unseen(line, model):
    """
    classifies a given string according to a language model. applies add-1 smoothing even to 4grams that have not been seen before in the corpus.
    """
    four_grams = line_to_4grams(line)
    log_prob = dict() # multiplying probabilities can lead to very small numbers, which are often not handled well by computers. so we sum up log probabilities instead. 
    unseen_4grams = dict()
    unseen_4grams_set = set()
    for lang in model.keys():
        unseen_4grams[lang] = set()
        for four_gram in four_grams:
            if not (four_gram in model[lang].keys()):
                unseen_4grams[lang].add(four_gram)
                unseen_4grams_set.add(four_gram)

    # we assume it's some alien language if there are many 4grams that we haven't seen before
    if len(unseen_4grams_set) / (len(set(four_grams))+EPSILON) > OTHER_THRESHOLD:
        return OTHER_STRING
    
    for lang in model.keys():
        log_prob[lang] = 0
        count = model[lang][COUNT_KEY]
        for four_gram in four_grams:
            four_gram_count = model[lang].get(four_gram, 1) # default value of 1 due to add-1 smoothing
            log_prob[lang] += log(four_gram_count/(EPSILON+count+len(unseen_4grams[lang])))
    return max(log_prob, key=log_prob.get) # logarithm functions are increasing so we can still take the max
