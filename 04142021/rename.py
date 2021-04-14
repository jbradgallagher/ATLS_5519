import os
import glob


filelist = glob.glob("*.txt")

for file in filelist:
	newFile = "gen_" + file
	os.rename(file,newFile)
