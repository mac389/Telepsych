import pandas as pd
import Graphics as artist
import matplotlib.pyplot as plt 
import numpy as np 

import itertools

from scipy.stats import ks_2samp
from csv import DictReader
from matplotlib import rcParams 
from collections import Counter 
filenames = {'before':'./data/before-intervention.csv',
			  'after':'./data/after-intervention.csv'}

big_data_set = [dict(row.items() + {'stage':stage}.items()) for stage,csvfile in filenames.iteritems()
					for row in DictReader(open(csvfile,'r'))]

#make pd
iqr = lambda data: 0.5*(np.percentile(data,75) - np.percentile(data,25))

DISPO = 'time to leaving ED'
df = pd.DataFrame(big_data_set)
print df.columns
#Are ages different?
'''
age_before = np.array(df['Age'].loc[df['stage']=='before'].values).astype(int)
print np.median(age_before), iqr(age_before)

age_after = np.array(df['Age'].loc[df['stage']=='after'].values).astype(int)
print np.median(age_after), iqr(age_after)
'''
gender_before = df['Sex'].loc[df['stage']=='before'].values
print dict(Counter(gender_before))

gender_after = df['Sex'].loc[df['stage']=='after'].values
print dict(Counter(gender_after))

'''
        Median IQR 
Before  40.0 14.0
After   40.0 14.125

'''