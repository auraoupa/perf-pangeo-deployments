#!/usr/bin/env python

# # The imports
import xarray as xr
import time
import dask


# # The workers
ask_workers=2
ask_memory='4GB'
from dask_jobqueue import SLURMCluster 
from dask.distributed import Client 
cluster = SLURMCluster(cores=1,processes=1,name='pangeo',walltime='02:30:00',
                       job_extra=['--constraint=HSW24','--exclusive',
                                  '--nodes=1'],memory=ask_memory,
                       interface='ib0') 
cluster.scale(ask_workers)
c= Client(cluster)
c

from dask.utils import ensure_dict, format_bytes

wk = c.scheduler_info()["workers"]

text="Workers= " + str(len(wk))
memory = [w["memory_limit"] for w in wk.values()]
cores = sum(w["nthreads"] for w in wk.values())
text += ", Cores=" + str(cores)
if all(memory):
    text += ", Memory=" + format_bytes(sum(memory))
print(text)
#Workers= 2, Cores=2, Memory=8.00 GB

# # The data
%time ds=xr.open_zarr('/store/albert7a/eNATL60/zarr/eNATL60-BLBT02-SSH-1h')
#2.07 s

%time mean=ds.sossheig.mean(dim='time_counter')
#306 ms
%time mean.load()
#58min
cluster.close()




