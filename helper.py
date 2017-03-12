import sys
import random
import json
import re
import numpy as np

#	remove non-ascii text in a string
def remove_nonascii(text):
	return str(''.join([i if ord(i) < 128 else "" for i in text]))

#	kepp characters in a string iff it's in the alphabet
#	For training
def filter_with_alphabet(text, alphabet):
	return ''.join(c for c in text if c in alphabet)

#	sanitizes a line read from raw sources
#	For general purposes
def sanitize_line(line):
	return remove_nonascii(" ".join(line.split())).lower()
	
#	core function that will return the parsed sentence as a list of grams
def tokenize(Dict, sentence, gram_length, token_weight):
	try:
		text = sentence.split(" ") # string
	except:
		text = sentence # list
	if text[0] == "":
		text = text[1:]
	result = []
	N = len(text)
	# randomized algorithm, up to change
	it = 0
	while (it < N):
		mass = np.zeros(gram_length)
		for i in range(1, gram_length + 1):
			if (it + i <= N):
				gram = " ".join(text[it:it + i])
				if not gram in Dict: continue
				mass[i - 1] = Dict.get(gram) * token_weight[i] * 1.0
		mass /= sum(mass)
		tmp_len = np.random.choice(gram_length, p = mass) + 1# gram length for this time
		result.append(" ".join(text[it:it + tmp_len]))
		it += tmp_len
	return result
