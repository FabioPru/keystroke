# Imports
import sys
import numpy as np
import pandas as pd
import json
import random
import matplotlib.pyplot as plt
import seaborn as sns
import scipy

from sklearn.experimental import enable_hist_gradient_boosting
from sklearn import base, neural_network, neighbors, feature_extraction, datasets, linear_model, metrics, model_selection, preprocessing, svm, ensemble, decomposition, feature_extraction, utils
import time

path = sys.argv[1]

s = pd.read_csv(path+'sentences.csv', index_col=False, encoding='latin1')
k = pd.read_csv(path+'keystrokes.csv', index_col=False, encoding='latin1')

# Runs in approx. 50s
k_sorted = k.sort_values(by='s_id')
rs = 0; re = 0; ranges = {}
for idx, val in k_sorted['s_id'].value_counts().sort_index().iteritems():
    re += val
    ranges[idx] = (rs, re)
    rs += val
    
for s_id, row in s.iterrows():
    if ranges.get(s_id) != None:
        t, v = ranges.get(s_id)
        k_sentence = k_sorted.iloc[t:v, :]
    else:
        k_sentence = k_sorted.iloc[0:0, :]
    
    ###### YOUR CODE HERE #####
    ## Will run ranging over sentence with s_id, row, k_sentence ##

    s.at[s_id, 'text_len'] = len(row['text'])
    s.at[s_id, 't_filter_10000'] = k_sentence['t'].apply(lambda x: min(x, 10000)).sum()
    

    ###########################

text = s.groupby('path')['text'].apply(lambda x: ' '.join(x))
st_id = s.groupby('path')['id'].min()
end_id = s.groupby('path')['id'].max()

for i, (t, sid, eid) in enumerate(zip(text,st_id,end_id)):
    file = open("../../frontend/files/my-path!" + str(i) + "!" + str(sid) + "!" + str(eid) + ".txt", "w")
    file.write(t)
    file.close()  

k.to_csv(path+'sentences.csv', index=False)
s.to_csv(path+'sentences.csv', index=False)
