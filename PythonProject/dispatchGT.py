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
import os 
from os import path

import loadingData
import utilityFunctions as uf
import game

###Declarations of constants to play
##Delta time definitions
dt=0.0833 # 5 min 
TN = 288 # Slots of time of data available
t = 1 # Counter for hour
N = 0 # Number of players
i= 1 # counter for players
MaxIter = 10
k = 1 # Counter for iterations
ep1 = 0.05
ep2 = 0.001
loadMultiplier = 12

##Players
# PV = 0 
# WT = 1
# LD = 2
# BT = 3
# DE = 4
# EG = 5

###Declaration of lists to save data from csv
td  = []
pv = []
wt = []
ld = []
teg = []

###Declaration of lists to collect data from game
bt = []
de = []
eg = []

def set_number_of_players():
	playwithgrid = uf.get_playwithgrid()
	global N
	if (playwithgrid==True):
		N = 6
	else:
		N = 5

def loadData():
	##ff from file
	playwithgrid = uf.get_playwithgrid()
	print('playwithgrid {}'.format(playwithgrid))
	dataset = uf.get_dataset()
	electricTariffMultiplier = uf.get_electric_tariff_multi()
	td_ff, pv_ff, wt_ff, ld_ff, bt_ff, de_ff, teg_ff= loadingData.openFile(dataset, playwithgrid)
	ld_ff =  [i * -1 * loadMultiplier for i in ld_ff]
	teg_ff =  [i * -1 * electricTariffMultiplier for i in teg_ff]
	return td_ff, pv_ff, wt_ff, ld_ff, bt_ff, de_ff, teg_ff

def graphInitialData():
	fig_fd = plt.figure(1)
	playwithgrid = uf.get_playwithgrid()
	
	hours = mdates.HourLocator(interval = 2) #every two hours
	minutes = mdates.MinuteLocator(interval = 30) #every 30 minutes
	hoursFmt = mdates.DateFormatter('%H')

	plt.rcParams['axes.grid'] = True

	if( playwithgrid == True):
		ax1 = fig_fd.add_subplot(2,1,1)
		ax2 = fig_fd.add_subplot(2,1,2)
		p1_ax2, = ax2.plot(td, teg, 'r', label = "Tariff")
		handles_ax2, labels_ax2 = ax2.get_legend_handles_labels()
		ax2.legend(handles_ax2, labels_ax2)
		ax2.xaxis.set_major_locator(hours)
		ax2.xaxis.set_major_formatter(hoursFmt)
		ax2.xaxis.set_minor_locator(minutes)
		ax2.set_xlabel("Hours in a day")
		ax2.set_ylabel("Tariff per kWh [$]")
	else:
		ax1 = fig_fd.add_subplot(1,1,1)

	p1_ax1,= ax1.plot(td, pv,'r',label = "PV")
	p2_ax1,= ax1.plot(td, wt,'g',label = "WT")
	p3_ax1,= ax1.plot(td, ld,'b',label = "LD")
	p4_ax1,= ax1.plot(td, bt,'c',label = "BT")
	p5_ax1,= ax1.plot(td, bt,'y',label = "DE")

	handles_ax1, labels_ax1 = ax1.get_legend_handles_labels()

	ax1.legend(handles_ax1, labels_ax1, fontsize = 'small', ncol =2)
	ax1.xaxis.set_major_locator(hours)
	ax1.xaxis.set_major_formatter(hoursFmt)
	ax1.xaxis.set_minor_locator(minutes)
	ax1.set_xlabel("Hours in a day")
	ax1.set_ylabel("kWh")
	
	test_name = uf.get_test_name()
	get_path_to_save(test_name)

	fig_fd.subplots_adjust(hspace=0.8)
	fig_name = './' + test_name + '/InitialData.eps'
	plt.savefig(fig_name, format='eps', dpi =1000)
	#plt.show()

def defineBounds(t, bt = 0):
	pv_bounds = (0, pv[t])
	wt_bounds = (0, wt[t])
	ld_bounds = (ld[t]*0.98, ld[t]*1.02)
	bt_bounds = uf.bt_power_constraint(bt, dt)
	de_bounds = (uf.de_min, uf.de_max)
	eg_bounds = (0, None)
	players_bounds = [ pv_bounds, \
					   wt_bounds, \
					   ld_bounds, \
					   bt_bounds, \
					   de_bounds, \
					   eg_bounds, \
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

	const.append(None)
	return const

def defineUtilityFunctions(i, pv, wt, ld, bt, de, eg, dt, ld_nom, teg=0):
	utility_functions = [partial (uf.pv_utility_fn, wt = wt, ld = ld, bt = bt, de = de, dt = dt, eg = eg),\
						 partial (uf.wt_utility_fn, pv = pv, ld = ld, bt = bt, de = de, dt = dt, eg = eg),\
						 partial (uf.ld_utility_fn, pv = pv, wt = wt, bt = bt, de = de, dt = dt, ld_nom = ld_nom, eg = eg),\
						 partial (uf.bt_utility_fn, pv = pv, wt = wt, ld = ld, de = de, dt = dt, eg = eg),\
						 partial (uf.de_utility_fn, pv = pv, wt = wt, bt = bt, ld = ld, dt = dt, eg = eg),\
						 partial (uf.eg_utility_fn, pv = pv, wt = wt, bt = bt, ld = ld, de = de, dt = dt, teg = teg),\
						] 
	return utility_functions[i]

def defineFirstGuest (t, bt_prev, de_prev):
	power_to_optimize_t = np.zeros(6)
	power_to_optimize_t[0] = pv[t]
	power_to_optimize_t[1] = wt[t]
	power_to_optimize_t[2] = ld[t]
	power_to_optimize_t[3] = bt[t]
	power_to_optimize_t[4] = de[t]
	power_to_optimize_t[5] = 0
	return power_to_optimize_t

def calculatingGame():
	##Initializing game
	t = 0
	power_to_optimize = np.zeros((288,6))
	
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
				utility_function = defineUtilityFunctions( \
									i, \
									power_to_optimize[t][0], \
									power_to_optimize[t][1], \
									power_to_optimize[t][2], \
									power_to_optimize[t][3], \
									power_to_optimize[t][4], \
									power_to_optimize[t][5], \
									dt, \
									ld[t], \
									teg[t] \
									)
				constraints = defineConstraints(dt,power_to_optimize[:,4], t)
				
				#res = minimize_scalar(utility_functions[i], bounds=players_bounds[i], method='bounded')
				res = minimize(utility_function,\
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
				print ('eg \t\t eg[t] {} \t\t eg_opt {} '.format(de[t],power_to_optimize[t][5]))
				print ('----------------------------------------------')

				
			print ('################# End players role #####################')
			
			pf = uf.penalty_fn(power_to_optimize[t][0], \
					      power_to_optimize[t][1], \
						  power_to_optimize[t][2], \
						  power_to_optimize[t][3], \
						  power_to_optimize[t][4], \
						  power_to_optimize[t][5])


			ne = uf.verifyNashEquilibrium(power_to_optimize[t][0], \
					      			  power_to_optimize[t][1], \
						  			  power_to_optimize[t][2], \
						  			  power_to_optimize[t][3], \
						  			  power_to_optimize[t][4], \
						  			  power_to_optimize[t][5], \
						  			  dt,\
						  			  ld[t], \
						  			  teg[t] \
						  			  )

			print ('pf {}'.format(pf))
			print ('ne {}'.format(ne))
			print ('bt_soc {}'.format(uf.bt_soc))

			if (np.abs(pf) < ep1):
				if ( ne == True):
					break
				else:
					uf.ne_update_alpha()
			else:
				uf.pf_update_alpha()

		uf.soc_bt_update_fn(power_to_optimize[t][3], dt)
		uf.update_penalty_fn(power_to_optimize[t][0], \
					      	 power_to_optimize[t][1], \
						  	 power_to_optimize[t][2], \
						  	 power_to_optimize[t][3], \
						  	 power_to_optimize[t][4], \
						  	 power_to_optimize[t][5])

	return power_to_optimize			


def get_path_to_save(testname):
	if not os.path.exists(testname):
		print ('get_path_to_save')
		os.mkdir(testname)

def graphFinalData():
	finalData = calculatingGame()
	bt_soc_list = uf.get_bt_soc_list()
	pf_list = uf.get_penalty_fn()

	for i in bt_soc_list:
		print ('bt_soc_from_list {}'.format(i))
	
	plt.rcParams['axes.grid'] = True

	fig_fd = plt.figure(2)
	ax1 = fig_fd.add_subplot(3,1,1)
	ax2 = fig_fd.add_subplot(3,1,2)
	ax3 = fig_fd.add_subplot(3,1,3)

	ax1.set_title('Resources dispatch')
	ax2.set_title('Battery state')
	ax3.set_title('Power balance value')

	ax1.set_xlabel("Hours in a day")
	ax1.set_ylabel("kWh")

	ax2.set_xlabel("Hours in a day")
	ax2.set_ylabel("% of charge")

	ax3.set_xlabel("Hours in a day")
	ax3.set_ylabel("kWh")

	hours = mdates.HourLocator(interval = 2) #every two hours
	minutes = mdates.MinuteLocator(interval = 30) #every 30 minutes
	hoursFmt = mdates.DateFormatter('%H')

	ax1.xaxis.set_major_locator(hours)
	ax1.xaxis.set_major_formatter(hoursFmt)
	ax1.xaxis.set_minor_locator(minutes)

	ax2.xaxis.set_major_locator(hours)
	ax2.xaxis.set_major_formatter(hoursFmt)
	ax2.xaxis.set_minor_locator(minutes)

	ax3.xaxis.set_major_locator(hours)
	ax3.xaxis.set_major_formatter(hoursFmt)
	ax3.xaxis.set_minor_locator(minutes)

	ax2.set_ylim([uf.bt_soc_min-10, uf.bt_soc_max+10])

	p1_ax1,= ax1.plot(td, finalData[:,0],'r',label = "PV")
	p2_ax1,= ax1.plot(td, finalData[:,1],'g',label = "WT")
	p3_ax1,= ax1.plot(td, finalData[:,2],'b',label = "LD")
	p4_ax1,= ax1.plot(td, finalData[:,3],'c',label = "BT")
	p5_ax1,= ax1.plot(td, finalData[:,4],'y',label = "DE")
	
	if(uf.get_playwithgrid() == True):
		p6_ax1,= ax1.plot(td, finalData[:,5],'m',label = "EG")
	
	p1_ax2,= ax2.plot(td, bt_soc_list,'r',label = "SOC")

	p1_ax3,= ax3.plot(td, pf_list,'b',label = "Power balance")

	handles_ax1, labels_ax1 = ax1.get_legend_handles_labels()
	handles_ax2, labels_ax2 = ax2.get_legend_handles_labels()
	handles_ax3, labels_ax3 = ax3.get_legend_handles_labels()

	ax1.legend(handles_ax1, labels_ax1, fontsize = 'small', ncol =1, bbox_to_anchor=(1, 1.2))
	ax2.legend(handles_ax2, labels_ax2, fontsize = 'small', ncol =2)
	ax3.legend(handles_ax3, labels_ax3, fontsize = 'small', ncol =2)

	fig_fd.subplots_adjust(hspace=0.8)
	
	test_name = uf.get_test_name()
	get_path_to_save(test_name)
	electricTariffMultiplier = uf.get_electric_tariff_multi()
	fig_name = './' + test_name + '/optimizedData_LoadMultiplier_{}_MaxIter_{}_BatCap_{}_Socinit_{}_BTC_{}_DERU_{}_ElecCostMulti_{}_pg{}.eps'.format(loadMultiplier, \
					MaxIter, uf.bt_rated_capacity, uf.bt_soc_init, \
					uf.bt_C, uf.de_ramp_up,electricTariffMultiplier,\
					uf.get_playwithgrid())

	#fig_name = './fig/optimizedData_LoadMultiplier_{}_MaxIter_{}_BatCap_{}_Socinit_{}_BTC_{}_DERU_{}.eps'.format(loadMultiplier, MaxIter, uf.bt_rated_capacity, uf.bt_soc_init, uf.bt_C, uf.de_ramp_up)
	plt.savefig(fig_name, format='eps', dpi =1000)
	#plt.show()


uf.define_parameters()
set_number_of_players()
td, pv, wt, ld, bt, de, teg = loadData()
graphInitialData()
graphFinalData()
