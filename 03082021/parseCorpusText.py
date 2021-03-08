import os
import sys
import getopt
import re
import glob


def parseCorpus(inputFile):
	filehd = open(inputFile, "r")
	lines = filehd.readlines()
	filehd.close()

	cnt = 0;
	haveOpenedFile = False;
	for line in lines:
		if re.search("NAME",line) and not haveOpenedFile:
			speaker = line.split("<b>")
			print(len(speaker),speaker)
			name = speaker[1].split("<")
			speaker_file = name[0] + ".txt"
			if not os.path.exists(speaker_file):
				outhd = open(speaker_file, "w")
				haveOpenedFile = True
			else:
				outhd = open(speaker_file, "a")
				haveOpenedFile = True
		if re.search("\/A>",line) and haveOpenedFile:
			speaker_line = line.split(">")
			speakerLineClean = speaker_line[1].split("<")
			outhd.write(speakerLineClean[0] + "\n")
		else:
			if re.search("</blockquote>",line) and haveOpenedFile:
				outhd.close()
				haveOpenedFile = False;



def makeCSV_Corpus(corpusCSVFile):

	myCorpusFiles = glob.glob("*.txt")
	corpusCSV = open(corpusCSVFile, "w")
	for file in myCorpusFiles:
		tag = file.split(".")
		name = tag[0];
		filehd = open(file, "r")
		speakerData = filehd.readlines()
		filehd.close()
		speakerField = ""
		for line in speakerData:
			line = line.lower()
			line = re.sub(r'\n+', " ", line)
			speakerField = speakerField + line
		speakerField = name + "," + speakerField + "\n"
		corpusCSV.write(speakerField)
	corpusCSV.close()


def printUsage():
	print()
	print("Usage: " + sys.argv[0] + " -i <inputTextFile> -c <corpusCSVFile>")
	print()
	sys.exit()


def main():
	inputFile = ""
	corpusCSVFileName = ""
	makeCSV = False

	if(len(sys.argv) == 1):
		printUsage()
	else:
		try:
			opts, args = getopt.getopt(sys.argv[1:], 'i:c:')
			for o, a in opts:
				if o == '-i':
					inputFile = a
				if o == "-c":
					corpusCSVFileName = a
					makeCSV = True
			
				if makeCSV:
					makeCSV_Corpus(corpusCSVFileName)
				else:
					parseCorpus(inputFile)

		except getopt.GetoptError as err:
			print(err) 
				
if __name__ == '__main__':
	main()