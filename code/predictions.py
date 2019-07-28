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
predicted = preds.sort_values(['ipc', 'prb'], ascending=[True, False])
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

# Calc predictions using the model and write them to file
predictions = model.predict(patent_sequences)
with open("preds.csv", 'w', newline='') as predfile:
    pred = csv.DictWriter(predfile, fieldnames=['pub','ipc','prb'])
    for p in range(patents.shape[0]):
        print(p)
        for c in range(len(ipcs_unique)):
            mute = pred.writerow({'pub': patents.pub[p],'ipc':ipcs_unique[c], 'prb':predictions[p,c]})

# Use the predictions.py to validate the model

preds = pd.DataFrame(columns=['pub','ipc','prb'])
counter = 0
for p in range(patents.shape[0]):
    counter += 1
    print(counter)
    for c in range(len(ipcs_unique)):
        preds = preds.append({'pub': patents.pub[p],'ipc':ipcs_unique[c], 'prb':predictions[p,c]},
                       ignore_index=True)

predicted = pd.DataFrame(columns=['pub','ipc','prb'])
pub_frequencies = ipcs.pub.value_counts()
preds = preds.sort_values(['pub', 'prb'], ascending=[True, False])
counter = 0
for i in preds.pub.unique():
    print(counter)
    counter += 1
    predicted = predicted.append(preds[preds.pub == i].head(pub_frequencies[i]))

        # The inner join of the predicted and original assignments would be the ipc matches
        pd.merge(ipcs, predicted[['pub', 'ipc']]).shape

