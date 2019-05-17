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
MaxIter = 5
k = 1 # Counter for iterations
ep1 = 0.005
ep2 = 0.001
loadMultiplier = 1

###Declaration of lists to save data from csv
t  = []
pv = []
wt = []
ld = []
bt = []
de = []
args_items = []

td, pv, wt, ld, bt, de = loadingData.openFile('../FormattedDataSets/dataWithoutBatteries.csv')
ld =  [i * -1*loadMultiplier for i in ld]

def graphInitialData():
	plt.figure(1)
	ax = plt.subplot(1,1,1)
	p1,= plt.plot(td, pv,'r',label = "PV")

	p2,= plt.plot(td, wt,'g',label = "WT")

	p3,= plt.plot(td, ld,'b',label = "LD")

	p4,= plt.plot(td, bt,'c',label = "BT")

	p5,= plt.plot(td, bt,'y',label = "DE")

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
	plt.savefig('./fig/initialData.eps', format='eps', dpi =1000)
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
	bt_bounds = uf.bt_power_constraint(bt, dt)
	de_bounds = (uf.de_min, uf.de_max)

	#print ('Bounds')
	#print ('pv_bounds {}'. format(pv_bounds))
	#print ('wt_bounds {}'. format(wt_bounds))
	#print ('ld_bounds {}'. format(ld_bounds))
	#print ('bt_bounds {}'. format(bt_bounds))
	#print ('de_bounds {}'. format(de_bounds))

	players_bounds = [ pv_bounds, \
					   wt_bounds, \
					   ld_bounds, \
					   bt_bounds, \
					   de_bounds
					 ]
	return players_bounds

def defineConstraints(dt, de_list, t):
	const = []
	const.append(None)
	const.append(None)
	const.append(None)
	const.append([{"type": "ineq", "fun": uf.soc_bt_max_constraint_fn, 'args': (dt,)},
			      {"type": "ineq", "fun": uf.soc_bt_min_constraint_fn, 'args': (dt,)}])

	const.append([{"type": "ineq", "fun": uf.ramp_up_oil_constraint_fn, 'args': (de_list[t-1],dt,)},
			   	  {"type": "ineq", "fun": uf.ramp_down_oil_constraint_fn, 'args': (de_list[t-1],dt,)},
			   	  {"type": "ineq", "fun": uf.minimun_running_time_de_constraint_fn, 'args': (de_list, t, dt,)}])

	#bt_cons = [{"type": "ineq", "fun": uf.soc_bt_max_constraint_fn, 'args': (dt,)},
	#		   {"type": "ineq", "fun": uf.soc_bt_min_constraint_fn, 'args': (dt,)}]
	#print ('const[3] {}'.format(const[3]))
	return const

def defineUtilityFunctions(pv, wt, ld, bt, de, dt):
	utility_functions = [partial (uf.pv_utility_fn, wt = wt, ld = ld, bt = bt, de = de, dt = dt),\
						 partial (uf.wt_utility_fn, pv = pv, ld = ld, bt = bt, de = de, dt = dt),\
						 partial (uf.ld_utility_fn, pv = pv, wt = wt, bt = bt, de = de, dt = dt),\
						 partial (uf.bt_utility_fn, pv = pv, wt = wt, ld = ld, de = de, dt = dt),\
						 partial (uf.de_utility_fn, pv = pv, wt = wt, bt = bt, ld = ld, dt = dt),\
						] 
	return utility_functions

def defineFirstGuest (t, bt_prev, de_prev):
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
	
	for t in range(0,288):
		print ('Sample # {}'.format(t))
		if (t == 0):
			power_to_optimize[t]= defineFirstGuest(t, bt[t], de[t])
		else:
			power_to_optimize[t]= defineFirstGuest(t, power_to_optimize[t-1][3], power_to_optimize[t-1][4])
		uf.reinit_alpha()
		for k in range(0, MaxIter):
			print ("Iteration number {}, time {}".format(k, t))
			players_bounds = defineBounds(t, power_to_optimize[t][3])
			for i in range(0, N):
				print('player # {}'.format(i))
				utility_functions = defineUtilityFunctions( \
									power_to_optimize[t][0], \
									power_to_optimize[t][1], \
									power_to_optimize[t][2], \
									power_to_optimize[t][3], \
									power_to_optimize[t][4], \
									dt \
									)
				constraints = defineConstraints(dt,power_to_optimize[:,4], t)
				
				#res = minimize_scalar(utility_functions[i], bounds=players_bounds[i], method='bounded')
				res = minimize(utility_functions[i],\
				   x0 = power_to_optimize[t][i],\
				   bounds=[players_bounds[i]], \
				   #bounds=bt_bounds, \
				   constraints = constraints[i])
				#res = minimize_scalar(utility_functions[i], bounds=players_bounds[i], method='bounded')
				power_to_optimize[t][i] = res.x

				print ('pv \t\t pv[t] {} \t\t pv_opt {} '.format(pv[t],power_to_optimize[t][0]))
				print ('wt \t\t wt[t] {} \t\t wt_opt {} '.format(wt[t],power_to_optimize[t][1]))
				print ('ld \t\t ld[t] {} \t\t ld_opt {} '.format(ld[t],power_to_optimize[t][2]))
				print ('bt \t\t bt[t] {} \t\t bt_opt {} '.format(bt[t],power_to_optimize[t][3]))
				print ('de \t\t de[t] {} \t\t de_opt {} '.format(de[t],power_to_optimize[t][4]))
				print ('----------------------------------------------')

				
			print ('################# End players role #####################')
			pf = uf.penalty_fn(power_to_optimize[t][0], \
					      power_to_optimize[t][1], \
						  power_to_optimize[t][2], \
						  power_to_optimize[t][3], \
						  power_to_optimize[t][4])
			print ('pf {}'.format(pf))
			if (np.abs(pf) < ep1):
				if (uf.verifyNashEquilibrium(power_to_optimize[t][0], \
					      			  power_to_optimize[t][1], \
						  			  power_to_optimize[t][2], \
						  			  power_to_optimize[t][3], \
						  			  power_to_optimize[t][4],
						  			  dt) == True):
					break
				else:
					uf.ne_update_alpha()
			else:
				uf.pf_update_alpha()
		uf.soc_bt_update_fn(power_to_optimize[t][3], dt)
	return power_to_optimize			

def testBatteryOptimization():
	print ('testBatteryOptimization')
	t = 132
	pv_b = pv[t]
	wt_b = wt[t]
	ld_b = -ld[t]
	bt_b = -0.089
	de_b = 0.0
	uf.bt_soc = 57.81111637
	print ('pv {}, \nwt {},\nld {},\nbt {},\nde {}\n'.format(pv_b, wt_b, ld_b, bt_b, de_b))
	
	bt_bounds = [uf.bt_power_constraint(bt_b, dt)]

	print ('bt_bounds {}'.format(bt_bounds))
	bt_partial = partial (uf.bt_utility_fn, pv = pv_b, wt = wt_b, ld = ld_b, de = de_b, dt = dt)
	bt_cons = [{"type": "ineq", "fun": uf.soc_bt_max_constraint_fn, 'args': (dt,)},
			   {"type": "ineq", "fun": uf.soc_bt_min_constraint_fn, 'args': (dt,)}]

	res = minimize(bt_partial,\
				   x0 = bt_b,\
				   bounds=[(0,10)], \
				   #bounds=bt_bounds, \
				   constraints = bt_cons)
	bt_b = res.x
	uf.soc_bt_fn(bt_b, dt)
	print ('----------------------------------------------------')
	print ('soc_final {}'.format(uf.bt_soc))
	print ('####################################################')
	print ('res.x {}'.format(res.x))


def testNashEquilibrium():
	t=0
	pv_b = pv[t]
	wt_b = wt[t]
	ld_b = -ld[t]
	bt_b = -0.089
	de_b = 0.0
	uf.verifyNashEquilibrium(pv_b, wt_b, ld_b, bt_b, de_b, dt)

def graphFinalData():
	finalData = calculatingGame()
	bt_soc_list = uf.get_bt_soc_list()
	
	plt.rcParams['axes.grid'] = True

	fig_fd = plt.figure(1)
	ax1 = fig_fd.add_subplot(2,1,1)
	ax2 = fig_fd.add_subplot(2,1,2)

	ax1.set_title('Resources and Load dispatch')
	ax2.set_title('Battery state')

	ax1.set_xlabel("Measurement (5 min each)")
	ax1.set_ylabel("kWh")

	ax2.set_xlabel("Estimated SOC (5 min each)")
	ax2.set_ylabel("% of charge")

	hours = mdates.HourLocator(interval = 2) #every two hour
	minutes = mdates.MinuteLocator(interval = 30) #every 30 minutes
	hoursFmt = mdates.DateFormatter('%H')
	xlabels = range (0, 23, 1)	

	ax1.xaxis.set_major_locator(hours)
	ax1.xaxis.set_major_formatter(hoursFmt)
	ax1.xaxis.set_minor_locator(minutes)

	ax2.xaxis.set_major_locator(hours)
	ax2.xaxis.set_major_formatter(hoursFmt)
	ax2.xaxis.set_minor_locator(minutes)

	p1_ax1,= ax1.plot(td, finalData[:,0],'r',label = "PV")
	p2_ax1,= ax1.plot(td, finalData[:,1],'g',label = "WT")
	p3_ax2,= ax1.plot(td, finalData[:,2],'b',label = "LD")
	p4_ax3,= ax1.plot(td, finalData[:,3],'c',label = "BT")
	p5_ax4,= ax1.plot(td, finalData[:,4],'y',label = "DE")
	
	p_ax2,= plt.plot(td, bt_soc_list,'r',label = "SOC")

	handles_ax1, labels_ax1 = ax1.get_legend_handles_labels()
	handles_ax2, labels_ax2 = ax2.get_legend_handles_labels()
	ax1.legend(handles_ax1, labels_ax1)
	ax2.legend(handles_ax2, labels_ax2)

	fig_fd.subplots_adjust(hspace=0.5)
	
	plt.savefig('./fig/optimizedData_LoadMultiplier_{}_MaxIter_{}_BatCap_{}_socinit_{}.eps'.format(loadMultiplier, MaxIter, uf.bt_max_energy_stored, uf.bt_soc_init), format='eps', dpi =1000)
	plt.show()


#graphInitialData()
#calculatingGame()
#testBatteryOptimization()
#defineConstraints(dt)
#testNashEquilibrium()

graphInitialData()
graphFinalData()
