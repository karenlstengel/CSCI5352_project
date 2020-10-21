import numpy as np
import random
import math

def run_temporal_SIR(temporal_network, gamma, beta, tmin=0, tmax=100, dt=1, initial_infected=None, initial_recovered=None):
    n = temporal_network.number_of_nodes()
    if initial_infected is None:
        initial_infected = random.randrange(n)
    if initial_recovered is None:
        initial_recovered = []

    t = tmin
    I = [len(initial_infected)]
    R = [len(initial_recovered)]
    S = [n - I[0] - R[0]]
    times = [tmin]
    while time <= tmax:
        # infect shit

        t += dt
        times.append(t)
    return np.array(times), np.array(S), np.array(I), np.array(R)

def run_temporal_viral_load(temporal_network, gamma, beta, tmin=0, tmax=100, dt=1, initial_infected=None, initial_recovered=None):
    n = temporal_network.number_of_nodes()
    if initial_infected is None:
        initial_infected = random.randrange(n)
    if initial_recovered is None:
        initial_recovered = []

    t = tmin
    I = [len(initial_infected)]
    R = [len(initial_recovered)]
    S = [n - I[0] - R[0]]
    times = [tmin]
    while time <= tmax:
        # infect shit

        t += dt
        times.append(t)
    return np.array(times), np.array(S), np.array(I), np.array(R)

# Helper functions
def viral_load(time):
    # for a placeholder, here is a gamma function
    return time/4*math.exp(time/2)
