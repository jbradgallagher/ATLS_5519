from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import sys
import getopt
import matplotlib.pyplot as plt


def plot_tfidf_classfeats_h(dfs,labels):
    ''' Plot the data frames returned by the function plot_tfidf_classfeats(). '''
    fig = plt.figure(figsize=(12, 9), facecolor="w")
    x = np.arange(len(dfs[0]))
    for i, df in enumerate(dfs):
        ax = fig.add_subplot(1, len(dfs), i+1)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_frame_on(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        ax.set_xlabel("Mean Tf-Idf Score", labelpad=16, fontsize=14)
        ax.set_title("label = " + str(labels[i]), fontsize=16)
        ax.ticklabel_format(axis='x', style='sci', scilimits=(-2,2))
        ax.barh(x, df.score, align='center', color='#3F5D7D')
        ax.set_yticks(x)
        ax.set_ylim([-1, x[-1]+1])
        yticks = ax.set_yticklabels(df.term)
        plt.subplots_adjust(bottom=0.09, right=0.97, left=0.15, top=0.95, wspace=0.52)
    plt.show()

def getTopScores(fileList,mySubCorpus):


	vectorizer = TfidfVectorizer(max_df=.65, min_df=1, stop_words='english', use_idf=True, norm=None)
	transformed_documents = vectorizer.fit_transform(mySubCorpus)



	transformed_documents_as_array = transformed_documents.toarray()


	# make the output folder if it doesn't already exist
	Path("./tf_idf_output").mkdir(parents=True, exist_ok=True)

	# construct a list of output file paths using the previous list of text files the relative path for tf_idf_output
	output_filenames = [str(txt_file).replace(".txt", ".csv").replace("txt/", "tf_idf_output/") for txt_file in fileList]

	# loop each item in transformed_documents_as_array, using enumerate to keep track of the current position

	dfs = []
	labels = []
	for counter, doc in enumerate(transformed_documents_as_array):
    	# construct a dataframe
		tf_idf_tuples = list(zip(vectorizer.get_feature_names(), doc))
		one_doc_as_df = pd.DataFrame.from_records(tf_idf_tuples, columns=['term', 'score']).sort_values(by='score', ascending=True).reset_index(drop=True)

    	# output to a csv using the enumerated value for the filename
		one_doc_as_df.to_csv(output_filenames[counter])
		dfs.append(one_doc_as_df[-10:])
		labelparts = output_filenames[counter].split("/")
		label = labelparts[1].split(".")
		labels.append(label[0])

	plot_tfidf_classfeats_h(dfs,labels)



myfiles =[]
for file in Path("txt").rglob("*.txt"):
     myfiles.append(file.parent / file.name)

myfiles.sort()

corpus = []
for file in myfiles:
    with open(file) as f:
        fileString = f.read()
    corpus.append(fileString)

getTopScores(myfiles,corpus)






