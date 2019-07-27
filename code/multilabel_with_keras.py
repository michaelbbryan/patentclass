import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
import datetime
from keras.models import Sequential
from keras.layers import GRU, Dense, Activation, Embedding, Flatten, GlobalMaxPool1D, Dropout, Conv1D
from keras.callbacks import ReduceLROnPlateau, EarlyStopping, ModelCheckpoint
from keras.losses import binary_crossentropy
from keras.optimizers import Adam
import matplotlib.pyplot as plt
import csv
import os

# Config to turn on JIT compilation
config = tf.ConfigProto()
config.graph_options.optimizer_options.global_jit_level = tf.OptimizerOptions.ON_1
sess = tf.Session(config=config)

os.environ["TF_XLA_FLAGS="] = "--tf_xla_cpu_global_jit"

# Set globals
GLOVE_EMBEDDING = "glove.840B.300d.txt"
OUTPUT_PATH = "logs"
MAX_WORDS = 100000          # Maximum number of words to embed, the most frequently observed
MAX_LEN = 5000              # Maximum number of words in each patent text
EMBED_SIZE = 300            # Number of latent dimensions from embedding
VALIDATION_SPLIT = 0.1      # Cross validation split
BATCH_SIZE = 32             # Number of observations per training iteration within an epoch
EPOCHS = 20                 # Number of epochs to fit the model
GATED_RECURRENT_UNITS = 512 # Size of the convolutional layer

# Get the data
patents = pd.read_csv("txtheaders.csv", dtype={"pub": str, "txt": str})
ipcs = pd.read_csv("ipcheaders.csv", dtype={"pub": str, "ipc": str})
ipcs_unique = ipcs.ipc.unique()
patent_text = patents["txt"].str.lower()

# Start the binarizer with the list of all possible codes
binarizer = MultiLabelBinarizer(classes=(ipcs_unique))
# Then use the binarizer on the set of ipc labels
ipcs_grouped = ipcs.groupby("pub")
ipcs_df = ipcs_grouped["ipc"].aggregate(lambda x: list(x)).reset_index(name="ipc")
ipcs_binarized = binarizer.fit_transform(ipcs_df["ipc"])

# Convert patent text to word tokenized sequences
tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=MAX_WORDS, lower=True, oov_token="OOV")
tokenizer.fit_on_texts(patent_text)
patent_sequences = tf.keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences(patent_text), maxlen=MAX_LEN)

# Load the Glove embeddings
embeddings_index = {}
with open(GLOVE_EMBEDDING, encoding="utf8") as f:
    for line in f:
        values = line.rstrip().rsplit(" ")
        word = values[0]
        embed = np.asarray(values[1:], dtype="float32")
        embeddings_index[word] = embed

# Apply the Glove embeddings to the tokenized words, building an embedding index
no_embedding = 0
word_index = tokenizer.word_index
num_words = min(MAX_WORDS, len(word_index) + 1)
embedding_matrix = np.zeros((num_words, EMBED_SIZE), dtype="float32")
for word, i in word_index.items():
    if i >= MAX_WORDS:
        continue
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector
        dup =  embedding_vector
    else:
        embedding_matrix[i] = dup
        no_embedding = no_embedding + 1

print(no_embedding," words have no embedding")

# Calculate the weights, cost for each class; more frequent less weighted
ipc_inv = {}
for i in ipcs_unique:
    ipc_inv[i] = 1/(ipcs['ipc']==i).sum()

total_weight = sum(ipc_inv.values())
ipc_weights = {}
w = 0
for i in ipcs_unique:
    ipc_weights[w] = ipc_inv[i]/total_weight
    w = w+1

# Define the model
model = Sequential()
model.add(Embedding(MAX_WORDS, EMBED_SIZE,input_length = MAX_LEN))
model.add(GRU(GATED_RECURRENT_UNITS, dropout=0.1, return_sequences=True))
model.add(GRU(GATED_RECURRENT_UNITS, dropout=0.1))
model.add(Dense(len(ipcs.ipc.unique()), activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Set the checkpoint and callback saves between epochs
checkpoint_path = "cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path, save_weights_only=True, verbose=1)
callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=5, monitor='val_loss'),
    tf.keras.callbacks.TensorBoard(log_dir='./logs'),
    cp_callback]

# Fit the model
print(datetime.datetime.now())
fit_history = model.fit(patent_sequences, ipcs_binarized,
#                    class_weight=ipc_weights,
                    epochs=EPOCHS,
                    batch_size=BATCH_SIZE,
                    validation_split=VALIDATION_SPLIT,
                    callbacks=callbacks)
print(datetime.datetime.now())

# Use the model history plot

# Calc predictions using the model and write them to file
predictions = model.predict(patent_sequences)
with open("preds.csv", 'w', newline='') as predfile:
    pred = csv.DictWriter(predfile, fieldnames=['pub','code','prb'])
    for p in range(patents.shape[0]):
        print(p)
        for c in range( len(ipcs_unique)):
            mute = pred.writerow({'pub': patents.pub[p],'ipc':ipcs_unique[c], 'prb':predictions[p,c]})

# Use the predictions.py to validate the model
