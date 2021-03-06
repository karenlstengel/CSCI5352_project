import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.integrate import solve_ivp
from numpy.matlib import repmat
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from numpy.linalg import inv
import utilities

nStates = 100
tStates = np.linspace(0, 20, nStates-1)
b = utilities.betaVL(tStates, 0.2, 1.0)
bConst = utilities.betaConstant(tStates, np.mean(b))

plt.figure()
plt.subplot(121)
plt.title(r"$\beta(t)$ and infectious threshold")
plt.plot(tStates, utilities.betaVL(tStates, 0, 1.0), linewidth=2)
plt.plot([np.min(tStates), np.max(tStates)], [0.3, 0.3], 'k--', linewidth=2)
plt.xlabel("Time (days)", fontsize=14)
plt.ylabel("Probability of transmission", fontsize=14)
plt.subplot(122)
plt.title(r"$\beta(t)I_{\beta(t)\geq threshold}$")
plt.plot(tStates, utilities.betaVL(tStates, 0.3, 1.0), linewidth=2)
plt.show()
