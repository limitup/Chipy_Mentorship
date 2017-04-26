import json
import pandas as pd
import numpy as np
from pandas.tseries.offsets import MonthEnd


# Open file and save data in contents variable
with open('./PET.txt') as json_file:
   # Returns a list of JSON objects
   contents = json_file.readlines()
json_file.close()

#list of dictionaries
js_data = [json.loads(x) for x in contents]


def monthly_data(items):
	#iterate k:v pair in dicitonary
	for key,value in item.items():
		#boolean for key
		# print (key,value)
		if key == 'category_id':
			continue
		elif key == 'series_id' and value.endswith('.M'):
			# print (value)
			for k,v in item.items():
				if k == 'data':
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
df.to_csv('monthly_crude_data.csv')
