import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc

SMALL_SIZE = 10
MEDIUM_SIZE = 12
BIGGER_SIZE = 14

#rc('font',**{'family':'STIXGeneral','serif':['Palatino']})
font = {'family' : 'serif',
        'size'   : 12}

rc('font', **font)
rc('text', usetex=True)

rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
rc('xtick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
rc('figure', titlesize=BIGGER_SIZE)

a_k = 0.5
b = -20

def satisfaction(l_k, d_k = 1):
    val = d_k*b*(((l_k/d_k)**a_k)-1)
    return val

def graph():
    d_k = np.linspace(0.5,  1.5, 100)
    s_k = np.zeros(100)
    for i in range(0, 100):
        s_k[i] = satisfaction(d_k[i])
    fig = plt.figure(1, figsize=(6,5))
    ax = fig.add_subplot(1,1,1)
    for axis in ['top','bottom','left','right']:
  		ax.spines[axis].set_linewidth(1)
    ax.plot(d_k, s_k, 'r', linewidth= 2)
    ax.set_xlim(0.45, 1.55)
    ax.set_ylim(-5, 8)
    ax.set_xlabel(r"Actual Consumption/Nominal User Demand")
    ax.set_ylabel(r'Load satisfaction $S_k$')
    ax.tick_params(length = 5,bottom=True, top=False, left=True, right= True)
    ax.patch.set_linewidth(0.5) 
    fig_name = './satisfaction.eps'
    plt.savefig(fig_name, format='eps')
    plt.show()


if __name__ == '__main__':
	graph()
