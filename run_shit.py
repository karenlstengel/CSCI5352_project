# run da functions etc
import os
import temporal_network
import matplotlib.pyplot as plt
import pickle
import webweb
from Network import *
from utils import * # TODO this is where the network builing functions will live
os.system('clear')
n = 100
m = 2
exponent = 2.8
nu = 100
epsilon = 1e-3
#
# activities = temporal_network.generate_activities(n, exponent, nu, epsilon)
# temporalA = temporal_network.construct_activity_driven_model(n, m, activities, tmin=0, tmax=10, dt=1)
#
# # visualize
# web = webweb.Web(title="test")
#
# for time, A in temporalA.items():
#     print(time)
#     web.networks.__dict__[str(time)] = webweb.webweb.Network(adjacency=A)
#
# web.display.sizeBy = 'strength'
# web.display.showLegend = True
# web.display.colorPalette = 'Dark2'
# web.display.colorBy = ''
# web.show()


#
filename = "Data/School/thiers_2011.csv"
filename = "Data/School/thiers_2012.csv"
#filename = "Data/Workplace/tij_InVS.dat"
filename = "Data/School/primaryschool.csv"
filename = "Data/School/High-School_data_2013.csv"
delimiter = " "

nodesA, temporalA = import_temporal_networks(filename, delimiter)
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

#---------------------------------------------------------------------------------
#OOP Version
exp_name = 'testing_temporal_VL/'

staticA = temporal_to_static_network(temporalA)
network = Network(nodesA, temporalA, contagionType = 'VL')
#print(network.node_list.keys())
network.run_temporal_contagion(0, 0, tmax=10, exp_name = exp_name)
plot_stats(network.edge_list, network.node_list, tmax = 10, time_steps = 'day', exp_name = exp_name)

print('DONE.')
# pickle things to plot later
#print(nodeList[2])
