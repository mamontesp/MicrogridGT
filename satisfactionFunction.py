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
    plt.plot(d_k, s_k, 'r', label="Load satisfaction")
    plt.legend()
    plt.xlim(0.45, 1.55)
    plt.ylim(-5, 10)
    plt.title(r'$S_k, \alpha =0.5 \beta = $-1')
    plt.xlabel("Actual Consumption/Nominal User Demand")
    plt.ylabel(r'$S_k$')
    plt.grid()
    fig_name = './satisfactionFunction.eps'
    plt.savefig(fig_name, format='eps', dpi =1000)
    plt.show()


if __name__ == '__main__':
    graph()
