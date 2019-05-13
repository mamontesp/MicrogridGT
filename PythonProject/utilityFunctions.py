import numpy as np

##Penalty function modelling
alpha = 0.1

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
a_oil_consumption = 1
b_oil_consumption= 2
c_oil_consumption = 1
de_min = 1
de_max = 10
de_ramp_up = 2
de_ramp_down = 1
de_min_running_time = 0.3

##Battery modelling
bt_unit_electric_price = 1.0
bt_unit_maintenance_cost = 2.0
bt_self_dis_rate = 0.001
bt_capacity = 10 
bt_char_eff = 0.95
bt_dis_eff = 1/0.95
bt_soc_max = 100
bt_soc_min = 60
bt_energy_min = -0.2 *  bt_capacity / bt_char_eff
bt_energy_max = 0.2 *  bt_capacity * bt_dis_eff

##Load modelling
ld_weight_satisfaction = 0.2
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

	return -1*((pv_unit_electric_price-pv_unit_maintenance_cost)*pv*dt \
	- alpha * np.power(penalty_fn(pv,wt,de,bt,ld),2))

##Utility function of WT taking into account power balance
def wt_utility_fn(wt, pv, ld, bt, de, dt):
	return -1*((wt_unit_electric_price-wt_unit_maintenance_cost)*wt*dt \
	- alpha * np.power(penalty_fn(pv,wt,de,bt,ld),2))

##Utility function of DE taking into account power balance
def de_utility_fn(de, pv, wt, ld, bt, dt):
	return -1*((de_unit_electric_price-de_unit_maintenance_cost)*de*dt - de_oil_price * de_rate_oil_consumption * dt\
	- alpha * np.power(penalty_fn(pv,wt,de,bt,ld),2))

##Rate consumption of oil function
def rate_oil_consumption_fn(de):
	return aOil* np.power(de,2) + bOil*de + cOil

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
		return (bt_unit_electric_price*bt*dt \
			- bt_unit_maintenance_cost*np.abs(bt)*dt \
			- alpha * np.power(penalty_fn(pv,wt,de,bt,ld),2))

def soc_bt_fn(bt, soc_curr, soc_past):
	if (bt > 0):
		soc_curr = soc_past*(1-bt_self_dis_rate) - (bt*dt)/bt_capacity*bt_dis_eff
	else:
		soc_curr = soc_past*(1-bt_self_dis_rate) - (bt*dt)/bt_capacity*bt_char_eff

def soc_bt_max_min_constraint_fn(soc):
	if ((soc < bt_soc_max) and (soc > bt_soc_min)):
		return True
	else:
		return False

def bt_energy_min_max_constraint(bt):
	if ((bt*dt < bt_energy_max) and (bt*dt > bt_energy_min)):
		return True
	else:
		return False

def bt_energy_to_charge_constraint(soc):
	bt_energy_max_charge = np.max(bt_energy_max, -(bt_soc_max - soc)*bt_capacity*bt_char_eff)
	bt_energy_max_discharge = np.min(bt_energy_min, (soc - bt_soc_min)*bt_capacity*bt_dis_eff)
	return bt_energy_max_charge, bt_energy_max_discharge


##Utility function of LD taking into account power balance
def ld_utility_fn(ld, pv, wt, bt, de, dt):
	return ((1-ld_weight_satisfaction)*ld_unit_electric_price*ld + ld_weight_satisfaction*ld_satifaction_fn(ld))

## Satisfaction function of load consumption
def ld_satifaction_fn(ld):
	return ld_nom*ld_beta*(np.power((ld/ld_nom),ld_alpha) - 1)


##Bounds definitions
#def pv_bounds(pv):
#	return 0, pv

#def wt_bounds(wt):
#	return 0, wt

#def ld_bounds(ld):
#	return ld*0.95, ld*1.05

#def bt_bounds(a):
	##Argument added just for keep a similar structure to previous functions
#	return (bt_energy_min/dt), (bt_energy_max/dt)

#def de_bounds(a):
	##Argument added just for keep a similar structure to previous functions
#	return de_min, de_max

