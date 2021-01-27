import random
import nltk

import ssl
import sys
import getopt

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
	nltk.download('gutenberg')

def getSourceLines(fname):
	fileLines = []
	#read the source file, storing each line (multiple words)
	#in an element of "fileLines" and return the list 
	try:
		with open(fname, "r") as fh:
			fileLines = fh.readlines()
	except IOError:
		printUsage()

	return fileLines

def getSimilarWord(corpus,wrd,srange):
	simWrds = corpus.similar_words(wrd,srange)

	if len(simWrds) == 0:
		return wrd
	else:
		return simWrds[random.randint(0,len(simWrds)-1)]
		
def printSimilarTranslation(corpus,corpusLines,srange,useStopWords):
	stop_words = set(nltk.corpus.stopwords.words('english'))
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
			#make sure the first element of tok is all letters, if not print out "wrd" as is
			if(len(tok) > 0):
				for c in tok:
					if c.isalpha():
						#make sure tok[0] is not in stop words, if it is print out "wrd" as is
						if (useStopWords and not c.lower() in stop_words) or not useStopWords:
						#if tok[0] is not in "stop_words" make call to getNthWord
							print(getSimilarWord(corpus,c,srange), end="")
						else:
							print(c, end="")
					else:
						print(c, end="")
				print(end=" ")
			else:
				print(wrd, end=" ")
			
		print()

def printUsage():
	print()
	print("Usage: " + sys.argv[0] + " -D (download nltk data) -B,J,M,S,W,H,K (corpus selection) -A (don't use stop words)")
	print("		  -s <sourceText> -n <similar_poolsize (default=20)> (larger number results in more diverse text)\n")
	print("Corpora:")
	print("(-B) William Blake, (-J) Jane Austen,")
	print("(-M) John Milton, (-S) William Shakespeare,")
	print("(-W) Walt Whitman, (-H) Herman Melville, (-K) The Bible")
	print("(-G) Whole Gutenberg Corpus\n")
	sys.exit()


def main():
	useStopWords = True
	sourceFile = ""
	srange = 20

	if(len(sys.argv) == 1):
		printUsage()
	else:
		try:
			opts, args = getopt.getopt(sys.argv[1:], 'DABJMSWHKGd:s:n:')
			for o, a in opts:
				if o == '-D':
					getDownloads()
					sys.exit()
				if o == '-A':
					useStopWords = False
				if o == '-s':
					sourceFile = a
				if o == '-n':
					srange = int(a)
				if o == '-B':
					corpus = nltk.text.ContextIndex([word.lower( ) for word in nltk.corpus.gutenberg.words('blake-poems.txt')])
				if o == '-J':
					corpus = nltk.text.ContextIndex([word.lower( ) for word in nltk.corpus.gutenberg.words('austen-sense.txt')])
				if o == '-M':
					corpus = nltk.text.ContextIndex([word.lower( ) for word in nltk.corpus.gutenberg.words('milton-paradise.txt')])
				if o == '-S':
					corpus = nltk.text.ContextIndex([word.lower( ) for word in nltk.corpus.gutenberg.words('shakespeare-macbeth.txt')])
				if o == '-W':
					corpus = nltk.text.ContextIndex([word.lower( ) for word in nltk.corpus.gutenberg.words('whitman-leaves.txt')])
				if o == '-H':
					corpus = nltk.text.ContextIndex([word.lower( ) for word in nltk.corpus.gutenberg.words('melville-moby_dick.txt')])
				if o == '-K':
					corpus = nltk.text.ContextIndex([word.lower( ) for word in nltk.corpus.gutenberg.words('bible-kjv.txt')])
				if o == '-G':
					corpus = nltk.text.ContextIndex([word.lower( ) for word in nltk.corpus.gutenberg.words()])
					
			printSimilarTranslation(corpus,getSourceLines(sourceFile),srange,useStopWords)
					
		except getopt.GetoptError as err:
			print(err)


if __name__ == '__main__':
	main()