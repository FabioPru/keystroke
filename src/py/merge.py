# Imports
import sys
import numpy as np
import pandas as pd
import json
import random
import matplotlib.pyplot as plt
import seaborn as sns
import scipy

path = sys.argv[1]

s = pd.read_csv(path+'sentences.csv', index_col=False, encoding='latin1')
cocogen = pd.read_csv(path+'cocogen.csv', index_col=False, encoding='latin1')


mys = pd.concat([s, cocogen], axis=1)

mys.to_csv(path+'sentences.csv', index=False)
