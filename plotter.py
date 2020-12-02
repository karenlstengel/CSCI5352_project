import os
import temporal_network
import matplotlib.pyplot as plt
import pickle
import webweb
from Network import *
from utils import * # TODO this is where the network builing functions will live
os.system('clear')

exp_name = 'static_SIR'

edge_list = pickle.load( open( "output/" + exp_name + "edge_list.p", "rb" ) )
node_list = pickle.load( open( "output/" + exp_name + "node_list.p", "rb" ) )
drawContagion_nx(edge_list, node_list, index, t, times, exp_name = exp_name, pos = self.pos, contagionModel = self.contagionModel, SIR_prob = self.SIR_prob)

plot_stats(edge_list, node_list, tmax = 100, time_steps = 'day', exp_name = exp_name)'''
i = 62
while i <= 67: #289:
    os.system('cp ' + exp_name + 'simTime_00061.pdf ' + exp_name + 'simTime_{0:05d}.pdf'.format(i))
    i = i + 1'''
