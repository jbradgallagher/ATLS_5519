from itertools import permutations
import sys
import time
import getopt

frequency = 20.

def buildPermutations(myInput):
	perms = permutations(myInput)
	return perms

def printPermutations(myPerms):
	for perm in myPerms:
		for wrd in perm:
			print(wrd, end=' ', flush='true')
			time.sleep(1./frequency)
		print()

def printUsage():
	print("Usage: " + sys.argv[0] + " -t <list of words>  -f <frequency>")
	sys.exit()

def main():
	global frequency
	if(len(sys.argv) == 1):
		printUsage()
	else:
		try:
			opts, args = getopt.getopt(sys.argv[1:], 't:f:')
			for o, a in opts:
				if o == '-f':
					try:
						frequency = float(a)
					except ValueError:
						printUsage()
				if o == '-t':
					myWords = str(a)

			printPermutations(buildPermutations(myWords.split(' ')))
		except getopt.GetoptError as err:
			print(err)
	

if __name__ == '__main__':
	main()

