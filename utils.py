import numpy as np
import random
import csv
import math
from scipy.sparse import csr_matrix
import graph_tool as gt

def drawTimeStep(edgeList, nodeList, ts):
    print('Drawing the graph for time ' + str(ts))

    # make a graph from edgelist
    # add attributes to nodes

# Helper functions
# use this to import sociopatterns data
def import_temporal_networks(filename, delimiter = " "):
    temporalEdgeList = dict()
    node_num = set([])
    with open(filename) as contactData:
        contactList = csv.reader(contactData, delimiter=delimiter)
        for contact in contactList:
            t = float(contact[0])
            i = int(contact[1])
            j = int(contact[2])
            node_num.add(i)
            node_num.add(j)
            try:
                temporalEdgeList[t].extend([(i,j), (j,i)])
            except:
                temporalEdgeList[t] =[(i,j), (j,i)]
    return len(node_num), temporalEdgeList

def viral_load(time):
    # update with implementation similar to what Dan has in testing paper
    # other options
    # for a placeholder, here is a gamma function
    return time/4*math.exp(time/2)
def vl_prob():
    # update with implementation similar to what Dan has in testing paper
    return 0.5

def generate_activities(n, exponent, nu, epsilon):
    activities = list()
    for index in range(n):
        u = random.uniform(0, 1)
        activities.append(nu*invCDFPowerLaw(u, epsilon, 1, exponent))
    return sorted(activities)

def invCDFPowerLaw(u, a, b, exponent):
    return (a**(1-exponent) + u*(b**(1-exponent) - a**(1-exponent)))**(1/(1-exponent))
