import time
from functools import partial
import numpy as np
from scipy.optimize import minimize_scalar

def error(w1, w0, x, y_actual):
    y_pred = w0 + w1 * x
    mse = ((y_actual - y_pred) ** 2).mean()
    return mse

##Utility function of PV taking into account power balance
##Penalty function modelling
alpha = 0.1
##Penalty function to restrict power balance
def penalty_fn(pv, wt, de, bt, ld):
    return pv + wt + de + bt - ld

##PV modelling
pv_unit_electric_price = 5.0
pv_unit_maintenance_cost = 1.0

def pv_utility_fn(pv, wt, ld, bt, de, dt):
    #pv = pv[0]
    print ('PV {}'.format(pv))
    print ('WT {}'.format(wt))
    print ('LD {}'.format(ld))
    print ('BT {}'.format(bt))
    print ('DE {}'.format(de))

    return float(-1*((pv_unit_electric_price-pv_unit_maintenance_cost)*pv*dt \
    - alpha * np.power(penalty_fn(pv,wt,de,bt,ld),2)))



w0 = 50
x = np.arange(int(1e5))
y = np.arange(int(1e5)) + 52
error_partial = partial(error, w0=w0, x=x, y_actual=y)

wt = 0.17
ld = 0.1289866668
bt = 0
de = 0
dt = 0.083
pv_partial = partial(pv_utility_fn, wt=wt, ld=ld, bt=bt, de=de, dt=dt)
pv = minimize_scalar(pv_partial, bounds=(0, 2))
print ('pv solutions')
print pv
print ('pv solutions 2')
p_time = []
for _ in range(100):
    p_time_ = time.time()
    p = minimize_scalar(error_partial, bounds=(-5, 5))
    print p
    p_time_ = time.time() - p_time_
    p_time.append(p_time_  / p.nfev)

l_time = []
for _ in range(100):
    l_time_ = time.time()
    l = minimize_scalar(lambda w1: error(w1, w0, x, y), bounds=(-5, 5))
    print l
    l_time_ = time.time() - l_time_
    l_time.append(l_time_ / l.nfev)

print('Same performance?{}'.format(np.median(p_time) == np.median(l_time)))
# Same performance? True