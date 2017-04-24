import pandas as pd
import Graphics as artist
import matplotlib.pyplot as plt 

import itertools

from scipy.stats import ks_2samp
from csv import DictReader
from matplotlib import rcParams 
from scipy.stats import mannwhitneyu
filenames = {'before':'./data/before-time-to-dc.csv',
			  'after':'./data/after-time-to-dc.csv'}

big_data_set = [dict(row.items() + {'stage':stage}.items()) for stage,csvfile in filenames.iteritems()
					for row in DictReader(open(csvfile,'r'))]

#make pd

DISPO = 'time to leaving ED'
DISPO = 'time to dc home'
df = pd.DataFrame(big_data_set)
df=df.convert_objects(convert_numeric=True)

#Recreate initial diagram
rcParams['text.usetex'] = True

BEFORE = df.loc[df['stage']=='before',DISPO]
AFTER = df.loc[df['stage']=='after',DISPO]
RANGE = (df[DISPO].min(),df[DISPO].max())

print mannwhitneyu(BEFORE,AFTER)

print BEFORE.median(),1.57*0.5*(BEFORE.quantile(.75)-BEFORE.quantile(.25))/float(len(BEFORE)) 
print AFTER.median(), 1.57*0.5*(AFTER.quantile(.75)-AFTER.quantile(.25)) /float(len(AFTER))
'''
					Median     IQR
		before     844.5 7.33628676471
		after	   631.5 12.9961111111
'''

'''
fig = plt.figure()
ax = fig.add_subplot(111)
artist.adjust_spines(ax)
k,p = ks_2samp(BEFORE.values,AFTER.values)
ax.hist([BEFORE.values,AFTER.values],
		color=['k','r'], label=[artist.format('before (n=%d)'%(len(BEFORE))), 
		artist.format('after (n=%d)'%(len(AFTER)))],range=RANGE)
ax.set_xlabel(artist.format('Time to Dispo (minutes)'))
ax.set_ylabel(artist.format('No. of patients'))
ax.annotate(r'\Large $\mathbf{\left(p=%.04f \right)\mathbf}$'%p,
            xy=(3, 1), xycoords='data',
            xytext=(0.71, 0.82), textcoords='axes fraction')
plt.tight_layout()
plt.legend(frameon=False)
plt.savefig('./imgs/dispo-distro-third-table.png')
'''
#Hue by following fields: [plan, final_dispo], hue by stage
#Sub-questions, any difference between plan and final_dispo; time to psych consult,

#Demographics: compare gender, age, indicator variable for date of service?, ICD diagnosis