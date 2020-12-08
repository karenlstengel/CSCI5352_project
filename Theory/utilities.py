import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.integrate import solve_ivp
from numpy.linalg import inv


def betaVL(t, threshold, maxP):
    timeToPeak = 4
    p = math.e/timeToPeak*np.multiply(t, np.exp(-t/timeToPeak))
    p[np.where(p < threshold)] = 0
    return maxP*p

def betaConstant(t, p):
    return p*np.ones(np.size(t,axis=0))

def f(t, X, beta):
    S = X[0]
    I = X[1:]
    n = np.size(beta, axis=0)+1
    dX = np.zeros(np.size(beta, axis=0)+1)
    dX[0] = -S*np.sum(np.multiply(beta, I))
    dX[1] = S*np.sum(np.multiply(beta, I)) - I[0]
    dX[2:-1] = I[0:-2] - I[1:-1]
    dX[-1] = I[-2]
    return dX

def calculateCriticalMax(N, nInfectiousStates, tStates, threshold, tolerance=0.01):
    T = np.zeros((nInfectiousStates, nInfectiousStates))
    S = np.diag(-np.ones(nInfectiousStates), k=0) + np.diag(np.ones(nInfectiousStates-1), k=-1)

    pMin = 0
    T[0, :] = N*betaVL(tStates, threshold, pMin)
    l = np.linalg.eigvals(-np.matmul(T,inv(S)))
    lowerRho = np.max(np.abs(l))

    pMax = 1.0
    T[0, :] = N*betaVL(tStates, threshold, pMax)
    l = np.linalg.eigvals(-np.matmul(T,inv(S)))
    upperRho = np.max(np.abs(l))

    if upperRho < 1.0:
        print("Uhhhhh.")
        return
    maxIterations = 100
    iterations = 0
    while upperRho - lowerRho > tolerance and iterations <= maxIterations:
        pNew = 0.5*(pMin + pMax)
        T[0, :] = N*betaVL(tStates, 0.2, pNew)
        l = np.linalg.eigvals(-np.matmul(T,inv(S)))
        newRho = np.max(np.abs(l))
        if newRho < 1.0:
            lowerRho = newRho
            pMin = pNew
        else:
            upperRho = newRho
            pMax = pNew
        iterations += 1
    return pMin
