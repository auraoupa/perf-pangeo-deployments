# How to deploy the conda environment for the performance tests

## The configuration file 

  - [environment.yml](https://github.com/AurelieAlbert/perf-pangeo-deployments/blob/master/conda/environment.yml)
  
## On jupytr

 - conda env create -f environment.yml
 - python -m ipykernel install --user --name perf-pangeo --display-name perf-pangeo
