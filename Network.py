import numpy as np
import random
import csv
import math
from scipy.sparse import csr_matrix
from utils import *

class Network:
    def __init__(self, nodes, edge_list, node_attrs = None, k = 2.5):
        '''
            num_nodes : number of nodes in the network if not passing in a file
        '''
        #NEED TO UPDATE SOME OF THESE TO ACCOUNT FOR THE OTHER WAYS TO LOAD IN OR GENERATE NETWORKS...
        self.contagionModel = contagionType # could also be SIR

        default_node_attrs = node_attrs if node_attrs is not None else {'status': 'S', 'infect_time': -1, 'infect_prob': 0.0, 'remove_time': -1}
        # this dictionary will be assigned to each node at initialization unless we pass in a list.
        self.node_list = dict({n:dict(default_node_attrs) for n in nodes})
        self.netType = 'temporal' if len(edge_list) > 1 else 'static'
        self.edge_list = edge_list # need to generate for each timestep based off of edge_probs[p]
        self.pos = setPos(k)

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

            drawContagion_nx(self.edgeList, self.nodeList, list(edgeList.keys())[t], exp_name = 'testing_drawFunc_nx/', pos = self.pos)

        return np.array(times), np.array(S), np.array(I), np.array(R)

    def setPos(self, k = 2.5):
        G_temp = nx.Graph()
        for t in self.edgeList.keys():
            #all_edges_inTime.add(edgeList[t])
            G_temp.add_edges_from(self.edgeList[t])

        self.pos = nx.spring_layout(G_temp, k = k)
