# 

 # N-Gram Models - Question 1
 # ngram.py - February 9, 2015
 # Timothy Kim

 
 # See report for documentation and comments

##
import nltk
import random
import math
import os.path
from collections import Counter
from nltk import word_tokenize

def trainer(file, ngram):
	#creates a new text file with <s> and </s> inserted
	#into the beginning and end of every line(sentence)
	#creates vocab.txt with all unique tokens (word types)
	print "creating altered txt file..."
	newfile = open("traintemp.txt", "w+")
	vocab = open("trainvocab.txt", "w+")
	for line in file:
		temp = line[:-1] #strips newline character
		newfile.write("<s> " + temp + " </s>" + '\n')
	file.close()
	#reads newly created file and tokenizes by whitespace
	#vocabulary extracted to a list of unique word types
	print "extracting vocabulary..."
	newfile.seek(0)
	text = newfile.read()
	newfile.close()
	tokens = text.split()
	ctr = Counter(tokens)
	numvocab = len(set(tokens))
	udist = nltk.FreqDist(tokens)
	vocab.write("WORD TYPE : COUNT\n")
	for item in sorted(set(tokens)):
		vocab.write("{} : {}\n".format(item, udist[item]))
	vocab.close()
	print "creating ngram model and calculating frequency distribution..."
	nglist = createNgram(tokens, ngram)
	fdist = nltk.FreqDist(nglist)
	if ngram == 3:
		tdist = nltk.FreqDist(createNgram(tokens, 2))
	#starting with <s>, generates a random sentence of random length
	#without accounting for probability
	
	#randNextWord takes a word string as a parameter and uses that
	#to find a random ngram and recursively calls function again
	def randNextWord(fword):
		nwordlist = []
		sentence.append(fword)
		print ".",
		for sample in fdist:
			if sample[0] == fword:
				nwordlist.append(sample[1])
		randw = random.choice(nwordlist)
		if ngram == 3:
			randNext3Word(fword, randw)
		else:	
			if randw == "</s>":
				sentence.append(randw)
				print ""
			else:
				randNextWord(randw)
			
	def randNext3Word(fword,nword):
		nwordlist = []
		sentence.append(nword)
		print ".",
		for sample in fdist:
			if sample[0] == fword and sample[1] == nword:
				nwordlist.append(sample[2])
		randw = random.choice(nwordlist)
		if randw == "</s>":
			sentence.append(randw)
			print ""
		else:
			randNext3Word(nword,randw)
			
	if ngram != 0:
		sentfile = open("randomsentences"+str(ngram)+"gram.txt", "a+")
		probfile = open("sentenceprobs"+str(ngram)+"gram.txt", "a+")
		sentfile.write("SENTENCE\n : LOG PROBABILITY\n")
		if ngram == 2:
			probfile.write("(B,A) : P(A|B) : log probability(running total)\n")
		elif ngram == 3:
			probfile.write("(B,C,A) : P(A|B,C) : log probability(running total)\n")
		for i in range(0, 50):
			print "generating random sentence", i,
			sentence = []
			sentProb = 0.0
			randNextWord("<s>")
			sentfile.write(" ".join(map(str, sentence)))
			print "calculating probabilities..."
			if ngram == 2:
				for i in range(len(sentence)-1):
					probfile.write("({},{}) : ".format(sentence[i], sentence[i+1]))
					count = fdist[(sentence[i], sentence[i+1])]
					prob = float(count + 1) / (ctr[sentence[i]] + numvocab)
					probfile.write("{} : ".format(prob))
					prob = math.log(prob)
					sentProb = sentProb + prob
					probfile.write("{}\n".format(sentProb))
			elif ngram == 3:
				for i in range(len(sentence)-2):
					probfile.write("({},{},{}) : ".format(sentence[i], sentence[i+1], sentence[i+2]))
					count = fdist[(sentence[i], sentence[i+1], sentence[i+2])]
					prob = float(count + 1) / (tdist[sentence[i], sentence[i+1]] + numvocab)
					probfile.write("{} : ".format(prob))
					prob = math.log(prob)
					sentProb = sentProb + prob
					probfile.write("{}\n".format(sentProb))
			sentfile.write("\n : {}\n".format(sentProb))
			probfile.write("\n")
		sentfile.close()
		probfile.close()
	
		
	
def tester(file, ngram):
	#reads newly created file and tokenizes by whitespace
	#vocabulary extracted to a list of unique word types
	if os.path.isfile("traintemp.txt") ==  False:
		print "traintemp.txt not found, please run train first"
	else:
		print "creating altered txt file..."
		newfile = open("testtemp.txt", "w+")
		for line in file:
			temp = line[:-1] #strips newline character
			newfile.write("<s> " + temp + " </s>" + '\n')
		file.close()
		newfile.close()
		newfile = open("traintemp.txt", "r")
		text = newfile.read()
		newfile.close()
		tokens = text.split()
		ctr = Counter(tokens)
		numvocab = len(set(tokens))
		udist = nltk.FreqDist(tokens)
		print "retrieving ngram model and frequency distributions..."
		if ngram == 0:
			nglist = createNgram(tokens, 3)
		else :
			nglist = createNgram(tokens, ngram)
		fdist = nltk.FreqDist(nglist)
		if ngram == 3 or ngram == 0:
			tdist = nltk.FreqDist(createNgram(tokens, 2))	
		evalfile = open("evalsentences"+str(ngram)+"gram.txt", "a+")
		evalfile.write("SENTENCE\nDELETED: WORD\nHIGHEST: LIKELIHOOD | P(A|B): PROBABILITY\n\n")
		for i in range (0, 30):
			#get 1 random sentence from test text
			#prevent out of bounds for deletion
			if ngram == 2:
				print "evaluating sentence", i, "..."
				randomline = random.choice(open("testtemp.txt").readlines())
				randomline = randomline[:-1]
				sentence = randomline.split()
				randomI = random.randrange(1,len(sentence)-1)
			elif ngram == 3:
				print "evaluating sentence", i, "..."
				randomline = random.choice(open("testtemp.txt").readlines())
				randomline = randomline[:-1]
				sentence = randomline.split()
				randomI = random.randrange(2, len(sentence)-1)
			elif ngram == 0:
				print "computing perplexity of ngram models using test corpus..."
			if ngram != 0:
				delword = sentence[randomI]
				prevword = sentence[randomI-1]
				prevprev = sentence[randomI-2]
			likely = ""
			high = 0.0
			high2 = 0.0
			if ngram != 0:
				for sample in fdist:
					if ngram == 2:
						if sample[0] == prevword:
							tmp = fdist[sample[0],sample[1]]
							prob = float(tmp + 1) / (ctr[sample[0]] + numvocab)
							if prob > high:
								high = prob
								likely = sample[1]
					elif ngram == 3:
						if sample[0] == prevprev and sample[1] == prevword:
							tmp = fdist[sample[0], sample[1], sample[2]]
							prob = float(tmp + 1) / (tdist[sample[0], sample[1]] + numvocab)
							if prob > high:
								high = prob
								likely = sample[2]
				if high == 0.0 and likely == "":
					tmp = 0
					if ngram == 2:
						prob = float(tmp + 1) / (ctr[prevword] + numvocab)
					if ngram == 3:
						prob = float(tmp + 1) / (tdist[prevprev, prevword] + numvocab)
					high = prob
					likely = delword 
			if ngram == 0 and i == 0:
				for sample in tdist:
					tmp = tdist[sample[0],sample[1]]
					prob = float(tmp + 1) / (ctr[sample[0]] + numvocab)
					prob = math.log(prob)
					high = high + prob
				for sample in fdist:
					tmp = fdist[sample[0], sample[1], sample[2]]
					prob = float(tmp + 1) / (tdist[sample[0], sample[1]] + numvocab)
					prob = math.log(prob)
					high2 = high2 + prob
			if ngram == 2:
				evalfile.write("{}\nDELETED: {}\nLIKELY: {} | P(A|B): {}\n\n".format(randomline, delword, likely, high))
			elif ngram == 3:
				evalfile.write("{}\nDELETED: {}\nLIKELY: {} | P(A|B,C): {}\n\n".format(randomline, delword, likely, high))
			elif ngram == 0:
				numwords = len(tokens)
				high = math.pow(high, -1/numwords)
				high2 = math.pow(high2, -1/numwords)
				print "perplexity of bigram model:", high
				print "perplexity of trigram model:", high2
				return
				
				
def createNgram(tokenlist, n):
	return zip(*[tokenlist[i:] for i in range(n)])
	
	
#obtains command line arguments and runs function
if __name__=="__main__":
	from sys import argv
	if len(argv) != 4:
		print "Usage: ngram.py [train|test] [filename] [2|3]"
	else:
		fd = open(argv[2], "r")
		if argv[1] == "train":
			if argv[3] == "2":
				trainer(fd, 2)
			elif argv[3] == "3":
				trainer(fd, 3)
			else:
				print "Usage: ngram.py [train|test] [filename] [2|3]"
		elif argv[1] == "test":
			if argv[3] == "2":
				tester(fd, 2)
			elif argv[3] == "3":
				tester(fd, 3)
			elif argv[3] == "0":
				tester(fd, 0)
			else:
				print "Usage: ngram.py [train|test] [filename] [2|3]"
		else :
			print "Usage: ngram.py [train|test] [filename] [2|3]"


						
				
				
				