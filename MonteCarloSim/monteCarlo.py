# -*- coding: utf-8 -*-
"""
@author: Sriraj
"""

import yfinance as yf
import pandas as pd
from scipy.stats import lognorm
import numpy as np
from multiprocessing import Process, Queue

tracked = pd.read_csv("trackedTickers.csv")
tickOut = pd.read_csv("tickerOutput.csv")

def runSim(row, result_queue):
    if(tracked.iloc[row]['executed']==1):
        return
    ticker = yf.Ticker(tracked.iloc[row]['tickers'])
    print("executing " + tracked.iloc[row]['tickers'])
    hist = ticker.history(start='2024-07-01', end='2025-02-01')
    df = pd.DataFrame(hist)
    nLog = np.log(df['Open'])
    
    sumu = 0
    
    n = 10000
    
    
    for i in range(n):
        sample = lognorm.rvs(nLog.std(), scale = np.exp(nLog.mean()), size = 10000)
        sumu = sumu + sample.mean()
    
    m = sumu/n
    
    result_queue.put((row, m))

if __name__ == "__main__":
    result_queue = Queue()
    processes = []
    for i in range(len(tracked)):
        p = Process(target=runSim, args=(i,result_queue))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
        
    while not result_queue.empty():
        row, m = result_queue.get()
        tracked.at[row, 'executed'] = 1
        tickOut.loc[len(tickOut)] = [tracked.iloc[row]['tickers'], m]
    
    tracked.to_csv('trackedTickers.csv', index=False)
    tickOut.to_csv('tickerOutput.csv', index=False)