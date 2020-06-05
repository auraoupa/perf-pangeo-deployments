# How to deploy the conda environment for the performance tests

## The configuration file 

  - [environment.yml](../environment.yml)
  
## On jupytr

 - conda env create --prefix /mnt/meom/workdir/alberta/cond-envs -f environment.yml
 - python -m ipykernel install --user --name perf-pangeo --display-name perf-pangeo
