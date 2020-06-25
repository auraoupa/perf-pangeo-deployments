# Performance tests on various pangeo deployments

## Pangeo deployments

  - Dell personnal computer : Processeur Intel Xeon with 4 cores
  - [IGE](http://www.ige-grenoble.fr/) team-size computing server cal1 : 20 cores in total, with a restriction to 2 cores per user
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
      
So depending on the number of workers asked, the adequate queue wille be selected.

## The data

The exact same dataset has been uploaded in every PANGEO deployment : the sea surface height in the North Atlantic 
region simulated by NEMO between 2009, July the 1st and 2010, October the 1st, hereafter eNATL60-BLBT02-SSH. 

The dataset is a zarr archive, is 621GB big (due to compression since original data is 1.85TB) and contains 17 641 individual files, contains 11688x8354x4729 points with a chunksize of 240x240x480 (110MB).

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
            <td>279ms</td>
            <td></td>
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
             <td>Normal nodes</td>
             <td>33.66GB</td>
             <td>1h50</td>
      </tr>
       <tr>
            <td>Cluster cal1</td>
            <td><Normal nodes/td>
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
            <td></td>
            <td></td>
            <td></td>
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
             <td> Normal nodes</td>
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
