Open pattern_matching.py.
At the bottom of the file, there is a call to the function "main."
The parameter "length" is most likely the only parameter that you need to set.
This parameter determines how many questions to generate.
For example, a length of 5 will generate 5 questions (this is the default configuration).
A definition of terms/parameters can be found below, and can also be found in pattern_matching.py.

length: the number of problems to generate
sequence item: a 3-tuple of the form (index, color, shape)
input sequence: a list of sequence items describing objects on the left side of the image
output sequence: a list of sequence items describing objects on the right side of the image
text passage sequence: a list of sequence items describing objects in the text passage entry of the json file
answer sequence: a list of sequence items describing objects in the answer entry of the json file; the correct answer to the generated problem
io_sequences: the input and output sequences; these must be the same length for a given problem
ta_sequences: the text passage and answer sequences; these must be the same length for a given problem
answer choice length: the number of answer choices to be generated for a problem