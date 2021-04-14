import os
import sys
import getopt
import re


def parseCorpus(inputFile,outputPrefix):
	filehd = open(inputFile, "r")
	lines = filehd.readlines()
	filehd.close()

	cnt = 0;
	outFile = outputPrefix + "_" + "%04d" % cnt + ".txt"
	outhd = open(outFile, "w")
	for line in lines:
		if not re.search("PoemHunter",line):
			outhd.write(line)
		else:
			outhd.close()
			cnt = cnt + 1
			outFile = outputPrefix + "_" + "%04d" % cnt + ".txt"
			outhd = open(outFile, "w")

def parseCorpusOnNewLines(inputFile,outputPrefix):
	filehd = open(inputFile, "r")
	lines = filehd.readlines() #note, read whole file into string lines
	filehd.close()
	cnt = 0;
	
	haveOpenedFile = False;
	for line in lines:
		if not re.match(r'^\n',line):
			if not haveOpenedFile:
				outFile = outputPrefix + "_" + "%04d" % cnt + ".txt"
				outhd = open(outFile, "w")
				haveOpenedFile = True;
				cnt = cnt + 1
			outhd.write(line)
		else:
			outhd.close()
			haveOpenedFile = False;
			

def printUsage():
	print()
	print("Usage: " + sys.argv[0] + " -i <inputTextFile> -o <outputFilePrefix> -N (split on newlines)")
	print()
	sys.exit()


def main():
	inputFile = ""
	outputPrefix = ""
	splitOnNewLines = False

	if(len(sys.argv) == 1):
		printUsage()
	else:
		try:
			opts, args = getopt.getopt(sys.argv[1:], 'Ni:o:')
			for o, a in opts:
				if o == '-i':
					inputFile = a
				if o == '-o':
					outputPrefix = a
				if o == '-N':
					splitOnNewLines = True

			if(splitOnNewLines):
				parseCorpusOnNewLines(inputFile,outputPrefix)
			else:
				parseCorpus(inputFile,outputPrefix)

		except getopt.GetoptError as err:
			print(err) 
				
if __name__ == '__main__':
	main()