import numpy as np

##Penalty function modelling
alpha = 0.5

##PV modelling
pv_unit_electric_price = 5.0
pv_unit_maintenance_cost = 1.0

#WT modelling
wt_unit_electric_price = 4.0
wt_unit_maintenance_cost = 3.0

##Diesel modelling
de_oil_price = 3.0
de_unit_electric_price = 4.0
de_unit_maintenance_cost = 3.0
de_rate_oil_consumption = 2
de_a_oil_consumption = 1
de_b_oil_consumption= 2
de_c_oil_consumption = 1
de_min = 0
de_max = 10
de_ramp_up = 2
de_ramp_down = 1
de_min_running_time = 0.3

##Battery modelling
bt_unit_electric_price = 0.1
bt_unit_maintenance_cost = 0.05
bt_self_dis_rate = 0.0001
bt_capacity = 10 
bt_char_eff = 0.95
bt_dis_eff = 0.95
bt_soc_max = 100
bt_soc_min = 60
bt_power_charge = -0.2 *  bt_capacity * bt_char_eff
bt_power_discharge = 0.2 *  bt_capacity * bt_dis_eff
bt_soc = 100

##Load modelling
ld_weight_satisfaction = 0.9
ld_unit_electric_price = 2
ld_beta = -20
ld_alpha = 0.5
ld_nom = 0.022

##Penalty function to restrict power balance
def penalty_fn(pv, wt, de, bt, ld):
	return pv + wt + de + bt - ld

##Utility function of PV taking into account power balance
def pv_utility_fn(pv, wt, ld, bt, de, dt):
	#pv = pv[0]
	#print ('PV {}'.format(pv))
	#print ('WT {}'.format(wt))
	#print ('LD {}'.format(ld))
	#print ('BT {}'.format(bt))
	#print ('DE {}'.format(de))

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

def ramp_up_oil_constraint_fn(de_curr, de_past, dt):
	if((de_curr - de_past) < (dt*de_ramp_up)):
		return True
	else:
		return False

def ramp_down_oil_constraint_fn(de_curr, de_past, dt):
	if((de_past - de_curr) < (dt*de_ramp_down)):
		return True
	else:
		return False

def minimun_running_time_de_constraint_fn(de_activation_list, dt):
	len_de_act = len(de_activation_list)
	counter = 0
	running_times = [] 
	for i in range(len_de_act):
		if (de_activation_list[i]==1):
			counter =+ 1
		else:
			if(counter!=0):
				if (counter*dt < de_min_running_time):
					return False
				running_times.append(counter*dt)
				counter = 0
	return True

def bt_utility_fn(bt, pv, wt, ld, de, dt):
	#print ('bt {}'.format(bt))
	#print ('pv {}'.format(pv))
	#print ('wt {}'.format(wt))
	#print ('ld {}'.format(ld))
	#print ('de {}'.format(de))
	print ('penalty_fn {}'.format(-alpha*np.power(penalty_fn(pv,wt,de,bt,ld),2)))
	return -1*(bt_unit_electric_price*bt*dt \
		- bt_unit_maintenance_cost*np.abs(bt)*dt \
		- alpha * np.power(penalty_fn(pv,wt,de,bt,ld),2))

def soc_bt_update_fn(bt, dt):
	global bt_soc
	bt_soc = soc_bt_fn(bt,dt)


def soc_bt_fn(bt, dt):
	global bt_soc
	print ('soc_bt_fn')
	print ('bt {}'.format(bt))
	print ('bt_soc {}'.format(bt_soc))
	bt_soc = (bt_soc*(1-bt_self_dis_rate) - (bt*dt)/bt_capacity*bt_char_eff)
	return bt_soc


def soc_bt_max_constraint_fn(bt, dt):
	soc_bt_max_cn = bt_soc_max - bt_soc
	print ('soc_bt_max_cn {}'.format(soc_bt_max_cn))
	return soc_bt_max_cn

def soc_bt_min_constraint_fn(bt, dt):
	soc_bt_min_cn = soc_bt_fn(bt, dt) - bt_soc_min 
	print ('soc_bt_min_cn {}'.format(soc_bt_min_cn))
	return soc_bt_min_cn

#def bt_energy_min_max_constraint(bt,dt):
#	if ((bt*dt < bt_energy_max) and (bt*dt > bt_energy_min)):
#		return True
#	else:
#		return False

def bt_power_constraint(bt,dt):
	print ('bt_power_charge {}'.format(bt_power_charge))
	print ('bt_power_discharge {}'.format(bt_power_discharge))
	global bt_soc
	print ('bt_soc 1 {}'.format(bt_soc))
	bt_soc = soc_bt_fn(bt, dt)
	print ('bt_soc 2 {}'.format(bt_soc))
	bt_power_max_charge = max(bt_power_charge, -(bt_soc_max - bt_soc)*bt_capacity*bt_char_eff)
	bt_power_max_discharge = min(bt_power_discharge, (bt_soc - bt_soc_min)*bt_capacity*bt_dis_eff)

	
	print('bt_power_max_charge {}'.format(bt_power_max_charge))
	print('bt_power_max_discharge {}'.format(bt_power_max_discharge))
	return bt_power_max_charge, bt_power_max_discharge

##Utility function of LD taking into account power balance
def ld_utility_fn(ld, pv, wt, bt, de, dt):
	#ld = ld[0]
	#print ('PV {}'.format(pv))
	#print ('WT {}'.format(wt))
	#print ('LD {}'.format(ld))
	#print ('BT {}'.format(bt))
	#print ('DE {}'.format(de))
	return ((1-ld_weight_satisfaction)*ld_unit_electric_price*ld + ld_weight_satisfaction*ld_satifaction_fn(ld))

## Satisfaction function of load consumption
def ld_satifaction_fn(ld):
	return ld_nom*ld_beta*(np.power((ld/ld_nom),ld_alpha) - 1)