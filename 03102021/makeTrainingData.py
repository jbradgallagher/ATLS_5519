import os
import sys
import getopt
import re
import random

def readFiles(fileList):
	fileList_hd = open(fileList, "r")
	files = fileList_hd.readlines()
	fileList_hd.close();

	cnt = 1
	allPoems = []
	for poemFile in files:
		poemFile = poemFile.strip('\n')
		poemhd = open(poemFile, "r", encoding="utf-8")
		poem = poemhd.readlines()
		poemhd.close()
		for line in poem:
			if re.match("^\w+", line) and not re.match("^\.", line):
				line = line + "::" + str(cnt)
				allPoems.append(line)
		cnt += 1

	random.shuffle(allPoems)
	return allPoems

def exportTrainData(myPoems):
	lineDataHd = open("10_poets_lines.txt", "w", encoding="utf-8")
	labelDataHd = open("10_poets_labels.txt", "w", encoding="utf-8")

	for line in myPoems:
		data = line.split("::")
		lineDataHd.write(data[0])
		labelDataHd.write(data[1] + "\n")
	lineDataHd.close()
	labelDataHd.close()


def printUsage():
	print()
	print("Usage: " + sys.argv[0] + " -i <fileList>")
	print()
	sys.exit()


def main():
	inputFile = ""
	data = []
	if(len(sys.argv) == 1):
		printUsage()
	else:
		try:
			opts, args = getopt.getopt(sys.argv[1:], 'i:')
			for o, a in opts:
				if o == '-i':
					inputFile = a
			
			exportTrainData(readFiles(inputFile))

		except getopt.GetoptError as err:
			print(err) 
				
if __name__ == '__main__':
	main()