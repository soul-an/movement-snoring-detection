#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 15:44:27 2019

@author: tauro
"""
import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt


import glob 

files = list(glob.glob("movement_test_data/*.csv"))
files.sort()

test_file = files[-1]
files.pop(-1)

df = pd.DataFrame()

for file in files:
    df_open = pd.read_csv(file, header=None)
    df = pd.concat([df, df_open], axis=0)
    del df_open
    
df = df.reset_index(drop=True)

df.columns = ['obs']


obs_per_sec = round(df.shape[0]/(4*4*60))


mean = df.obs.mean()

median = df.obs.median()

#df['obs_ma_1'] = df['obs'].rolling(window=obs_per_sec).mean()

#df['obs_ma_2'] = df['obs'].rolling(window=2*obs_per_sec).mean()

#df['obs_ma_4'] = df['obs'].rolling(window=4*obs_per_sec).mean()

df['obs_mean'] = mean

df['diff_mean'] = mean - df['obs']

#df['diff_mean_ma_1s'] = df['diff_mean'].rolling(window=obs_per_sec).mean()

#df['diff_mean_ma_01s'] = df['diff_mean'].rolling(window=obs_per_sec//10).mean()

df['delta_mean'] = abs(df['diff_mean'] / mean)

df['delta_mean_ma_100ms'] = df['delta_mean'].rolling(window=obs_per_sec//10).mean()

df['delta_mean_ma_200ms'] = df['delta_mean'].rolling(window=obs_per_sec//5).mean()

df['diff_1'] = abs(df['obs'].diff(1))

df['diff_1_rolling_mean_abs'] = df['diff_1'].rolling(window=10).mean()

df['diff_2'] = abs(df['diff_1_rolling_mean_abs'].diff())


aa = df.iloc[20000:30000]    # Long movement (possibly intense)

bb = df.iloc[50000:52000]     # Calm

cc = df.iloc[64000:65000]   # Very Short movement

dd = df.iloc[95000:98000]   # Medium movement

ee = df.iloc[4000:7000]     #Movement

ff = df.iloc[30000:35000]   #Movement

#from matplotlib.pyplot import figure
#figure(num=None, figsize=(60, 6))
#plt.plot(df['obs'])



#Flagging as movement those with delta_mean_ma_5th > 0.2 25 observations after recording

#df_test = df.copy()

df['movement'] = 0

for index, row in df.iterrows():

    df.loc[index-49:index+1, 'movement'] = np.where(
            
            (df.iloc[index]['delta_mean_ma_200ms'] > 0.2) & (~np.isnan(df.iloc[index]['delta_mean_ma_200ms']))
            , 1, 0)

    
df.loc[(np.isnan(df['delta_mean_ma_200ms'])), 'delta_mean_ma_200ms'] = 0



import statistics

from statistics import StatisticsError


movement_detected = []

for sec in range(0, df.shape[0], obs_per_sec):
    try:
        verdict = bool(np.where(statistics.mode(df.iloc[sec:sec+obs_per_sec]['movement']) == 1, True, False))
    except StatisticsError:
        verdict = True
        
    movement_detected.append(verdict)











df_test = pd.read_csv(test_file, header=None, names=['obs'])

mean_test = df_test.obs.mean()

median_test = df_test.obs.median()

df_test['obs_mean'] = mean_test

df_test['diff_mean'] = mean_test - df_test['obs']

#df['diff_mean_ma_1s'] = df['diff_mean'].rolling(window=obs_per_sec).mean()

#df['diff_mean_ma_01s'] = df['diff_mean'].rolling(window=obs_per_sec//10).mean()

df_test['delta_mean'] = abs(df_test['diff_mean'] / mean_test)

df_test['delta_mean_ma_100ms'] = df_test['delta_mean'].rolling(window=obs_per_sec//10).mean()

df_test['delta_mean_ma_200ms'] = df_test['delta_mean'].rolling(window=obs_per_sec//5).mean()



df_test['movement'] = 0

for index, row in df_test.iterrows():

    df_test.loc[index-49:index+1, 'movement'] = np.where(
            
            (df_test.iloc[index]['delta_mean_ma_200ms'] > 0.2) & (~np.isnan(df_test.iloc[index]['delta_mean_ma_200ms']))
            , 1, 0)

    
df_test.loc[(np.isnan(df_test['delta_mean_ma_200ms'])), 'delta_mean_ma_200ms'] = 0






import statistics

from statistics import StatisticsError


movement_detected = pd.Series()

for sec in range(0, df_test.shape[0], obs_per_sec):
    try:
        verdict = bool(np.where(statistics.mode(df_test.iloc[sec:sec+obs_per_sec]['movement']) == 1, True, False))
    except StatisticsError:
        verdict = True
        
    movement_detected[str(sec)+":"+str(sec+obs_per_sec)] = verdict






dd = df_test.iloc[95000:98000]   # Medium movement




#from scipy.fftpack import fft
#from scipy.signal.windows import bohman
#
#intervals = range(0, df1.shape[0], 250)
#
#
#max_amp_index = {}
#
#for interval in intervals:
#    window = bohman(250)
#    
#    max_index = np.argmax(window)
#    
#    max_val = window.max()
#    
#    max_amp_index[str(interval)] = (max_val, max_index)
#
#
#
#plt.plot(window)
#
#
#df['ma_2'] = df['obs'].rolling(window=2, min_periods=1).mean()
#
#
#
#
#
#
#ft = fft(df.obs)
#
#sns.lineplot(data=df)
#
#sns.lineplot(data=ft)
#
#
#df.obs.mean()

