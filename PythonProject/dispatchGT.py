from __future__ import print_function
import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.optimize import fmin

import loadingData
import utilityFunctions
import game

###Declarations of constants to play
##Delta time definitions
dt=0.0833 # 5 min 
TN = 288 # Slots of time of data available
t = 1 # Counter for hour
N = 3 # Number of players
i= 1 # counter for players
d1 = 2
d2 = 2.5
MaxIter = 100
k = 1 # Counter for iterations
ep1 = 0.001
ep2 = 0.001

###Declaration of lists to save data from csv
t  = []
pv = []
wt = []
ld = []
bt = []
de = []

t, pv, wt, ld, bt, de = loadingData.openFile('../FormattedDataSets/dataWithoutBatteries.csv')


def graphInitialData():
	plt.figure(1)
	ax = plt.subplot(1,1,1)
	p1,= plt.plot(t, pv,'ro',label = "PV")

	p2,= plt.plot(t, wt,'go',label = "WT")

	p3,= plt.plot(t, ld,'bo',label = "LD")

	p4,= plt.plot(t, bt,'co',label = "BT")

	p5,= plt.plot(t, bt,'yo',label = "DE")

	hours = mdates.HourLocator(interval = 2) #every two hour
	minutes = mdates.MinuteLocator(interval = 30) #every 30 minutes
	hoursFmt = mdates.DateFormatter('%H')
	xlabels = range (0, 23, 1)	
	handles, labels = ax.get_legend_handles_labels()
	ax.legend(handles, labels)
	ax.xaxis.set_major_locator(hours)
	ax.xaxis.set_major_formatter(hoursFmt)
	ax.xaxis.set_minor_locator(minutes)
	##plt.xticks(xlabels, xlabels, rotation = 'vertical')
	plt.xlabel("Measurement (5 min each)")
	plt.ylabel("kWh")
	plt.grid(True)
	plt.show()

def calculatingGame():
	for t in range(0, TN):
		##initializing game
		pv_required.append(pv[t])
		wt_required.append(wt[t])
		for k in range(0, MaxIter):
			for i in range(0, N):
				pv_required[t] = fmin(pv_utility_fn, pv_required[t], args=(pv_required[t], wt_required[t], ld[t] ));
				print(pv_required[t])


graphInitialData()
print (t)