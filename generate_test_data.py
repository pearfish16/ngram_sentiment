# This file loads data from ./data/rawtext and outputs data to ./data/custom_sentiment
# The result data can be used directly by dan_sentiment.py

from os.path import join
import cPickle, time, argparse
from helper import sanitize_line, filter_with_alphabet, remove_nonascii, tokenize
from utils import default_gram_length, default_token_weight, default_repeat, default_alphabet # Each sentence should be repeated this many times in tokenizing
gram_length = default_gram_length
token_weight = default_token_weight
alphabet = default_alphabet
repeat = default_repeat
dim = 100

parser = argparse.ArgumentParser(description='Generate Test Data')
parser.add_argument('-input', help='input location of dataset', default='./data/rawtext/')
parser.add_argument('-output', help='output location of dataset', default='./data/custom_sentiment')
parser.add_argument('-vectors', help='location of embedding vectors', default='./vectors/fixed_vectors.txt')
parser.add_argument('-gramcnt', help='location of gram_counts', default='./vectors/gram_count.txt')
args = vars(parser.parse_args())

# load vectors 
gram_label = {}
label_gram = {}
counter = 0
embedding = [[] for i in range(dim)] # The embedding is d * V matrix
with open(args["vectors"], "r") as F:
	for line in F:
		vector = line.split(" ")
		gram_string = vector[0] # gram string is in the form "the-united-states"
		gram_string = " ".join(gram_string.split("_"))
		vector = vector[1:]
		for i in range(dim):
			embedding[i].append(vector[i])
		label_gram[counter] = gram_string
		gram_label[gram_string] = counter
		counter += 1
counter -= 1
print "Finish Loading Vectors."

# load gram_counts
gram_count = {}
with open(args["gramcnt"], "r") as F:
	for line in F:
		gram_string, count = line.split(",")
		count = int(count)
		if gram_string in gram_label: gram_count[gram_string] = count
print "Finish Loading Gram Counts."

# dump word_embeddings
cPickle.dump(embedding, open(join(args["output"], "sentiment_custom_We"), 'wb'))

for file_name in ['train-rootfine', 'dev-rootfine', 'test-rootfine']:
	output = []
	with open(join(args["input"], file_name), "r") as F:
		for line in F:
			vector = line.split(" ")
			label = vector[0]
			sentence = sanitize_line(filter_with_alphabet(" ".join(vector[1:]), alphabet))
			for i in range(repeat):
				tokenized_sentence = tokenize(gram_count, sentence, gram_length, token_weight)
				for j in range(len(tokenized_sentence)):
					tokenized_sentence[j] = gram_label.get(tokenized_sentence[j], 0) # 0 is the, not meaningful
				output.append([tokenized_sentence, label])
	cPickle.dump(output, open(join(args["output"], file_name), 'wb'))
	print "Finish Dumping File " + file_name