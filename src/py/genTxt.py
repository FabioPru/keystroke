
# Imports
import sys
import numpy as np
import pandas as pd
import json

path = sys.argv[1]

k = pd.read_csv(path+'keystroke.csv', index_col=False, encoding='latin1')

s = [' ' for _ in range(k['pos'].max() + 2)]

for idx, row in k.iterrows():
    try:
        if row['op'] == '+':
            s[row[3]] = row[2]
    except:
        pass

for c in s:
    if c == "\\n":
        print("")
    else:        
        print(c, end='')