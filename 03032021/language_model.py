#!/usr/bin/env python3

import sys, getopt
import codecs;
from collections import Counter
from collections import defaultdict
import numpy as np
import random
from nltk.tokenize import sent_tokenize, word_tokenize

trigramFreqs = []
trigrams = []
bigramFreqs = []
bigrams = []
unigrams = []
unigramFreqs = []
word2index = []
index2word = []
unknowns = []

corpusFile = ''
testFile = ''

bigram2trigram = defaultdict(dict)
bigram2trigramProb = defaultdict(dict)
bigram2trigramRProb = defaultdict(dict)
bigram2trigramRCProb = defaultdict(dict)
bigram2trigramRSorted = defaultdict(dict)

vocabSize = 0
k = 0.01
skipUNK = True

def trigramProb(trigram):
	global trigramFreqs,bigramFreqs;
	return trigramFreqs[trigram]/bigramFreqs[(trigram[0],trigram[1])]

def trigramProbAddOneSmoothed(trigram):
	global trigramFreqs,bigramFreqs,vocabSize,k
	return (trigramFreqs[trigram] + k)/(bigramFreqs[(trigram[0],trigram[1])] + (k*vocabSize))

def trigramSentenceProb(words):
	global word2index
	return sum(np.log([trigramProbAddOneSmoothed( (word2index[words[i-2]], word2index[words[i-1]], word2index[words[i]]) ) for i in range(2,len(words))])) + \
	np.log(unigramProbAddOneSmoothed(word2index[words[0]])) + np.log(bigramProbAddOneSmoothed( (word2index[words[0]], word2index[words[1]])))
	
def bigramProb(bigram):
	global bigramFreqs,unigramFreqs
	return bigramFreqs[bigram]/unigramFreqs[bigram[0]]
	
def bigramProbAddOneSmoothed(bigram):
	global bigramFreqs,unigramFreqs,vocabSize,k
	return (bigramFreqs[bigram] + k)/(unigramFreqs[bigram[0]] + (k*vocabSize))

def bigramSentenceProb(words):
	global word2index
	return sum(np.log([bigramProbAddOneSmoothed( (word2index[words[i-1]], word2index[words[i]])) for i in range(1, len(words))])) + \
	np.log(unigramProbAddOneSmoothed(word2index[words[0]]));

def unigramProb(unigram): 
	global unigramFreqs
	return unigramFreqs[unigram]/sum(unigramFreqs.values())

def unigramProbAddOneSmoothed(unigram): 
	global unigramFreqs,vocabSize,k
	return (unigramFreqs[unigram] + k)/(sum(unigramFreqs.values()) + (vocabSize*k))

def unigramSentenceProb(words): 
	return sum(np.log([unigramProbAddOneSmoothed( (word2index[word])) for word in words]))

def getPerplexityUnigram(words):
	return np.exp(-unigramSentenceProb(words)/len(words))
def getPerplexityBigram(words):
	return np.exp(-bigramSentenceProb(words)/len(words))
def getPerplexityTrigram(words):
	return np.exp(-trigramSentenceProb(words)/len(words))

def printUnigramStatistics(words):
	global word2index
	for word in words:
		print("UnigramProbSmth: ",word,unigramProbAddOneSmoothed(word2index[word]))
	print("UNIGRAM SENTENCE PROB: ",unigramSentenceProb(words))	
	print("Perplexity: ",getPerplexityUnigram(words))

def printBigramStatistics(words):
	global word2index
	for i in range(1,len(words)):
		print("BigramProbSmth: ",words[i-1],words[i],bigramProbAddOneSmoothed( (word2index[words[i-1]],word2index[words[i]])))
	print("BIGRAM SENTENCE PROB: ",bigramSentenceProb(words))
	print("Perplexity: ",getPerplexityBigram(words))	

def printTrigramStatistics(words):
	global word2index
	for i in range(2,len(words)):
		print("TrigramProbSmth: ",words[i-2],words[i-1],words[i],trigramProbAddOneSmoothed( (word2index[words[i-2]],word2index[words[i-1]], word2index[words[i]])))
		print("TrigramProb: ",words[i-2],words[i-1],words[i],trigramProb( (word2index[words[i-2]],word2index[words[i-1]], word2index[words[i]])))
	print("TRIGRAM SENTENCE PROB: ",trigramSentenceProb(words))
	print("Perplexity: ",getPerplexityTrigram(words))

def printStats(words):
	printUnigramStatistics(words)
	printBigramStatistics(words)
	printTrigramStatistics(words)

def segmentAndTokenize(text):
	sentences = sent_tokenize(text)
	words = []
	for i in range(0,len(sentences)):
		wordsInSentence = word_tokenize(sentences[i])
		wordsInSentence.insert(0, "<s>")
		wordsInSentence.insert(0, "<s>")
		wordsInSentence.append("</s>")
		words.extend(wordsInSentence)
		
	return words 	

def makeBigram2TrigramData():
	global bigram2trigram,bigram2trigramRSorted,bigram2trigramProb,word2index
	#init dicts
	for i in range(2,len(words)):
		bigramKey = (word2index[words[i-2]], word2index[words[i-1]])
		bigram2trigram[bigramKey][word2index[words[i]]] = 0
		bigram2trigramRSorted[bigramKey][word2index[words[i]]] = 0
		bigram2trigramProb[bigramKey][word2index[words[i]]] = 0.0
	#make a dict fo a dict, with nested dict key == word2index value
	#and with value of the count
	for i in range(2,len(words)):
		bigramKey = (word2index[words[i-2]], word2index[words[i-1]])
		aDict = bigram2trigram[bigramKey]
		aDict[word2index[words[i]]] += 1

	#make reverse sorted count dict
    #so that if you had three possible trigrams
    # with values 3, 1, 1, they get stored as
    # 3,4,5, now probability partition is easy to calculate
	values = []
	for key in bigram2trigram:
		aDict = bigram2trigram[key]
		for dKey in aDict:
			values.append(aDict[dKey])
		values.sort(reverse=True)
	
		prevDkey = 0;
		dictKeys = list(aDict.keys())
		for dKey2 in dictKeys:
			for v in values:
				if(aDict[dKey2] == v):
					bigram2trigramRSorted[key][dKey2] = v + prevDkey
					prevDkey = v + prevDkey
					break;
		values.clear()

def computeDistribution(words):
	global bigram2trigram,bigram2trigramProb,bigram2trigramRProb,bigram2trigramRCProb
	global bigram2trigramRSorted,index2word

	for key in bigram2trigramRSorted:
		maxCount = -999
		for tKey in bigram2trigramRSorted[key]:
			if(bigram2trigramRSorted[key][tKey] > maxCount):
				maxCount = bigram2trigramRSorted[key][tKey]
		for tKey in bigram2trigramRSorted[key]:
			bigram2trigramProb[key][tKey] = float(bigram2trigramRSorted[key][tKey])/float(maxCount)
			bigram2trigramRProb[key][float(bigram2trigramRSorted[key][tKey])/float(maxCount)] = tKey

	for key in bigram2trigramRProb:
		aDict = bigram2trigramRProb[key]
		rProbKeys = list(aDict.keys())
		rProbKeys.sort(reverse=True)
		prevRkey = 0.0
		for rKey in rProbKeys:
			bigram2trigramRCProb[key][rKey] = index2word[aDict[rKey]]
			prevRkey = prevRkey + rKey

def getRandomUnknown():
	global unknowns;
	return unknowns[random.randint(0,len(unknowns)-1)]

def makeASentence():
	global bigram2trigramRCProb,word2index,skipUNK
	mySentence = []
	eos = False;
	begSent = ("<s>", "<s>")
	mySentence.append("<s>")
	mySentence.append("<s>")
	while not eos:
		aDict = bigram2trigramRCProb[(word2index[begSent[0]], word2index[begSent[1]])]
		rKeys = list(aDict.keys())
		rKeys.sort()
		
		prevRkey = 0.0
		rProb = random.random();
		for key in rKeys:
			if(rProb > prevRkey and rProb < key):
				if(aDict[key] == "<UNK>"):
					if(skipUNK):
						eos = True
						mySentence.clear();
						break;
					else:
						mySentence.append(getRandomUnknown())
				else:
					mySentence.append(aDict[key])
				begSent = (begSent[1], aDict[key])
				foundWord = True;
				if(begSent[1] == "</s>"):
					eos = True
				break;
			prevRkey = key
	return mySentence

def makeLine(aSentence):
	myLine = ""
	for wrd in aSentence:
		if(len(myLine) == 0):
			myLine = wrd
		else:
			myLine = myLine + " " + wrd
	return myLine

def makeLineStripped(aSentence):
	myLine = ""
	for wrd in aSentence:
		if(wrd != "<s>" and wrd != "</s>"):
			if(len(myLine) == 0):
				myLine = wrd
			else:
				myLine = myLine + " " + wrd
	return myLine

corpusFile = sys.argv[1]
k = float(sys.argv[2])
text = open(corpusFile, "r").read()
#words = text.split()
words = segmentAndTokenize(text);

rawfreqs = Counter(words)
word2index = defaultdict(lambda: len(word2index))
UNK = word2index["<UNK>"]
[word2index[word] for word, freq in rawfreqs.items() if freq > 1]
for word, freq in rawfreqs.items(): 
	if freq == 1:
		unknowns.append(word)
	
word2index = defaultdict(lambda: UNK, word2index)

index2word = defaultdict(lambda: 0)
for wkey in word2index:
	index2word[word2index[wkey]] = wkey

vocabSize = float(len(word2index))

unigrams = [word2index[word] for word in words]	
unigramFreqs = Counter(unigrams)
bigrams = [ (word2index[words[i-1]], word2index[words[i]]) for i in range(1, len(words)) ]
bigramFreqs = Counter(bigrams)
trigrams = [ (word2index[words[i-2]], word2index[words[i-1]], word2index[words[i]]) for i in range(2, len(words)) ]
trigramFreqs = Counter(trigrams);




makeBigram2TrigramData()
computeDistribution(words)

cnt = 0;
gcrp = open("generated_corpus.txt", "w")
gsnt = open("generated.txt", "w")
while cnt < 50:
	mySentence = makeASentence()
	if(len(mySentence) > 1):
		cnt += 1
		gcrp.write(makeLine(mySentence))
		gsnt.write(makeLineStripped(mySentence)+"\n")
gcrp.close()
gsnt.close()

testHandle = open("generated_corpus.txt","r")
testData = testHandle.readlines()
for line in testData:
	triGramPerplexity = getPerplexityTrigram(line.split())
	print(triGramPerplexity)
	#printStats(line.split())

