import random
import time

materials = ["SAND","BRICK","STRAW","DRIFTWOOD","WOOD","SUNLIGHT","WIND","DUST","STARDUST","TURBULENT DREAMS","DREAMS"]
preps= ["IN", "ON","INSIDE", "OUTSIDE", "UNDERNEATH", "BEHIND"]
places=["EARTH", "THE GROUND", "HEAVEN", "HELL", "THE OCEAN", "THE DESERT","A ROARING RIVER","A DESOLATE MOON BASE","A DENSE FOREST","A DESERT","A LARGE CITY","A SMALL TOWN"]
lights=["CANDLELIGHT", "ELECTRIC LIGHT", "A CAMPFIRE", "THE SUN"]
inhabit=["ALL OF MY FRIENDS", "MY FAMILY", "ALL OF MY ENIMIES", "SOME PRETTY DANGEROUS ANIMALS"]


lineOneBegin = "A HOUSE OF "
lineThreeBegin = "USING "
lineFourBegin = "INHABITED BY "

def getRandomWord(wrdList):
	return wrdList[random.randint(0,len(wrdList)-1)]

def makeSomeSpace(num):
	return ''.join(' ' for i in range(num))
	
def buildPoem():
	
	poem = []

	poem.append(lineOneBegin+getRandomWord(materials))
	poem.append(makeSomeSpace(4)+getRandomWord(preps)+makeSomeSpace(1)+getRandomWord(places))
	poem.append(makeSomeSpace(8)+lineThreeBegin+getRandomWord(lights))
	poem.append(makeSomeSpace(12)+lineFourBegin+getRandomWord(inhabit))

	return poem
	
def printPoem():
	print()
	for line in buildPoem():
		print(line)
	print()

def printPoemByLetter():
	print()
	for line in buildPoem():
		for char in line:
			print(char, end='', flush='true')
			time.sleep(1./20.)
		print()
	print()

def main():
	printPoemByLetter()

if __name__ == '__main__':
	main()
