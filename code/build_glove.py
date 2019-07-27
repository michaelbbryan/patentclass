"""
Build a patent text word embedding of the 2018 grant text using GloVe
"""
import tensorflow as tf
import pandas as pd
from glove import Corpus, Glove

MAX_WORDS = 200000
MAX_LEN = 200000

patents = pd.read_csv("txtheaders.csv")
patent_text = patents["txt"].str.lower()
tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=MAX_WORDS, lower=True, oov_token="OOV")
tokenizer.fit_on_texts(patent_text)
patent_sequences = tf.keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences(patent_text), maxlen=MAX_LEN)

patent_words = []
for t in range(patent_sequences.shape[0]):
    pt1 = tokenizer.sequences_to_texts(patent_sequences[t].reshape(1, MAX_LEN))
    pt2 = [x for x in pt1[0].split(" ") if
           not any(char.isdigit() for char in x)
           and len(x)<16]
    patent_words.extend(pt2)

corpus = Corpus()
corpus.fit(patent_words, window=20)
embeddings = Glove(no_components=200, learning_rate=0.05)
embeddings.fit(corpus.matrix, epochs=30, no_threads=4, verbose=True)
embeddings.add_dictionary(corpus.dictionary)
embeddings.save('patent.glove')
# embeddings = glove.load('patent.glove')

print(embeddings.word_vectors[embeddings.dictionary['computer']])
