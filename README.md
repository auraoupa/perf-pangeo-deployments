# Performance tests on various pangeo deployments

## Pangeo deployments

  - personnal computer
  - IGE cluster cal1
  - GRICAD intensive computing cluster dahu
  - CNES intensive computing cluster hal
  - CINES supercomputer occigen
  - IDRIS supercomputer jean-zay
  - PANGEO cloud

## The data

The exact same dataset has been uploaded in every PANGEO deployment : the sea surface height in the North Atlantic 
region simulated by NEMO between 2009, July the 1st and 2010, October the 1st, hereafter eNATL60-BLBT02-SSH. 

The dataset is a zarr archive, is 621Go big and contains 17 641 indivdual files.

## The tests

The opening of the zarr (perf 1), the virtual computation of the time-mean over the whole period (perf 2) and the actual computation (perf 3) will be timed.

To garantee the robustness of the test, the exact same python configuration will be deployed, it is described in the conda environment.yml file.

For the machine with different computation nodes, several tests will be made.

