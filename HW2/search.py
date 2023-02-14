#!/usr/bin/python3
import re
import nltk
import sys
import getopt
import pickle

def usage():
    print("usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")

def shunting_yard(tokens):
        output = []
        operators = []
        for token in tokens:
            if token == '(':
                operators.append(token)
            elif token == ')':
                while operators[-1] != '(':
                    output.append(operators.pop())
                operators.pop()
            elif token == 'AND':
                while operators and operators[-1] == 'NOT':
                    output.append(operators.pop())
                operators.append(token)
            elif token == 'OR':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                operators.append(token)
            elif token == 'NOT':
                operators.append(token)
            else:
                output.append(token)
        while operators:
            output.append(operators.pop())
        return output

"""
    Function to evaluate the boolean expression in inverse polish notation, using the postings list, find the documents that satisfy the query
"""

def evaluate(shunting_yard_list, postings_list):

    seen = set()
    for i in postings_list:
        for j in postings_list[i]:
            if j not in seen:
                seen.add(j)

    stack = []
    for token in shunting_yard_list:
        if token == 'AND':
            a = stack.pop()
            b = stack.pop()
            # intersection of a and b
            stack.append([x for x in a if x in b])
        elif token == 'OR':
            a = stack.pop()
            b = stack.pop()
            # union of a and b
            stack.append(a + b)
        elif token == 'NOT':
            a = stack.pop()
            # invert a
            stack.append([x for x in seen if x not in a])
        else:
            stack.append(postings_list[token])
    return stack.pop()

def run_search(dict_file, postings_file, queries_file, results_file):
    """
    using the given dictionary file and postings file,
    perform searching on the given queries file and output the results to a file
    """
    print('running search on the queries...')
    
    postings = pickle.load(open(postings_file, "rb"))
    queries = open(queries_file, "r")
    for query in queries.readlines():
        tokens = query.split()
        print(evaluate(shunting_yard(tokens), postings))




dictionary_file = postings_file = file_of_queries = output_file_of_results = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file  = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None :
    usage()
    sys.exit(2)

run_search(dictionary_file, postings_file, file_of_queries, file_of_output)
