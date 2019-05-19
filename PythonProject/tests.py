from scipy.optimize import fmin
from scipy.optimize import minimize
from scipy.optimize import minimize_scalar
from scipy.optimize import Bounds
from functools import partial

import loadingData
import utilityFunctions as uf
import game

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
	ld_b = ld[t]
	bt_b = -0.089
	de_b = 0.0
	uf.verifyNashEquilibrium(pv_b, wt_b, ld_b, bt_b, de_b, dt, ld[t])