import collections
import pathlib
import re
import string
import sys

import tensorflow as tf

from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras import preprocessing
from tensorflow.keras import utils
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization

import tensorflow_text as tf_text


FILE_NAMES = ["edgar_allan_poe_lines.txt","edna_millay_lines.txt","gertrude_stein_lines.txt"]
BUFFER_SIZE = 50000
BATCH_SIZE = int(sys.argv[1])
VALIDATION_SIZE = 500
VOCAB_SIZE = 10000
MAX_SEQUENCE_LENGTH = 250


AUTOTUNE = tf.data.experimental.AUTOTUNE

#tf.config.set_visible_devices([], 'GPU')

def configure_dataset(dataset):
  return dataset.cache().prefetch(buffer_size=AUTOTUNE)

def labeler(example, index):
  return example, tf.cast(index, tf.int64)

def create_model(vocab_size, num_labels):
  model = tf.keras.Sequential([
      layers.Embedding(vocab_size, 64, mask_zero=True),
      layers.Conv1D(64, 5, padding="valid", activation="relu", strides=2),
      layers.GlobalMaxPooling1D(),
      layers.Dense(num_labels)
  ])
  return model


parent_dir = "./"




labeled_data_sets = []

for i, file_name in enumerate(FILE_NAMES):
  lines_dataset = tf.data.TextLineDataset(str(file_name))
  labeled_dataset = lines_dataset.map(lambda ex: labeler(ex, i))
  labeled_data_sets.append(labeled_dataset)

all_labeled_data = labeled_data_sets[0]
for labeled_dataset in labeled_data_sets[1:]:
  all_labeled_data = all_labeled_data.concatenate(labeled_dataset)

all_labeled_data = all_labeled_data.shuffle(
    BUFFER_SIZE, reshuffle_each_iteration=False)

for text, label in all_labeled_data.take(10):
  print("Sentence: ", text.numpy())
  print("Label:", label.numpy())

tokenizer = tf_text.UnicodeScriptTokenizer()

def tokenize(text, unused_label):
  lower_case = tf_text.case_fold_utf8(text)
  return tokenizer.tokenize(lower_case)

tokenized_ds = all_labeled_data.map(tokenize)

for text_batch in tokenized_ds.take(5):
  print("Tokens: ", text_batch.numpy())


tokenized_ds = configure_dataset(tokenized_ds)

vocab_dict = collections.defaultdict(lambda: 0)
for toks in tokenized_ds.as_numpy_iterator():
  for tok in toks:
    vocab_dict[tok] += 1

vocab = sorted(vocab_dict.items(), key=lambda x: x[1], reverse=True)
vocab = [token for token, count in vocab]
#vocab = vocab[:VOCAB_SIZE]
vocab_size = len(vocab)
print("Vocab size: ", vocab_size)
print("First five vocab entries:", vocab[:5])


keys = vocab
values = range(2, len(vocab) + 2)  # reserve 0 for padding, 1 for OOV

init = tf.lookup.KeyValueTensorInitializer(
    keys, values, key_dtype=tf.string, value_dtype=tf.int64)

num_oov_buckets = 1
vocab_table = tf.lookup.StaticVocabularyTable(init, num_oov_buckets)


def preprocess_text(text, label):
  standardized = tf_text.case_fold_utf8(text)
  tokenized = tokenizer.tokenize(standardized)
  vectorized = vocab_table.lookup(tokenized)
  return vectorized, label



example_text, example_label = next(iter(all_labeled_data))
print("Sentence: ", example_text.numpy())
vectorized_text, example_label = preprocess_text(example_text, example_label)
print("Vectorized sentence: ", vectorized_text.numpy())

#training

all_encoded_data = all_labeled_data.map(preprocess_text)
train_data = all_encoded_data.skip(VALIDATION_SIZE).shuffle(BUFFER_SIZE)
validation_data = all_encoded_data.take(VALIDATION_SIZE)

train_data = train_data.padded_batch(BATCH_SIZE)
validation_data = validation_data.padded_batch(BATCH_SIZE)

#print info

sample_text, sample_labels = next(iter(validation_data))
print("Text batch shape: ", sample_text.shape)
print("Label batch shape: ", sample_labels.shape)
print("First text example: ", sample_text[0])
print("First label example: ", sample_labels[0])

#housekeeping

vocab_size += 2
train_data = configure_dataset(train_data)
validation_data = configure_dataset(validation_data)

#train model

model = create_model(vocab_size=vocab_size, num_labels=3)
model.compile(
    optimizer='adam',
    loss=losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy'])
history = model.fit(train_data, validation_data=validation_data, epochs=3)

loss, accuracy = model.evaluate(validation_data)

print("Loss: ", loss)
print("Accuracy: {:2.2%}".format(accuracy))

#export
preprocess_layer = TextVectorization(
    max_tokens=vocab_size,
    standardize=tf_text.case_fold_utf8,
    split=tokenizer.tokenize,
    output_mode='int',
    output_sequence_length=MAX_SEQUENCE_LENGTH)
preprocess_layer.set_vocabulary(vocab)

export_model = tf.keras.Sequential(
    [preprocess_layer, model,
     layers.Activation('sigmoid')])

export_model.compile(
    loss=losses.SparseCategoricalCrossentropy(from_logits=False),
    optimizer='adam',
    metrics=['accuracy'])

# Create a test dataset of raw strings
test_ds = all_labeled_data.take(VALIDATION_SIZE).batch(BATCH_SIZE)
test_ds = configure_dataset(test_ds)
loss, accuracy = export_model.evaluate(test_ds)
print("Loss: ", loss)
print("Accuracy: {:2.2%}".format(accuracy))





ashberies = open("files_list.txt", "r");
ashbey_files = ashberies.readlines()
outFile = open("poet_classifications.txt", "w", encoding="utf-8")

for ashFile in ashbey_files:
	ashFile = ashFile.strip('\n')
	aFile = open(ashFile, "r")
	ashLines = aFile.readlines()
	if len(ashLines) >= 1:
		predicted_scores = export_model.predict(ashLines)
		predicted_labels = tf.argmax(predicted_scores, axis=1)
		labelOneSum = 0.0;
		labelTwoSum = 0.0;
		labelThreeSum = 0.0;
		lbl_cnt1 = 1;
		lbl_cnt2 = 1;
		lbl_cnt3 = 1;
		for input, label, score in zip(ashLines, predicted_labels, predicted_scores):
	  		if(label.numpy() == 0):
	  			labelOneSum = labelOneSum + score[0]
	  			lbl_cnt1 = lbl_cnt1 + 1
	  		if(label.numpy() == 1):
	  			labelTwoSum = labelTwoSum + score[1]
	  			lbl_cnt2 = lbl_cnt2 + 1
	  		if(label.numpy() == 2):
	  			labelThreeSum = labelThreeSum + score[2]
	  			lbl_cnt3 = lbl_cnt3 + 1
	  	
		if lbl_cnt1 > 1:
	  		lbl_cnt1 = lbl_cnt1 - 1;
		if lbl_cnt2 > 1:
	  		lbl_cnt2 = lbl_cnt2 - 1;
		if lbl_cnt3 > 1:
	  		lbl_cnt3 = lbl_cnt3 - 1;
	  		
		oneAvg = labelOneSum/lbl_cnt1
		twoAvg = labelTwoSum/lbl_cnt2
		threeAvg = labelThreeSum/lbl_cnt3

		asFileParts = ashFile.split("/")
		outName = "gen_" + asFileParts[len(asFileParts)-1]
		outString = outName + " " + str(oneAvg) + " " + str(twoAvg) + " " + str(threeAvg) + "\n"
		outFile.write(outString)
	else:
		asFileParts = ashFile.split("/")
		outName = "gen_" + asFileParts[len(asFileParts)-1]
		outString = outName + " " + "0.0 0.0 0.0" "\n"
		outFile.write(outString)

outFile.close()

poetOneList = []
poetTwoList = []
poetThreeList = []

clFile = open("poet_classifications.txt", "r")
lines = clFile.readlines()
clFile.close()

for line in lines:
	data = line.split(" ")
	if(data[1] > data[2] and data[1] > data[3]):
		poetOneList.append(data[0])
	if(data[2] > data[1] and data[2] > data[3]):
		poetTwoList.append(data[0])
	if(data[3] > data[2] and data[3] > data[1]):
		poetThreeList.append(data[0])

poetOne = open("poetOne_files.txt", "w", encoding="utf-8")

for file in poetOneList:
	poetOne.write(file+"\n")

poetOne.close()

poetTwo = open("poetTwo_files.txt", "w", encoding="utf-8")

for file in poetTwoList:
	poetTwo.write(file+"\n")

poetTwo.close()

poetThree = open("poetThree_files.txt", "w", encoding="utf-8")

for file in poetThreeList:
	poetThree.write(file+"\n")

poetThree.close()








