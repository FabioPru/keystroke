import sys
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import string

suffix = ''
# keystroke,word,sentence,file,user dataframe
k = pd.read_csv('../../pads/keystrokes' + suffix + '.csv',
                index_col=False, encoding='latin1')
w = pd.read_csv('../../pads/words' + suffix + '.csv', index_col=False)
s = pd.read_csv('../../pads/sentences' + suffix + '.csv', index_col=False)
f = pd.read_csv('../../pads/files' + suffix + '.csv', index_col=False)
u = pd.read_csv('../../pads/users' + suffix + '.csv', index_col=False)

k_sorted = k.sort_values(by='f_id')
rs = 0
re = 0
ranges = {}
for idx, val in k_sorted['f_id'].value_counts().sort_index().iteritems():
    re += val
    ranges[idx] = (rs, re)
    rs += val

for f_id, row in f.iterrows():
    if ranges.get(f_id) != None:
        u, v = ranges.get(f_id)
        k_file = k_sorted.iloc[u:v, :]
    else:
        k_file = k_sorted.iloc[0:0, :]
    #######
    text = f.at[f_id, 'text']
    for idx, row in k_file.iterrows():
        ps = row['pos']
        if ps < len(text)-1 and ps > 0:
            if text[ps].isalpha() or text[ps].isdigit():
                if text[ps-1].isalpha() or text[ps-1].isdigit():
                    # inside a word
                    k.at[idx, 'keyst_type'] = 0
                else:
                    if ps > 1 and text[ps-1] == ' ' and text[ps-2] == '.':
                        # space after period/comma/etc.
                        k.at[idx, 'keyst_type'] = 4
                    elif text[ps-1] == ' ':
                        # space after word before word
                        k.at[idx, 'keyst_type'] = 2
                    else:
                        k.at[idx, 'keyst_type'] = -1
            elif text[ps] == ' ':
                if (text[ps-1].isalpha() or text[ps-1].isdigit()) and (text[ps+1].isalpha() or text[ps+1].isdigit()):
                    # last character of word
                    k.at[idx, 'keyst_type'] = 1
                elif (text[ps+1].isalpha() or text[ps+1].isdigit()) and text[ps-1] == '.':
                    # period (end of sentence)
                    k.at[idx, 'keyst_type'] = 3
                else:
                    k.at[idx, 'keyst_type'] = -1
            else:
                k.at[idx, 'keyst_type'] = -1

        else:
            # first or last char of file
            k.at[idx, 'keyst_type'] = -1


k.to_csv('../../pads/keystrokes.csv', index=False)
