import markovify
import os
import sys
import getopt



def printMarkov(inFile,levels,numSentences,numTries):
	with open(inFile) as f:
		text = f.read()

	text_model = markovify.Text(text, state_size=levels)

	for i in range(numSentences):
		print(text_model.make_sentence(tries=numTries))

def printUsage():
	print("python3 markov_simple.py -f <corpus> -n <levels> -N <num sentences>")
	sys.exit()

def main():
	
	
	inFile = ""
	levels = 1
	numSentences = 3
	numTries = 100

	if(len(sys.argv) == 1):
		printUsage()
	else:
		try:
			opts, args = getopt.getopt(sys.argv[1:], 'f:n:N:t:')
			for o, a in opts:
				if o == '-f':
					inFile = a
				if o == '-n':
					levels = int(a)
				if o == '-N':
					numSentences = int(a)
				if o == '-t':
					numTries = int(a)
			

			
			printMarkov(inFile,levels,numSentences,numTries)
		
					
		except getopt.GetoptError as err:
			print(err)


if __name__ == '__main__':
	main()