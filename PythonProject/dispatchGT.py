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
from functools import partial

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

def defineBounds(t, bt = 0):
	pv_bounds = (0, pv[t])
	wt_bounds = (0, wt[t])
	ld_bounds = (0, ld[t])
	bt_bounds = (uf.bt_energy_to_charge_constraint(bt,dt))
	de_bounds = (uf.de_min, uf.de_max)


	players_bounds = [ pv_bounds, \
					   wt_bounds, \
					   ld_bounds, \
					   bt_bounds, \
					   de_bounds
					 ]
	return players_bounds

def defineUtilityFunctions(pv, wt, ld, bt, de, dt):
	utility_functions = [partial (uf.pv_utility_fn, wt = wt, ld = ld, bt = bt, de = de, dt = dt),\
						 partial (uf.wt_utility_fn, pv = pv, ld = ld, bt = bt, de = de, dt = dt),\
						 partial (uf.ld_utility_fn, pv = pv, wt = wt, bt = bt, de = de, dt = dt),\
						 partial (uf.bt_utility_fn, pv = pv, wt = wt, ld = ld, de = de, dt = dt),\
						 partial (uf.de_utility_fn, pv = pv, wt = wt, bt = bt, ld = ld, dt = dt),\
						] 
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
	##Initializing game
	t = 0
	power_to_optimize = np.zeros((288,5))
	power_to_optimize[t]= defineFirstGuest(t)
	

	for k in range(0, 3):
		for i in range(0, N):
			players_bounds = defineBounds(t, power_to_optimize[t][3])
			utility_functions = defineUtilityFunctions( \
								power_to_optimize[t][0], \
								power_to_optimize[t][1], \
								power_to_optimize[t][2], \
								power_to_optimize[t][3], \
								power_to_optimize[t][4], \
								dt \
								)
			
			res = minimize_scalar(utility_functions[i], bounds=players_bounds[i], method='bounded')
			#res = minimize_scalar(utility_functions[i], bounds=(0,0), method='bounded')
			power_to_optimize[t][i] = res.x
			#print ("x {}, fn {}". format(res.x, res.fun))
			#print ("Found max for utility function {} with x {} and fun value {}".format(i,power_to_optimize[t][i], res.fun))
			print ('pv \t\t pv[t] {} \t\t pv_opt {} '.format(pv[t],power_to_optimize[t][0]))
			print ('wt \t\t wt[t] {} \t\t wt_opt {} '.format(wt[t],power_to_optimize[t][1]))
			print ('ld \t\t ld[t] {} \t\t ld_opt {} '.format(ld[t],power_to_optimize[t][2]))
			print ('bt \t\t bt[t] {} \t\t bt_opt {} '.format(bt[t],power_to_optimize[t][3]))
			print ('de \t\t de[t] {} \t\t de_opt {} '.format(de[t],power_to_optimize[t][4]))
			print ('----------------------------------------------')

		print ("Iteration number {}".format(k))

#graphInitialData()
calculatingGame()


