"""
Follwing the model fitting
this material applies the predicted probabilities (output of the multilabel model)
to calculate accuracy and error
"""

import pandas as pd

ipcs = pd.read_csv("ipcheaders.csv", dtype={"pub": str, "ipc": str})
preds = pd.read_csv("preds.dat", dtype={"pub": str, "ipc": str, "prb": float})
preds = preds.sort_values(['ipc', 'prb'], ascending=[True, False])

ipc_frequencies = ipcs.ipc.value_counts()

counter = 0
for i in ipc_frequencies:
    counter += 1
    predicted = predicted.append(preds[preds.ipc == i].head(ipc_frequencies[i]))

# The inner join of the predicted and original assignments would be the ipc matches
pd.merge(ipcs,predicted[['pub','ipc']]).shape
ipcs.shape

    correct = 0
    incorrect = 0
    missing = 0
    observed =  ipcs[ipcs.ipc == i].pub.tolist()
    success = len(set(predicted) & set(observed))
    correct = correct + success
    missing = missing + len(predicted) - success
    print(counter,i,correct,incorrect,missing)


i = "G06F3"
