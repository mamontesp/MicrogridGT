import numpy as np

##Utility PV definitions
pv_unit_electric_price = 5.0
pv_unit_maintenance_cost = 1.0
wt_unit_electric_price = 4.0
wt_unit_maintenance_cost = 3.0
de_unit_electric_price = 4.0
de_oil_price = 3.0
de_unit_maintenance_cost = 3.0
de_rate_oil_consumption = 2
alpha = 0.1

##Penalty function to restrict power balance
def penalty_fn(pv, wt, de, bt, ld):
	return pv + wt + de + bt - ld

##Utility function of PV taking into account power balance
def pv_utility_fn(pv, wt, de, bt, ld, dt):
	return -1*(pv_unit_electric_price-pv_unit_maintenance_cost)*pv*dt \
	- alpha * np.power(penalty_fn((pv,wt,de,bt,ld),2))

##Utility function of WT taking into account power balance
def wt_utility_fn(pv, wt, de, bt, ld, dt):
	return -1*(wt_unit_electric_price-wt_unit_maintenance_cost)*wt*dt \
	- alpha * np.power(penalty_fn((pv,wt,de,bt,ld),2))

##Utility function of DE taking into account power balance
def de_utility_fn(pv, wt, de, bt, ld, dt):
	return -1*(de_unit_electric_price-de_unit_maintenance_cost)*de*dt - de_oil_price * de_rate_oil_consumption \
		- alpha * np.power(penalty_fn((pv,wt,de,bt,ld),2))



