#!/usr/bin/python3
import math
import sys
import getopt
import os
import pickle
# nltk.download('punkt')
# nltk.download('stopwords')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


def usage():
    print("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")


ELEMENT_SIZE = 6

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
    # path = "./nltk_data/corpora/reuters/" + in_dir

    dictionary = {}
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    postings_lists = {}

    try:
        with os.scandir(path) as it:
            for entry in it:
                file = open(entry, 'r')
                file_name = int(entry.name)
                lines = file.readlines()
                for line in lines:
                    tokens = [word_tokenize(t) for t in sent_tokenize(line)]
                    if len(tokens) != 0:
                        for t in tokens[0]:
                            stemmed = stemmer.stem(t).lower()
                            if stemmed in dictionary and stemmed not in stop_words:
                                postings_lists[stemmed].append(file_name)
                            elif stemmed not in dictionary and stemmed not in stop_words:
                                dictionary[stemmed] = 0
                                postings_lists[stemmed] = [file_name]

    except IOError:
        print("No such file in path:", path)

    term_doc_freq = []
    for k in sorted(postings_lists.keys()):
        term_doc_freq.append((k, sorted(list(set([t for t in postings_lists[k]])))))
    print(term_doc_freq)

    # {word: offset}
    file_offset = {}

    for k in postings_lists:
        postings_lists[k] = sorted(set(postings_lists[k]))

    postings_output = []

    #  12345 11556 89292 29387
    for k in postings_lists:
        # 1 2 3 4 5
        posting_str = ""
        postings = postings_lists[k]

        for i in postings:
            str_i = str(i)
            while len(str_i) < ELEMENT_SIZE:
                str_i = " " + str_i
            posting_str += str_i + " "


        steps = math.floor(math.sqrt(len(postings)))
        counter = 0

        posting_str = posting_str.rstrip() + "\n"
        print(posting_str)
        postings_output.append(posting_str)

        """
        if len(postings) > 3:
            temp = (k, [i for i in range(0, len(postings), math.floor(math.sqrt(len(postings))))])
            key = temp[0]
            pointers = temp[1]
            print("temp", temp)

            for i in range(len(pointers) - 1):
                tup = (postings_lists[key][0][0], pointers[i + 1])
                postings_lists[key][pointers[i]] = tup
        else:
            continue
        """

    # print(postings_output)
    row_dict = {}
    postings_file = open("postings.txt", "w+")
    c = 0
    for p in postings_lists:
        c += 1

    for key in enumerate(postings_lists.keys()):
        row_dict[key] = i
        postings_file.writelines(postings_lists[key])

    print(term_doc_freq)
    with open(out_dict, "wb") as handle:
        pickle.dump(term_doc_freq, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open(out_postings, "wb") as handle:
        pickle.dump(postings_lists, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print("indexing done...")


input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i':  # input directory
        input_directory = a
    elif o == '-d':  # dictionary file
        output_file_dictionary = a
    elif o == '-p':  # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"

if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

build_index(input_directory, output_file_dictionary, output_file_postings)
