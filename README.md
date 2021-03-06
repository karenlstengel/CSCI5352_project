# CSCI5352_project

## Python requirements
1. python v3.6 or greater  
2. numpy  
3. networkx  
4. matlplotlib

<!--- end of section -->

## Making GIFs

#### Make GIFs from images:
`sudo apt-get install imagemagick` or `brew install imagemagick` (on MacOS)  
`convert -delay 20 -loop 0 *.pdf myimage.gif`  

<!--- end of section -->

## Algorithm pseudocode
Feel free to change as you see fit:

```graphTimes = num of timesteps for temporal graphs. either 1 or == simTimes  
simTimes = num of timesteps for simulation  
G_list or dictionary or something  
n nodes  
p_edges = list of time probabilities for time dependent edges  

for timestep t in graphTimes:  
    G_list.add(graph-tools graph with n nodes and edge probability p_edges[t])  

t = 1
while t < simTimes or len(infected list) < n:  
    if len(infected list) > 0:

        for node in infected list:
            calculate probability of spread (SIR -> prob as defined in model)
            save probability to node?
            if probability > 0:
                for n in neighbors:
                    if n in state S | R:
                        and spread with probability
                        add infected neighbors to infected list
                        calculate viral load at t
                        save viral load to node

    else:
        randomly pick one node to infect -> t_infect = 0  
        add node to infected list
        calculate viral load at t
        save viral load to node

    do a visualization for time t graph. should probably save graph to be safe.
```

<!--- end of section -->
## Stats/other for setting up code
#### edge probablities for temporal network

include plt here that is prob p vs time t

<!--- end of section -->
## Experiment outline

1. static network (probablity of edges = mean(probability of edges in temporal network?))
    - SIR model
    - viral load model
2. temporal network
    - SIR model
    - viral load model
3. social (real) network [Socio patterns](http://www.sociopatterns.org/datasets/)
    - SIR model
    - viral load

<!--- end of section -->
