import io
import os
import sys
import random
import re
import getopt
import glob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#nltk.download('stopwords')
#nltk.download('punkt')
stop_words = set(stopwords.words('english'))


def removeDups(myList):
	newList = []
	for i in myList:
		if i not in newList:
			newList.append(i)
	return newList

def returnWords(line,wrdSize):
	new_words = []
	words = nltk.word_tokenize(line)
	for wrd in [word.lower() for word in words]:
		if not wrd in stop_words and len(wrd) > wrdSize:
			new_words.append(wrd)
			
	return new_words


def getFileDict(prefixName,wrdSize):
	fileDict = {}
	fileList = glob.glob(prefixName+"*")

	for file in fileList:
		fileHandle = open(file.strip('\n'), "r")
		fileContents = fileHandle.read();
		fileDict[file.strip('\n').split('.')[0]] = returnWords(fileContents,wrdSize)

	return fileDict



def hypertextRemix(corpusOnePrefix,corpusTwoPrefix,whichFrame,wrdSize):

	wordsToLink = []
	corpusOneDict = getFileDict(corpusOnePrefix,wrdSize)
	corpusTwoDict = getFileDict(corpusTwoPrefix,wrdSize)
	linkToFileDict = dict() 
	for fileNameOneKey in corpusOneDict:

		allFoundWords = []
		for fileNameTwoKey in corpusTwoDict:
			#go over the list of filtered words for corpusTwo file "pkey"
			for wrd in corpusTwoDict[fileNameTwoKey]:
				if wrd in corpusOneDict[fileNameOneKey]:
					allFoundWords.append(wrd)
					try:
						linkToFileDict[wrd].append(fileNameTwoKey)
					except:
						linkToFileDict[wrd] = []
						linkToFileDict[wrd].append(fileNameTwoKey)
					
					
		wordsToLink = removeDups(allFoundWords)

		#now we write the HTML file for the first file in corpusOneDict
		outHTMLFname = fileNameOneKey + ".html"
		inFileName = fileNameOneKey + ".txt"
		inTextFile = open(inFileName, "r")
		outHTMLFile = open(outHTMLFname, "w")

		inTextLines = inTextFile.readlines()
	
		outHTMLFile.write("<html>\n<head>\n")
		outHTMLFile.write("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />\n")
		outHTMLFile.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"hylrm.css\" />\n")
		outHTMLFile.write("</head>\n")
		outHTMLFile.write("<body>\n")
		outHTMLFile.write("<div id=\"poem\">\n")

		for line in inTextLines:
			newline = []
			myLine = ""
				
			wrds = line.split()
			for wrd in wrds:
				foundWrd = False
				saveWrd = ""
				for lwrd in wordsToLink:
					if re.search(lwrd, wrd.lower()):
						foundWrd = True
						saveWrd = lwrd
						break
				if foundWrd:
					foundWrd = False
					fileToLink = linkToFileDict[saveWrd.lower()][random.randint(0,len(linkToFileDict[saveWrd.lower()])-1)] + ".html"
					link = "<a href=\"" + fileToLink + "\"" + " target=\"" + whichFrame + "\"" + " style=\"color:000000;\">" + wrd + "</a>"
					newline.append(link)
				else:
					newline.append(wrd)

			newline.append("</br>")
			myLine = " ".join(newline)
			myLine = myLine + "\n"
			outHTMLFile.write(myLine)

		inTextFile.close()
		outHTMLFile.write("</p>\n</div>\n</body>\n</html\n>")
		outHTMLFile.close()

def printUsage():
	print()
	print("Usage: " + sys.argv[0] + " -p <corpusPrefixOne> -q <corpusPrefixTwo> -f <leftFrame || rightFrame> -n <minimum size of word>")
	print()

def main():
	corpPrefixOne = ""
	corpPrefixTwo = ""
	makeFrame = ""
	wrdSize = 3
	if(len(sys.argv) == 1):
			printUsage()
	else:
		try:
			opts, args = getopt.getopt(sys.argv[1:], 'p:q:f:n:')
			for o, a in opts:
				if o == '-p':
					corpPrefixOne = a
				if o == '-q':
					corpPrefixTwo = a
				if o == '-f':
					makeFrame = a
				if o == '-n':
					wrdSize = int(a)

			hypertextRemix(corpPrefixOne,corpPrefixTwo,makeFrame,wrdSize)

		except getopt.GetoptError as err:
			print(err)


if __name__ == '__main__':
	main()





	


	
