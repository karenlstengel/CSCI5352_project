import numpy as np

def construct_temporal_networks(n, model="activity", tmin=0, tmax=100, dt=1)
    if model == "activity-driven":
        print("under dev")
    elif model == "neighbor-exchange":
        # construct initial network with the configuration model
        print("under dev")
    elif model == "temporal-switching":
        print("under dev")

def construct_activity_driven_model(n, m, activities, tmin=0, tmax=100, dt=1):
    # at each time step turn on a node w.p. a_i *deltaT
    t = tmin
    temporalA = list()
    while t < tmax:
        A = np.zeros((n,n))
        for index in range(n):
            if random.random() <= activity[index]*dt:
                A[index, random.sample(range(n), m)] = 1
        temporalA.append(A)
        t += dt
    return temporalA

def construct_neighbor_exchange_model(initialA, tmin=0, tmax=100, dt=1):
    # this does random edge swaps
    A = initialA.copy()
    temporalA = [A]
    while t < tmax:
        i, j = np.nonzero(A)
        ix = random.sample(range(len(i)), 2)
        A[i[ix], j[ix]] = 0
        A[j[ix], i[ix]] = 0
        # thise might reduce the number of edges if this edge already exists
        A[i[ix], j[reverse(ix)]] = 1
        A[j[ix], i[reverse(ix)]] = 1
        t += dt
        temporalA.append(A)

    return temporalA

def construct_temporal_switching_model():
    print("under dev")

def poisson_edge_duration():
    print("under dev")

# use this to import sociopatterns data
def import_temporal_networks():
    print("under dev")
