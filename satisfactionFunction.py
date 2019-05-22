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
    plt.plot(d_k, s_k)
    plt.xlim(0.4, 1.6)
    plt.ylim(-7, 15)
    plt.title("Satisfaction function")
    plt.xlabel("Demand")
    plt.ylabel("Satisfaction")
    plt.grid()
    plt.show()

if __name__ == '__main__':
    graph()
