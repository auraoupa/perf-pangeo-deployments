# Benchmarking the french HPC PANGEO deployments

This repo gathers the results of some performance tests done with PANGEO ecosystem deployed on several machine.

The idea is to compare the machines on one simple computation that involves a lot of data.

I also want to know if every machine is scalable : more workers/memory/cores => computation faster ?

Also the format of the data (multiple netcdf files or zarr archive), the impact of the filestystem type on the opening and the impact of the chunk size will also be investigated.

## What is a PANGEO deployment

A description of what is PANGEO is available here : https://pangeo.io/index.html, it is first of all a community of scientists, engineers and developpers that collaborate on dealing with big amount of data produced mainly in geoscience fields of research and industry. There are no PANGEO library or module per se but we call PANGEO software ecosystem an ensemble of open-source tools that put together will help the user produce scientific diagnostic adapted to the data size.

A PANGEO deployment consists in the installation of a number of software on a machine, adapting some of the tools to the type of machine considered (HPC, cloud, personnal computer) In this case, the PANGEO deployment is described by [this list of python libraries](https://github.com/AurelieAlbert/perf-pangeo-deployments/blob/master/conda/environment.yml) that I will install via conda, in addition to the deployment of jupyter notebook server according to the machine : it can be a simple browser or a virtual distributed server.

## The data and the test

The exact same dataset has been uploaded on every machine we want to test. 

It is the sea surface height in the North Atlantic region simulated by [NEMO ocean model](https://www.nemo-ocean.eu/) between 2009, July the 1st and 2010, October the 1st, hereafter eNATL60-BLBT02-SSH (see [this repo](https://github.com/ocean-next/eNATL60) for more informations on the simulation). 

The dataset is a 621GB big zarr archive (due to compression since original data is 1.85TB) and contains 17 641 individual files, 11688x8354x4729 points with a chunksize of 240x240x480 (110MB).

The zarr archive have been constructed from multiple netcdf4 daily files with [this script](https://github.com/auraoupa/make-zarr-occigen/blob/master/script_fbriol.ipynb).

The netcdf daily files are also available on some machines : Occigen and HAL. In these 2 deployments I have tested the impact of the data format (netcdf or zarr) on the opening of the files and the computation of the time mean. The number of workers and cores is 20 for all the tests, and the available memory is 2.4TB for HSW24 and 3.6TB for HAL

The results are :

<table>
    <thead>
        <tr>
            <th>Deployment</th>
            <th>Format</th>
            <th>Opening</th>
            <th>Computing mean</th>
        </tr>
    </thead>
    <tbody>
        <tr>
             <td rowspan="2" scope="rowgroup">Occigen</td>
             <td>netcdf</td>
             <td>9.78s</td>
             <td>1/6 of dasks tasks in 1h30</td>
        </tr>
        <tr>
            <td>zarr</td>
            <td>893ms</td>
            <td>5min50</td>
        </tr>
        <tr>
             <td rowspan="2" scope="rowgroup">HAL</td>
             <td>netcdf</td>
             <td>4.77s</td>
             <td>>4h</td>  
        </tr>
        <tr>
            <td>zarr</td>
            <td>149ms</td>
            <td>4min47</td>
        </tr>
    </tbody>
</table>

***The zarr format clearly allows a faster opening and computation on the two machines, the computation is not even completed on the occigen machine, even when increasing number of workers and the memory.***

The chunksize is also a very relevant parameter we need to tune before doing parallelized computation with dask and xarray. 

The selection of the chunks happens when building the zarr archive or when opening the netcdf files. 

I have made a test with two zarr archives : the first is chunked equally along time and x dimensions and chunksize along y dimension is chosen to have a final chunk size of roughly hundreds of MB (240x240x480, 110MB). 

The second archive is chunked only on the time dimension (1x4729x8354, 158MB). Two operations will be performed with theses 2 archives : a temporal mean and a spatial mean. 

They will be computed on HAL cluster with 20 workers/cores and a total of 3.6TB of memory.

The results are :

<table>
    <thead>
        <tr>
            <th>Chunksize</th>
            <th>Opening</th>
            <th>Computing temporal mean</th>
            <th>Computing spatial mean</th>
        </tr>
    </thead>
    <tbody>
        <tr>
             <td>240x240x480</td>
             <td>90ms</td>
             <td>4min52 (41761 Tasks)</td>
             <td>4min17(41602 Tasks)</td>
        </tr>
        <tr>
            <td>1x4729x8354</td>
            <td>158ms</td>
            <td>14min39s (27275 Tasks)</td>
            <td>4min53 (35065 Tasks)</td>
        </tr>
    </tbody>
</table>

***The temporal mean of data that is chunked along the time dimension only takes more than three times more time that when the data is chunked also along x and y dimensions.*** 

***The spatial mean is not impacted because in the two cases, the time dimension is chunked (in 11688 or 48 pieces).***


## Description of Pangeo deployments

Every deployment has its own characteristics regarding the filesystem, the processors available for computation and the way we can access them.

### Personnal computer

The more direct deployment is on a *personnal computer* : in my case, it is a Dell machine with 2 Intel Xeon Processors with 4 cores and a total of 33,66 GB memory. The data are accessible through a sshfs mounting (data lives on a local server). I simply launch a jupyter notebook on a firefox browser.

On this very simple PANGEO deployment, I made several tests by varying the number of workers, the number of cores and size of memory being fixed.

The results are :

<table>
    <thead>
        <tr>
            <th>Workers</th>
            <th>Cores</th>
            <th>Memory</th>
            <th>Timing of computation</th>
        </tr>
    </thead>
    <tbody>
        <tr>
             <td>2</td>
             <td>8</td>
             <td>33,66GB</td>
             <td>1h50 +/- </td>
        </tr>
         <tr>
             <td>4</td>
             <td>8</td>
             <td>33,66GB</td>
             <td>1h49 +/- </td>
        </tr>
         <tr>
             <td>8</td>
             <td>8</td>
             <td>33,66GB</td>
             <td> 1h50 </td>
        </tr>
    </tbody>
</table>

***The number of workers does not seem to be a relevant parameter as the performance are really similar with 2, 4 or 8 workers.***

### MEOM jupyterhub

At the MEOM team level of the laboratory IGE, we have a virtual machine jupytr with jupyterhub that grants every user 2 cores and 2GB of memory for computation on data stored on the same server. The physical machine behind has 2 Inte(R)Xeon(R) CPUs with 16 cores.

There is no possible variation of the key parameters on this deployment, so the result will only be useful to compare to other deployments. It takes 3h41 +/- 23mn to compute the temporal mean there.

### GRICAD cluster DAHU

On a regional level, [GRICAD](https://gricad-doc.univ-grenoble-alpes.fr/) (Grenoble Alpes Recherche - Infrastructure de Calcul Intensif et de Données) offers teh access to intensive computing ressources, among them the cluster [dahu](https://gricad-doc.univ-grenoble-alpes.fr/hpc/description/)

To run a jupyter notebook, I first have to submit a job to request the ressource I need, then a tunnel is put in place to run the notebook in a local browser.

Three types of nodes are available and differ by the number of cores (16 [gold6244], 24 [gold6126] or 32 [gold6130]), they all have 192GB of memory.

I will first try to replicate the PC and CAL1 performances by selecting 8 cores and 33,66GB of memeory and 2 cores and 8,39GB of memory respectively, on the 2 nodes.

- [GRICAD] intensive computing cluster 
  
Several nodes are available by submitting a job first, then launching jupyter notebook on the requested node :

      - gold6130-32cores-192
      - gold6126-24cores-192
      - gold6244-16cores-192
      
  - [CNES](https://cnes.fr/fr/) intensive computing cluster hal
  
 A lot of nodes are accessible via dask-jobqueue (a job is submitted) :
 
      - Qdev-1core-4GB-12H
      - Qdev-4cores-15GB-12h
      - Qdevfullnode-16cores-60GB
      - Batch-1core-5GB-12h
      - Batch-1core-5GB-72h
      - Batch-4cores-20GB-12h
      - Batchfullnodes-24cores-120GB-12h
      - Batch2019fullnodes-40cores-184GB-12h
      
  - [CINES](https://www.cines.fr/) supercomputer [occigen](https://www.cines.fr/calcul/materiels/occigen/)
  
 4 types of nodes are accessible via dask-jobqueue (a job is submitted) :
 
      - HSW24-24cores-128Go
      - BDW28-28cores-64Go
      - VISU-28cores-256Go-6h (only 6 nodes)
      - SkylakeGPU-224cores-3To (upon request)
      
  - [IDRIS](http://www.idris.fr/info/missions.html) supercomputer [jean-zay](http://www.idris.fr/jean-zay/)
  
  Several nodes are available by submitting a job first, then launching jupyter notebook on the requested node :
  
      - normal queue cpu-p1
      - prepost

      - Skylake-40cores-192GB
      - GPU-V100-4cores-32GB
      - GPU-V100-8cores-32GB (for AI only)
      - Skylake-48cores-3TB
      - GPU-P6000-40cores-192GB
      
  - [PANGEO](https://pangeo.io/index.html) [cloud](https://pangeo.io/deployments.html)
  
  3 queues  are available directly in the jupyterhub that will access the same type of nodes (8.59GB per node) :
  
      - small-1-4GB
      - medium-4-8GB
      - large-12-16GB
      
So depending on the number of workers asked, the adequate queue will be selected.

## Results of the tests

Three parameters seem to have an impact on the performation of computation : the number of workers, the number of cores and the memory available.

I want to compare the deployments along this 3 parameters :
  - results for a given number of workers are presented in Table 1 (2 workers, 20 workers)
  - results for a given size of memory are presented in Table 2 (8GB, 1TB)
  - results for a given number of cores, same memory on HAL : 
  
  <table>
    <thead>
        <tr>
            <th>Number of workers</th>
            <th>Number of cores</th>
            <th>Memory</th>
            <th>Temporal mean</th>
        </tr>
    </thead>
    <tbody>
        <tr>
             <td>20</td>
             <td>20</td>
             <td>184GB</td>
             <td>5min07</td>
        </tr>
        <tr>
            <td>5</td>
            <td>20</td>
            <td>184GB</td>
            <td>5min58</td>
        </tr>
    </tbody>
</table>


I also want to investigate the scalability of the deployments by increasing workers or memory :
  - results for occigen
  - results for hal
  - results for jean-zay
  - results for gricad

I finally investigate the difference between requesting my workers on one single node or on several one, results :



- Table 1 : Computation of temporal mean with 2 workers

<table>
    <thead>
        <tr>
            <th>Machine</th>
            <th>Node type</th>
            <th>Total memory</th>
            <th>Timing</th>
        </tr>
    </thead>
    <tbody>
        <tr>
             <td>Personnal Computer</td>
             <td>Intel Xeon</td>
             <td>33.66GB</td>
             <td>1h50</td>
      </tr>
       <tr>
            <td>Cluster cal1</td>
            <td>Intel Xeon</td>
            <td>8.39GB</td>
            <td>3h19</td>
        </tr>
        <tr>
            <td>Cluster dahu GRICAD</td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td rowspan="7" scope="rowgroup">HPC hal CNES</td>
            <td>Qdev-1core</td>
            <td></td>
            <td></td>
        </tr>
         <tr>
            <td>Qdev-4cores</td>
            <td>30GB</td>
            <td>48min</td>
        </tr>
         <tr>
            <td>Qdev-fullnode-16cores</td>
            <td>120GB</td>
            <td>45min19</td>
        </tr>
         <tr>
            <td>Batch-1core</td>
            <td></td>
            <td></td>
        </tr>
         <tr>
            <td>Batch-4cores</td>
            <td></td>
            <td></td>
        </tr>
         <tr>
            <td>Batch-fullnode-24cores</td>
            <td>240GB</td>
            <td>46min18</td>
        </tr>
         <tr>
            <td>Batch2019-fullnode-40cores</td>
            <td></td>
            <td></td>
        </tr>
       <tr>
             <td rowspan="3" scope="rowgroup">HPC Occigen</td>
             <td> HSW24 node </td>
             <td>240GB</td>
             <td>51min48</td>
      </tr>
      <tr>
             <td> BDW28 node </td>
             <td>120GB</td>
             <td>57min8</td>
       </tr>
       <tr>
             <td> VISU node </td>
             <td>270.19GB</td>
             <td>9min17</td>
       </tr>
       <tr>
            <td>HPC jean-zay IDRIS</td>
            <td>cpu-p1</td>
            <td>8.59GB</td>
            <td>51min24</td>
        </tr>
        <tr>
            <td>PANGEO cloud</td>
            <td> Medium </td>
            <td>8.59GB</td>
            <td>1h19</td>
        </tr>
     </tbody>
</table>

- Table 2 : Computation of temporal mean with 4 workers

<table>
    <thead>
        <tr>
            <th>Machine</th>
            <th>Node type</th>
            <th>Total memory</th>
            <th>Timing</th>
        </tr>
    </thead>
    <tbody>
        <tr>
             <td>Personnal Computer</td>
             <td> Intel Xeon</td>
             <td>33.66GB</td>
             <td>1h49</td>
      </tr>
        <tr>
            <td>Cluster dahu GRICAD</td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td rowspan="7" scope="rowgroup">HPC hal CNES</td>
            <td>Qdev-1core</td>
            <td></td>
            <td></td>
        </tr>
         <tr>
            <td>Qdev-4cores</td>
            <td></td>
            <td></td>
        </tr>
         <tr>
            <td>Qdev-fullnode-16cores</td>
            <td>240GB</td>
            <td>22min37</td>
        </tr>
         <tr>
            <td>Batch-1core</td>
            <td></td>
            <td></td>
        </tr>
         <tr>
            <td>Batch-4cores</td>
            <td>80GB</td>
            <td>24min15</td>
        </tr>
         <tr>
            <td>Batch-fullnode-24cores</td>
            <td></td>
            <td></td>
        </tr>
         <tr>
            <td>Batch2019-fullnode-40cores</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
             <td rowspan="3" scope="rowgroup">HPC Occigen</td>
             <td> HSW24 node </td>
             <td>480GB</td>
             <td>28min31</td>
      </tr>
      <tr>
             <td> BDW28 node </td>
             <td>240GB</td>
             <td>28min53</td>
       </tr>
       <tr>
             <td> VISU node </td>
             <td>270.19GB</td>
             <td>6min55</td>
       </tr>
       <tr>
            <td>HPC jean-zay IDRIS</td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>PANGEO cloud</td>
            <td> Large </td>
            <td>17.18GB</td>
            <td>39min</td>
        </tr>
    </tbody>
</table>

- Table 3 : Computation of temporal mean with 10 workers

<table>
    <thead>
        <tr>
            <th>Machine</th>
            <th>Node type</th>
            <th>Total memory</th>
            <th>Timing</th>
        </tr>
    </thead>
    <tbody>
         <tr>
            <td>Cluster dahu GRICAD</td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td rowspan="7" scope="rowgroup">HPC hal CNES</td>
            <td>Qdev-1core</td>
            <td></td>
            <td></td>
        </tr>
         <tr>
            <td>Qdev-4cores</td>
            <td></td>
            <td></td>
        </tr>
         <tr>
            <td>Qdev-fullnode-16cores</td>
            <td></td>
            <td></td>
        </tr>
         <tr>
            <td>Batch-1core</td>
            <td></td>
            <td></td>
        </tr>
         <tr>
            <td>Batch-4cores</td>
            <td></td>
            <td></td>
        </tr>
         <tr>
            <td>Batch-fullnode-24cores</td>
            <td></td>
            <td></td>
        </tr>
         <tr>
            <td>Batch2019-fullnode-40cores</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
             <td rowspan="3" scope="rowgroup">HPC Occigen</td>
             <td> HSW24 node </td>
             <td>1.2TB</td>
             <td>10min9</td>
      </tr>
      <tr>
             <td> BDW28 node </td>
             <td>600GB</td>
             <td>10min52</td>
       </tr>
       <tr>
             <td> VISU node </td>
             <td></td>
             <td></td>
       </tr>
       <tr>
            <td>HPC jean-zay IDRIS</td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>PANGEO cloud</td>
            <td> Large </td>
            <td>42.95GB</td>
            <td>18min37</td>
        </tr>
    </tbody>
</table>

- Table 4 : Computation of temporal mean with 20 workers

<table>
    <thead>
        <tr>
            <th>Machine</th>
            <th>Node type</th>
            <th>Total memory</th>
            <th>Timing</th>
        </tr>
    </thead>
    <tbody>
         <tr>
            <td>Cluster dahu GRICAD</td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td rowspan="7" scope="rowgroup">HPC hal CNES</td>
            <td>Qdev-1core</td>
            <td></td>
            <td></td>
        </tr>
         <tr>
            <td>Qdev-4cores</td>
            <td></td>
            <td></td>
        </tr>
         <tr>
            <td>Qdev-fullnode-16cores</td>
            <td></td>
            <td></td>
        </tr>
         <tr>
            <td>Batch-1core</td>
            <td></td>
            <td></td>
        </tr>
         <tr>
            <td>Batch-4cores</td>
            <td></td>
            <td></td>
        </tr>
         <tr>
            <td>Batch-fullnode-24cores</td>
            <td></td>
            <td></td>
        </tr>
         <tr>
            <td>Batch2019-fullnode-40cores</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
             <td rowspan="3" scope="rowgroup">HPC Occigen</td>
             <td> HSW24 node </td>
             <td>2.4TB</td>
             <td>5min7</td>
      </tr>
      <tr>
             <td> BDW28 node </td>
             <td>1.2TB</td>
             <td>5min31</td>
       </tr>
       <tr>
             <td> VISU node </td>
             <td></td>
             <td></td>
       </tr>
       <tr>
            <td>HPC jean-zay IDRIS</td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>PANGEO cloud</td>
            <td> Large </td>
            <td>85.9GB</td>
            <td>10min5</td>
        </tr>
    </tbody>
</table>
