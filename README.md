# Benchmarking the french HPC PANGEO deployments

This repo gathers the results of some performance tests done with PANGEO ecosystem deployed on several machines.

The idea is to compare the machines on one simple computation that involves a lot of data.

I also want to know if every machine is scalable : does more workers/memory/cores mean the computation goes faster and by how much ?

Also the format of the data (multiple netcdf files or zarr archive), the impact of the filestystem type on the opening and the impact of the chunk size will also be investigated.

## What is a PANGEO deployment

A description of what is PANGEO is available here : https://pangeo.io/index.html, it is first of all a community of scientists, engineers and developpers that collaborate on dealing with big amount of data produced mainly in geoscience fields of research and industry. There are no PANGEO library or module per se but we call PANGEO software ecosystem an ensemble of open-source tools that put together will help the user produce scientific diagnostics adapted to the data size.

A PANGEO deployment consists in the installation of a number of software on a machine, adapting some of the tools to the type of machine considered (HPC, cloud, personnal computer) In my case, the PANGEO deployment is described by [this list of python libraries](https://github.com/AurelieAlbert/perf-pangeo-deployments/blob/master/conda/environment.yml) that I will install via conda, in addition to the deployment of a jupyter notebook server adapted to the machine : it can be a simple browser or a virtual distributed server.

## The data and the test

The exact same dataset has been uploaded on every machine I want to test. 

It is the hourly sea surface height in the North Atlantic region simulated by [NEMO ocean model](https://www.nemo-ocean.eu/) between 2009, July the 1st and 2010, October the 1st, hereafter eNATL60-BLBT02-SSH (see [this repo](https://github.com/ocean-next/eNATL60) for more informations on the simulation). 

The dataset is 1.85TB big compressed into a 621GB zarr archive and contains 17 641 individual files, 11688x8354x4729 grid points with a chunksize of 240x240x480 (110MB).

![plot of file](https://github.com/AurelieAlbert/perf-pangeo-deployments/blob/master/figs/enatl60-ssh-file-chunk.png)

The zarr archive have been constructed from multiple netcdf4 daily files with [this script](https://github.com/auraoupa/make-zarr-occigen/blob/master/script_fbriol.ipynb).

The elementary test consists in computing the temporal mean over the whole period (16 months) for every grid point. It is a very common operation in oceanography when we want to compare the results of oceanic simulation with satellite observations for instance (see [here](https://github.com/ocean-next/demo-compare-ssh-eNATL60-AVISO) for a demo and a plot).

Thanks to [xarray](http://xarray.pydata.org/en/stable/) and [dask](https://dask.org/) librairies (very important part of the PANGEO ecosystem), the computation is parallelized along each chunk of the dataset. The efficiency of the parallization should be a matter of how many workers/cores and memory dask is dealing with.

The netcdf daily files are also available on some machines : Occigen and HAL (see below for a description of these machines). In these 2 deployments I have tested the impact of the data format (netcdf or zarr) on the opening of the files and on the computation of the temporal mean. To make this test, I requested 20 workers, and 2.4TB on occigen and 3.6TB on HAL.

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
             <td>Killed Workers</td>
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

***The zarr format clearly allows a faster opening and computation on the two machines. The computation with netcdf files can not even complete on the occigen machine, even when increasing number of workers/cores and the memory.***

The chunksize is also a very relevant parameter that needs to be tuned before doing parallelized computation with dask and xarray. 

The selection of the chunk size happens when building the zarr archive or when opening the netcdf files. 

I have made a test with two zarr archives : the first is chunked equally along time and x dimensions and the chunk size along y dimension is chosen in order to have a final chunk size of roughly hundreds of MB (240x240x480, 110MB). 

The second archive is chunked only on the time dimension (1x4729x8354, 158MB). Two operations will be performed with these 2 archives : a temporal mean and a spatial mean. 

They will be computed on HAL cluster with 20 workers and a total of 3.6TB of memory.

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

***The temporal mean of data that is chunked along the time dimension only is three times slower than when the data is chunked also along x and y dimensions.*** 

***The spatial mean is not impacted because in the two cases, the time dimension is chunked (in 11688 or 48 chunks).***


## Description of Pangeo deployments

Every deployment has its own characteristics regarding the filesystem, the processors available for computation and the way we can access them.

### Personnal computer (PC)

The more direct deployment is on a personnal computer : in my case, it is a Dell machine with 2 Intel Xeon Processors with 4 cores and a total of 33,66 GB memory. The dataset is accessible through a sshfs mounting (data lives on a local server). I simply launch a jupyter notebook in a firefox browser.

On this very simple PANGEO deployment, I made several tests by varying the number of workers, the number of cores and size of memory remaining constant.

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

### MEOM jupyterhub (CAL1)

At the [MEOM team](https://meom-group.github.io/) level of the [laboratory IGE](http://www.ige-grenoble.fr/), we have access to a virtual machine jupytr with a jupyterhub server that grants every user 2 cores and 2GB of memory for computation on data stored on the same server. The physical machine behind has 2 Inte(R)Xeon(R) CPUs with 16 cores.

Exceptionnally, I was able to perform the test using 8.39GB.

***There is no possible variation of the key parameters on this deployment, so the result will only be useful to compare to other deployments. It takes 3h41 +/- 23mn to compute the temporal mean there, so more than twice slower than on a personnal computer.***

### GRICAD cluster DAHU (DAHU)

At the regional level, [GRICAD](https://gricad-doc.univ-grenoble-alpes.fr/) (Grenoble Alpes Recherche - Infrastructure de Calcul Intensif et de Données) offers the access to intensive computing ressources, among them the cluster [dahu](https://gricad-doc.univ-grenoble-alpes.fr/hpc/description/)

To run a jupyter notebook, I first have to submit a job to request the ressources I need, then a ssh tunnel is set up to run the notebook in a local browser.

Three types of nodes are available and differ by the number of cores (24 [gold6126] or 32 [gold6130|gold5218]), they theoretically all have 192GB of memory in total.

I will first try to replicate the PC and CAL1 performances by selecting 8 cores and 2 cores on every node available.

Results are :

<table>
    <thead>
        <tr>
            <th>Node type</th>
            <th>Workers</th>
            <th>Cores</th>
            <th>Memory</th>
            <th>Timing of opening dataset</th>
            <th>Timing of computation</th>
        </tr>
    </thead>
    <tbody>
        <tr>
             <td>Gold5218</td>
             <td>2</td>
             <td>2</td>
             <td>201,35GB</td>
             <td>1,97s</td>
             <td>1h11</td>
        </tr>
        <tr>
             <td>Gold6126</td>
             <td>2</td>
             <td>2</td>
             <td>201,19GB</td>
             <td>841ms</td>
             <td>59mn</td>
        </tr>
        <tr>
             <td>Gold6130</td>
             <td>2</td>
             <td>2</td>
             <td>201,19GB</td>
             <td>579ms</td>
             <td>1h05</td>
        </tr>
        <tr>
             <td>Gold5218</td>
             <td>8</td>
             <td>8</td>
             <td>201,35GB</td>
             <td>759ms</td>
             <td>21mn</td>
        </tr>
        <tr>
             <td>Gold6126</td>
             <td>8</td>
             <td>8</td>
             <td>201,19GB</td>
             <td>979ms</td>
             <td>20mn</td>
        </tr>
        <tr>
             <td>Gold6130</td>
             <td>8</td>
             <td>8</td>
             <td>201,19GB</td>
             <td>2.64s</td>
             <td>27min</td>
        </tr>
    </tbody>
</table>

***We can see that the performance are better compared to PC and CAL1 but do not change much between nodes. Memory seems to be a key parameter.***

Now, I will look at the performances when using all the cores in one or mode node, for every node type when it is possible.

Results are :

<table>
    <thead>
        <tr>
            <th>Node type</th>
            <th>Workers</th>
            <th>Cores</th>
            <th>Memory</th>
            <th>Timing of opening dataset</th>
            <th>Timing of computation</th>
        </tr>
    </thead>
    <tbody>
        <tr>
             <td>Gold6126</td>
             <td>24</td>
             <td>24</td>
             <td>201.39GB</td>
             <td>3.33s</td>
             <td>13mn</td>
        </tr>
        <tr>
             <td>Gold6130</td>
             <td>32</td>
             <td>32</td>
             <td>201.19GB</td>
             <td>5.4s</td>
             <td>10mn</td>
        </tr>
        <tr>
             <td>Gold6130</td>
             <td>64</td>
             <td>64</td>
             <td>201.19GB</td>
             <td>2.1s</td>
             <td>9min53 +/- 11s</td>
        </tr>
        <tr>
             <td>Gold6130</td>
             <td>128</td>
             <td>128</td>
             <td>201.19GB</td>
             <td>2.1s</td>
             <td>9min57</td>
        </tr>
    </tbody>
</table>

![plot](https://github.com/AurelieAlbert/perf-pangeo-deployments/blob/master/figs/Perf-gricad.png)

***We can see there is a difference of performance when increasing the number of cores, the memory size remaining constant but it reaches a threshold of 10mn even when doubling the number of cores. It is strange noting that the memory did not increase when asking for more cores than the number of cores in one node, I would have assumed it would have doubled when asking for 64 cores (=2 nodes) [x4 for 128 cores].***

### CNES cluster HAL (HAL)

Hal is the [CNES](https://cnes.fr/fr/) intermediate size HPC cluster, with about 460 nodes, 12 000 cores and a 8.5 PB Spectrum Scale Storage. Nodes and storage are interconnected with Infiniband at 56GB/s, and the storage system provides a bandwith up to 100GB/s ([ref](https://www.researchgate.net/publication/340169325_The_Pangeo_Ecosystem_Interactive_Computing_Tools_for_the_Geosciences_Benchmarking_on_HPC)). 

Everyone with an account on this cluster can access the Jupyterhub service directly on the web : https://jupyterhub.cnes.fr/. The connection to the service will automatically launch a job on one computation node on which the jupyter notebook will be deployed (several choices for the spawning : from 1 core-4GB-12h to 40 cores-184GB-12h)

Once the notebook is running, I can also request more computation ressources by submitting job via [dask-jobqueue](https://jobqueue.dask.org/en/latest/) library that is part of PANGEO deployment and was developped for that exact purpose.

A large variety of nodes is present in this cluster, so that I can make the key parameters (cores/workers/memory) vary at will :
 
      - Qdev-1core(4GB) = Qdev1
      - Qdev-4cores-(5GB) = Qdev4
      - Qdevfullnode-16cores(60GB) = Qfull
      - Batch-1core(5GB) = Batch1
      - Batch-4cores(20GB) = Batch4
      - Batchfullnodes-24cores(120GB) = Bfull
      - Batch2019fullnodes-40cores(184GB) = B2019

Dask-jobqueue allows the request in terms of workers/cores and memory, the job is then submitted to the according queue.

I will first request the same amount of cores and memory than for the previous deployments (CAL, PC and DAHU)

Results are :

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
             <td>2</td>
             <td>8GB</td>
             <td>45min</td>
        </tr>
        <tr>
             <td>2</td>
             <td>2</td>
             <td>200GB</td>
             <td>48mn</td>
        </tr>
         <tr>
             <td>8</td>
             <td>8</td>
             <td>32GB</td>
             <td>12min</td>
        </tr>
         <tr>
             <td>8</td>
             <td>8</td>
             <td>200GB</td>
             <td>11min</td>
        </tr>
         <tr>
             <td>24</td>
             <td>24</td>
             <td>200GB</td>
             <td>4min19</td>
        </tr>
         <tr>
             <td>32</td>
             <td>32</td>
             <td>192GB</td>
             <td>3min24</td>
        </tr>
         <tr>
             <td>64</td>
             <td>64</td>
             <td>192GB</td>
             <td>2min2</td>
        </tr>
         <tr>
             <td>128</td>
             <td>128</td>
             <td>192GB</td>
             <td>3min10</td>
        </tr>
    </tbody>
</table>

***We will plot and comment the comparison between all deployments in the next section.***

***We have a first idea of the scalability of HAL, when selectionning the results with a fixed memory of 192GB (plot below) : it is scaling well up to 64 cores.***

![plot](https://github.com/AurelieAlbert/perf-pangeo-deployments/blob/master/figs/Perf-hal1.png)

Then, I will gradually increase the number of cores and/or the memory to describe further the scalability on HAL.

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
             <td>2</td>
             <td>8GB</td>
             <td>45min</td>
        </tr>
        <tr>
             <td>2</td>
             <td>2</td>
             <td>30GB</td>
             <td>48min</td>
        </tr>
       <tr>
             <td>2</td>
             <td>2</td>
             <td>120GB</td>
             <td>45min</td>
        </tr>
        <tr>
             <td>2</td>
             <td>2</td>
             <td>200GB</td>
             <td>48min</td>
        </tr>
        <tr>
             <td>2</td>
             <td>2</td>
             <td>368GB</td>
             <td>45min</td>
        </tr>
        <tr>
             <td>4</td>
             <td>4</td>
             <td>80GB</td>
             <td>24min</td>
        </tr>
        <tr>
             <td>4</td>
             <td>4</td>
             <td>240GB</td>
             <td>22min</td>
        </tr>
        <tr>
             <td>4</td>
             <td>4</td>
             <td>736GB</td>
             <td>23min</td>
       </tr>
       <tr>
             <td>8</td>
             <td>8</td>
             <td>32GB</td>
             <td>12min</td>
        </tr>
        <tr>
             <td>8</td>
             <td>8</td>
             <td>200GB</td>
             <td>11min39</td>
        </tr>
        <tr>
             <td>8</td>
             <td>8</td>
             <td>1.47TB</td>
             <td>15min7</td>
        </tr>
</table>

![plot](https://github.com/AurelieAlbert/perf-pangeo-deployments/blob/master/figs/Perf-hal2.png)

***We can see that increasing the memory size does not make the computation faster when using 2, 4 or 8 workers***

On HAL, we have the possiblity to ask for 1 core on several nodes or several cores in 1 node. We can also specify how much memory, so we can make vary either the number of workers or the memory, the other 2 parameters being fixed.

The results are :

  <table>
    <thead>
        <tr>
            <th>Number of nodes</th>
            <th>Number of workers</th>
            <th>Number of cores</th>
            <th>Memory</th>
            <th>Temporal mean</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>5</td>
            <td>20</td>
            <td>184GB</td>
            <td>5min58</td>
        </tr>
       <tr>
            <td>1</td>
            <td>20</td>
            <td>20</td>
            <td>184GB</td>
            <td>5min52</td>
        </tr>
        <tr>
             <td>20</td>
             <td>20</td>
             <td>20</td>
             <td>184GB</td>
             <td>5min07</td>
        </tr>
    </tbody>
</table>  

***There is a 20% improvment of performance when asking for 20 nodes instead of 1 node, the number of cores and memory available being the same. The increase of number of workers does not change significantly the performance.***

So, lastly I want to have the best results by asking all the cores and memory of 5, 10 and 20 nodes, testing the different type of nodes.

The results are : 

  <table>
    <thead>
        <tr>
            <th>Node type</th>
            <th>Number of nodes</th>
            <th>Number of workers</th>
            <th>Number of cores</th>
            <th>Memory</th>
            <th>Temporal mean</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th>qdev1</th>
            <td>5</td>
            <td>5</td>
            <td>5</td>
            <td>25GB</td>
            <td>1203s</td>
        </tr>
        <tr>
            <th>qdev4</th>
            <td>5</td>
            <td>20</td>
            <td>20</td>
            <td>25GB</td>
            <td>304s</td>
        </tr>
        <tr>
            <th>batch4</th>
            <td>5</td>
            <td>20</td>
            <td>20</td>
            <td>100GB</td>
            <td>300s</td>
        </tr>
        <tr>
            <th>qfull</th>
            <td>5</td>
            <td>20</td>
            <td>80</td>
            <td>300GB</td>
            <td>119s</td>
        </tr>
        <tr>
            <th>bfull</th>
            <td>5</td>
            <td>30</td>
            <td>120</td>
            <td>600GB</td>
            <td>113s</td>
        </tr>
        <tr>
            <th>b2019</th>
            <td>5</td>
            <td>40</td>
            <td>200</td>
            <td>920GB</td>
            <td>106s</td>
        </tr>
        <tr>
            <th>qdev1</th>
            <td>10</td>
            <td>10</td>
            <td>10</td>
            <td>50GB</td>
            <td>664s</td>
        </tr>
        <tr>
            <th>qdev4</th>
            <td>10</td>
            <td>40</td>
            <td>40</td>
            <td>50GB</td>
            <td>179s</td>
        </tr>
        <tr>
            <th>batch4</th>
            <td>10</td>
            <td>40</td>
            <td>40</td>
            <td>200GB</td>
            <td>192s</td>
        </tr>
        <tr>
            <th>qfull</th>
            <td>10</td>
            <td>40</td>
            <td>160</td>
            <td>600GB</td>
            <td>98s</td>
        </tr>
        <tr>
            <th>bfull</th>
            <td>10</td>
            <td>60</td>
            <td>240</td>
            <td>1200GB</td>
            <td>93s</td>
        </tr>
        <tr>
            <th>b2019</th>
            <td>10</td>
            <td>80</td>
            <td>400</td>
            <td>1840GB</td>
            <td>96s</td>
        </tr>
        <tr>
            <th>qdev1</th>
            <td>20</td>
            <td>20</td>
            <td>20</td>
            <td>100GB</td>
            <td>355+/-31s</td>
        </tr>
        <tr>
            <th>qdev4</th>
            <td>20</td>
            <td>80</td>
            <td>80</td>
            <td>100GB</td>
            <td>116s</td>
        </tr>
        <tr>
            <th>batch4</th>
            <td>20</td>
            <td>80</td>
            <td>80</td>
            <td>400GB</td>
            <td>146s</td>
        </tr>
        <tr>
            <th>qfull</th>
            <td>20</td>
            <td>80</td>
            <td>320</td>
            <td>1200GB</td>
            <td>100</td>
        </tr>
        <tr>
            <th>bfull</th>
            <td>20</td>
            <td>120</td>
            <td>480</td>
            <td>2400GB</td>
            <td>117s</td>
        </tr>
    </tbody>
</table>  

![plot](https://github.com/AurelieAlbert/perf-pangeo-deployments/blob/master/figs/Perf-hal3.png)

***We can see that qdev1 seems more scalable than the other nodes, because the performance is very low with 5 nodes***

The same plot is reproduced without the qdev1 results, for better readability.

![plot](https://github.com/AurelieAlbert/perf-pangeo-deployments/blob/master/figs/Perf-hal3b.png)

***Qdev4 and Batch4 are also more scalable for the same reason. The best performance is however obtained with qfull, bfull and b2019 nodes with 10 nodes.***

### CINES HPC Occigen (OCC)

CINES (National Computing Center for Higher Education) is a French public institution, located in Montpellier (south of France) and supervised by the French ministry for Higher Education and Research. It hosts advanced equipment including Occigen, a parallel bullx supercomputer, designed by the French company Bull. This supercomputer has a peak power of 2.1 Pflops (2 million billion operations per second). Designed on the basis of shared memory compute nodes interconnected via an InfiniBand network , it consists of 85824 core Intel Xeon ™ each with 2.5 GB of memory. A local storage capacity of 5 Po allows rapid access (106 GB/s) data ( /scratch ) managed by the parallel file system “Lustre”. 

2 types of nodes are accessible via dask-jobqueue (a job is submitted) :
 
      - HSW24-24cores-128Go
      - BDW28-28cores-64Go
      
There are also 4 nodes dedicated to visualization and pre/post processing (jupyter is running directly on one node) :

      - VISU-28cores-256Go-6h 
      
We first try to replicate the set up of the other machines tested so far :

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
             <td>2</td>
             <td>8GB</td>
             <td>58min</td>
        </tr>
        <tr>
             <td>2</td>
             <td>2</td>
             <td>200GB</td>
             <td>49mn</td>
        </tr>
         <tr>
             <td>8</td>
             <td>8</td>
             <td>32GB</td>
             <td>13min</td>
        </tr>
         <tr>
             <td>8</td>
             <td>8</td>
             <td>200GB</td>
             <td>15min</td>
        </tr>
         <tr>
             <td>24</td>
             <td>24</td>
             <td>200GB</td>
             <td>4min54</td>
        </tr>
         <tr>
             <td>32</td>
             <td>32</td>
             <td>192GB</td>
             <td>3min46</td>
        </tr>
         <tr>
             <td>64</td>
             <td>64</td>
             <td>192GB</td>
             <td>1min59</td>
        </tr>
         <tr>
             <td>128</td>
             <td>128</td>
             <td>192GB</td>
             <td>1min10</td>
        </tr>
    </tbody>
</table>

We can now compare HAL and Occigen 
 - to CAL1 :
 
 ![plot](https://github.com/AurelieAlbert/perf-pangeo-deployments/blob/master/figs/Perf-2cores.png)
 
 - to PC :
 
  ![plot](https://github.com/AurelieAlbert/perf-pangeo-deployments/blob/master/figs/Perf-8cores.png)

 - to GRICAD :
 
  ![plot](https://github.com/AurelieAlbert/perf-pangeo-deployments/blob/master/figs/Perf-200GB.png)


Then the performances of occigen nodes are assessed by requesting 5, 10 or 20 entire nodes.

  <table>
    <thead>
        <tr>
            <th>Node type</th>
            <th>Number of nodes</th>
            <th>Number of workers</th>
            <th>Number of cores</th>
            <th>Memory</th>
            <th>Temporal mean</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th>HSW24</th>
            <td>5</td>
            <td>140</td>
            <td>140</td>
            <td>600,60GB</td>
            <td>75s</td>
        </tr>
        <tr>
            <th>BDW28</th>
            <td>5</td>
            <td>140</td>
            <td>140</td>
            <td>299,60GB</td>
            <td>77</td>
        </tr>
        <tr>
            <th>HSW24</th>
            <td>10</td>
            <td>280</td>
            <td>280</td>
            <td>1200GB</td>
            <td>52s</td>
        </tr>
        <tr>
            <th>BDW28</th>
            <td>10</td>
            <td>280</td>
            <td>280</td>
            <td>599,20GB</td>
            <td>48s</td>
        </tr>
        <tr>
            <th>HSW24</th>
            <td>20</td>
            <td>560</td>
            <td>560</td>
            <td>2400GB</td>
            <td>38s</td>
        </tr>
        <tr>
            <th>BDW28</th>
            <td>20</td>
            <td>560</td>
            <td>1120</td>
            <td>1200GB</td>
            <td>40s</td>
        </tr>
        <tr>
            <th>VISU</th>
            <td>1</td>
            <td>8</td>
            <td>56</td>
            <td>270,19GB</td>
            <td>350s</td>
        </tr>
    </tbody>
</table>  
     
![plot](https://github.com/AurelieAlbert/perf-pangeo-deployments/blob/master/figs/Perf-occ3.png)


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

## Compilation of the results

First we will draw the results for all deployments with 2 cores :

Then, with 8 cores :


Three parameters seem to have an impact on the performation of computation : the number of workers, the number of cores and the memory available.

I want to compare the deployments along this 3 parameters :
  - results for a given number of workers are presented in Table 1 (2 workers, 20 workers)
  - results for a given size of memory are presented in Table 2 (8GB, 1TB)
  - results for a given number of cores, same memory on HAL : 
  
 
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
