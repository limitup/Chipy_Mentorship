#! usr/bin/python3

import json
import pandas as pd
import numpy as np
from pandas.tseries.offsets import MonthEnd

# Open file and save data in contents variable
with open('./PET.txt') as json_file:
   # Returns a list of JSON objects
   contents = json_file.readlines()
json_file.close()


# Example of JSON object in PET.txt file.  Each object has an array for the data.


# {"series_id":"PET.EMM_EPMR_PTE_R10_DPG.W",
# "name":"East Coast Regular All Formulations Retail Gasoline Prices, Weekly",
# "units":"Dollars per Gallon",
# "f":"W","unitsshort":"$\/gal",
# "description":"East Coast Regular All Formulations Retail Gasoline Prices",
# "copyright":"None","source":"EIA, U.S. Energy Information Administration",
# "geography":"USA-CT+USA-DC+USA-DE+USA-FL+USA-GA+USA-MA+USA-MD+USA-ME+USA-NC+USA-NH+USA-NJ+USA-NY+USA-PA+USA-RI+USA-SC+USA-VA+USA-VT+USA-WV",
# "start":"19920511","end":"20170417",
# "last_updated":"2017-04-18T10:08:52-04:00",
# "data":[["20170417",2.397],
# 		["20170410",2.374],
# 		["20170403",2.303],
# 		["20170327",2.276],
# 		["20170320",2.266],
# 		["20170313",2.273],
# 		...
# 		["20170306",2.285],
# 		["20170227",2.286],
# 		["20170220",2.294],
# 		["20170213",2.293],
# 		["20170206",2.301],
# 		["20170130",2.32]]}
# {"series_id":"PET.EMM_EPMR_PTE_R10_DPG.W",
# "name":"East C............



#list of JSON objects converted python dictionaries
js_data = [json.loads(x) for x in contents]


# function
def monthly_data(items):
	#iterate k:v pair in dicitonary
	for key,value in item.items():
		#boolean for key
		# print (key,value)
		if key == 'category_id':
  			continue
		elif key == 'series_id' and value.endswith('.M'):
			# print (value)
			####show example of data####
			for k,v in item.items():
				if k == 'data':
                    # Parse dates from array[:,0] for datetime index
					dates = [x[:4]+'/'+x[4:] for x in np.array(v)[:,0]]
					data_points = np.array(v)[:,1]
					# print (type(data_points[:,0]))
					df = pd.DataFrame(data_points,index=dates,columns=[value])

					df= df.reset_index()
					df['index'] = pd.to_datetime(df['index']) + MonthEnd(1)
					df= df.set_index('index')
					return df

#iterate list of dictionaries
data=[]
for item in js_data:
	# d = monthly_data(item)
	# monthly_data(item)
	# print (type(d))
	data.append(monthly_data(item))
# print (data)
df = pd.concat(data,axis=1,verify_integrity=True)
df.to_csv('monthly_crude_data.csv',chunksize= 5000)
