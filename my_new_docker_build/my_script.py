
import json
import numpy as np
import os
import pandas as pd
import urllib.request

# connect to poloniex's API
url = 'https://api.binance.com/api/v1/klines?symbol=XRPBTC&interval=1d'

# parse json returned from the API to Pandas DF
openUrl = urllib.request.urlopen(url)
r = openUrl.read()
openUrl.close()
d = json.loads(r.decode())
df = pd.DataFrame(d,columns=['opentime', 'open', 'high', 'low', 'close','volume','closetime','assetvolume','trades','bav','qav','ignore'])

original_columns=[u'opentime', u'open', u'high', u'low', u'close',u'volume',u'closetime',u'assetvolume',u'trades',u'bav',u'qav',u'ignore']
new_columns = ['opentime', 'open', 'high', 'low', 'close','volume','closetime','assetvolume','trades','bav','qav','ignore']
df = df.loc[:,original_columns]
df.columns = new_columns
df.to_csv("C:\\MyProjects\\python\\my_new_docker_build\\xrp2015to2017.csv",index=None)