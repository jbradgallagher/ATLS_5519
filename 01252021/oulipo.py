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
	nltk.download('punkt')
	nltk.download('stopwords')
	nltk.download('averaged_perceptron_tagger')

def getDictionary(fname):
	fullDict = []
	stop_words = set(stopwords.words('english'))
	newWords = []
	#read the dictionary file, storing each line (one word per line)
	#as an element in "fullDict"
	try:
		with open(fname, "r") as fh:
			fullDict = fh.readlines()
	except IOError:
		printUsage()
	#loop over the words in fullDict, make sure all letters are lowercase
	#and skip words that began with a capital letter or that appear in the
	#the "stop_words" list.  Append the words that fit this criteria to newWords
	#and return the list	
	for wrd in [word.lower() for word in fullDict if not re.match(r'^[A-Z]',word)]:
		wrd = wrd.strip("\n")
		if not wrd in stop_words:
			newWords.append(wrd)

	return newWords

def getCorpusLines(fname):
	fileLines = []
	#read the source file, storing each line (multiple words)
	#in an element of "fileLines" and return the list 
	try:
		with open(fname, "r") as fh:
			fileLines = fh.readlines()
	except IOError:
		printUsage()

	return fileLines

def getIndexDictionary(wrdList):
	indexDict = {}
	#this function takes as input the list created by "getDictionary()"
	#we need a fast way to find the index in our dictionary list based
	#on a word found in our source text. This loop builds a
	#python dictionary, key-value pairs of the form {word, N}
	#where N is the index into the dictionary list
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
	
	#first we get the index into "dictWordList" from 
	# "indexDirectory", using the lower cassed word (wrd) as a key 
	# that was read from our source text. If it doesn't exist in 
	# "indexDictionary" then just return "wrd"
	try:
		idx = indexDictionary[wrd]
	except:
		replaceWord = wrd
		return replaceWord

	#if we have a valid index (idx), get the part of speech tag
	# of our input word (wrd). nltk.pos_tag will return a list
	# of tuples, but since we are doing this one word at a time
	# that list will only have one element. The tuple contains (word,tag)
	# so, myWrdPos[0][0] is the word and myWrdPos[0][1] is the tag
	myWrdPos = nltk.pos_tag(nltk.word_tokenize(wrd))
	#check to see if we are either running in nounRestrict mode or not,
	# if not, run the W+N operation on the word regardless of its part of speech
	# if we are using nounRestrict mode, make sure the input word (wrd)
	# has an 'NN' part of speech tag, if not, return "wrd" as "replaceWord"
	if (myWrdPos[0][1] == 'NN' and nounRestrict) or not nounRestrict:
		#run a while loop into "num" part of speech types are encountered
		# then return the "replacedWord"
		while typeCount < num:
			#if idx is still less than the size of "dictWordList" minus 1
			# increment "idx" to get the next word in "dictWordList"
			# to test if it has the same tag as the input word ("wrd")
			# if we have reached the end of the list, reset "idx" to 0 (begining of list)
			if idx != len(dictWordList) - 1:
				idx += 1
			else:
				idx = 0
			#get the next word pos tuple
			nextWrdPos = nltk.pos_tag(nltk.word_tokenize(dictWordList[idx]))
			#test if the nextWrdPos tag is the same as the myWrdPos tag
			#if so assign the nextWrdPos word (which is accessed in the first
			# element of the tuple, nextWrdPos[0][0])
			if(myWrdPos[0][1] == nextWrdPos[0][1]):
				replaceWord = nextWrdPos[0][0]
				typeCount += 1
	else:
		replaceWord = wrd

	return replaceWord

def printOulipo(nounRestrict,num,corpusLines,dictWordList,indexDictionary):
	stop_words = set(stopwords.words('english'))
	#loop over each line in our source text
	for line in corpusLines:
		#rstrip will remove any space at the end of the line
		line = line.rstrip()
		#do a rudimentary splitting of the line on spaces
		# to create a list of words in "lineData" This list
		# will still have words attached to punctuation, since it just
		# splits on empty space
		lineData = line.split(' ')
		#loop over each word in lineData
		for wrd in lineData:
			# "wrd" may have punctuation (commas or a period) concatenated to it
			# by running nltk.word_tokenize(wrd) we get a list returned that will
			# for "wrd" = "dog," for instance will have tok[0] = "dog" and tok[1] = ","
			# so we only look at the 0th element of "tok" and get rid of the punctuation
			# in this way. Note this isn't taking care of the case of porrly parsed text
			# like ",dog" 
			tok = nltk.word_tokenize(wrd.lower())
			#make sure tok has a size greater than zero and then
			#make sure the first element of tok is all letters, if not print out "wrd" as is
			if(len(tok) > 0):
				if tok[0].isalpha():
					#make sure tok[0] is not in stop words, if it is print out "wrd" as is
					if not tok[0].lower() in stop_words:
						#if tok[0] is not in "stop_words" make call to getNthWord
						print(getNthWord(nounRestrict,num,tok[0].lower(),dictWordList,indexDictionary), end=" ")
					else:
						print(wrd, end=" ")
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