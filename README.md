# CSCI5352_project

## Python environment

With the `.yml` file:
1. `conda gt create -f csci5352_proj_env.yml`
2. `conda activate gt`
3. `conda gt list`

If the `.yml` import doesn't work here is how to install `graph-tools` with Conda:
1. `conda create --name gt -c conda-forge graph-tool`
2. `conda activate gt`
3. `conda install -n gt -c conda-forge {package names, ipython, jupyter, ...}`
4. `conda gt list`

## Algorithm pseudocode

## Experiment outline

1. static network
    - SIR model
    - viral load model
2. temporal network
    - SIR model
    - viral load model
3. social (real) network [Socio patterns](http://www.sociopatterns.org/datasets/)
    - SIR model
    - viral load
