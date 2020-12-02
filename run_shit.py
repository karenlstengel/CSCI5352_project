# run da functions etc
import os
import temporal_network
import matplotlib.pyplot as plt
import networkx as nx
import pickle
import webweb
from Network import *
from utils import * # TODO this is where the network builing functions will live
os.system('clear')

filename = "Data/School/thiers_2011.csv"
filename = "Data/School/thiers_2012.csv"
#filename = "Data/Workplace/tij_InVS.dat"
filename = "Data/School/primaryschool.csv"
filename = "Data/School/High-School_data_2013.csv" # 20 secs. -> convert to minutes
delimiter = " "

#nodesA, temporalA = import_temporal_networks(filename, delimiter)
n = 100
p = 0.15
m = 2
exponent = 2.8
nu = 100
epsilon = 1e-3
#
#activities = generate_activities(n, exponent, nu, epsilon)
#nodesA, temporalA = construct_activity_driven_model(n, m, activities, tmin=0, tmax=100, dt=1)
G = nx.gnp_random_graph(n, p, directed=False)
nodesA = G.nodes()
print(nodesA)
initial_infected = np.random.choice(list(nodesA))
#---------------------------------------------------------------------------------
#OOP Version
exp_name = 'static_VL/'

staticA = {0: list(G.edges())}#temporal_to_static_network(temporalA)
#network = Network(nodesA, temporalA, contagionType = 'VL')
network = Network(nodesA, staticA, contagionType = 'VL')

network.run_temporal_contagion(0, 0, tmax=100, exp_name = exp_name, time_steps = 'day', initial_infected = initial_infected)
#plot_stats(network.edge_list, network.node_list, tmax = 100, time_steps = 'day', exp_name = exp_name)

print('DONE.')
# pickle things to plot later
pickle.dump( network.edge_list, open( "output/" + exp_name + "edge_list.p", "wb" ) )
pickle.dump( network.node_list, open( "output/" + exp_name + "node_list.p", "wb" ) )


print("Starting SIR model")
exp_name = 'static_SIR/'
#network2 = Network(nodesA, temporalA, contagionType = 'SIR')
network2 = Network(nodesA, staticA, contagionType = 'SIR')

network2.run_temporal_contagion(0, 0, tmax=1000, exp_name = exp_name, time_steps = 'day', initial_infected = initial_infected)
#plot_stats(network.edge_list, network.node_list, tmax = 100, time_steps = 'day', exp_name = exp_name)

print('DONE.')
# pickle things to plot later
pickle.dump( network2.edge_list, open( "output/" + exp_name + "edge_list.p", "wb" ) )
pickle.dump( network2.node_list, open( "output/" + exp_name + "node_list.p", "wb" ) )



#
'''web = webweb.Web(title="test")

i = 0
for time, A in temporalA.items():
    i += 1
    if i == 100:
        i = 0
        web.networks.__dict__[str(time)] = webweb.webweb.Network(adjacency=A)

web.display.sizeBy = 'strength'
web.display.showLegend = True
web.display.colorPalette = 'Dark2'
web.display.colorBy = 'degree'
web.show()'''
