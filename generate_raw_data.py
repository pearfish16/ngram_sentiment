# This file loads data from ./data/sentiment and outputs data to ./data/rawtext

import cPickle, time, argparse

parser = argparse.ArgumentParser(description='Generate raw data')
parser.add_argument('-input', help='input location of dataset', default='./data/custom_sentiment/')
parser.add_argument('-output', help='output location of dataset', default='./data/custom_rawtext/')
parser.add_argument('-vocab', help='location of vocab', default='./data/sentiment/wordMapAll.bin')
args = vars(parser.parse_args())

# load data
vocab = cPickle.load(open(args['vocab'], 'rb'))
int_to_word = {}
for key in vocab:
	int_to_word[vocab[key]] = key

for file_name in ['train-rootfine', 'dev-rootfine', 'test-rootfine']:
	dataset = cPickle.load(open(args['input'] + file_name, 'rb'))
	with open(args['output'] + file_name, 'w') as F:
		for sent, label in dataset:
			#for i in range(len(sent)):
			#	sent[i] = int_to_word[sent[i]] 
			for i in range(len(sent)):
				sent[i] = str(sent[i])
			F.write(str(label) + ' ' + (' '.join(sent)) + '\n')
