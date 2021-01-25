import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import ssl
import sys
import getopt
import itertools 
import re

def setSSLContext():
	try:
		_create_unverified_https_context = ssl._create_unverified_context
	except AttributeError:
		pass
	else:
		ssl._create_default_https_context = _create_unverified_https_context

def getDownloads():
	setSSLContext()
	nltk.download('stopwords')
	nltk.download('averaged_perceptron_tagger')

def getDictionary(fname):
	fullDict = []
	stop_words = set(stopwords.words('english'))
	newWords = []
	try:
		with open(fname, "r") as fh:
			fullDict = fh.readlines()
	except IOError:
		printUsage()

	for wrd in [word.lower() for word in fullDict if not re.match(r'^[A-Z]',word)]:
		wrd = wrd.strip("\n")
		if not wrd in stop_words:
			newWords.append(wrd)

	return newWords

def getCorpusLines(fname):
	fileLines = []
	try:
		with open(fname, "r") as fh:
			fileLines = fh.readlines()
	except IOError:
		printUsage()

	return fileLines

def getIndexDictionary(wrdList):
	indexDict = {}

	wrdCnt = 0
	for wrd in wrdList:
		indexDict[wrd] = wrdCnt
		wrdCnt += 1	
	
	return indexDict

def getNthWord(nounRestrict,num,wrd,dictWordList,indexDictionary):
	idx = 0
	nidx = 0
	typeCount = 0
	replaceWord = ""
	
	try:
		idx = indexDictionary[wrd]
	except:
		replaceWord = wrd
		return replaceWord

	counter = itertools.count(idx)

	myWrdPos = nltk.pos_tag(nltk.word_tokenize(wrd))
	if (myWrdPos[0][1] == 'NN' and nounRestrict) or not nounRestrict:
		while typeCount < num:
			if nidx != len(dictWordList) - 1:
				nidx = next(counter)
			else:
				counter = itertools.count()
				nidx = next(counter)
			nextWrdPos = nltk.pos_tag(nltk.word_tokenize(dictWordList[nidx]))
			if(myWrdPos[0][1] == nextWrdPos[0][1]):
				replaceWord = nextWrdPos[0][0]
				typeCount += 1
	else:
		replaceWord = wrd

	return replaceWord

def printOulipo(nounRestrict,num,corpusLines,dictWordList,indexDictionary):
	stop_words = set(stopwords.words('english'))
	for line in corpusLines:
		line = line.rstrip()
		lineData = line.split(' ')
		for wrd in lineData:
			if wrd.isalpha():
				tok = nltk.word_tokenize(wrd)
				if not tok[0].lower() in stop_words:
					print(getNthWord(nounRestrict,num,tok[0].lower(),dictWordList,indexDictionary), end=" ")
				else:
					print(wrd, end=" ")
			else:
				print(wrd, end=" ")
		print()

def printUsage():
	print("Usage: " + sys.argv[0] + " -D (download nltk data) -N (restrict to nouns) -d <dictionary text>  -s <source text> -n <N+ words>")
	sys.exit()
	

def main():
	
	dictionaryFile = ""
	nounRestrict = False
	num = 0
	idx = 0
	dictWordList = []
	indexDictionary = {}
	sourceDictionary = {}

	if(len(sys.argv) == 1):
		printUsage()
	else:
		try:
			opts, args = getopt.getopt(sys.argv[1:], 'DNd:s:n:')
			for o, a in opts:
				if o == '-D':
					getDownloads()
					sys.exit()
				if o == '-N':
					nounRestrict = True;
				if o == '-d':
					dictionaryFile = a
				if o == '-s':
					sourceFile = a
				if o == '-n':
					num = int(a)
			

			dictWordList = getDictionary(dictionaryFile)
			indexDictionary = getIndexDictionary(dictWordList)


			printOulipo(nounRestrict,num,getCorpusLines(sourceFile),dictWordList,indexDictionary)

					
		except getopt.GetoptError as err:
			print(err)


if __name__ == '__main__':
	main()