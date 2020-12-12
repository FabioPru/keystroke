
# Imports
import sys
import numpy as np
import pandas as pd
import json

path = sys.argv[1]
writeto = sys.argv[2]

df = pd.read_json(path+'df.json')
ops = pd.read_json(path+'ops.json')

cl = df.columns[4:-3]

for c in cl:
    df[c] = df[c].fillna(-1).astype(int)

s = pd.DataFrame(columns=['st', 'et', 'char_bank', 'offset', 'opcode'])

def incIfAtLeast(x, val, trsh):
    if x >= trsh:
        return x+val
    else:
        return x

def incIfExactly(x, val, trsh):
    if x == trsh:
        return x+val
    else:
        return x

def roundUp(x):
    if ((x * 2) % 2) == 1:
        return x + 0.5
    else:
        return x

for i in range(1, len(df.index)):
    prevt = df.iloc[i-1, 0]
    ct = df.iloc[i, 0]
    opno = df.iloc[i, -3]
    chbank = df.iloc[i, 1]
    #print("prevt ", prevt, "; ct ", ct, "; opno ", opno)    
    offset = 0
    done = 0
    pos = 0
    l = []
                
    for j in range(0, opno):
        idx = df.iloc[i,4+j];
        #print("op no ", j, " id ", idx, " opcode ", ops.iloc[idx, 3], " chars ", ops.iloc[idx, 1])
        
        if ops.iloc[idx, 3] == '=':
            offset += ops.iloc[idx, 1]
        
        if ops.iloc[idx, 3] == '-':
            for t in range(0, ops.iloc[idx, 1]):
                l.append(['-', '' , offset])
                
        if ops.iloc[idx, 3] == '+':
            for t in range(0, ops.iloc[idx, 1]):
                l.append(['+', chbank[done] , offset])   
                offset += 1
                done += 1
                
    for k in range(0, len(l)):
        pos = l[k][2]
        if l[k][0] == '+':
            s['offset'] = s['offset'].apply(func=incIfAtLeast, args=(1, pos,))

        if l[k][0] == '-':
            #deleting something makes it negative so it doesn't get pushed
            #s['offset'] = s['offset'].apply(func=negativize, args=(pos,))
            s['offset'] = s['offset'].apply(func=incIfExactly, args=(-0.5, pos,))
            s['offset'] = s['offset'].apply(func=incIfAtLeast, args=(-1, pos+1,))
            pos -= 0.5

            
        s = s.append({'st': prevt + (k)*(ct - prevt)/(len(l)), 'et': prevt + (k+1)*(ct - prevt)/(len(l)), 'char_bank': l[k][1], 'offset': pos, 'opcode': l[k][0]}, ignore_index=True)
            
    
s['offset'] = s['offset'].apply(func=roundUp)

s['path'] = path

s = s.astype({"st": int, "et": int, "offset": int})

with open(writeto+'keystrokes.csv', 'a') as f:
    s.to_csv(f, index = None, header=False, encoding='utf-8')

