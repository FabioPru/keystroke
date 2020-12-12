# Imports
import sys
import numpy as np
import pandas as pd
import json

path = sys.argv[1]
writeto = sys.argv[2]
id_start = int(sys.argv[3])

s = pd.read_csv(path+'sentence.csv', index_col=False, encoding='latin1')
k = pd.read_csv(path+'keystroke.csv', index_col=False, encoding='latin1')

# GIVE A PROVISORY ID
s['id'] = -1
k['s_id'] = -1
ctr = 0
for i in range(0,len(s)):
    s.iloc[i, 4] = ctr
    ctr += 1

for i in range(0,len(s)):
    start = s.iloc[i, 1]
    end = s.iloc[i, 2]
    if i != 0:
        start = s.iloc[i-1, 2]


    k.loc[(k['pos'] >= start) & (k['pos'] < end), 's_id'] = s.iloc[i, 4]

k = k[k['s_id'] != -1]

# DELETE COPY PASTED SENTENCES
def dropSentence (id):
    global s
    global k
    s = s[s.id != id]
    k = k[k.s_id != id]

# Removing copy pasted sentences
ids_to_remove = set()
for j in range(0, len(s)):
    allowance = 0
    vc = k[(k['s_id'] == j) & (k['op'] == '+')]['t'].value_counts()
    if len(vc) <= 2:
        ids_to_remove.add(j)
    elif (100 * (vc.iloc[0] + vc.iloc[1])) > (90 * len(s.iloc[j,0])):
        ids_to_remove.add(j)

    for idx, val in vc.iteritems():
        if idx < 80:
            allowance += 1
    if allowance > 8:
        ids_to_remove.add(j)

# Removing long (>20 char) sentences that were deleted all at once
for j in range(0, len(s)):
    allowance = 0
    vc = k[(k['s_id'] == j) & (k['op'] == '-')]['t'].value_counts()
    if len(vc) >= 2 and len(k[(k['s_id'] == j) & (k['op'] == '-')]['t']) > 20:
        if (100 * (vc.iloc[0] + vc.iloc[1])) > (90 * len(s.iloc[j,0])):
            ids_to_remove.add(j)

    for idx, val in vc.iteritems():
        if idx < 60:
            allowance += 1
    if allowance > 10:
        ids_to_remove.add(j)
# Removing sentences less than 20 chars long
for j in range(0, len(s)):
    if len(s.iloc[j, 0]) < 20:
        ids_to_remove.add(j)

    if s.iloc[j, 0].count('\n') > 2:
        ids_to_remove.add(j)

# Removing sentences that have chars in the final text that are not part of the keystrokes

def lessOrEqualLatin (str1, str2):
    l = 'poiuytrewqlkjhgfdsamnbvcxzPOIUYTREWQKLJHGFDSAMNBVCXZ'
    d = {}
    mistakes = 0; length = 0;
    for c in l:
        d[c] = 0
    for char in str2:
        if char in l:
            d[char] += 1
            length += 1
    for char in str1:
        if char in l:
            d[char] -= 1
    for c in l:
        if d[c] < 0:
            mistakes -= d[c]
    if 30 * mistakes > length:
        return False
    return True

for j in range(0, len(s)):
    st = ""
    for idx, val in k[(k['s_id'] == j) & (k['op'] == '+')]['char'].iteritems():
        st += str(val)
    #print s.iloc[j,0]
    #print st
    if lessOrEqualLatin(s.iloc[j, 0], st) == False:
        ids_to_remove.add(j)

    if len(s.iloc[j, 0]) > len(st) + 5:
        ids_to_remove.add(j)


if len(ids_to_remove) > 0:
	print(  "		     Removed ", len(ids_to_remove), " copy pasted sentences")

for id in ids_to_remove:
    dropSentence(id) 

k['s_id'] = -1

# GIVE A TRUE ID
for i in range(0,len(s)):
    s.iloc[i, 4] = id_start
    id_start += 1

for i in range(0,len(s)):
    start = s.iloc[i, 1]
    end = s.iloc[i, 2]
    if i != 0:
        start = s.iloc[i-1, 2]
    k.loc[(k['pos'] >= start) & (k['pos'] <= end), 's_id'] = s.iloc[i, 4]

# Removing keystrokes that don't belong to any sentence
k = k[k['s_id'] != -1]


with open(writeto+'keystrokes.csv', 'a') as f1:
    k.to_csv(f1, index = None, header=False, encoding='utf-8')

with open(writeto+'sentences.csv', 'a') as f2:
    s.to_csv(f2, index = None, header=False, encoding='utf-8')

with open('../sh/accumulator.out', 'w') as the_file:
    the_file.write(str(id_start))

print ( "                Wrote ", len(s), " sentences, ", len(k), " keystrokes to file")
