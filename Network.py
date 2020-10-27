import numpy as np
import random
import csv
import math
from scipy.sparse import csr_matrix
from utils import *

class Network:
    def __init__(self, num_nodes = 100, edge_probs = [], contagionType = "VL", filename = None, delimiter = " ", node_attrs = None):
        '''
            num_nodes : number of nodes in the network if not passing in a file
        '''
        #NEED TO UPDATE SOME OF THESE TO ACCOUNT FOR THE OTHER WAYS TO LOAD IN OR GENERATE NETWORKS...
        self.contagionModel = contagionType # could also be SIR

        default_node_attrs = node_attrs if node_attrs is not None else {'status': 'S', 'infect_time': -1, 'infect_prob': 0.0, 'remove_time': -1}
        # this dictionary will be assigned to each node at initialization unless we pass in a list.
        if filename is None:
            self.node_list = {t:{n:default_node_attrs for n in range(num_nodes)} for t in range(len(edge_probs))} #num_nodes
            self.edge_probs = edge_probs
            self.netType = 'temporal' if len(edge_probs) > 1 else 'static'
            self.edge_list = {} # need to generate for each timestep based off of edge_probs[p]
        else:
            num_nodes, self.edge_list = import_temporal_networks(filename, delimiter)
            self.node_list = {t:{n:default_node_attrs for n in range(num_nodes)} for t in range(len(self.edge_list))}



    def run_temporal_contagion(self, gamma, beta, tmin=0, tmax=100, dt=1, initial_infected=None, initial_recovered=None):
        n = len(self.node_list)

        if initial_infected is None:
            initial_infected = random.randrange(n)
            self.node_list[t][n]['status'] = 'I'
            self.node_list[t][n]['infect_time'] = tmin

        if initial_recovered is None:
            initial_recovered = []

        if len(temporal_network) > 1: #case where we are doing dynamics on a dynamic network
            tmax = len(temporal_network)

        t = tmin
        I = set([initial_infected]) # list of infected nodes at time t
        R = set(initial_recovered) # list of recovered nodes at time t

        S = [n - len(I) - len(R)]
        times = [tmin]
        while t <= tmax:
            # infect shit
            # for i in I:
                # if self.contagionModel == 'VL' -> calculate viral viral_load at time t (t - 'infected_time')
                # ->calculate probability of infection: infectiousness was taken to be proportional to the logarithm of viral load in excess of 106 cp/ml {Larremore 2020}
                #else -> use default SIR probability

                #if VL is low enough and time since infection is > 7 # might change
                    # set status of i to 'R' and change removed time to be t
                    # remove from I
                    # add to R
                #for nodes in edge list of i at time t
                    #if node is 'S'
                        #infect with probablility p
                        #add to I
                        # update status, infect_time at time t

            t += dt
            times.append(t)
        return np.array(times), np.array(S), np.array(I), np.array(R)

    #need to update these to work with OOP design

    def construct_activity_driven_model(self, n, m, activities, tmin=0, tmax=100, dt=1):
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

    def construct_neighbor_exchange_model(self, initialA, tmin=0, tmax=100, dt=1):
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

    def temporal_to_static_network(self, temporalA, isWeighted=False):
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


    def generate_activities_from_data(self, filename, delimiter, n, exponent, a, b, nu, epsilon):
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
