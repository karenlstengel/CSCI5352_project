import numpy as np
import matplotlib.pyplot as plt
import math
from numpy.linalg import inv
import utilities

N = 1000
nInfectiousStates = 10
tStates = np.linspace(0, 20, nInfectiousStates)
threshold = 0.2
pCrit =  utilities.calculateCriticalMax(N, nInfectiousStates, tStates, threshold)
print(pCrit)
print(N*np.sum(utilities.betaVL(tStates, threshold, pCrit)))

T = np.zeros((nInfectiousStates, nInfectiousStates))
S = np.diag(-np.ones(nInfectiousStates), k=0) + np.diag(np.ones(nInfectiousStates-1), k=-1)
p = np.linspace(0.0, 20*pCrit, 100)
spectralRadius = list()
for pMax in p:
    T[0, :] = N*utilities.betaVL(tStates, threshold, pMax)
    l = np.linalg.eigvals(-np.matmul(T,inv(S)))
    spectralRadius.append(np.max(np.abs(l)))

plt.figure()
plt.plot(p, spectralRadius, 'k-')
plt.plot([pCrit, pCrit],[0, 2], 'r--')
plt.ylabel("Spectral Radius")
plt.xlabel(r"$p_{max}$")
plt.show()
