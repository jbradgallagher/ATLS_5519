import multiprocessing
import gensim
from gensim.models import Word2Vec
import matplotlib.pyplot as plt
import matplotlib.cm as cm
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
	return text.strip()


def make_trainData(inFile,useStopWords):
	outFile = ""
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
	return Word2Vec(data, size=200, window=5, min_count=5, workers=multiprocessing.cpu_count())


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

def getAllWordEmbeddings(myModel):
	embeddings = []
	words = []

	for wrd in list(myModel.wv.vocab):
		embeddings.append(myModel.wv[wrd])
		words.append(wrd)

	return embeddings,words


def tsne_plot_3d(title, label, embeddings, a=1):
	fig = plt.figure()
	ax = Axes3D(fig)
	colors = cm.rainbow(np.linspace(0, 1, 1))
	plt.scatter(embeddings[:, 0], embeddings[:, 1], embeddings[:, 2], c=colors, alpha=a, label=label)
	plt.legend(loc=4)
	plt.title(title)
	plt.show()


def tsne_plot_similar_words(title, labels, embedding_clusters, word_clusters, a, filename=None):
	plt.figure(figsize=(16, 9))
	colors = cm.rainbow(np.linspace(0, 1, len(labels)))
	for label, embeddings, words, color in zip(labels, embedding_clusters, word_clusters, colors):
		x = embeddings[:, 0]
		y = embeddings[:, 1]
		plt.scatter(x, y, c=color, alpha=a, label=label)
		for i, word in enumerate(words):
			plt.annotate(word, alpha=0.5, xy=(x[i], y[i]), xytext=(5, 2), textcoords='offset points', ha='right', va='bottom', size=8)
	plt.legend(loc=4)
	plt.title(title)
	plt.grid(True)
	if filename:
		plt.savefig(filename, format='png', dpi=150, bbox_inches='tight')
	plt.show()

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
	myWord = ""
	myWord2 = ""
	words = []
	words2 = []
	scores = []
	scores2 = []
	embeddings = []
	embedding_clusters = []
	embeddings_2d = []
	embeddings_3d = []
	if(len(sys.argv) == 1):
		printUsage()
	else:
		try:
			opts, args = getopt.getopt(sys.argv[1:], 'f:n:p:m:W:w:3S')
			for o, a in opts:
				if o == '-f':
					inFile = a
				if o == '-n':
					neighborCnt = int(a)
				if o == '-p':
					prplx = int(a)
				if o == '-m':
					wordList = a
				if o == '-3':
					twoD = False
					threeD = True
				if o == '-W':
					myWord = a
					simCircle = True
				if o == '-w':
					myWord2 = a
					useTwoWords = True
				if o == '-S':
					useStopWords = True

			#parse input file for training
			#train word2vec model
			make_trainData(inFile,useStopWords)
			myModel = train_word2vec(inFile)
			if(simCircle):
				if(useTwoWords):
					words, scores, words2, scores2 = getNeighborSimilarityTwoWords(myModel,myWord,myWord2,neighborCnt)
					plotSimilarityCircleTwoWords(words,scores,myWord,words2,scores2,myWord2)
				else:
					words, scores = getNeighborSimilarity(myModel,myWord,neighborCnt)
					plotSimilarityCircle(words,scores,myWord)
			else:
				if(twoD):
					wlist = getWrdList(wordList)
					embedding_clusters, word_clusters = getWordEmbeddings(myModel,wlist,neighborCnt)
					embedding_clusters = np.array(embedding_clusters)
					n, m, k = embedding_clusters.shape
					tsne_2d = TSNE(perplexity=prplx, n_components=2, init='pca', n_iter=3500, random_state=32)
					embeddings_2d = np.array(tsne_2d.fit_transform(embedding_clusters.reshape(n * m, k))).reshape(n, m, 2)
					tsne_plot_similar_words('Similar Words', wlist, embeddings_2d, word_clusters, 0.7, 'similar_words.png')
				else:
					embeddings, words = getAllWordEmbeddings(myModel)
					embeddings = np.array(embeddings)
					tsne_3d = TSNE(perplexity=prplx, n_components=3, init='pca', n_iter=3500, random_state=12)
					embeddings_3d = tsne_3d.fit_transform(embeddings)
					tsne_plot_3d('Visualizing Embeddings using t-SNE', 'All Embeddings', embeddings_3d, a=0.1)



			
			
		
					
		except getopt.GetoptError as err:
			print(err)


if __name__ == '__main__':
	main()


