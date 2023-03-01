This is the README file for A0268807N's and A0269064X submission
Email(s): e1103307@u.nus.edu and e1109901@u.nus.edu

== Python Version ==

I'm (We're) using Python Version 3.9.5 for this assignment.

== General Notes about this assignment ==

Give an overview of your program, describe the important algorithms/steps 
in your program, and discuss your experiments in general.  A few paragraphs 
are usually sufficient.

The program consists of two main steps, constructing the index file and using it to search.

INDEX:
Firstly, the program iterates over every file in the input file directory. For each file it reads every line and
tokenizes them. The tokens are stemmed with PorterStemmer nltk.stem.porter. The stemmed words are used as keys for a
dict containing lists of the documents where the word appears.
Format: {key: [doc1,doc2,doc3]}

We then construct a dict with the words/tokens as keys, as well as the document frequency and the offset
in the postings file. This makes the dictionary output file, which we save using pickle.
Format: {key: [doc freq, offset]}

The first dict is used to create the output file postings.txt and to calculate the offset and document frequency
for the second dict. The postings.txt file consis'ts only of document ID's and the occasional @-sign indic'ating a
skip pointer. The ID's and skip pointers are all padded with whitespaces making them 6 characters long, for easier
indexing. While building the postings output we keep track of the offset for each key, and save the offset in
the second dict.

postings.txt is saved as a plain text file, where each row corresponds to a specific key.
Format: "    45    @6    70........"
The dictionary file keeps track of the offset for each key.


SEARCH:
The first in searching is to parse the query. This is done using the shunting yard algorithm, which changes the
query to reverse polish/postfix notation. With this notation we can easily parse and evaluate the query with
different logic for AND, OR and NOT operations. AND is the most complicated, since it makes use of skip pointers to
optimize merging.

For example the query: "time AND stock" becomes "time stock AND"

Evaluation is done by taking the rightmost operation and two (or one for NOT operations) tokens and performing
intersection, union or inverting for AND, OR and NOT respectively.

OR simply merges the two lists. This is done by iterating over both lists and inserting every new value in increasing
order.

NOT inverts the list and returns every element NOT in the oringial list.

When performing the AND operation, we iterate over both lists and only insert elements to the output if we encounter
a value that is present in both lists. If the value from list a is smaller than the value in list b, we increase the
pointer in list a, and vice versa. If we encounter a skip pointer, we jump ahead to see if it is worth skipping or not,
if it is we increase the pointer with the amount specified by the pointer, otherwise we simply increase by normal amount.
This returns the intersection of the two lists.

When the entire expression has been evaluated we output the result sorted set of documents to one line in the output file.


== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

index.py
This constructs the index, consisting of the postings.txt and dictionary.txt files.

seach.py
Uses the index from index.py to evaluate a query expression and outputs the resulting set of documents to
output-file-of-results.


== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] I/We, A0268807N and A0269064X, certify that I/we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I/we
expressly vow that I/we have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I/We, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

We suggest that we should be graded as follows:

<Please fill in>

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>

Used for implementing the shunting yard algorithm in search.py to parse boolean expression
https://en.wikipedia.org/wiki/Shunting_yard_algorithm