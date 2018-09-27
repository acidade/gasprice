import requests
import pandas as pd
import time
import datetime

# config: save to csv every 'n_rounds'; get gasprices every 'waittime' seconds; 'filename'; 'csv_separator'
n_rounds = 10
waittime = 1
filename = 'gasprices'
csv_separator = ';'

# start timestamp for csv file to make sure to have a unique filename when saving
time_start = time.time()
timestamp_file = datetime.datetime.fromtimestamp(time_start).strftime('%Y%m%d%H%M%S')

# define dataframe
cols = ['timestamp', 'etherchain_safeLow', 'etherchain_standard', 'ethgasstation_safeLow', 'ethgasstation_standard']
df = pd.DataFrame(data=None, index=None, columns=cols)
#display(df)

count = 0

# start endless loop. Press Ctrl+C to stop
while True:
  
  try:
    # Get JSON from https://www.etherchain.org/api/gasPriceOracle and https://ethgasstation.info/json/ethgasAPI.json
    etherchain = requests.get('https://www.etherchain.org/api/gasPriceOracle').json()
    gasstation = requests.get('https://ethgasstation.info/json/ethgasAPI.json').json()

    etherchain_low = float(etherchain['safeLow'])
    etherchain_std = float(etherchain['standard'])

    gasstation_low = gasstation['safeLow']/10
    gasstation_std = gasstation['average']/10
  
    # timestamp for ETHGasStation safeLow output
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} SafeLow: {gasstation_low}')

    # add values to dataframe
    vals = [timestamp, etherchain_low, etherchain_std, gasstation_low, gasstation_std]
    df = df.append(dict(zip(cols, vals)), ignore_index=True)
    #display(df)
  
    count += 1

    # after n_rounds, write dataframe to file
    if count == n_rounds:
      outputfile = filename+'_'+timestamp_file+'.csv'
      print(f'Writing data to file: {outputfile}')
      df.to_csv(outputfile, sep=csv_separator)
      count = 0

    time.sleep(waittime)

  # catching Ctrl+C...
  except KeyboardInterrupt:
    print(' --> Exit through KeyboardInterrupt')
    break

  # catching if something else goes wrong... probably a problem with server responses
  except:
    print('Fail: something went wrong. Trying again...')