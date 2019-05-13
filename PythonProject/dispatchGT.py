from __future__ import print_function
import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.optimize import fmin
from scipy.optimize import minimize
from scipy.optimize import minimize_scalar
from scipy.optimize import Bounds

import loadingData
import utilityFunctions as uf
import game

###Declarations of constants to play
##Delta time definitions
dt=0.0833 # 5 min 
TN = 288 # Slots of time of data available
t = 1 # Counter for hour
N = 5 # Number of players
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
args_items = []

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
	plt.xlabel("Measurement (5 min each)")
	plt.ylabel("kWh")
	plt.grid(True)
	plt.show()

##Players
# PV = 0 
# WT = 1
# LD = 2
# BT = 3
# DE = 4

def defineBounds(t):
	pv_bounds = Bounds(lb=0, ub=pv[t])
	wt_bounds = Bounds(lb=0, ub=wt[t])
	ld_bounds = Bounds(lb=0, ub=ld[t])
	bt_bounds = Bounds(lb=uf.bt_energy_min/dt, ub=uf.bt_energy_max/dt)
	de_bounds = Bounds(lb=uf.de_min, ub=uf.de_max)

	players_bounds = [ pv_bounds, \
					   wt_bounds, \
					   ld_bounds, \
					   bt_bounds, \
					   de_bounds
					 ]
	return players_bounds

def defineUtilityFunctions():
	utility_functions = [uf.pv_utility_fn, \
						 uf.wt_utility_fn, \
						 uf.ld_utility_fn, \
						 uf.bt_utility_fn, \
						 uf.de_utility_fn]
	return utility_functions

def defineFirstGuest (t):
	power_to_optimize_t = np.zeros(5) 
	power_to_optimize_t[0] = pv[t]
	power_to_optimize_t[1] = wt[t]
	power_to_optimize_t[2] = ld[t]
	power_to_optimize_t[3] = bt[t]
	power_to_optimize_t[4] = de[t]
	return power_to_optimize_t

def calculatingGame():
	##initializing game
	t = 0
	power_to_optimize = np.zeros((288,5))
	utility_functions = defineUtilityFunctions()

	power_to_optimize[t] = defineFirstGuest(t)
	players_bounds = defineBounds(t)

	for k in range(0, 3):
		for i in range(0, N):
			args_items = range(0, N)
			del args_items[i]
			print (args_items)
			pv_bounds = Bounds(lb=0, ub=pv[t])			
			x0_array = np.array([power_to_optimize[t][i]])
			print ('x0array {} , shape {}'.format(x0_array, x0_array.shape))
			#power_to_optimize[t][i] = minimize_scalar (utility_functions[i], 
			#	args=(power_to_optimize[t][args_items[0]], \
			#	power_to_optimize[t][args_items[1]], \
			#	power_to_optimize[t][args_items[2]], \
			#	power_to_optimize[t][args_items[3]], \
			#	dt), \
			#	method = 'bounded', \
			#	bounds = (0.,3.)\
			#	)

			#power_to_optimize[t][i] = minimize(utility_functions[i],x0=power_to_optimize[t][i], \
			#	args=(power_to_optimize[t][args_items[0]], \
			#	power_to_optimize[t][args_items[1]], \
			#	power_to_optimize[t][args_items[2]], \
			#	power_to_optimize[t][args_items[3]], \
			#	dt), \
			#	bounds=((2,200),))


			power_to_optimize[t][i] = fmin(utility_functions[i],x0=power_to_optimize[t][i], \
				args=(power_to_optimize[t][args_items[0]], \
				power_to_optimize[t][args_items[1]], \
				power_to_optimize[t][args_items[2]], \
				power_to_optimize[t][args_items[3]], \
				dt))

			print ("Found max for utility function {} with {}".format(i,power_to_optimize[t][i]))
			del args_items[:]
		print ("Iteration number {}".format(k))

#graphInitialData()
calculatingGame()