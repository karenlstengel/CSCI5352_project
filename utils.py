import numpy as np
import random
import csv
import math
from scipy.sparse import csr_matrix
import graph_tool as gt

def drawContagion_nx(edgeList, nodeList, ts, exp_name = '', pos = None):
    #print("hi")
    if not os.path.exists('output/' + exp_name):
        os.makedirs('output/' + exp_name)

    plt.figure(figsize = (10,10))

    #for ts in [list(edgeList.keys())[0]]: #list(edgeList.keys())):
    print('Drawing the graph for time ' + str(ts))

    I = []
    S = []
    R = []

    G = nx.Graph()
    G.add_nodes_from(list(nodeList.keys()))
    #print('Nodes: ', G.nodes())
    #print(edgeList[ts])
    G.add_edges_from(edgeList[ts])
    #nx.draw(G)
    #G_gv = nx.nx_agraph.to_agraph(G)
    #print(G_gv.get_node('0'))

    for node, vals in nodeList.items():
        if vals['status'] == 'I':
            I.append(node)
        elif vals['status'] == 'S':
            S.append(node)
        elif vals['status'] == 'R':
            R.append(node)

    edge_probs = []
    for edge in edgeList[ts]:
        if nodeList[edge[0]]['status'] == 'I':
            if nodeList[edge[1]]['status'] == 'S':
                edge_probs.append(nodeList[edge[0]]['infect_prob'])

        elif nodeList[edge[1]]['status'] == 'I':
            if nodeList[edge[0]]['status'] == 'S':
                edge_probs.append(nodeList[edge[1]]['infect_prob'])
        else:
            edge_probs.append(nodeList[edge[0]]['infect_prob'])
        #G.edges()[edge]['weight'] = edge_colors[-1]
    #print(edge_probs)

    norm = mc.Normalize(vmin=0.0, vmax=1.0, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap='plasma')
    edge_colors = []
    for v in edge_probs:
        edge_colors.append(mapper.to_rgba(v))

    # nodes
    nx.draw_networkx_nodes(G,pos,
                       nodelist=S,
                       node_color='y',
                       node_size=50,
                       alpha=0.8,
                       label = 'S').set_edgecolor('k');
    nx.draw_networkx_nodes(G,pos,
                       nodelist=I,
                       node_color='r',
                       node_size=50,
                       alpha=0.8,
                       label = 'I').set_edgecolor('k');
    nx.draw_networkx_nodes(G,pos,
                       nodelist=R,
                       node_color='gray',
                       node_size=50,
                       alpha=0.8,
                       label = 'R').set_edgecolor('k');

    # edges
    e_cb = nx.draw_networkx_edges(G, pos, width=1.0,
                           edge_cmap = 'plasma',
                           edge_vmin = 0, edge_vmax = 1.0,
                           edge_color = edge_colors);

    labels={n:str(n) for n in nodeList.keys()}
    #nx.draw_networkx_labels(G,pos,labels,font_size=8)

    plt.legend(title = 'Legend');


    cbar = plt.colorbar(e_cb, ticks = np.arange(0.0, 1.1, 0.1), label = 'Probability of Infection')
    cbar.ax.set_yticklabels([str(round(n, 1)) for n in np.arange(0.0, 1.1, 0.1)])

    plt.title('Test 1, time: ' + str(int(ts)))
    plt.savefig('output/' + exp_name + 'simTime_{0:05d}.jpg'.format(int(ts)))
    #--------------------------------------------------------------------------

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

def viral_load(time_steps): # adjust for delta t

    #function based off of Dan's paper. might need to tweak based on how we do time scales
    #these are in terms of log_10
    vl_list = [0.0]

    # first point to draw from dist (first time of infectiousness)
    inf_onset_day = random.uniform(2,4) # VL = 10^3

    # peak point to draw from dist
    peak_day = inf_onset_day + 0.2 + math.gamma(1.8)
    peak_VL = unf(7, 11)

    # last point to draw from dist
    recovery_day = peak_day + random.uniform(5, 10) #VL = 10^6

    #slope before infectious
    s_beforeInf = (3 - 0)/(inf_onset_day - 0)

    #slope after infectious and before peak
    s_mid = (peak_VL - 3)/(peak_day - inf_onset_day)
    b_mid = peak_VL - s_mid*peak_day

    #slope after peak
    s_afterPeak = (peak_VL - 6)/(peak_day - recovery_day)
    b_afterPeak = peak_VL - s_afterPeak*peak_day
    #get day when we are no longer infectious, <= 3
    lastDay = (3 - b_afterPeak)/s_afterPeak # when VL = 3 again

    if time_steps == 'hour':
        lastDay = lastDay * 24
        inf_onset_day = inf_onset_day * 24
        peak_day = peak_day * 24

    elif time_steps == 'minute':
        lastDay = lastDay *24*60
        inf_onset_day = inf_onset_day * 24*60
        peak_day = peak_day * 24*60

    elif time_steps == 'daily':
        lastDay = int(lastDay)
        inf_onset_day = int(inf_onset_day)
        peak_day = int(peakDay)
        
    #iterate for each day and save to list based on slopes.
    t = 1
    while t <= lastDay: #fix below to account for different time scales
        if t < inf_onset_day:
            vl_list.append(s_beforeInf*t + 0)
        elif t == inf_onset_day:
            vl_list.append(3)
        elif inf_onset_day < t and t < peak_day:
            vl_list.append(s_mid*t + b_mid)
        elif t == peak_day:
            vl_list.append(peak_VL)
        else:
            vl_list.append(s_afterPeak*t + b_afterPeak)
        t = t + 1

    return vl_list

def vl_prob(viral_load):
    # update with implementation similar to what Dan has in testing paper
    if viral_load < 3:
        return 0.0
    elif viral_load >= 6:
        return 1.0
    else:
        return (math.log10(viral_load) - math.log10(3))/math.log10(2) # check on this

def get_edge_duration(edgeList, edge, t):
    return 0.0 # write this function

def prob_with_edge_duration(vl_prob, duration):
    #need to come up with how to increase the probability based off of how long duration is
    return 0.0

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
