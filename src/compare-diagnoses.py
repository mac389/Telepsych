import pandas as pd
import Graphics as artist
import matplotlib.pyplot as plt 
import numpy as np 

import itertools

from scipy.stats import ks_2samp
from csv import DictReader
from collections import Counter
from FisherExact import fisher_exact
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import percentileofscore
filenames = {'before':'./data/before-intervention.csv',
			  'after':'./data/after-intervention.csv'}

big_data_set = [dict(row.items() + {'stage':stage}.items()) for stage,csvfile in filenames.iteritems()
					for row in DictReader(open(csvfile,'r'))]

def process(key):
	code = None
	try:
		code = key.split('^')[1].split('.')[0]
	except:
		pass 
	return code

def count(lst,token):
	count = 0
	for item in lst:
		if type(item) == str and token in item:
			count += 1
	return count

#make pd
iqr = lambda data: 0.5*(np.percentile(data,75) - np.percentile(data,25))

df = pd.DataFrame(big_data_set)

#BEFORE
#How many with codable diagnoses?
BEFORE = df.loc[df['stage']=='before']
AFTER = df.loc[df['stage']=='after']

ICDS = {'BEFORE':dict(Counter(list(itertools.chain.from_iterable(BEFORE.filter(regex='Diag_*').values)))),
'AFTER': dict(Counter(list(itertools.chain.from_iterable(AFTER.filter(regex='Diag_*').values))))}

combined_keys = list(itertools.chain.from_iterable([ICDS[x].keys() for x in ICDS]))
combined_keys = map(process,combined_keys)
combined_keys = list(set([key for key in combined_keys if key]))

combined = pd.DataFrame([{"before": count(ICDS['BEFORE'],key),
						 "after": count(ICDS['AFTER'],key)} 
						 for key in combined_keys], index=combined_keys)


bootstraps = []
data = np.array(combined.values, dtype=int)
n_iterations = 10000
bootstraps += [cosine_similarity(data.T)[0,1]]
for _ in xrange(n_iterations):
	np.random.shuffle(data[:,-1])
	bootstraps += [cosine_similarity(data.T)[0,1]]
bootstraps = np.array(bootstraps)
np.savetxt('bootstraps.csv',1000*bootstraps, delimiter=',', fmt='%d')

print 100-percentileofscore(bootstraps,bootstraps[0])