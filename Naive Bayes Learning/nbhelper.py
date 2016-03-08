import glob
import math
from nbsuffixstrip import suffix_strip

# Definition for a new word into a list
def new_word(word_list, cl, word):
    word_list[word] = {cl[0]: 0, cl[1]: 0, cl[2]: 0, cl[3]: 0}
    return word_list


# Calculating the occurrences of the word
def calculate_value(word_list, w, cl):
    word_list[w][cl] += 1
    return word_list


# Calculating the total word in the entire document
def calculate_total_words_in_class(word_list, cl):
    total_count_in_class = 0
    for word in word_list:
        total_count_in_class += word_list[word][cl]
    return total_count_in_class


# Smoothing the words if a class with a occurrence of a word is 0 then smooth the class
def smoothing_the_words(word_list, list_of_classes):
    found = False
    for word in word_list:
        for cl in list_of_classes:
            if word_list[word][cl] == 0:
                found = True
                break
        if found:
            break
    for word in word_list:
        for cl in list_of_classes:
            word_list[word][cl] += 1
    return word_list


# Building the list with the total of words for a class and document
def build_count_values(word_list, cl, c1, c2, c3, c4):
    total = c1 + c2 + c3 + c4
    word_list['words_in_document'] = {cl[0]: c1, cl[1]: c2, cl[2]: c3, cl[3]: c4, 'total': total}
    return word_list


# Building the list of words for a feature
def build_class_features(word_list, cl, list_of_classes, word):
    if word not in word_list:
        new_word(word_list, list_of_classes, word)
    word_list[word][cl] += 1
    return word_list


# Read the file given a file name
def read_file(file_name):
    word_split = []
    with open(file_name, "r") as file:
        data = file.read()
        while data:
            word_split = data.split()
            data = file.read()
    return word_split


# Write the learned model into a file
def write_model(model):
    with open("nbmodel.txt", "w") as file:
        file.write(str(model))


# Build a class feature from the given folder
def build_class_from_file(directory, cl, list_of_classes, word_list):
    for file_name in glob.glob(directory):
        words = read_file(file_name)
        for w in words:
            w = suffix_strip(w)
            build_class_features(word_list, cl, list_of_classes, w)
    return word_list


#################################################################################################


# Get a probability for a particular class
def get_probability_for_class(model, word_list, cl):
    count_for_class = 1
    for word in word_list:
        if word in model['data']:
            count_for_class += math.log(model['data'][word][cl]/model['words_in_document'][cl])
    return count_for_class


# Get the prior for a particular class
def get_prior_for_class(model, cl):
    document_data = model['words_in_document']
    prior_for_class = (document_data[cl] / document_data['total'])
    return prior_for_class


# Get the max probability in case of 4 way
def max_of_probability(pt, pd, nt, nd):
    data = "truthful positive"
    maximum = pt
    if maximum < pd:
        maximum = pd
        data = "deceptive positive"
    if maximum < nt:
        maximum = nt
        data = "truthful negative"
    if maximum < nd:
        data = "deceptive negative"
    return data


# Get the max of positive or negative in case of 2 way
def max_of_positive_or_negative(p, n):
    if p >= n:
        return 'positive'
    else:
        return 'negative'


# Get the max of truthful or deceptive in case of 2 way
def max_of_truthful_or_deceptive(t, d):
    if t >= d:
        return 'truthful'
    else:
        return 'deceptive'


# Define the probability of the each class
def probability(model, words, cl):
    prior = get_prior_for_class(model, cl)
    p = get_probability_for_class(model, words, cl)
    probability_of_word = prior * p
    return probability_of_word


# Write the output file
def write_to_file(list):
    with open("nboutput.txt", "w") as f:
        for k in list:
            f.write(k + "\n")


# Read the model
def read_model():
    with open('nbmodel.txt', "r") as f:
        data = f.read()
    return data
