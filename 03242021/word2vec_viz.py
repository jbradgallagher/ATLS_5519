import multiprocessing
import gensim
from gensim.models import Word2Vec
import gensim.downloader as api
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patheffects as path_effects
from mpl_toolkits.mplot3d import Axes3D
from sklearn.manifold import TSNE
import numpy as np
import sys
import getopt
import nltk
import re
import math



def preprocess_text(text):
	text = re.sub('[\d+\:\d+]', '', text)
	text = re.sub('[^a-zA-Z0-9]+', ' ', text)
	text = re.sub(' +', ' ', text)
	text = re.sub(r'^\s+', '', text)
	text = re.sub(r'\s+$', '', text)
	return text.strip()


def make_trainData(inFile,useStopWords):
	outFile = ""
	stop_words = []
	all_text = open(inFile, "r", encoding='utf-8').read()
	outFile = "train_" + inFile
	outFH = open(outFile, "w", encoding='utf-8')

	if(useStopWords):
		stop_words = set(nltk.corpus.stopwords.words('english'))
		for sentence in nltk.sent_tokenize(all_text):
			aSentence = ""
			for wrd in nltk.word_tokenize(sentence):
				if wrd.lower() not in stop_words:
					aSentence = aSentence + " " + wrd.lower()
			aSentence = re.sub(r'^\s+', '', aSentence)
			outFH.write(preprocess_text(aSentence.lower())+"\n")
	else:
		for sentence in nltk.sent_tokenize(all_text):
			outFH.write(preprocess_text(sentence.lower())+"\n")

def train_word2vec(filename):
	train_filename = "train_" + filename
	data = gensim.models.word2vec.LineSentence(train_filename)
	return Word2Vec(data, size=200, window=5, min_count=1, workers=multiprocessing.cpu_count())

def train_word2vec_text8():
	corpus = api.load("text8")
	return Word2Vec(corpus, size=200, window=5, min_count=5, workers=multiprocessing.cpu_count())

def getWordEmbeddings(myModel,wrdList,neighborCnt):

	embedding_clusters = []
	word_clusters = []
	for word in wrdList:
		embeddings = []
		words = []
		for similarWrd, _ in myModel.most_similar(word,topn=neighborCnt):
			words.append(similarWrd)
			embeddings.append(myModel[similarWrd])
		embedding_clusters.append(embeddings)
		word_clusters.append(words)

	return embedding_clusters,word_clusters

def getNeighborSimilarityTwoWords(myModel,myWord,myWord2,neighborCnt):

	words = []
	words2 = []
	scores = []
	scores2 = []

	words,scores = getNeighborSimilarity(myModel,myWord,neighborCnt)
	words2, scores2 = getNeighborSimilarity(myModel,myWord2,neighborCnt)
	
	return words,scores,words2,scores2


def getNeighborSimilarity(myModel,myWord,neighborCnt):

	words = []
	scores = []
	norms = []
	for similarWrd, score in myModel.most_similar(myWord,topn=neighborCnt):
		words.append(similarWrd)
		scores.append(score)

	norms = normalizeScores(scores)
	return words,norms

def normalizeScores(scores):
	smax = -999.0
	smin = 999.0
	for score in scores:
		if(score < smin):
			smin = score
		if(score > smax):
			smax = score
	#normalize between 	0, 2*np.pi
	norm = []
	for score in scores:
		nscore = (2*np.pi)* ((score - smin)/(smax-smin))
		norm.append(nscore)
	return norm

def getTopNNeighbors(myModel,myWord,neighborCnt):
	words = []
	scores = []
	norms = []
	for similarWrd, score in myModel.most_similar(myWord,topn=neighborCnt):
		words.append(similarWrd)
		scores.append(score)

	for word, score in zip(words[:5],scores[:5]):
		print(myWord,word,score)


def getNegationNeighbor(myModel,myWord,myWord2,myWord3,neighborCnt):

	#vec1, vec2, vec3 = myModel.wv.get_vector(myWord), myModel.wv.get_vector(myWord3), myModel.wv.get_vector(myWord3)

	#result = myModel.similar_by_vector(vec1 - vec2 + vec3)
	result = myModel.wv.most_similar(positive=[myWord, myWord2], negative=[myWord3])
	#print(result)
	return result


def getAllWordEmbeddings(myModel):
	embeddings = []
	words = []

	for wrd in list(myModel.wv.vocab):
		embeddings.append(myModel.wv[wrd])
		words.append(wrd)

	return embeddings,words


def plotSimilarityCircle(words,scores,myWord):
	plt.figure(figsize=(9, 9))
	colors = cm.rainbow(np.linspace(0, 1, len(words)))
	plt.annotate(myWord, alpha=1.0, xy=(0,0), xytext=(5,2), textcoords='offset points', ha='right', va='bottom', size=16)
	for word, score, color in zip(words,scores,colors):
		x = 5 * np.cos(score)
		y = 5 * np.sin(score)
		plt.scatter(x, y, c=color, alpha=1.0, label=word)
		plt.annotate(word, alpha=0.5, xy=(x,y), xytext=(5,2), textcoords='offset points', ha='right', va='bottom', size=8)
	plt.show()

def plotSimilarityCircleTwoWords(words,scores,myWord,words2,scores2,myWord2):
	plt.figure(figsize=(16, 9))
	colors = cm.rainbow(np.linspace(0, 1, len(words)))
	plt.annotate(myWord, alpha=1.0, xy=(-4,0), xytext=(5,2), textcoords='offset points', ha='right', va='bottom', size=16)
	for word, score, color in zip(words,scores,colors):
		x = -4 + (5 * np.cos(score))
		y = 5 * np.sin(score)
		plt.scatter(x, y, c=color, alpha=1.0, label=word)
		plt.annotate(word, alpha=0.5, xy=(x,y), xytext=(5,2), textcoords='offset points', ha='right', va='bottom', size=8)

	plt.annotate(myWord2, alpha=1.0, xy=(4,0), xytext=(5,2), textcoords='offset points', ha='right', va='bottom', size=16)
	for word, score, color in zip(words2,scores2,colors):
		x = 4 + (5 * np.cos(score))
		y = 5 * np.sin(score)
		plt.scatter(x, y, c=color, alpha=1.0, label=word)
		plt.annotate(word, alpha=0.5, xy=(x,y), xytext=(5,2), textcoords='offset points', ha='right', va='bottom', size=8)
	plt.show()

def plotSimilarityCircleStride(words,scores,myWord,stride,offset):
	plt.figure(figsize=(9, 9))
	colors = cm.rainbow(np.linspace(0, 1, len(words)))
	txt = plt.text(0,0,myWord,c="white",size=16)
	txt.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'),path_effects.Normal()])
	#plt.annotate(myWord, alpha=1.0, xy=(0,0), xytext=(5,2), textcoords='offset points', ha='right', va='bottom', size=16)
	cnt = 0
	nwords = []
	nscores = []
	norms = []
	ncolors = []

	# collects words and scores across the stride
	#and normalize again

	for word, score, color in zip(words,scores,colors):
		if cnt % stride == 0:
			nwords.append(word)
			nscores.append(float(cnt)/360.)
		cnt += 1

	norms = normalizeScores(nscores)
	ncolors = cm.rainbow(np.linspace(0, 1, len(nwords)))
	for word, norm, color in zip(nwords[:len(nwords)-1],norms[:len(norms)-1],ncolors[:len(ncolors)-1]):
			x = np.cos(norm)
			y = np.sin(norm)
			plt.scatter(x, y, c=color, alpha=0.0, label=word)
			xoffset = offset*np.cos(norm)
			yoffset = offset*np.sin(norm)
			txt = plt.text(x+xoffset,y+yoffset,word,c=color,size=12)
			txt.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'),path_effects.Normal()])
	plt.axis('off')
	plt.show()

def plotSimilarityCircleStrideNegation(words,scores,myWord,stride,offset,myWord1,myWord2,myWord3):
	plt.figure(figsize=(9, 9))
	colors = cm.rainbow(np.linspace(0, 1, len(words)))
	equation = "(" + myWord1 + " " + "+" + " " + myWord2 + ")" + " " + "-" + " " + myWord3 + " " + "=" + " " + myWord
	
	txt = plt.text(-1.0*len(equation)*0.018,0,equation,c="white",size=16)
	txt.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'),path_effects.Normal()])
	#plt.annotate(myWord, alpha=1.0, xy=(0,0), xytext=(5,2), textcoords='offset points', ha='right', va='bottom', size=16)
	cnt = 0
	nwords = []
	nscores = []
	norms = []
	ncolors = []

	# collects words and scores across the stride
	#and normalize again

	for word, score, color in zip(words,scores,colors):
		if cnt % stride == 0:
			nwords.append(word)
			nscores.append(float(cnt)/360.)
		cnt += 1

	norms = normalizeScores(nscores)
	ncolors = cm.rainbow(np.linspace(0, 1, len(nwords)))
	for word, norm, color in zip(nwords[:len(nwords)-1],norms[:len(norms)-1],ncolors[:len(ncolors)-1]):
			x = np.cos(norm)
			y = np.sin(norm)
			plt.scatter(x, y, c=color, alpha=0.0, label=word)
			xoffset = offset*np.cos(norm)
			yoffset = offset*np.sin(norm)
			txt = plt.text(x+xoffset,y+yoffset,word,c=color,size=12)
			txt.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'),path_effects.Normal()])

	plt.axis('off')
	plt.show()

def plotSimilarityCircleStrideTwoWords(words,scores,myWord,words2,scores2,myWord2,stride,offset):
	plt.figure(figsize=(19, 9))
	colors = cm.rainbow(np.linspace(0, 1, len(words)))
	txt = plt.text(-1,0,myWord,c="white",size=16)
	txt.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'),path_effects.Normal()])
	#plt.annotate(myWord, alpha=1.0, xy=(0,0), xytext=(5,2), textcoords='offset points', ha='right', va='bottom', size=16)
	cnt = 0
	nwords = []
	nscores = []
	norms = []
	ncolors = []

	# collects words and scores across the stride
	#and normalize again

	for word, score, color in zip(words,scores,colors):
		if cnt % stride == 0:
			nwords.append(word)
			nscores.append(float(cnt)/360.)
		cnt += 1

	norms = normalizeScores(nscores)
	ncolors = cm.rainbow(np.linspace(0, 1, len(nwords)))
	for word, norm, color in zip(nwords[:len(nwords)-1],norms[:len(norms)-1],ncolors[:len(ncolors)-1]):
			x = -1 + np.cos(norm)
			y = np.sin(norm)
			plt.scatter(x, y, c=color, alpha=0.0, label=word)
			xoffset = offset*np.cos(norm)
			yoffset = offset*np.sin(norm)
			txt = plt.text(x+xoffset,y+yoffset,word,c=color,size=12)
			txt.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'),path_effects.Normal()])

	# collects words and scores across the stride
	#and normalize again
	txt = plt.text(1,0,myWord2,c="white",size=16)
	txt.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'),path_effects.Normal()])
	cnt = 0
	nwords2 = []
	nscores2 = []
	norms2 = []
	ncolors2 = []
	for word, score, color in zip(words2,scores2,colors):
		if cnt % stride == 0:
			nwords2.append(word)
			nscores2.append(float(cnt)/360.)
		cnt += 1

	norms2 = normalizeScores(nscores2)
	ncolors2 = cm.rainbow(np.linspace(0, 1, len(nwords2)))
	for word, norm, color in zip(nwords2[:len(nwords2)-1],norms2[:len(norms2)-1],ncolors2[:len(ncolors2)-1]):
			x = 1 + np.cos(norm)
			y = np.sin(norm)
			plt.scatter(x, y, c=color, alpha=0.0, label=word)
			xoffset = offset*np.cos(norm)
			yoffset = offset*np.sin(norm)
			txt = plt.text(x+xoffset,y+yoffset,word,c=color,size=12)
			txt.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'),path_effects.Normal()])
	plt.axis('off')
	plt.show()

def getWrdList(fname):
	wlist = []
	fd = open(fname, "r", encoding='utf-8')
	wlist = fd.readlines()
	fd.close()
	wlist = [wrd.rstrip() for wrd in wlist]
	return wlist

def printUsage():
	print("|(2d and 3d TSNE Plots)| python3 word2vec_viz.py -f <inFile> -p <perplexity> -n <neighbor count (for 2d)> -m <word list (for 2d)> -3 <make 3d plot>")
	print("|(circle Similarity plot)| python3 word2vec_viz.py -f <inFile> -W <word> -w <word number two (optional)> -n <neighbor count>")
	sys.exit()

def main():
	
	
	inFile = ""
	wordList = ""
	neighborCnt = 30
	prplx = 30
	twoD = True
	threeD = False
	simCircle = False
	useStopWords = False
	useTwoWords = False
	useNegation = False
	usePreTrained = False

	myWord = ""
	myWord2 = ""
	myWord3 = ""
	words = []
	words2 = []
	scores = []
	scores2 = []
	embeddings = []
	embedding_clusters = []
	embeddings_2d = []
	embeddings_3d = []
	stride = 22
	offset = 0.25
	if(len(sys.argv) == 1):
		printUsage()
	else:
		try:
			opts, args = getopt.getopt(sys.argv[1:], 'f:n:p:m:W:w:N:s:o:3SP')
			for o, a in opts:
				if o == '-f':
					inFile = a
				if o == '-n':
					neighborCnt = int(a)
				if o == '-W':
					simCircle = True
					myWord = a
				if o == '-w':
					useTwoWords = True
					myWord2 = a
				if o == '-N':
					useNegation = True
					myWord3 = a
				if o == '-S':
					useStopWords = True
				if o == '-s':
					stride = int(a)
				if o == '-o':
					offset = float(a)
				if o == '-P':
					usePreTrained = True

			#parse input file for training
			#train word2vec model
			if usePreTrained:
				myModel = train_word2vec_text8()
			else:
				make_trainData(inFile,useStopWords)
				myModel = train_word2vec(inFile)
			
			if(simCircle and not useNegation):
				if(useTwoWords):
					words, scores, words2, scores2 = getNeighborSimilarityTwoWords(myModel,myWord,myWord2,neighborCnt)
					plotSimilarityCircleStrideTwoWords(words,scores,myWord,words2,scores2,myWord2,stride,offset)
				else:
					words, scores = getNeighborSimilarity(myModel,myWord,neighborCnt)
					plotSimilarityCircleStride(words,scores,myWord,stride,offset)
			if(useNegation):
				negateResult = getNegationNeighbor(myModel,myWord,myWord2,myWord3,neighborCnt)
				words, scores = getNeighborSimilarity(myModel,myWord,neighborCnt)
				plotSimilarityCircleStrideNegation(words,scores,negateResult[0][0],stride,offset,myWord,myWord2,myWord3)
			#getTopNNeighbors(myModel,myWord,neighborCnt)
			#getNegationNeighbor(myModel,myWord,myWord2,myWord3,neighborCnt)


			
			
		
					
		except getopt.GetoptError as err:
			print(err)


if __name__ == '__main__':
	main()


