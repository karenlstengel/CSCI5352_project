import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.integrate import solve_ivp
from numpy.matlib import repmat
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from numpy.linalg import inv

tmax = 150
nStates = 100
tStates = np.linspace(0, 20, nStates-1)
b = betaVL(tStates, 0.3, 1.0)
bConst = betaConstant(tStates, np.mean(b))

N = 1000
initial_states = np.zeros(nStates)
initial_states[1] = 1
initial_states[0] = N - np.sum(initial_states[1:])
sol1 = solve_ivp(f, (0, tmax), initial_states, t_eval=np.arange(0, tmax, 0.1), args=(b,))
t1 = sol1.t
y1 = sol1.y.T

sol2 = solve_ivp(f, (0, tmax), initial_states, t_eval=np.arange(0, tmax, 0.1), args=(bConst,))
t2 = sol2.t
y2 = sol2.y.T

plt.figure()
plt.subplot(121)
plt.title(r"$\beta(t)$ and infectious threshold")
plt.plot(tStates, betaVL(tStates, 0, 1.0), linewidth=2)
plt.plot([np.min(tStates), np.max(tStates)], [0.3, 0.3], 'k--', linewidth=2)
plt.xlabel("Time (days)", fontsize=14)
plt.ylabel("Probability of transmission", fontsize=14)
plt.subplot(122)
plt.title(r"$\beta(t)I_{\beta(t)\geq threshold}$")
plt.plot(tStates, betaVL(tStates, 0.3, 1.0), linewidth=2)
plt.show()

plt.figure()
plt.plot(t1, y1[:, 0], label=r"$S$")
plt.plot(t1, y1[:, 1], label=r"$I_1$")
plt.plot(t1, y1[:, -1], label=r"$I_n$")
plt.ylabel("Number of people")
plt.xlabel("Time (days)", fontsize=14)
plt.legend()

plt.figure()
plt.plot(t1, y1[:, 0], label="S")
for i in np.arange(1, nStates, 10, dtype=int):
    plt.plot(t1, y1[:, i], label="I"+ str(i))
plt.ylabel("Number of people", fontsize=14)
plt.xlabel("Time (days)", fontsize=14)
plt.legend()
plt.show()

plt.figure()
plt.subplot(311)
plt.title(r"$\beta(t)=\frac{e}{4} t e^{-t/4}$")
plt.imshow(y1.T, cmap=cm.coolwarm, aspect="auto", extent=(0, tmax, 0, nStates))
plt.subplot(312)
plt.title(r"$\beta(t)=c$")
plt.imshow(y2.T, cmap=cm.coolwarm, aspect="auto", extent=(0, tmax, 0, nStates))
plt.subplot(313)
plt.title("Difference")
plt.imshow(y2.T - y1.T, aspect="auto", extent=(0, tmax, 0, nStates))
plt.xlabel("Time (days)")
plt.ylabel("State Number")
plt.tight_layout()
plt.show()


N = 1000
nStates = 100
tStates = np.linspace(0, 20, nStates)
T = np.zeros((nStates, nStates))
S = np.diag(-np.ones(nStates), k=0) + np.diag(np.ones(nStates-1), k=-1)
p = np.arange(0.0, 1, 0.01)
spectralRadius = list()
for pMax in p:
    T[0, :] += N*betaVL(tStates, 1.0, pMax)
    l = np.linalg.eigvals(-np.matmul(T,inv(S)))
    spectralRadius.append(np.max(np.abs(l)))

plt.figure()
plt.plot(p, spectralRadius)
plt.show()
