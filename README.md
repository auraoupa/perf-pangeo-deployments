# Performance tests on various pangeo deployments

This repo gathers the results of some performance tests done with PANGEO ecosystem deployed on several machine.
The idea is to compare the machines on one simple computation that involves a lot of data.
I also want to know if every machine is scalable : more workers => computation faster ?
Also the format of the data (multiple netcdf files or zarr archive), the impact of the filestystem type on the opening and the impact of the chunk size will be briefly investigated.

## Description of Pangeo deployments

Every deployment has its own characteristics regarding the filesystem, the processors available for computation and the way we can access them.

The more direct deployment is on a *personnal computer* : in my case, it is a Dell machine with Intel Xeon Processors with 4 cores. The data are accessible through a sshfs mounting (data lives on a local server)

  - Dell personnal computer : Processeur Intel Xeon with 4 cores
  - [IGE](http://www.ige-grenoble.fr/) team-size computing server cal1 : 2 Inte(R)Xeon(R) CPUs with 16 cores (32 in total), with a restriction to 2 cores and 2GB per user on Virtual Machine jupytr (where jupyterhub is deployed)
  - [GRICAD](https://gricad-doc.univ-grenoble-alpes.fr/) intensive computing cluster [dahu](https://gricad-doc.univ-grenoble-alpes.fr/hpc/description/)
  
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

## The data

The exact same dataset has been uploaded in every PANGEO deployment : the sea surface height in the North Atlantic 
region simulated by NEMO between 2009, July the 1st and 2010, October the 1st, hereafter eNATL60-BLBT02-SSH. 

The dataset is a zarr archive, is 621GB big (due to compression since original data is 1.85TB) and contains 17 641 individual files, contains 11688x8354x4729 points with a chunksize of 240x240x480 (110MB).

The zarr archive have been constructed from multiple netcdf4 daily files with this script.

The netcdf files are available on some PANGEO deployment : occigen and hal. On these 2 deployments I have tested the impact of the data format (netcdf or zarr) on the opening of the files and the computation of the time mean. The number of workers is 20 for all the tests, and the available memory is 2.4TB for HSW24 and 3.6TB for HAL

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
             <td></td>
             <td></td>
        </tr>
        <tr>
            <td>zarr</td>
            <td>893ms</td>
            <td></td>
        </tr>
        <tr>
             <td rowspan="2" scope="rowgroup">HAL</td>
             <td>netcdf</td>
             <td>4.77s</td>
             <td></td>
        </tr>
        <tr>
            <td>zarr</td>
            <td>149ms</td>
            <td>4min47</td>
        </tr>
    </tbody>
</table>


## The tests

First, the opening of the zarr on the different deployments will be timed. The comparison with the opening of the same data in form of netcdf files will be done where the data are available in the two formats (zarr and netcdf), ie on occigen and hal. (see Table 1 & 2)

Then, the time-mean over the whole period will be computed on every platforms using 2, 4, 10 and 20 workers when possible, to compare performance between deployments but also the scalability on each machine. (see Table 3 to X)

For the machine with different computation nodes, several tests will be made. (see Table XX to Y)

Last, the same computation will be done using all the workers of one node or the same number of workers on several nodes when possible, ie on hal and occigen. (see Table YY to Z)

To garantee the robustness of the test, the exact same python configuration will be deployed, it is described in the [conda environment.yml](https://github.com/AurelieAlbert/perf-pangeo-deployments/blob/master/conda/environment.yml) file.



## Results

- Table 1 : Opening the 621Go zarr archive containing 1.85TB of data.

<table>
    <thead>
        <tr>
            <th>Machine</th>
            <th>File System</th>
            <th>Timing</th>
        </tr>
    </thead>
    <tbody>
        <tr>
             <td>Personnal Computer</td>
             <td></td>
             <td>(1.47+1.43)/2s</td>
        </tr>
        <tr>
            <td>Cluster cal1</td>
            <td></td>
            <td>260ms</td>
        </tr>
        <tr>
            <td>Cluster dahu GRICAD</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>HPC hal CNES</td>
            <td></td>
            <td>279ms+124ms</td>
        </tr>
        <tr>
            <td>HPC occigen CINES</td>
            <td></td>
            <td>(2.29+2.11)/2s</td>
        </tr>
        <tr>
            <td>HPC jean-zay IDRIS</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>PANGEO cloud</td>
            <td></td>
            <td>(3.23+1.27+1.77+2.35+2.23+2.13)/6</td>
        </tr>
    </tbody>
</table>

- Table 3 : Computation of temporal mean with 2 workers

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

- Table 4 : Computation of temporal mean with 4 workers

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

- Table 5 : Computation of temporal mean with 10 workers

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

- Table 6 : Computation of temporal mean with 20 workers

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
