import numpy as np
import random
import csv
import math
from scipy.sparse import csr_matrix
from utils import *

class Network:
    def __init__(self, nodes, edge_list, node_attrs = None, k = 2.5, SIR_prob = 0.1):
        '''
            num_nodes : number of nodes in the network if not passing in a file
        '''
        #NEED TO UPDATE SOME OF THESE TO ACCOUNT FOR THE OTHER WAYS TO LOAD IN OR GENERATE NETWORKS...
        self.contagionModel = contagionType # could also be SIR

        default_node_attrs = node_attrs if node_attrs is not None else {'status': 'S', 'infect_time': -1, 'viral_loads': [], 'remove_time': -1}
        # this dictionary will be assigned to each node at initialization unless we pass in a list.
        self.node_list = dict({n:dict(default_node_attrs) for n in nodes})
        self.netType = 'temporal' if len(edge_list) > 1 else 'static'
        self.edge_list = edge_list # need to generate for each timestep based off of edge_probs[p]
        self.pos = setPos(k) #for visualizations
        self.SIR_prob = SIR_prob

    def run_temporal_contagion(self, gamma, beta, tmin=0, tmax=100, dt=1, time_steps = 'daily', initial_infected=None, initial_recovered=None, useEdgeDuration = False, exp_name = 'testing_drawFunc_nx/'):
        # dt in
        n = len(self.node_list)

        if initial_infected is None:
            initial_infected = random.randrange(n)
            self.node_list[n]['status'] = 'I'
            self.node_list[n]['infect_time'] = tmin
            self.node_list[n]['viral_loads'] = viral_load(time_steps) #might need to change this based on literature....
            self.node_list[n]['remove_time'] = len(self.node_list[n]['viral_loads'])
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
            #account for a static network
            index = t
            if self.netType == 'static':
                index = 0

            # infect shit
            for infected_node in I:
                prob_of_infection = 0.0

                if self.contagionModel == 'VL':
                    # -> calculate viral viral_load at time t (t - 'infected_time')
                    vl_current = self.node_list[infected_node][t - self.node_list[infected_node]['infect_time']]

                    # ->calculate probability of infection: infectiousness was taken to be proportional to the logarithm of viral load in excess of 106 cp/ml {Larremore 2020}
                    prob_of_infection = vl_prob(vl_current)
                else:
                    #else -> use default SIR probability
                    prob_of_infection = self.SIR_prob

                #if VL is low enough and time since infection is > 7 # might change DOUBLE CHECK THIS IF NEEDED.
                if (t - nodeList[infected_node]['infect_time']) >= 7 and vl_current <= threshold:
                    print("not infectious")
                    # set status of i to 'R' and change removed time to be t
                    self.node_list[infected_node]['status'] = 'R'
                    # remove from I
                    I.remove(infected_node)

                else:
                    for edge_tuple in edge_list[index]: # of i at time t
                        if infected_node in edge_tuple:

                            #if node is 'S'
                            i_n_index = edge_tuple.index(infected_node)
                            neighbor = edge_tuple[0]
                            if i_n_index == 0:
                                neighbor = edge_tuple[1]
                            if edge_tuple[neighbor]['status'] == 'S':

                                # do edge duration if using
                                if useEdgeDuration:
                                    duration = get_edge_duration(edgeList, edge, t)
                                    prob_of_infection = prob_with_edge_duration(prob_of_infection, duration)
                                
                                #infect with probablility p
                                to_infect = random.random()
                                if to_infect < prob_of_infection:
                                    # update status, infect_time at time t
                                    self.node_list[neighbor]['status'] = 'I'
                                    self.node_list[neighbor]['infect_time'] = t
                                    self.node_list[neighbor]['viral_loads'] = viral_load(time_steps)
                                    self.node_list[neighbor]['remove_time'] = t + len(self.node_list[neighbor]['viral_loads'])

            for n in self.node_list.keys():
                if self.node_list[n]['status'] == 'I':
                    # check if this is the last day its infectious
                    if(t - self.node_list[infected_node]['infect_time']) > len(self.node_list[n]['viral_loads']):
                        # no longer infectious. remove from I and add to R
                        I.remove(n)
                        R.add(n)
                    else: # otherwise add it to I
                        I.add(n)
                elif self.node_list[n]['status'] == 'R':
                    R.add(n)

            t += dt
            times.append(t)

            drawContagion_nx(self.edgeList, self.nodeList, list(self.edge_list.keys())[index], exp_name = 'testing_drawFunc_nx/', pos = self.pos)
        for n_final in self.node_list.keys():
            if n_final not in I and n_final not in R:
                S.add(n_final)
        return np.array(times), np.array(S), np.array(I), np.array(R)

    def setPos(self, k = 2.5):
        G_temp = nx.Graph()
        for t in self.edgeList.keys():
            #all_edges_inTime.add(edgeList[t])
            G_temp.add_edges_from(self.edge_list[t])

        self.pos = nx.spring_layout(G_temp, k = k)
