import pandas as pd
import Graphics as artist
import matplotlib.pyplot as plt 
import numpy as np 

import itertools

from scipy.stats import ks_2samp
from csv import DictReader
from matplotlib import rcParams 
filenames = {'before':'./data/before-intervention.csv',
			  'after':'./data/after-intervention.csv'}

big_data_set = [dict(row.items() + {'stage':stage}.items()) for stage,csvfile in filenames.iteritems()
					for row in DictReader(open(csvfile,'r'))]

#make pd
iqr = lambda data: 0.5*(np.percentile(data,75) - np.percentile(data,25))

DISPO = 'time to leaving ED'
df = pd.DataFrame(big_data_set)
df=df.convert_objects(convert_numeric=True)

#Recreate initial diagram
rcParams['text.usetex'] = True
possible_dispos = df['standardized plan'].unique()


tmp = {stage:{dispo:[] for dispo in possible_dispos} 
					for stage in filenames.iterkeys()}

gpd = df.groupby(['stage','standardized plan'])[DISPO]
for key,value in gpd.groups.iteritems():
	tmp[key[0]][key[1]] = df.ix[value][DISPO]



for possible_dispo in possible_dispos:
	if possible_dispo != 'evaluate':
		fig = plt.figure()
		ax = fig.add_subplot(111)
		artist.adjust_spines(ax)

		BEFORE = tmp['before'][possible_dispo]
		AFTER = tmp['after'][possible_dispo]

		RANGE = (min(min(BEFORE),min(AFTER)),max(max(BEFORE),max(AFTER)))
		k,p = ks_2samp(BEFORE,AFTER)
		ax.hist([BEFORE,AFTER],
				color=['k','r'], 
				label=[r'\Large \textbf{before, }$\mathbf{n=%d}$; $\mathbf{%d \pm %d}$'%(len(BEFORE),
					np.median(BEFORE),iqr(BEFORE)), r'\Large \textbf{after, }$\mathbf{n=%d}$; $\mathbf{%d \pm %d}$'%(len(AFTER),
					np.median(AFTER),iqr(AFTER))])
		ax.set_xlabel(artist.format('Time to Dispo (minutes)'))
		ax.set_ylabel(artist.format('No. of patients'))
		ax.annotate(r'\Large $\mathbf{\left(p=%.04f \right)\mathbf}$'%p,
		           xy=(3, 1), xycoords='data',
		           xytext=(0.55, 0.76), textcoords='axes fraction')
		ax.annotate(r'\Large \textbf{%s}'%(possible_dispo.capitalize()),
		           xy=(3, 1), xycoords='data',
		           xytext=(0.55, 0.82), textcoords='axes fraction')
		plt.tight_layout()
		plt.legend(frameon=False)
		plt.savefig('./imgs/distro-%s.png'%possible_dispo)

#Hue by following fields: [plan, final_dispo], hue by stage
#Sub-questions, any difference between plan and final_dispo; time to psych consult,

#Demographics: compare gender, age, indicator variable for date of service?, ICD diagnosis