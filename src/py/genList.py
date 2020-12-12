
# Imports
import sys
import numpy as np
import pandas as pd
import json

path = sys.argv[1]

df = pd.read_json(path+'df.json')
ops = pd.read_json(path+'ops.json')

cl = df.columns[4:-3]

for c in cl:
    df[c] = df[c].fillna(-1).astype(int)

print( len(df.index) )
print( path )


for i in range(1, len(df.index)):
    prevt = df.iloc[i-1, 0]
    ct = df.iloc[i, 0]
    opno = df.iloc[i, -3]
    chbank = df.iloc[i, 1]

    print( prevt )
    print( ct )

    #print("prevt ", prevt, "; ct ", ct, "; opno ", opno)    
    offset = 0
    done = 0
    pos = 0
    l = []
                
    for j in range(0, opno):
        idx = df.iloc[i,4+j];

        
        if ops.iloc[idx, 3] == '=':
            offset += ops.iloc[idx, 1]
        
        if ops.iloc[idx, 3] == '-':
            if ops.iloc[idx, 1] > 12:
                is_keystroke = 0
            else:
                is_keystroke = 1

            for t in range(0, ops.iloc[idx, 1]):
                l.append(['-', '' , offset, is_keystroke])
                
        if ops.iloc[idx, 3] == '+':
            if ops.iloc[idx, 1] > 6:
                is_keystroke = 0
            else:
                is_keystroke = 1

            for t in range(0, ops.iloc[idx, 1]):
                if done < len(chbank):
                    l.append(['+', chbank[done], offset, is_keystroke])   
                else:
                    l.append(['+', "", offset, is_keystroke])   
                offset += 1
                done += 1
                
    print( len(l) )
    for r in l:
        for j in range(0, 4):
            if r[j] == "\n":
                print( "\\n" )
            elif r[j] == " ":
                print( "#" )
            elif r[j] == "\"":
                print( "\"\"" )
            else:
                if j == 1:
                    print( r[j] ) 
                else:
                    print( r[j] )