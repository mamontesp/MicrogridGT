import matplotlib.pyplot as plt
import numpy as np

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
    fig = plt.figure(1)
    ax = fig.add_subplot(1,1,1)
    for axis in ['top','bottom','left','right']:
  		ax.spines[axis].set_linewidth(2)
    ax.plot(d_k, s_k, 'r', linewidth= 5)
    ax.set_xlim(0.45, 1.55)
    ax.set_ylim(-5, 8)
    ax.set_xlabel("Actual Consumption/Nominal User Demand")
    ax.set_ylabel(r'Load satisfaction $S_k$')
    ax.tick_params(length = 5,bottom=True, top=False, left=True, right= True)
    ax.patch.set_linewidth(0.5) 
    fig_name = './satisfactionFunction.eps'
#    plt.rcParams['axes.linewidth']=1
    plt.savefig(fig_name, format='eps', dpi =1000)
    plt.show()


if __name__ == '__main__':
	graph()
