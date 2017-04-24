import json

from csv import DictReader
from matplotlib import rcParams

import numpy as np 
import Graphics as artist
import matplotlib.pyplot as plt

filenames = {'before':'./data/before-intervention.csv',
			  'after':'./data/after-intervention.csv'}

def get_times(kwd):
	with open(kwd,'rb') as csvfile:
		reader = DictReader(csvfile)
		
		d = [row for row in reader]
	x = [item['time to leaving ED'] for item in d]
	return [int(item) for item in x if item != '']

iqr = lambda data: 0.5*(np.percentile(data,75) - np.percentile(data,25))

data = {time:get_times(filenames[time]) for time in filenames.keys()}
	
print np.median(data['before']),iqr(data['before'])
print np.median(data['after']), iqr(data['after'])

from scipy.stats import ks_2samp

print ks_2samp(data['before'],data['after'])

'''
rcParams['text.usetex'] = True

fig = plt.figure()
ax = fig.add_subplot(111)
artist.adjust_spines(ax)
ax.hist(data['before'],color='k',alpha=0.9,
		label=artist.format('before (n=%d)'%(len(data['before']))), range=(0,6000))
ax.hist(data['after'],color='r',alpha=0.6,
		label=artist.format('after (n=%d)'%(len(data['after']))), range=(0,6000))
ax.set_xlabel(artist.format('Time to Dispo (minutes)'))
ax.set_ylabel(artist.format('No. of patients'))
plt.tight_layout()
plt.legend(frameon=False)
plt.savefig('./imgs/dispo-distro.png')
'''