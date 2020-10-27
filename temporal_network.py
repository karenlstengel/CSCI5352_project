import numpy as np
import random
import csv
from scipy.sparse import csr_matrix

def generate_activities(n, exponent, nu, epsilon):
    activities = list()
    for index in range(n):
        u = random.uniform(0, 1)
        activities.append(nu*invCDFPowerLaw(u, epsilon, 1, exponent))
    return sorted(activities)

def invCDFPowerLaw(u, a, b, exponent):
    return (a**(1-exponent) + u*(b**(1-exponent) - a**(1-exponent)))**(1/(1-exponent))

def construct_activity_driven_model(n, m, activities, tmin=0, tmax=100, dt=1):
    # at each time step turn on a node w.p. a_i *deltaT
    t = tmin
    temporalEdgeList = dict()
    while t < tmax:
        edgeList = list()
        for index in range(n):
            if random.random() <= activities[index]*dt:
                indices = random.sample(range(n), m)
                edgeList.extend([(index, j) for j in indices])
                edgeList.extend([(j, index) for j in indices])
        temporalEdgeList[t] = edgeList
        t += dt
    return temporalEdgeList

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

# use this to import sociopatterns data
def import_temporal_networks(filename, delimiter):
    temporalEdgeList = dict()
    with open(filename) as contactData:
        contactList = csv.reader(contactData, delimiter=delimiter)
        for contact in contactList:
            t = float(contact[0])
            i = int(contact[1])
            j = int(contact[2])
            try:
                temporalEdgeList[t].extend([(i,j), (j,i)])
            except:
                temporalEdgeList[t] =[(i,j), (j,i)]
    return temporalEdgeList

def temporal_to_static_network(temporalA, isWeighted=False):
    if isWeighted:
        staticEdgeList = list()
    else:
        staticEdgeList = set()
    for time, edgeList in temporalA.items():
        for edge in edgeList:
            if isWeighted:
                staticEdgeList.append(edge)
            else:
                staticEdgeList.add(edge)
    if isWeighted:
        return staticEdgeList
    else:
        return list(staticEdgeList)


def generate_activities_from_data(filename, delimiter, n, exponent, a, b, nu, epsilon):
    activities = dict()
    with csv.open(filename, delimiter=delimiter) as contactList:
        for contactData in contactList:
            t = contactData[0]
            i = contactData[1]
            j =contactData[2]
            try:
                # increment the degree assuming undirected
                activities[t][i,j] += 1
                activities[t][j] += 1
            except:
                activities[t] = np.zeros(n)
                activities[t][i] = 1
                activities[t][j] = 1
    return activities # or should it be the average
