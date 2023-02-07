#!/usr/bin/python3
import re
import nltk
import sys
import getopt
import os
import bisect
import pickle
from collections import Counter

def usage():
    print("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")

def build_index(in_dir, out_dict, out_postings):
    """
    build index from documents stored in the input directory,
    then output the dictionary file and postings file
    """
    print('indexing...')
    # This is an empty method
    # Pls implement your code in below
    # nltk.download()
    path = "./nltk_data/corpora/reuters/first"

    # Should this be a list?
    inv_ind = {}
    with os.scandir(path) as it:
        # TODO: Optimize with BSBI or SPIMI
        # TODO: remove numbers
        for entry in it:
            file = open(entry, 'r')
            file_name = int(entry.name)
            lines = file.readlines()
            for line in lines:
                for word in line.split():   # https://stackoverflow.com/questions/21023901/how-to-split-at-all-special-characters-with-re-split
                    word = word.strip(" .,+:").lower()
                    if word not in inv_ind:
                        inv_ind[word] = []
                    bisect.insort(inv_ind[word], file_name)
    term_doc_freq = []
    for k in sorted(inv_ind.keys()):
        term_doc_freq.append((k, len(set(inv_ind[k]))))

    postings_lists = {}
    for k in inv_ind:
        postings_lists[k] = sorted(set(inv_ind[k]))

    with open("dictionary-file", "wb") as handle:
        pickle.dump(term_doc_freq, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open("postings-file", "wb") as handle:
        pickle.dump(postings_lists, handle, protocol=pickle.HIGHEST_PROTOCOL)


input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i': # input directory
        input_directory = a
    elif o == '-d': # dictionary file
        output_file_dictionary = a
    elif o == '-p': # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"

if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

build_index(input_directory, output_file_dictionary, output_file_postings)
