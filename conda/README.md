# How to deploy the conda environment for the performance tests

## The configuration file 

  - [environment.yml](https://github.com/AurelieAlbert/perf-pangeo-deployments/blob/master/conda/environment.yml)
  
## On jupytr

 - conda env create -f environment.yml
 - python -m ipykernel install --user --name perf-pangeo --display-name perf-pangeo
 
## On Occigen

 - on a linux machine with http access, build the perf-pangeo conda environment like previously described
 - conda install -c conda-forge conda-pack
 - conda pack -n perf-pangeo
 - scp perf-pangeo.tar.gz on occigen
 - tar -xzf perf-pangeo.tar.gz -C perf-pangeo
 - source perf-pangeo/bin/activate
 - python -m ipykernel install --user --name perf-pangeo --display-name perf-pangeo
