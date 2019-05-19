import numpy as np
import sympy as S
from sympy import Abs, Symbol
import argumentCollection as ac

pf_list = []
bt_soc_list = []

alpha = 0
d1 = 0
d2 = 0

pv_unit_electric_price = 0
pv_unit_maintenance_cost = 0
wt_unit_electric_price = 0
wt_unit_maintenance_cost = 0
de_oil_price = 0
de_unit_electric_price = 0
de_unit_maintenance_cost = 0
de_rate_oil_consumption = 0
de_a_oil_consumption = 0
de_b_oil_consumption= 0
de_c_oil_consumption = 0
de_min = 0
de_max = 0
de_ramp_up = 0
de_ramp_down = 0
de_min_running_time = 0
bt_unit_electric_price = 0
bt_unit_maintenance_cost = 0
bt_self_dis_rate = 0
bt_rated_capacity = 0
bt_C = 0
bt_char_eff = 0
bt_dis_eff = 0
bt_soc_max = 0
bt_soc_min = 0
bt_power_charge = 0
bt_power_discharge = 0
bt_soc_init = 0
bt_soc = 0
ld_weight_satisfaction = 0
ld_unit_electric_price = 0
ld_beta = 0
ld_alpha = 0

#Penalty function modelling
#alpha = 0.1
#d1 = 2
#d2 = 4
#pf_list = []
#bt_soc_list = []

##PV modelling
#pv_unit_electric_price = 2.0
#pv_unit_maintenance_cost = 0.5

#WT modelling
#wt_unit_electric_price = 4.0
#wt_unit_maintenance_cost = 3.0

##Diesel modelling
#de_oil_price = 3.0
#de_unit_electric_price = 4.0
#de_unit_maintenance_cost = 3.0
#de_rate_oil_consumption = 2
#de_a_oil_consumption = 1
#de_b_oil_consumption= 2
#de_c_oil_consumption = 1
#de_min = 0
#de_max = 10
#de_ramp_up = 20
#de_ramp_down = 10
#de_min_running_time = 0.3

##Battery modelling
#bt_unit_electric_price = 0.1
#bt_unit_maintenance_cost = 0.05
#bt_self_dis_rate = 0.0000001
#bt_rated_capacity = 2
#bt_C = 0.2
#bt_char_eff = 0.99
#bt_dis_eff = 0.99
#bt_soc_max = 100
#bt_soc_min = 60
#bt_power_charge = -bt_C * bt_rated_capacity * bt_char_eff
#bt_power_discharge = bt_C * bt_rated_capacity * bt_dis_eff
#bt_soc_init = bt_soc_min + 15
#bt_soc = bt_soc_init

##Load modelling
#ld_weight_satisfaction = 0.9
#ld_unit_electric_price = 0.4
#ld_beta = -1
#ld_alpha = 0.5

def define_parameters():
	Args=ac.ParsingArguments() 

	global alpha
	global d1 
	global d2 

	global pv_unit_electric_price 
	global pv_unit_maintenance_cost 
	global wt_unit_electric_price 
	global wt_unit_maintenance_cost 
	global de_oil_price 
	global de_unit_electric_price 
	global de_unit_maintenance_cost 
	global de_rate_oil_consumption 
	global de_a_oil_consumption 
	global de_b_oil_consumption
	global de_c_oil_consumption 
	global de_min 
	global de_max 
	global de_ramp_up 
	global de_ramp_down 
	global de_min_running_time 
	global bt_unit_electric_price 
	global bt_unit_maintenance_cost 
	global bt_self_dis_rate 
	global bt_rated_capacity 
	global bt_C 
	global bt_char_eff 
	global bt_dis_eff 
	global bt_soc_max 
	global bt_soc_min 
	global bt_power_charge 
	global bt_power_discharge 
	global bt_soc_init 
	global bt_soc 
	global ld_weight_satisfaction 
	global ld_unit_electric_price 
	global ld_beta 
	global ld_alpha 
	global test_name
	global samples_to_analize 
    
    #Penalty function modelling
	alpha =float(Args.alpha)
	d1 =float(Args.powerbalance)
	d2 =float(Args.nashequilibrium)

	##PV modelling
	pv_unit_electric_price =float(Args.pvuep)
	pv_unit_maintenance_cost =float(Args.pvumc)

	#WT modelling
	wt_unit_electric_price =float(Args.wtuep)
	wt_unit_maintenance_cost =float(Args.wtumc)

	##Diesel modelling
	
	de_unit_electric_price =float( Args.deuep)
	de_unit_maintenance_cost =float(Args.deumc)
	de_oil_price =float(Args.deoilprice)
	de_rate_oil_consumption =float(Args.derateconsumption)
	de_a_oil_consumption =float(Args.deaoilconsumption)
	de_b_oil_consumption=float(Args.deboilconsumption)
	de_c_oil_consumption =float(Args.decoilconsumption)
	de_min =float(Args.deminpower)
	de_max =float(Args.demaxpower)
	de_ramp_up =float(Args.derampup)
	de_ramp_down =float(Args.derampdown)
	de_min_running_time =float(Args.deminrunningtime)

	##Battery modelling
	bt_unit_electric_price =float(Args.btuep)
	bt_unit_maintenance_cost =float(Args.btumc)
	bt_self_dis_rate =float(Args.btselfdis)
	bt_rated_capacity =float(Args.btratedcap)
	bt_C =float(Args.btc)
	bt_char_eff =float(Args.btchargeeff)
	bt_dis_eff =float(Args.btdischargeeff)
	bt_soc_max =float(Args.btsocmax)
	bt_soc_min =float(Args.btsocmin)
	
	bt_soc_init =float(Args.btsocinit)
	bt_power_charge =float(-bt_C * bt_rated_capacity * bt_char_eff)
	bt_power_discharge =float(bt_C * bt_rated_capacity * bt_dis_eff)
	bt_soc = bt_soc_init

	##Load modelling
	ld_weight_satisfaction = float(Args.ldweightsat)
	ld_unit_electric_price = float(Args.lduep)
	ld_beta = float(Args.ldbeta)
	ld_alpha = float(Args.ldalpha)

	test_name = Args.testname
	samples_to_analize = float(Args.samplestoanalize)

def get_test_name():
    	return test_name

def get_samples_to_analize():
    	return samples_to_analize

#Updating alpha to penalty energy balance function
def reinit_alpha():
	global alpha
	alpha = 0.1

def pf_update_alpha():
	global alpha
	alpha *= d1

def ne_update_alpha():
	global alpha
	alpha *= d2

##Penalty function to restrict power balance
def update_penalty_fn(pv, wt, de, bt, ld):
	pf_list.append(penalty_fn(pv, wt, de, bt, ld))

def get_penalty_fn():
	return pf_list

def penalty_fn(pv, wt, de, bt, ld):
	return pv + wt + de + bt + ld

##Utility function of PV taking into account power balance
def pv_utility_fn(pv, wt, ld, bt, de, dt):
	return float(-1*((pv_unit_electric_price-pv_unit_maintenance_cost)*pv*dt \
	- alpha * np.power(penalty_fn(pv,wt,de,bt,ld),2)))

##Utility function of WT taking into account power balance
def wt_utility_fn(wt, pv, ld, bt, de, dt):
	return -1*((wt_unit_electric_price-wt_unit_maintenance_cost)*wt*dt \
	- alpha * np.power(penalty_fn(pv,wt,de,bt,ld),2))

##Utility function of DE taking into account power balance
def de_utility_fn(de, pv, wt, ld, bt, dt):
	return -1*((de_unit_electric_price-de_unit_maintenance_cost)*de*dt - de_oil_price * rate_oil_consumption_fn(de) * dt\
	- alpha * np.power(penalty_fn(pv,wt,de,bt,ld),2))

##Rate consumption of oil function
def rate_oil_consumption_fn(de):
	return de_a_oil_consumption* np.power(de,2) + de_b_oil_consumption*de + de_c_oil_consumption

def ramp_up_oil_constraint_fn(de, de_past, dt):
	return de_past - de + dt*de_ramp_up
		
def ramp_down_oil_constraint_fn(de, de_past, dt):
	return de - de_past +  (dt*de_ramp_down)

def minimun_running_time_de_constraint_fn(de, de_activation_list, t ,dt):
	len_de_act = t
	counter = 0
	for i in range(len_de_act):
		if (de > 0):
			if (de_activation_list[len_de_act - i] > 0):
				counter =+ 1
			else:
				if(counter!=0):
					return de_min_running_time - counter*dt
				else:
					return 0
		else:
			return 0
	return 0			
	

def bt_utility_fn(bt, pv, wt, ld, de, dt):
	#print ('bt {}'.format(bt))
	#print ('pv {}'.format(pv))
	#print ('wt {}'.format(wt))
	#print ('ld {}'.format(ld))
	#print ('de {}'.format(de))
	#print ('penalty_fn {}'.format(-alpha*np.power(penalty_fn(pv,wt,de,bt,ld),2)))
	return -1*(bt_unit_electric_price*bt*dt \
		- bt_unit_maintenance_cost*np.abs(bt)*dt \
		- alpha * np.power(penalty_fn(pv,wt,de,bt,ld),2))

def soc_bt_update_fn(bt, dt):
	global bt_soc
	print ('soc_bt_update_fn')
	print ('bt {}'.format(bt))
	bt_soc = soc_bt_fn(bt,dt)
	bt_soc_list.append(bt_soc)

def get_bt_soc_list():
	return bt_soc_list

def soc_bt_fn(bt, dt):
	#print ('soc_bt_fn')
	#print ('bt {}'.format(bt))
	#print ('bt_soc*(1-bt_self_dis_rate) {}'.format(bt_soc*(1-bt_self_dis_rate)))
	#print ('- (bt*dt)/bt_rated_capacity*bt_char_eff {}'.format( - ((bt*dt)/bt_rated_capacity)*bt_char_eff))
	return (bt_soc*(1-bt_self_dis_rate) - 100*((bt*dt)/bt_rated_capacity)*bt_char_eff)

def soc_bt_max_constraint_fn(bt, dt):
	soc_bt_max_cn = bt_soc_max - soc_bt_fn(bt, dt)
	#print ('soc_bt_max_cn {}'.format(soc_bt_max_cn))
	return soc_bt_max_cn

def soc_bt_min_constraint_fn(bt, dt):
	soc_bt_min_cn = soc_bt_fn(bt, dt) - bt_soc_min 
	#print ('soc_bt_min_cn {}'.format(soc_bt_min_cn))
	return soc_bt_min_cn


def bt_power_constraint(bt,dt):
	bt_power_max_charge = max(bt_power_charge, -(bt_soc_max - soc_bt_fn(bt, dt))*bt_rated_capacity*bt_char_eff)
	bt_power_max_discharge = min(bt_power_discharge, (soc_bt_fn(bt, dt) - bt_soc_min)*bt_rated_capacity*bt_dis_eff)
	#print('bt_power_max_charge {}'.format(bt_power_max_charge))
	#print('bt_power_max_discharge {}'.format(bt_power_max_discharge))
	return bt_power_max_charge, bt_power_max_discharge

## Satisfaction function of load consumption
def ld_satifaction_fn(ld, ld_nom):
	return ld_nom*ld_beta*(np.power((ld/ld_nom),ld_alpha) - 1)

##Utility function of LD taking into account power balance
def ld_utility_fn(ld, pv, wt, bt, de, dt, ld_nom):
	return -1*((1-ld_weight_satisfaction)*ld_unit_electric_price*ld + ld_weight_satisfaction*ld_satifaction_fn(ld, ld_nom))

	

def verifyNashEquilibrium(pv, wt, ld, bt, de, dt, ld_nom):
	error_ne = 0.5
	print ('pv {} \nwt {} \nld {} \nbt {} \nde {}'.format(pv, wt, ld, bt, de))

	p = Symbol('p', real= True)
	w = Symbol('w', real= True)
	l = Symbol('l', real= True)
	b = Symbol('b', real= True)
	d = Symbol('d', real= True)

	f_ne_p = -1*(pv_unit_electric_price-pv_unit_maintenance_cost)*dt*p
	f_ne_w = -1*(wt_unit_electric_price-wt_unit_maintenance_cost)*dt*w
	f_ne_l = -1*((1-ld_weight_satisfaction)*ld_unit_electric_price*l + ld_weight_satisfaction*(ld_nom*ld_beta*(((l/ld_nom)**ld_alpha) - 1)))
	f_ne_b = -1*(bt_unit_electric_price*dt*b - bt_unit_maintenance_cost*Abs(b)*dt)
	f_ne_d = -1*((de_unit_electric_price-de_unit_maintenance_cost)*dt*d - de_oil_price * (de_a_oil_consumption* d**2 + de_b_oil_consumption*d + de_c_oil_consumption) * dt)
	f_pf =  alpha * (p + w + d + b + l)**2

	f_nash_equilibrium = f_ne_p + f_ne_w + f_ne_l + f_ne_b + f_ne_d -f_pf
	
	#print ('f_ne_p = {}'.format(f_ne_p))
	#print ('f_ne_w = {}'.format(f_ne_w))
	#print ('f_ne_l = {}'.format(f_ne_l))
	#print ('f_ne_b = {}'.format(f_ne_b))
	#print ('f_ne_d = {}'.format(f_ne_d))
	#print ('f_nash_equilibrium {}'.format(f_nash_equilibrium))
	
	p_derivate = S.diff(f_nash_equilibrium, p)
	w_derivate = S.diff(f_nash_equilibrium, w)
	l_derivate = S.diff(f_nash_equilibrium, l)
	b_derivate = S.diff(f_nash_equilibrium, b)
	d_derivate = S.diff(f_nash_equilibrium, d)

	#print ('p_derivate = {}'.format(p_derivate))
	#print ('w_derivate = {}'.format(w_derivate))
	#print ('l_derivate = {}'.format(l_derivate))
	#print ('b_derivate = {}'.format(b_derivate))
	#print ('d_derivate = {}'.format(d_derivate))

	p_min = p_derivate.evalf(subs={p:pv, w: wt, l: ld, b:bt, d: de})
	w_min = w_derivate.evalf(subs={p:pv, w: wt, l: ld, b:bt, d: de})
	l_min = l_derivate.evalf(subs={p:pv, w: wt, l: ld, b:bt, d: de})
	b_min = b_derivate.evalf(subs={p:pv, w: wt, l: ld, b:bt, d: de})
	d_min = d_derivate.evalf(subs={p:pv, w: wt, l: ld, b:bt, d: de})

	print ('p_derivate {} \nw_derivate {} \nl_derivate {} \nb_derivate {} \nd_derivate {}'.format(p_min, w_min, l_min, b_min, d_min))
	if ((np.abs(p_min) < error_ne) and \
	 	(np.abs(w_min) < error_ne) and \
	 	(np.abs(l_min) < error_ne) and \
	 	(np.abs(b_min) < error_ne) and \
	 	(np.abs(d_min) < error_ne)):
		return True
	else:
		return False

	